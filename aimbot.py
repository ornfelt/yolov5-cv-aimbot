import warnings
warnings.filterwarnings("ignore")

import pyautogui
import pydirectinput

import keyboard as kb
import cv2

from sys import platform
from time import time, sleep
from threading import Thread, Lock

from gamecapture import GameCapture
from detection import Detection
from vision import Vision
from utilities import Utilities

class AimBot:
    capture = None
    detector = None
    vision = None

    is_running = False
    is_active = False
    is_single_thread = False
    lock = None
    state = None

    frame = None
    active_targets = None
    action_history = None
    mirror_ratio = 1
    start_time = 0

    def __init__(self, ist=True, mr=1):
        self.lock = Lock()
        self.active_targets = []
        self.action_history = []
        self.is_single_thread = ist
        self.mirror_ratio = 1 / mr

        self.capture = GameCapture()
        self.detector = Detection()
        self.vision = Vision()

    
    def shoot(self, target):
        try:
            if (target[0] < self.capture.w - 20 and target[0] > 20) \
                and (target[1] < self.capture.h - 20 and target[1] > 20):
                gui.moveTo(target[0], target[1])
                #sleep(1)
                gui.click()
                self.action_history.append((time() - self.start_time, target))
            else:
                raise Exception('Target out of screen bounds.')

        except Exception as e:
            gui.moveTo(self.capture.w/2, self.capture.h/2)
            self.action_history.append((time() - self.start_time, ('OOB')))
    
    def user_kill_signal(self):
        if kb.is_pressed('-'):
            self.toggle()
        if kb.is_pressed('='):
            self.stop()
            return True
        return False

    def monitor_toggle_actions(self):
        while self.is_running:
            self.user_kill_signal()

    def display(self, frame):
        # TODO: write frames to video file if recording
        cv2.imshow('MIRROR: ' + self.capture.windowname, cv2.resize(frame, (0,0), fx=self.mirror_ratio, fy=self.mirror_ratio))
        if cv2.waitKey(1) & 0xFF == ord('='):
            self.stop()

    def run_single_thread(self):
        while self.is_running:
            try:
                if self.user_kill_signal():
                    break
                frame = self.capture.capture_frame()

                if self.is_active:
                    predictions = self.detector.detect(frame)
                    target = self.vision.get_priority_target(predictions)
                    frame = self.vision.draw_bounding_boxes(frame, predictions)
                    frame = self.vision.draw_crosshair(frame, target)
                    
                    # HEHE
                    if target is not None:
                       self.shoot(target)
                       sleep(0.1)

                self.display(frame)
                
            except Exception as e:
                print(e)
                pass

        #out.release()
        cv2.destroyAllWindows()

        with open('output/actions.txt', 'w') as f:
            for action in self.action_history:
                f.write(str(action))

    def run(self):
        while self.is_running:
            # TODO: shoot active target
            pass

    def start(self):
        if not self.is_running:
            self.is_running = True
            self.start_time = time()

            #mt = Thread(target=self.monitor_toggle_actions)
            #mt.start()

            if self.is_single_thread:
                t = Thread(target=self.run_single_thread)
                t.start()
                #self.run_single_thread()
            else:
                t = Thread(target=self.run)
                t.start()

    def stop(self):
        self.lock.acquire()
        self.is_running = False
        self.is_active = False
        self.lock.release()
    
    def update(self, frame):
        self.lock.acquire()
        self.frame = frame
        self.lock.release()

    def toggle(self):
        self.lock.acquire()
        self.is_active = not self.is_active
        self.lock.release()

    def is_active(self):
        active = 0
        self.lock.acquire()
        active = self.is_active
        self.lock.release()
        return active


def main():   
    aimbot = AimBot(mr=3, ist=True)
    aimbot.start()

def usage():
    print('\033[96m'+'======================= '+'\033[91m'+'U S A G E'+'\033[96m'+' =======================\n'+'\033[0m')
    print('\033[92m'+"\t\tExit key: '=' \n\t\tToggle firing key: '-'"+'\033[0m')
    print('\033[96m'+'\n=========================================================='+'\033[0m')

gui = None
if __name__ == '__main__':
    if platform == "win32":
        gui = pydirectinput
    else:
        gui = pyautogui
    
    gui.PAUSE = 0

    usage()
    main()