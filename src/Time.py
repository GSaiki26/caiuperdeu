## Libs
from time import localtime, strftime, time, gmtime

## Data
class Timer: ## Create and timer.
    def Start(self): ## Start the timer.
        self.initTime = time() ## Start the cronometer.
    
    def GetTime(self) -> float: ## Method to get the current time.
        if not self.stoppedTime:
            currentTime = time() - self.initTime ## Get the current time.
            return round(currentTime, 2) ## Return the seconds.
        else:
            return round(self.stoppedTime, 2) ## Return the seconds.

    def StopTime(self) -> str:
        self.stoppedTime = time() - self.initTime
        return round(self.stoppedTime, 2) ## Return the seconds.
## Methods
def GetTime() -> str:
    t = localtime() ## Get the localtime
    return  ## Return the current time.

def TreatTime(seconds: float) -> str: ## Return a stringify time.
    return strftime('%H:%M:%S', gmtime(seconds))