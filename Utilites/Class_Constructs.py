import sys
import logging
from logging_module import *
import traceback

exec_log = BSIG_logger(log_file_name='dorag', get_logger_name='BSIG_logger.dorag')
#exec_log = BSIG_logger(log_file_name='logs/execution.log', file_handler_level='INFO', get_logger_name='base_bsig_logger.class_contructs_execution')
#err_log = BSIG_logger('logs/errors.log', file_handler_level='ERROR', get_logger_name='base_bsig_logger.class_contructs_error')

class AlfaDog(object): 

    '''I parse Alfa output files'''

    version = '1.0'

     
    def __init__(self, file_path, d_y, d_m, d_d):  
        exec_log.log.error('Fart!!!')
        self.file_path = file_path
        self.d_y = d_y
        self.d_m = d_m
        self.d_d = d_d

    def __str__(self):
        return self.file_path + '\n' + str(self.d_y) + '\n' + str(self.d_m) + '\n' + str(self.d_d)

    ''' Custom constructor for date from string '''
    @classmethod
    def date_from_str(cls, file_path, date_str):
        ''' pass date_str arg as 'yyyy-mm-dd' or 'yyyy/mm/dd' '''
        try:
            y,m,d = map(int, date_str.split('-'))
        except:
            pass       
        try:
            y,m,d = map(int, date_str.split('//'))
        except:
            pass         
        return cls(file_path, y, m, d)

    def __iter__(self):
        self.iterator = 0
        self.tokens = self.file_path.split('\\')
        self.n = len(self.tokens)
        return self

    def __next__(self):
        if self.iterator < self.n:
            result = self.tokens[self.iterator]
            self.iterator += 1
            return result
        else:
            raise StopIteration

    def get_file_ext(self):
        filename, file_extension =  path.splitext(self.file_path)
        return file_extension


if __name__ == '__main__':

    try:
        c = AlfaDog('a', 2019, 10, 2)
        d = AlfaDog.date_from_str('a', '2019-10-02')
        e = AlfaDog.date_from_str('a', '2019//10//02')

        print('******** c *********')
        print(c.d_d, c.d_m, c.d_y)
        print('******** d *********')
        print(d.d_d, d.d_m, d.d_y)
        print('******** e *********')
        print(e.d_d, e.d_m, e.d_y)

    except Exception as e:
        exc_type, exc_value, exc_traceback = sys.exc_info()
        #err_log.log.error(exc_type)
        #err_log.log.error(exc_value)
        #err_log.log.error(exc_traceback)
