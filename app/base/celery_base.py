from multiprocessing.pool import AsyncResult
from celery import Celery, Task
import os
from celery.bin import worker
from celery.result import GroupResult

from utils import decrypt, encrypt



# app=Celery('tasks')
# app.config_from_object('celeryconfig')





class CeleryBase:
    '''
    Celery를 사용하기 위한 기본 클래스
    Task에 대한 wrapper를 제공한다.
    
    '''
    def __init__(self, username, password,ENV=None, config=None):
        ## For local, #TODO : For production
        if ENV=="PROD":
            broker_url=os.environ.get("RABBITMQ_URL")
            broker_url=os.environ.get("RADIS_URL")
        elif ENV=="DOCKER":
            broker_url="rabbitmq"
            redis_url="redis"
        else:
            broker_url="localhost:5672"
            redis_url="localhost:6379"
            #url="localhost"
        if username=="guest":
            username="guest"
            password="guest"
                
        password=self.decrypt(password)
        ## TODO 
        #self.app=Celery('tasks',backend=f'redis://{username}:{password}@{redis_url}/0',broker=f'pyamqp://{username}:{password}@{broker_url}//')
        self.app=Celery('tasks',backend=f'redis://{redis_url}/0',broker=f'pyamqp://{username}:{password}@{broker_url}//')
        self.config()
        if config:
            self.config_update(**config)
    
        
    def process(self, x,y):
        @self.app.task(name="process")
        def _process(x,y):
            return x+y
        return _process.delay(x,y)        
            
    @classmethod
    def decrypt(cls, passward):
        '''
        환경변수에 SECRET_KEY를 사용하여
        password를 복호화한다. 없을때 예외처리 필요
        '''
        _key = os.environ.get("SECRET_KEY").encode()
        return decrypt(_key, passward)
    
    @classmethod
    def encrypt(cls, passward):
        '''
        password를 암호화한다.
        '''
        _key = os.environ.get("SECRET_KEY").encode()
        return encrypt(_key, passward)

    
    def config(self):
        '''
        celery의 기본 설정 정의
        '''
        class CeleryConfig:
            enable_utc = True
            timezone = 'Asia/Seoul'
            task_serializer="pickle"
            result_serializer="pickle"
            accept_content=["application/json","application/x-python-serialize"]
            result_accept_content=["application/json","application/x-python-serialize"]    

        self.app.config_from_object(CeleryConfig)

    def config_update(self, **kwargs):
        '''
        celery의 설정을 변경한다.
        '''
        self.app.conf.update(**kwargs)

    def register_task(self, name, func):
        '''
        function을 task로 등록한다.
        '''
        return self.app.task(name=name)(func)
    
    def create_signature(self, name, *args, **kwargs):
        '''
        task의 signature를 생성한다.
        '''
        
        return self.app.signature(name,app=self.app,args=args,kwargs=kwargs["kwargs"])

    def run_worker(self, *args):
        '''
        celery worker를 실행한다.
        타 쓰레드에서 실행할 것
        ref: https://docs.celeryq.dev/en/stable/userguide/workers.html
        celery worker --help

        Worker Options:
        -n, --hostname HOSTNAME         Set custom hostname (e.g., 'w1@%%h').
                                        Expands: %%h (hostname), %%n (name) and
                                        %%d, (domain).
        -D, --detach                    Start worker as a background process.
        -S, --statedb PATH              Path to the state database. The
                                        extension '.db' may be appended to the
                                        filename.
        -l, --loglevel                  [DEBUG|INFO|WARNING|ERROR|CRITICAL|FATAL]
                                        Logging level.
        -O, --optimization              [default|fair]
                                        Apply optimization profile.
        --prefetch-multiplier           <prefetch multiplier>
                                        Set custom prefetch multiplier value
                                        for this worker instance.

        Pool Options:
        -c, --concurrency               <concurrency>
                                        Number of child processes processing
                                        the queue.  The default is the number
                                        of CPUs available on your system.
        -P, --pool                      [prefork|eventlet|gevent|solo|processes|threads|custom]
                                        Pool implementation.
        -E, --task-events, --events     Send task-related events that can be
                                        captured by monitors like celery
                                        events, celerymon, and others.
        --time-limit FLOAT              Enables a hard time limit (in seconds
                                        int/float) for tasks.
        --soft-time-limit FLOAT         Enables a soft time limit (in seconds
                                        int/float) for tasks.
        --max-tasks-per-child INTEGER   Maximum number of tasks a pool worker
                                        can execute before it's terminated and
                                        replaced by a new worker.
        --max-memory-per-child INTEGER  Maximum amount of resident memory, in
                                        KiB, that may be consumed by a child
                                        process before it will be replaced by a
                                        new one.  If a single task causes a
                                        child process to exceed this limit, the
                                        task will be completed and the child
                                        process will be replaced afterwards.
                                        Default: no limit.

        Queue Options:
        --purge, --discard
        -Q, --queues COMMA SEPARATED LIST
        -X, --exclude-queues COMMA SEPARATED LIST
        -I, --include COMMA SEPARATED LIST

        Features:
        --without-gossip
        --without-mingle
        --without-heartbeat
        --heartbeat-interval INTEGER
        --autoscale <MIN WORKERS>, <MAX WORKERS>

        Embedded Beat Options:
        -B, --beat
        -s, --schedule-filename, --schedule TEXT
        --scheduler TEXT

        Daemonization Options:
        -f, --logfile TEXT  Log destination; defaults to stderr
        --pidfile TEXT
        --uid TEXT
        --gid TEXT
        --umask TEXT
        --executable TEXT

        Options:
        --help  Show this message and exit.     
        '''
        args=["worker","--loglevel=INFO"]
        if os.environ["concurrency"] is not None:
            args.append(f"--concurrency={os.environ['concurrency']}")
        # if os.environ["max_tasks_per_child"] is not None:
        #     args.append(f"--max-tasks-per-child={os.environ['max_tasks_per_child']}")
        return self.app.worker_main(argv=args)
    def get_result(self,task_id):
        res = AsyncResult(task_id, app=self.app)
        status = res.status
        result = res.result
        return status, result
    
    def get_result_by_group(self,group_id):
        group_result=GroupResult.restore(group_id,app=self.app)
        return group_result
    
    