import datetime


class SpyderLog:
    def __init__(self,this_format):
        self.this_format = this_format
        self.last_time = datetime.datetime.now()
    
    def debug(self,msg):
        print(self.time, self.elapsed, "DBG", msg)
        self.last_time = datetime.datetime.now()
    
    def info(self,msg):
        print(self.time,  self.elapsed, "INF", msg)
        self.last_time = datetime.datetime.now()
    
    @property
    def elapsed(self):
        tdelta = datetime.datetime.now() - self.last_time
        return "{:>3.2f}".format(tdelta.seconds / 60)
    
    @property
    def time(self):
        return datetime.datetime.now().strftime('%H:%M:%S')
