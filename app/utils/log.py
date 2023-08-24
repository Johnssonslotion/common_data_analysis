import logging
import time
import os

class BaseLogger:
    def init_logger(self,**kwargs): ## 강제로 logger를 초기화 하고 싶을때 사용
        logger_name = kwargs.get('logger_name')
        file_log=kwargs.get('file_log',True)
        if not logger_name:
            logger_name = __name__
        str_id=str(id(self))
        self.log_path = os.environ.get('LOG_PATH')
        if not self.log_path:
            self.log_path = os.path.join(os.getcwd(), 'logs')
        if not os.path.exists(self.log_path):
            os.makedirs(self.log_path)
        debug = kwargs.get('debug')
        # TODO : add log path to env
        
        ## log file name : format : request/function name_timestamp 
        self.logger = logging.getLogger(logger_name)
        self.status = ""
        strftime = time.strftime("%Y%m%d%H%M%S", time.localtime())
        log_file_name = f'[{strftime}][{logger_name}]_{str_id}.log'
        log_file_path=os.path.join(self.log_path, log_file_name)
        self.formatter = logging.Formatter('%(asctime)s:%(name)s:%(levelname)s:%(message)s')
        self.file_handler = logging.FileHandler(log_file_path)
        self.file_handler.setFormatter(self.formatter)
        if file_log:
            self.logger.addHandler(self.file_handler) ## 
        self.obj = None
        self.prefix = None
        self.fn = None
        self.state = None
        self.msg = None
        if debug:
            self.logger.setLevel(logging.DEBUG)
        else:
            self.logger.setLevel(logging.INFO)
        self.report(fn='__init__',state='init',msg='logger init')

    def __init__(self, **kwargs):
        ## called by the child class
        ## get log path from env
        logger_name = kwargs.get('logger_name')
        if not logger_name:
            logger_name = __name__
        
        self.log_path = os.environ.get('LOG_PATH')
        if not self.log_path:
            self.log_path = os.path.join(os.getcwd(), 'logs')
        if not os.path.exists(self.log_path):
            os.makedirs(self.log_path)
        debug = kwargs.get('debug')
        # TODO : add log path to env        
        ## log file name : format : request/function name_timestamp 
        self.logger = logging.getLogger(logger_name)
        self.status = ""
        strftime = time.strftime("%Y%m%d%H%M%S", time.localtime())
        log_file_name = f'{logger_name}_{strftime}.log'
        log_file_path=os.path.join(self.log_path, log_file_name)
        self.formatter = logging.Formatter('%(asctime)s:%(name)s:%(levelname)s:%(message)s')
        self.file_handler = logging.FileHandler(log_file_path)
        self.file_handler.setFormatter(self.formatter)
        self.logger.addHandler(self.file_handler)
        self.obj = None
        self.prefix = None
        self.fn = None
        self.state = None
        self.msg = None
        if debug:
            self.logger.setLevel(logging.DEBUG)
        else:
            self.logger.setLevel(logging.INFO)
        self.report(fn='__init__',state='init',msg='logger init')

    def report(self,msg=None,obj=None,prefix=None,fn=None, state=None):
        ## BASE STATE REPORTING FUNCTION
        ## obj : when class is called, init obj var
        ## prefix : when called from a function, attach prefix
        ## fn : function name
        ## state : status of the function
        ## msg : message to be logged
        ## format:[obj][prefix][fn][state][msg]
        if obj==None:
            obj=self.obj
            if obj==None:
                obj="OBJ NONE"
        else:
            self.obj=obj

        if prefix==None:
            prefix=self.prefix
            if prefix==None:
                prefix="PREFIX NONE"
        else:
            self.prefix=prefix

        if fn==None:
            fn=self.fn 
        else:
            self.fn=fn

        if state==None:
            state=self.state
        else:
            self.state=state

        if msg==None:
            self.logger.info(f"|{obj.upper()}|{prefix.upper()}|{fn.upper()}|{state.upper()}")
        else:
            self.logger.info(f"|{obj.upper()}|{prefix.upper()}|{fn.upper()}|{state.upper()}|{msg}")
        
    









