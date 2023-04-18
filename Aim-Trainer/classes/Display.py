from pygame import display
from pygame import image
from os.path import join
from os import getcwd

class Display(object):
    """
    Class to initialize the program window.
    """

    DEFAULT_COLOR = (255,255,255)
    DEFAULT_TITLE = "Window"
    DEFAULT_ICON_PATH = join(getcwd(),"images","icon2.png")

    def __init__(self,width,height,title=DEFAULT_TITLE,display_color=DEFAULT_COLOR,icon=DEFAULT_ICON_PATH):

        display.set_mode([width,height])
        display.set_caption(title)
        display.set_icon(image.load(icon))
        
        self.__display = display.get_surface()
        self.__color = display_color
        self.drawDisplay()
    

    def drawDisplay(self):
        self.__display.fill(self.__color)
 
 
    def getSurface(self):
        return self.__display

