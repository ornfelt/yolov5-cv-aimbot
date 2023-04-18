from pygame import Surface
from pygame import draw
from pygame import rect

class TargetArea(object):
    """
    Class for drawing an area for creating targets.
    """

    LINE_SPACING = 20
    LINE_SIZE = 1
    DEFAULT_COLORS = [(128,128,128),(148,148,148)]

    def __init__(self,surface,x1,y1,x2,y2,target_area_colors=DEFAULT_COLORS):
        """
        The target area is created using a position (x1, y1, x2, y2) of the surface.
        """

        if type(surface) is Surface:
            self.__surface = surface
        else: raise TypeError('The argument "surface" must be a Surface object.')  

        self.__geometry = [x1,y1,x2,y2]
        self.__colors = target_area_colors  

        if len(self.__colors) == 1:
            self.__colors[1] = self.DEFAULT_COLORS[1]
        elif len(self.__colors) < 1:
            self.__colors[1] = self.DEFAULT_COLORS


    def __drawLines(self,x1,y1,x2,y2):

        """
        Draws lines in the target area.
        """

        for x in range(x1,x2,self.LINE_SPACING):
            line = rect.Rect(x,y1,self.LINE_SIZE,y2-y1)
            draw.rect(self.__surface,self.__colors[1],line)

        for y in range(y1,y2,self.LINE_SPACING):
            line = rect.Rect(x1,y,x2-x1,self.LINE_SIZE)
            draw.rect(self.__surface,self.__colors[1],line)


    def drawArea(self):
        """
        Draws the target area.
        """

        background = rect.Rect(
            self.__geometry[0],
            self.__geometry[1],
            self.__geometry[2]-self.__geometry[0],
            self.__geometry[3]-self.__geometry[1]
            )
        draw.rect(self.__surface,self.__colors[0],background)
        self.__drawLines(*self.__geometry)
    

    def getGeometry(self):
        return self.__geometry


    def setGeometry(self,x1,y1,x2,y2):
        self.__geometry = [x1,y1,x2,y2]




