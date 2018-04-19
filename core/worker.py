import os
import workerthread
from logger import log, LogLevel

class Worker:
    def __init__(self,x):
        self.worker_id = x
        self.worker_thread = None

    
    def start_work(self,task):
        self.task = task
        self.status = None
        self.worker_thread = workerthread.WorkerThread()
        self.worker_thread.start_work(task)


    def is_active(self):
        if self.worker_thread:
            return self.worker_thread.is_active()
        return False


    def is_success(self):
        if self.worker_thread:
            if self.worker_thread.is_alive():
                return None
            else:
                if self.status == 'success':
                    return True
                else:
                    return False
        return None

    def get_id(self):
        return self.worker_id


    


   
        
