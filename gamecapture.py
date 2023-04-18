import numpy as np
import cv2
import pyautogui
from threading import Thread, Lock

from sys import platform
from PIL import Image
from time import time
from mss import mss

import win32gui
import win32ui
import win32con

class GameCapture:
    running = False
    lock = None
    screen_capture = None
    capture_area = None
    frame = None
    capture_frame = None
    windowname = None
    frame_number = 0
    frames_captured = 0
    w = 0
    h = 0

    def __init__(self, w = pyautogui.size()[0], h = pyautogui.size()[1], windowname = ''):        
        if platform == "darwin":
            h = h/2
            w = w/2
            self.screen_capture = mss()
            self.capture_frame = self.capture_frame_by_PIL
        elif platform == "win32":
            self.capture_frame = self.capture_frame_by_WIN32
        else:
            self.screen_capture = mss()
            self.capture_frame = self.capture_frame_by_PIL

        self.lock = Lock()
        self.capture_area = {"left": 0, "top": 0, "width": w, "height": h}
        self.w = w
        self.h = h
        self.windowname = windowname

    def start(self):
        self.running = True
        t = Thread(target=self.run)
        t.start()

    def stop(self):
        self.running = False

    def run(self):
        self.frame_number = 0

        while self.running:
            frame = self.capture_frame()
            self.lock.acquire()
            self.frame = frame
            self.frame_number += 1
            self.lock.release()
    
    # PM install for d3dshot is broken
    def capture_frame_byD3D(self):
        pass
    
    def capture_frame_by_PIL(self):
        self.frames_captured += 1
        frame = self.screen_capture.grab(self.capture_area)
        frame = np.asarray(Image.frombytes("RGB", frame.size, frame.bgra, "raw", "BGRX"))#.transpose(1,0,2)
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        return frame

    def capture_frame_by_WIN32(self):
        self.frames_captured += 1
        #hwnd = win32gui.FindWindow(None, self.windowname)
        hwnd = win32gui.GetDesktopWindow()
        wDC = win32gui.GetWindowDC(hwnd)
        dcObj = win32ui.CreateDCFromHandle(wDC)

        cDC = dcObj.CreateCompatibleDC()
        bmp = win32ui.CreateBitmap()
        bmp.CreateCompatibleBitmap(dcObj, self.w, self.h)
        cDC.SelectObject(bmp)
        cDC.BitBlt((0,0), (self.w, self.h), dcObj, (0,0), win32con.SRCCOPY)
        
        signedIntsArray = bmp.GetBitmapBits(True)
        frame = np.fromstring(signedIntsArray, dtype='uint8')
        frame.shape = (self.h, self.w, 4)

        dcObj.DeleteDC()
        cDC.DeleteDC()
        win32gui.ReleaseDC(hwnd, wDC)
        win32gui.DeleteObject(bmp.GetHandle())

        return cv2.cvtColor(frame, cv2.COLOR_RGBA2RGB)

    # TODO: Read frames from capture card