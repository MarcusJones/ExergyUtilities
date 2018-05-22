import datetime


class SpyderLog:
    def __init__(self,this_format):
        self.this_format = this_format
    def debug(self,msg):
        print(self.time, msg)
    def info(self,msg):
        print(self.time, msg)
    @property
    def time(self):
        return datetime.datetime.now().strftime('%H:%M:%S')
