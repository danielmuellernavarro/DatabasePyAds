import logging.handlers
import logging
import sys
import os
from datetime import datetime

# logger.debug('This is a debug message')
# logger.info('This is an info message')
# logger.warning('This is a warning message')
# logger.error('This is an error message')
# logger.critical('This is a critical message')

class Logger:
    def __init__(self, path, level, log_in_files=False):
        self.datetimeLastRecords = list()
        
        handlers = list()
        handlers.append(logging.StreamHandler())
        if log_in_files:
            handler = RotatingFileHandler(
                path,
                maxBytes=1024*1024,
                backupCount=16,
                encoding='utf-8')
            handler.doRollover()
            handlers.append(handler)
        logging.basicConfig(
            handlers = handlers,
            datefmt = '%Y-%m-%d %H:%M:%S',
            format = '%(asctime)s - %(msg)s',
            level = level
            )
        logging.getLogger().addHandler(logging.StreamHandler())
        logging.getLogger().addFilter(self)

    def filter(self, record):
        max_seconds = 10
        max_records = 10
        max_last_record = 5
        now = datetime.now()
        count = 0
        for x in self.datetimeLastRecords:
            diff = (now - x).total_seconds()
            if diff < max_seconds:
                count += 1
        if count < max_last_record or len(self.datetimeLastRecords) < max_records:
            self.datetimeLastRecords.append(datetime.fromtimestamp(record.created))
            if len(self.datetimeLastRecords) > max_records:
                self.datetimeLastRecords.pop(0)
            return True
        return False

class RotatingFileHandler(logging.handlers.RotatingFileHandler):
    def __init__(self, path, **kwargs):
        os.makedirs(os.path.dirname(path), exist_ok=True)
        super().__init__(path, **kwargs)
