import pyads
import time
import os
import logging
import traceback

from utils.db_result import dbResult
from utils.mysql_query import mysql_query
from utils.mssql_query import mssql_query
from utils.timeit import timeit
from utils.utils import convert_tc_str_array, convert_tc_config_var, convert_str_array_tc, convert_str_array2D_tc
from utils.logger import Logger
from utils.configparser import ConfigParser

VERSION = "1.4"
AMS_FILE = "ams_net_id.txt"

class PyAds():
  def __init__(self):
    self.baseDir = os.path.dirname(os.path.abspath(__file__))
    self.config = ConfigParser(os.path.join(self.baseDir, 'settings.json'))

    log_in_files = self.config["logging"]["log_in_files"]
    level = self.config["logging"]["level"]
    self.logger = Logger(os.path.join(self.baseDir, 'log', 'ads.log'), level=level, log_in_files=log_in_files)
    logging.debug('Script starts')

    self.ams_address = ''
    
    self.varExecute = self.config["AdsVar"]["execute"]
    self.varDone = self.config["AdsVar"]["done"]
    self.varError = self.config["AdsVar"]["error"]
    self.varBusy = self.config["AdsVar"]["busy"]
    self.busy = True
    self.varConfig = self.config["AdsVar"]["config"]

    self.varRequest = self.config["AdsVar"]["request"]
    self.varRequestLength = 0
    self.varRequestSize = 0

    self.varRowCount = self.config["AdsVar"]["rowCount"]
    self.varColumnCount = self.config["AdsVar"]["columnCount"]

    self.varColumnsName = self.config["AdsVar"]["columnsName"]
    self.varColumnsNameLenght = 0
    self.varColumnsNameSize = 0

    self.varTableValues = self.config["AdsVar"]["tableValues"]
    self.varTableValuesLenght = 0
    self.varTableValuesRowsSize = 0
    self.varTableValuesColumnsSize = 0

    self.varSerror = self.config["AdsVar"]["sError"]
    self.varSerrorLenght = 0

    self.ams_address = self.get_ams_address()
    self.plc = pyads.Connection(self.ams_address, pyads.PORT_TC3PLC1)
    self.plc.open()
    self.connect_ads()

    self.run()

  @staticmethod
  def get_ams_address():
    with open(AMS_FILE, 'r', encoding='utf-8') as f:
      for x in f:
          return x
    logging.debug('Ams Address not founded')
    return 'Not founded'

  # @timeit
  def do_query(self, config, request):
    result = dbResult()
    try:
      if config['type_database'] == 'mssql':
        result = mssql_query(config=config, request=request)
      else: # mysql
        result = mysql_query(config=config, request=request)
    except:
      result.values.append('Query could not be send:{0}'.format(request))
    return result

  # @timeit
  def process_execute(self):
    try:
      # read request
      lenght = self.varRequestLength*self.varRequestSize
      request = self.plc.read_by_name(self.varRequest, pyads.PLCTYPE_STRING*lenght)
      request = convert_tc_str_array(s=request, lenght=self.varRequestLength) 
      logging.info('request: {0}'.format(request))

      # read config
      nr_vars = 5
      lenght_var = 80 + 1
      lenght = (lenght_var)*nr_vars
      config = self.plc.read_by_name(self.varConfig, pyads.PLCTYPE_STRING*lenght)
      config = convert_tc_config_var(s=config, nr_vars=nr_vars, lenght_var=lenght_var)
      logging.debug('config: {0}'.format(config))

      # do request
      result = self.do_query(config=config, request=request)
      if result.ok:
        # row count
        self.plc.write_by_name(self.varRowCount, result.rowcount, pyads.PLCTYPE_DINT)
        
        # column count
        self.plc.write_by_name(self.varColumnCount, result.columncount, pyads.PLCTYPE_DINT)

        # columns
        val = convert_str_array_tc(
          s=result.colums, 
          lenghtString=self.varColumnsNameLenght, 
          sizeCols=self.varColumnsNameSize
          )
        self.plc.write_by_name(self.varColumnsName, val, pyads.PLCTYPE_STRING*len(val))

        # values
        val = convert_str_array2D_tc(
          s=result.values, 
          lenghtString=self.varTableValuesLenght, 
          sizeCols=self.varTableValuesColumnsSize, 
          sizeRows=self.varTableValuesRowsSize
          )
        self.plc.write_by_name(self.varTableValues, val, pyads.PLCTYPE_STRING*len(val))
        logging.info('values: {0}'.format(result.values))

        # done
        self.plc.write_by_name(self.varDone, True, pyads.PLCTYPE_BOOL)
      else:
        self.plc.write_by_name(self.varError, True, pyads.PLCTYPE_BOOL)
        error = result.values[0]
        error = error[:self.varSerrorLenght - 1]
        self.plc.write_by_name(self.varSerror, error, pyads.PLCTYPE_STRING)
        logging.debug(result)
    except Exception as e:
      error_log = traceback.format_exc()
      try:
        self.plc.write_by_name(self.varError, True, pyads.PLCTYPE_BOOL)
        self.plc.write_by_name(self.varSerror, error_log[:self.varSerrorLenght-1], pyads.PLCTYPE_STRING)
      except:
        error_log += '\n' + traceback.format_exc()
      finally:
        logging.debug('{0}'.format(error_log))

  def get_size_lenght(self):
    versionLenght = self.plc.read_by_name(self.config["AdsVar"]["versionLenght"], pyads.PLCTYPE_UDINT) + 1
    self.plc.write_by_name(self.config["AdsVar"]["version"], VERSION[:versionLenght-1], pyads.PLCTYPE_STRING)

    self.varRequestLength = self.plc.read_by_name(self.config["AdsVar"]["requestLength"], pyads.PLCTYPE_UDINT) + 1
    self.varRequestSize = self.plc.read_by_name(self.config["AdsVar"]["requestSize"], pyads.PLCTYPE_UDINT)

    self.varColumnsNameLenght = self.plc.read_by_name(self.config["AdsVar"]["columnsNameLenght"], pyads.PLCTYPE_UDINT) + 1
    self.varColumnsNameSize = self.plc.read_by_name(self.config["AdsVar"]["columnsNameSize"], pyads.PLCTYPE_UDINT)

    self.varTableValuesLenght = self.plc.read_by_name(self.config["AdsVar"]["tableValuesLenght"], pyads.PLCTYPE_UDINT) + 1
    self.varTableValuesRowsSize = self.plc.read_by_name(self.config["AdsVar"]["tableValuesRowsSize"], pyads.PLCTYPE_UDINT)
    self.varTableValuesColumnsSize = self.plc.read_by_name(self.config["AdsVar"]["tableValuesColumnsSize"], pyads.PLCTYPE_UDINT)

    self.varSerrorLenght = self.plc.read_by_name(self.config["AdsVar"]["errorLenght"], pyads.PLCTYPE_UDINT) + 1

  def run(self):
    self.get_size_lenght()
    while True:
      try:
        if self.busy:
          self.plc.write_by_name(self.varBusy, False, pyads.PLCTYPE_BOOL)
          self.busy = False
        if self.plc.read_by_name(self.varExecute, pyads.PLCTYPE_BOOL):
          self.busy = True
          self.plc.write_by_name(self.varBusy, True, pyads.PLCTYPE_BOOL)
          self.plc.write_by_name(self.varExecute, False, pyads.PLCTYPE_BOOL)
          self.process_execute()
      except:
        logging.error('Error:' + traceback.format_exc())
        self.connect_ads()
      time.sleep(0.1)

  def connect_ads(self):
    logging.debug('Connecting..')
    reconnect = True
    while reconnect:
      self.plc.close()
      self.ams_address = self.get_ams_address()
      self.plc = pyads.Connection(self.ams_address, pyads.PORT_TC3PLC1)      
      self.plc.open()
      try:
        self.get_size_lenght()
        logging.debug('Connected')
        reconnect = False
      except:
        logging.error('Error connecting\n'+ traceback.format_exc())
      time.sleep(2)

def main():
  pyAds = PyAds()

if __name__ == '__main__':
  main()

