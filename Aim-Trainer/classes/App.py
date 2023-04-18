from classes.Display import Display
from classes.FinalScoreboard import FinalScoreboard
from classes.Sounds import Sounds
from classes.TargetArea import TargetArea
from classes.Target import Target
from classes.Text import Text
from classes.Timer import Timer
from time import time
import pygame

class App(object):
    """
    Main Class
    """

    BORDER = 10

    DISPLAY_COLOR = (100,100,100)
    DISPLAY_GEOMETRY = [700,500]
    DISPLAY_TITLE = "Aim Trainer"

    FRAMES_PER_SECOND = 60

    LIVES = 5
    MISSING_SHOTS_DECREASES_LIFE = False

    SCOREBOARD_AREA = 50
    SCOREBOARD_COLOR = (255,255,255)
    SCOREBOARD_FONT = ('Comic Sans MS', 21)
    SCOREBOARD_FORMAT = "Hits:  %i   Accuracy:  %.1f%%   FPS: %i   Targets: %.2f/s   Lives: %i"
    SCOREBOARD_LOCATION = [BORDER+1,10]

    SOUNDS_BUFFER = 64

    TARGET_ADD_TIME = 0.2
    TARGET_AREA_COLORS = [(128,128,128),(148,148,148)]
    TARGET_BORDER = 0
    TARGET_AREA_GEOMETRY = [0+BORDER,SCOREBOARD_AREA+BORDER,DISPLAY_GEOMETRY[0]-BORDER,DISPLAY_GEOMETRY[1]-BORDER]
    TARGET_COLORS = [(255,0,0),(255,255,255)]
    TARGET_LIMIT_PER_SECOND = None
    TARGET_RADIUS = 40
    TARGETS_PER_SECOND = 1.8
    TARGET_SPEED = 0.4

    FINAL_SCOREBOARD_BACKGROUND_COLOR = (255,255,255)
    FINAL_SCOREBOARD_BORDER = 5
    FINAL_SCOREBOARD_BORDER_COLOR = (139,69,19)
    FINAL_SCOREBOARD_FONT = ("Arial",40)
    FINAL_SCOREBOARD_GEOMETRY = [TARGET_AREA_GEOMETRY[0]+50,TARGET_AREA_GEOMETRY[1]+50,TARGET_AREA_GEOMETRY[2]-50,TARGET_AREA_GEOMETRY[3]-50]
    FINAL_SCOREBOARD_TEXT_COLOR = (80,80,80)


    def __init__(self):

        self.sounds = Sounds(self.SOUNDS_BUFFER)
        pygame.init()

        self.display = Display(
            *self.DISPLAY_GEOMETRY,
            self.DISPLAY_TITLE,
            self.DISPLAY_COLOR
            )
        self.__surface = self.display.getSurface()

        self.finalScoreboard = FinalScoreboard(
            self.__surface,
            *self.FINAL_SCOREBOARD_GEOMETRY,
            self.FINAL_SCOREBOARD_FONT,
            self.FINAL_SCOREBOARD_BORDER,
            self.FINAL_SCOREBOARD_BORDER_COLOR,
            self.FINAL_SCOREBOARD_TEXT_COLOR,
            self.FINAL_SCOREBOARD_BACKGROUND_COLOR,
            self.TARGET_COLORS
            )

        self.scoreboardText = Text(
            self.__surface,
            *self.SCOREBOARD_LOCATION,
            text_font=self.SCOREBOARD_FONT,
            text_color=self.SCOREBOARD_COLOR
            )

        self.targetArea = TargetArea(
            self.__surface,
            *self.TARGET_AREA_GEOMETRY,
            self.TARGET_AREA_COLORS
            )

        self.__timer = Timer()
        self.__clock = pygame.time.Clock()


    def captureEvents(self):
        """
        Method for capturing events and taking action based on them.
        """

        for event in pygame.event.get():

            # Verifica se houve um evento para fechar a janela do programa.
            if event.type == pygame.QUIT:
                self.__stop = True
                break

            # Verifica se uma tecla foi pressionada.
            if event.type == pygame.KEYDOWN:

                # Se a tecla pressionada foi "Esc", o programa será fechado.
                if event.key == pygame.K_ESCAPE:
                    self.__stop = True
                    break

                # Se a tecla pressionada foi "Enter" ou "Space", será criada uma nova
                # sessão caso o usuário esteja na tela de fim de jogo.
                elif event.key in [pygame.K_RETURN,pygame.K_SPACE]:
                    if not self.__start:
                        self.__start = True

            # Se o botão "1" do mouse foi pressionado, será efetuado um disparo.
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                
                # Se uma sessão estiver em execução, será executado um som de tiro.
                # Senão, o som a ser executado será de uma arma sem munição.
                if self.__start:
                    self.sounds.playSound(self.sounds.shooting_sound)
                else:
                    self.sounds.playSound(self.sounds.without_ammunition_sound)
                    continue
                
                # Verifica se o tiro acertou algum alvo.
                for target in self.__targets.copy():

                    # Obtém a posição (x,y) do tiro em relação ao alvo
                    hit = target.checkHit()

                    # Se acertou, o número de acertos aumentará e o alvo será removido.
                    if hit:
                        self.sounds.playSound(self.sounds.metal_hit_sound)
                        self.__shots.append(hit)
                        self.__targets.remove(target)
                        self.__hits += 1
                        return

                # Se nenhum alvo foi acertado, o número de falhas aumentará e caso 
                # a opção para perda de vida por tiros perdidos esteja ativada, 
                # o usuário perderá uma vida na sessão.
                if self.MISSING_SHOTS_DECREASES_LIFE:
                    self.__lives -= 1
                self.__failures += 1


    def createTarget(self):
        """
        Method to create a target within the screen.
        """

        target = Target(
            surface = self.__surface,
            area_geometry = self.TARGET_AREA_GEOMETRY,
            radius=self.TARGET_RADIUS,
            target_colors=self.TARGET_COLORS
            )
        self.__targets.append(target)


    def gameOver(self):
        """
        Method for creating an endgame screen.
        """

        self.__start = False

        # Obtém as informações da última sessão para inserir os dados no placar final.
        hits = self.__hits
        accuracy = FinalScoreboard.getAccuracy(self.__hits+self.__failures,self.__hits)
        targets_per_second = self.__target_per_second
        time = self.__timer.getTime()
        shots = self.__shots.copy()

        
        # Enquanto o usuário não tentar fechar o programa ou pressionar uma tecla para criar
        # uma nova sessão, a tela de fim de jogo será desenhada.
        while not self.__stop and not self.__start:

            self.captureEvents()
            self.display.drawDisplay()
            self.targetArea.drawArea()

            # Coloca instrução no área do placar para continuar, criando uma nova sessão.
            self.scoreboardText.setText('GAME OVER:  Click "Enter" or "Space" to continue.')
            self.scoreboardText.drawText()

            self.finalScoreboard.drawFinalScoreboard(hits,accuracy,targets_per_second,time,shots)

            self.__clock.tick(self.FRAMES_PER_SECOND)
            pygame.display.flip()

        # Se o usuário pressionar uma botão para sair do programa, o mesmo fechará.
        # Se o usuário pressionar uma tecla para continuar, uma nova sessão será criada.
        if self.__stop:
            pygame.quit()
        else: self.run()


    def run(self):
        """
        Method to start a new session.
        """

        self.__failures = 0
        self.__hits = 0
        self.__stop = False
        self.__targets = []
        self.__shots = []
        self.__lives = self.LIVES
        self.__target_per_second = self.TARGETS_PER_SECOND
        self.__start = True

        # Define a fonte para o placar
        self.scoreboardText.setFont(self.SCOREBOARD_FONT)

        # Inicia o cronômetro
        self.__timer.start()

        last_time_to_create_target = time()
        last_time_to_add_tps = time()

        # Enquanto o usuário não tentar fechar o programa e possuir vidas, a sessão
        # continuará a ser executada.
        while not self.__stop and self.__lives > 0:
            self.captureEvents()

            # Cria um novo alvo com base na quantidade de alvos por segundo.
            if time() - last_time_to_create_target >= 1/self.__target_per_second:
                self.createTarget()
                last_time_to_create_target = time()

            # Aumenta a quantidade de alvos por segundos.
            if time() - last_time_to_add_tps  >= self.TARGET_ADD_TIME:
                if not self.TARGET_LIMIT_PER_SECOND or self.TARGET_LIMIT_PER_SECOND > self.__target_per_second: 
                    self.__target_per_second += 1/self.__target_per_second/100
                    last_time_to_add_tps  = time()

            self.update()

        # Se o programa saiu do "while" devido a chamada de um evento
        # para fechar o programa, o programa será finalizado. 
        # Se este não foi o caso, quer dizer que a sessão atual encerrou e irá
        # direto para a tela de fim de jogo.
        if self.__stop:
            pygame.quit()
        else:
            self.gameOver()


    def setScore(self):
        """
        Method for inserting updated information in the scoreboard.
        """

        hits = self.__hits
        accuracy = FinalScoreboard.getAccuracy(self.__hits+self.__failures,self.__hits)
        fps = self.__clock.get_fps()
        targets_per_second = self.__target_per_second
        self.scoreboardText.setText(self.SCOREBOARD_FORMAT%(hits,accuracy,fps,targets_per_second,self.__lives))


    def targetAnimation(self):
        """
        Method for generating target animation.
        """

        targets = self.__targets.copy()
        targets.reverse()
        
        for target in targets:
            try:

                # Caso não seja possível aumentar ainda mais o alvo,
                # seu tamanho diminuirá.
                if target.increase(self.TARGET_SPEED) == -1:
                    target.decreases(self.TARGET_SPEED)
                target.drawTarget(border=self.TARGET_BORDER)
            
            # Caso o alvo tenha diminuido até o limite, ele será removido 
            # e um som de alvo perdido será executado.
            except ValueError:
                self.sounds.playSound(self.sounds.target_loss_sound)
                self.__targets.remove(target)
                self.__lives -= 1


    def update(self):
        """
        Method for updating the graphics part of the program.
        """

        self.setScore()

        self.display.drawDisplay()
        self.scoreboardText.drawText()

        self.targetArea.drawArea()
        self.targetAnimation()

        self.__clock.tick(self.FRAMES_PER_SECOND)
        pygame.display.flip()
