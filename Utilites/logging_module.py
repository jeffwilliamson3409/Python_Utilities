import logging
import sys
import os
import time
import datetime
import json


class BSIG_logger(object):
  
    '''
[log_file_name] = absolute path to log file output \n
[get_logger_name] kwarg value should be the absolute path to your logger output file - defaults to base.bsig.logger \n
[file_handler_format_string] kwarg value should contruct your file handler output format - defaults to %(asctime)s - %(name)s - %(levelname)s - %(message)s
    '''  

    with open('C:\\Users\\jwilliamson\\Desktop\\BSIG_Config.json', 'r') as BSIG_config:
        data = json.load(BSIG_config)

    log_file_path = data['Logs']['DEV']['BSIG_log_file_path']

    def __init__(self,   
                 log_file_name = 'output', 
                 get_logger_name='BSIG_logger',                       
                 file_handler_format_string='%(asctime)s - %(name)s - %(levelname)s - %(message)s' 
                 ):   
        logging.root.setLevel(logging.INFO)
        self.get_logger_name = get_logger_name
        self.file_handler_format_string = file_handler_format_string
        self.log_file_name = BSIG_logger.log_file_path + log_file_name + '.log'
        self.file_handler = logging.FileHandler(self.log_file_name, mode="w")
        self.file_handler.setLevel(logging.INFO)
        self.file_handler.setFormatter(logging.Formatter(self.file_handler_format_string))
        self.log = logging.getLogger(self.get_logger_name)
        self.log.addHandler(self.file_handler)
       


