import pyads
from utils.utils import convert_tc_str_array, convert_tc_config_var


# AMS_ADDRESS = '5.76.220.70.1.1'
AMS_ADDRESS = '192.168.56.1.1.1'
VARIABLE = '.AdsPythonConfig.stPyAds[1].sDatabase'
# VARIABLE = 'MAIN.xFirstCycle'

plc = pyads.Connection(AMS_ADDRESS, pyads.PORT_TC3PLC1)

with plc:
    plc.write_by_name('DatabasePyAds.saTableValues', 'errorrrrr', pyads.PLCTYPE_STRING)

    lenght = 80
    # read_string = plc.read_by_name(VARIABLE, pyads.PLCTYPE_BOOL)
    print(VARIABLE)
    read_string = plc.read_by_name(VARIABLE, pyads.PLCTYPE_STRING*lenght)
    read_string = convert_tc_str_array(s=read_string)
    print(read_string)