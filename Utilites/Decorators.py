from functools import wraps
import time
import datetime


class Utility_Decorators(object):

    @staticmethod
    def decorator_logger(orig_func):
        import logging
        logging.basicConfig(filename='{}.log'.format(orig_func.__name__),level=logging.INFO)
        @wraps(orig_func)
        def wrapper(*args, **kwargs):
            timeStamp = datetime.datetime.now()
            logging.info(' {} Ran with args {} and kwargs {} >> {}'.format(orig_func.__name__, args, kwargs, timeStamp))
            return orig_func(*args, **kwargs)
        return wrapper

    @staticmethod
    def decorator_time(orig_func):
        @wraps(orig_func)
        def wrapper(*args, **kwargs):
            t1 = time.time()
            result = orig_func(*args, **kwargs)
            t2 = time.time() - t1
            print('{} took {} to run'.format(orig_func.__name__, t2))
            return result
        return wrapper


# decorator class
class decorator_logger_class(object):

    def __init__(self, function_on_which_the_decorator_is_operating):
        self.function_on_which_the_decorator_is_operating = function_on_which_the_decorator_is_operating

    def __call__(self, *args, **kwargs):
        import logging
        logging.basicConfig(filename='{}.log'.format(self.function_on_which_the_decorator_is_operating.__name__), level=logging.INFO)
        logging.info(' {} Ran with args {} and kwargs {}'.format(self.function_on_which_the_decorator_is_operating.__name__, args, kwargs))
        return self.function_on_which_the_decorator_is_operating(*args, **kwargs)



@Utility_Decorators.decorator_logger
@Utility_Decorators.decorator_time
def addEm(x, y, **kwargs):
    ans =  x + y
    print('{} + {} = {}'.format(x, y, ans))

addEm(3,6, Bill='A girl that is cool')




