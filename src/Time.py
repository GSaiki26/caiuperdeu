## Libs
from time import localtime, strftime, time

## Data
class Timer: ## Create and timer.
    def Start(self): ## Start the timer.
        self.initTime = time() ## Start the cronometer.
    
    def GetTime(self) -> float: ## Method to get the current time.
        currentTime = time() - self.initTime ## Get the current time.
        return round(currentTime, 2) ## Return the seconds.

## Methods
def GetTime() -> str:
    t = localtime() ## Get the localtime
    return strftime('%H:%M:%S',t) ## Return the current time.

