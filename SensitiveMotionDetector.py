# dev mode : This code is subject to change.

"""
    Information:
    sensitivity_parameters are for adjusting sensitivity of motion detection.
    headless represents whether there's a camera/monitior or not. 
    work represents what task you want to perform after motion motion is detected.
"""

import cv2
import imutils
import threading



class SensitveMotionDetector:
    def __init__(self,work,sensitivity_parameters = (1000,25), headless = True):
        self.sensitivity_parameters = sensitivity_parameters
        self.work = work
        self.headless = headless
        self.movement_count = 0
        self.detect_count = 0
    
    def job(self):
        self.work()
    
    def start_detector(self):
        camera = cv2.VideoCapture(0)
        _, previous_frame = camera.read()
        for i in range(20):
            pass
        previous_frame = imutils.resize(previous_frame,width=500)
        previous_frame = cv2.cvtColor(previous_frame,cv2.COLOR_BGR2GRAY)
        previous_frame = cv2.GaussianBlur(previous_frame,(5,5),0)
        
        while True:
            current_result, current_frame = camera.read()
            current_frame = imutils.resize(current_frame,width=500)
            current_frame = cv2.cvtColor(current_frame,cv2.COLOR_BGR2GRAY)
            current_frame = cv2.GaussianBlur(current_frame,(5,5),0)
            difference = cv2.absdiff(previous_frame,current_frame)
            threshold = cv2.threshold(difference,25,255,cv2.THRESH_BINARY)[1]
            previous_frame = current_frame
            if threshold.sum() > self.sensitivity_parameters[0]:
                self.movement_count += 1
                
            if not self.headless:
                cv2.imshow("Frame",current_frame)
                cv2.imshow("Threshold",threshold)
                key = cv2.waitKey(1)
                
                if key == ord('q'):
                    break
                
            if self.movement_count > self.sensitivity_parameters[1]:
                threading.Thread(target = self.job).start()
                self.movement_count = 0


def print_job():
        print(f"DETECTED {detector.detect_count}")
        detector.detect_count += 1

if __name__ == '__main__':
    detector = SensitveMotionDetector(print_job,(10e5,10),headless=True)
    detector.start_detector()
        
        
        
        