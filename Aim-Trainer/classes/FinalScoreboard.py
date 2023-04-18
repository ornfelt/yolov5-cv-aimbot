from classes.Target import Target
from classes.Text import Text
from pygame import Surface
from pygame import draw
from pygame import rect

class FinalScoreboard(object):
    """
    Class to create a final scoreboard display screen.
    """

    DEFAULT_BACKGROUND_COLOR = (255,255,255)
    DEFAULT_BORDER_SIZE = 5
    DEFAULT_BORDER_COLOR = (139,69,19)
    DEFAULT_TARGET_COLORS = [(255,0,0),(255,255,255)]
    DEFAULT_TEXT_FONT = ("Autumn",20)
    DEFAULT_TEXT_COLOR = (0,0,0)

    TARGET_BORDER = 2
    TARGET_RADIUS = 90
    SHOT_SIZE = int(TARGET_RADIUS/30+0.5)

    def __init__(self,surface,x1,y1,x2,y2,font=DEFAULT_TEXT_FONT,border=DEFAULT_BORDER_SIZE,
    border_color=DEFAULT_BORDER_COLOR,text_color=DEFAULT_TEXT_COLOR,
    background_color=DEFAULT_BACKGROUND_COLOR,target_colors=DEFAULT_TARGET_COLORS):

        """
        The final scoreboard is created using a position (x1, y1, x2, y2) of the surface.
        """

        if type(surface) is Surface:
            self.__surface = surface
        else: raise TypeError('The argument "surface" must be a Surface object.') 

        self.__surface = surface
        self.__geometry = [x1,y1,x2,y2]
        self.__font = font
        self.__border = border
        self.__border_color = border_color
        self.__text_color = text_color
        self.__background_color = background_color
        self.__target_colors = target_colors


    def __drawBorder(self):
        """
        Method to draw borders on the final scoreboard screen.
        """

        b1 = rect.Rect(
            self.__geometry[0],
            self.__geometry[1],
            self.__border,
            self.__geometry[3]-self.__geometry[1]
            )
        b2 = rect.Rect(
            self.__geometry[2]-self.__border,
            self.__geometry[1],self.__border,
            self.__geometry[3]-self.__geometry[1]
            )
        b3 = rect.Rect(
            self.__geometry[0],
            self.__geometry[1],
            self.__geometry[2]-self.__geometry[0],
            self.__border
            )
        b4 = rect.Rect(
            self.__geometry[0],
            self.__geometry[3]-self.__border,
            self.__geometry[2]-self.__geometry[0],
            self.__border
            )
        
        for border in [b1,b2,b3,b4]:   
            draw.rect(self.__surface,self.__border_color,border)


    def __drawTarget(self,location,shots,target_colors):
        """
        Method for drawing a target with all shots hit in it.
        """

        # Cria um alvo e aumenta o seu tamanho ao máximo.
        target = Target(self.__surface,radius=self.TARGET_RADIUS,target_colors=target_colors,location=location)
        target.increase(self.TARGET_RADIUS)
        target.drawTarget(border=self.TARGET_BORDER)
    
        # Desenha no alvo todos os tiros acertados.
        for shot in shots:

            # Calcula a posição do tiro no alvo: tamanho_do_alvo / 100 * posição_em_porcentagem_do_tiro
            shot_pos = []
            shot_pos.append(int(self.TARGET_RADIUS*2/100*shot[0]))
            shot_pos.append(int(self.TARGET_RADIUS*2/100*shot[1]))

            draw.circle(
                self.__surface,(0,0,0),
                [location[0]-self.TARGET_RADIUS+shot_pos[0],location[1]-self.TARGET_RADIUS+shot_pos[1]],
                self.SHOT_SIZE
            )


    def drawFinalScoreboard(self,hits,accuracy,targets_per_second,time,shots):
        """
        Method to draw the final scoreboard.

        The "shots" argument must be a list containing the 
        position (x, y) of each hit in percent.
        """

        background = rect.Rect(
            self.__geometry[0],
            self.__geometry[1],
            self.__geometry[2]-self.__geometry[0],
            self.__geometry[3]-self.__geometry[1]
            )   
        draw.rect(self.__surface,self.__background_color,background)

        # Cria um espaçamento entre as informações, com base no tamanho da tela do placar final.
        spacing_x = int(0.07*(self.__geometry[2]-self.__geometry[0]))
        spacing_y = int(0.12*(self.__geometry[3]-self.__geometry[1]))

        Text(
            self.__surface,self.__geometry[0]+spacing_x,self.__geometry[1]+spacing_y,
            text="Hits: %i"%hits,text_font=self.__font,text_color=self.__text_color
            ).drawText()
        Text(
            self.__surface,self.__geometry[0]+spacing_x,self.__geometry[1]+int(spacing_y/2)*5,
            text="Accuracy: %.1f%%"%accuracy,text_font=self.__font,text_color=self.__text_color
            ).drawText()
        Text(
            self.__surface,self.__geometry[0]+spacing_x,self.__geometry[1]+int(spacing_y/2)*8,
            text="Targets: %.2f/s"%targets_per_second,text_font=self.__font,text_color=self.__text_color
            ).drawText()
        Text(
            self.__surface,self.__geometry[0]+spacing_x,self.__geometry[1]+int(spacing_y/2)*11,
            text="Time: %s"%time,text_font=self.__font,text_color=self.__text_color
            ).drawText()           

        # Desenha a borda e o alvo com os tiros acertados.
        self.__drawBorder()
        self.__drawTarget(
            [self.__geometry[0]+self.TARGET_RADIUS+spacing_x*9,
            self.__geometry[1]+int(self.TARGET_RADIUS/2)*3],
            shots,self.__target_colors
            )


    @staticmethod
    def getAccuracy(targets,hits):
        """
        Method to obtain user accuracy.
        """
        
        if targets == 0: return 100
        elif hits == 0: return 0
        else: return 100/targets*hits
