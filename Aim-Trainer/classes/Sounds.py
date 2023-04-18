from pygame import mixer
from os.path import join
from os import getcwd

class Sounds(object):
    """
    Class for playing program sounds.
    """

    __cwd = getcwd()

    metal_hit_sound = 0
    shooting_sound = 1
    target_loss_sound = 2
    without_ammunition_sound = 3

    metal_hit_sound_path = join(__cwd,"sounds","metal_hit.wav")
    shooting_sound_path = join(__cwd,"sounds","shooting.wav")
    target_loss_sound_path = join(__cwd,"sounds","target_loss.wav")
    without_ammunition_sound_path = join(__cwd,"sounds","without_ammunition.wav")
    

    def __init__(self,buffer=64):

        # The "buffer" parameter must have a low value to decrease latency.
        mixer.init(buffer=buffer)

        self.__sounds = {}
        self.__sounds[self.metal_hit_sound] = mixer.Sound(self.metal_hit_sound_path)        
        self.__sounds[self.shooting_sound] = mixer.Sound(self.shooting_sound_path)
        self.__sounds[self.target_loss_sound] = mixer.Sound(self.target_loss_sound_path)
        self.__sounds[self.without_ammunition_sound] = mixer.Sound(self.without_ammunition_sound_path)


    def playSound(self,sound):
        """
        Method for playing specific loaded sounds.
        The "sound" parameter must be a Sounds attribute where the name ends with "sound".
        """
        if sound in self.__sounds:
            self.__sounds[sound].play()


    @staticmethod
    def playSoundFrom(filename):
        """
        Method to play sound from a file.
        """

        mixer.music.load(filename)
        mixer.music.play()
