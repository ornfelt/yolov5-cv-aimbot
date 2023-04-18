from pygame import Surface
from pygame import display
from pygame import draw
from pygame import mouse
from random import randint

class Target(object):
    """
    Class to create a target.
    """

    DEFAULT_RADIUS = 50
    DEFAULT_COLORS = [(255,0,0),(255,255,255)]

    __circle = None
    __increased = False
    __maxRadius = None
    __target = []

    def __init__(self,surface,area_geometry=False,radius=DEFAULT_RADIUS,target_colors=DEFAULT_COLORS,location=None):
        """
        The "area" parameter must be a sequence with the coordinates (x1, y1, x2, y2).

        If any value is passed to the "location" parameter, 
        the target will be created at that specific position. 
        If the "location" parameter is None, the target will be created at a 
        random position within the coordinates of the "frame_geometry" parameter.
        """

        if type(surface) is Surface:
            self.__surface = surface
        else: raise TypeError('The argument "surface" must be a Surface object.') 

        self.__surface = surface
        self.__maxRadius = radius

        self.radius = 0
        self.colors = target_colors

        # Se não existir uma localização específica, o alvo será criado 
        # alatóriamente dentro das coordernadas do parâmetro "area_geometry".
        if not location:
            self.x = randint(area_geometry[0]+int(radius/2*3),area_geometry[2]-int(radius/2*3))
            self.y = randint(area_geometry[1]+int(radius/2*3),area_geometry[3]-int(radius/2*3))
        else:
            self.x = location[0]
            self.y = location[1]
        self.drawTarget()
        

    def checkHit(self):
        """
        Checks if the mouse is within the coordinates (x1, y1, x2, y2) of the target. 
        If so, the mouse coordinates will be returned as a percentage of the target.
        """
        mouse_pos = mouse.get_pos()
        
        x1 = self.x-self.radius
        x2 = self.x+self.radius
        y1 = self.y-self.radius
        y2 = self.y+self.radius
        
        if x1 <= mouse_pos[0] <= x2:
            if y1 <= mouse_pos[1] <= y2:
                
                # Calcula a posição do tiro em relação ao alvo
                mouse_pos = [mouse_pos[0]-(self.x-self.radius),mouse_pos[1]-(self.y-self.radius)]

                # Calcula a posição do tiro em porcentagem
                percent = [100/(self.radius*2)*mouse_pos[0],100/(self.radius*2)*mouse_pos[1]]

                return percent
        return False


    def decreases(self,pixel=1):
        self.radius -= pixel


    def drawTarget(self,border=0,border_color=(0,0,0)):
        """
        Method to draw the target.
        """
        if self.radius < 0:
            raise ValueError("Radius must be a value >= 0")

        draw.circle(self.__surface,border_color,[self.x,self.y],int(self.radius+border)) # Desenha a borda do alvo.
        draw.circle(self.__surface,self.colors[0],[self.x,self.y],int(self.radius))
        draw.circle(self.__surface,self.colors[1],[self.x,self.y],int(self.radius/100*80)) # 80% do tamanho original.
        draw.circle(self.__surface,self.colors[0],[self.x,self.y],int(self.radius/100*60)) # 60% do tamanho original.
        draw.circle(self.__surface,self.colors[1],[self.x,self.y],int(self.radius/100*40)) # 40% of tamanho original.


    def increase(self,pixel=1):
        
        # Se o raio do alvo for maior ou igual ao raio máximo, 
        # será impedido de que o alvo aumente ainda mais.
        if self.radius >= self.__maxRadius or self.__increased:
            self.__increased = True
            return -1

        if self.radius + pixel > self.__maxRadius:
            pixel = self.__maxRadius - self.radius
        self.radius += pixel



        
        
