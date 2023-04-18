from time import gmtime,strftime,time

class Timer(object):

    __time = None

    def start(self):
        """
        Method to start the timer.
        """
        self.__time = time()
    
    
    def getTime(self,format="%M:%S"):
        """
        Method to get the time on the timer.
        """
        return strftime(format,gmtime(time()-self.__time))