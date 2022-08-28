from threading import Timer 


class Interval:

    def __init__(self, interval, func, func2) -> None:
        self.func = func
        self.func2 = func2
        self.interval = interval
        self.switch = False
        self.timer = Timer(interval, self._restart())
    
    def _restart(self):
        def wrapper():
            
            func = self.func 
            if self.switch == True:
                func = self.func2
            self.switch = not self.switch
            func()
            self.timer.cancel()
            self.timer = Timer(self.interval, self._restart())
            self.start()
        return wrapper
    
    def start(self):
        self.timer.start()

    def stop(self):
        self.timer.cancel()