import cv2
import pyautogui
import numpy as np
from pynput.mouse import Listener, Button
import time

class WorkerCounterApp:
    def _init__(self):
        # initialize variables and thresholds
        self.threshold_minerals = 0.15
        self.threshold_scv = 0.2
        self.threshold_scv_multi = 0.2

        # create video capture object
        self.screen_capture = cv2.VideoCapture(0) 

        # video capture resolution
        self.screen_capture.set(3, 1920)
        self.screen_capture.set(4, 1080)

        # initialize flags and counters
        self.scv = 0
        self.scv_multi = 0
        self.working_count = 0
        self.right_clicks = 0
        self.right_click = False
        self.mouse_in_green = False

        # load template images
        self.minerals_pic = cv2.imread("minerals.png", cv2.IMREAD_GRAYSCALE)
        self.scv_pic = cv2.imread("scv.png", cv2.IMREAD_GRAYSCALE)
        self.scv_multi_pic = cv2.imread("scvmulti.png", cv2.IMREAD_GRAYSCALE)

        # template images dimensions
        self.template_width1, self.template_height1 = self.minerals_pic.shape[::-1]   
        self.template_width2, self.template_height2 = self.scv_pic.shape[::-1]  
        self.template_width3, self.template_height3 = self.scv_multi_pic.shape[::-1]  


        # initialize mouse listener
        self.mouse_listener = Listener(on_click=self.on_click)
        self.mouse_listener.start()

    def on_click(self, x, y, button, pressed):
        if button == Button.right and pressed:
            self.right_click = True
        else:
            self.right_click = False















# while loop to run the live video
while True:
    try:
        
        # Capture the screen frame
        ret, current_frame = screen_capture.read()
        

        if not ret:
            break
                
        # Convert the current_frame to grayscale
        gray_frame = cv2.cvtColor(current_frame, cv2.COLOR_BGR2GRAY)
        gray_upper = gray_frame[0:840, 0:1920]
        gray_lowerleft = gray_frame[860:1080,580:860]
        gray_lower = gray_frame[860:1080,580:1140]        

        # Perform template matching for the minerals
        result1 = cv2.matchTemplate(gray_upper, minerals_pic, cv2.TM_SQDIFF_NORMED)
        loc1 = np.where(result1 <= threshold_minerals)

        # Perform template matching for the scv
        result2 = cv2.matchTemplate(gray_lowerleft, scv_pic, cv2.TM_SQDIFF_NORMED)
        loc2 = np.where(result2 <= threshold_scv)

        # Perform template matching for the scv_multi
        result3 = cv2.matchTemplate(gray_lower, scv_multi_pic, cv2.TM_SQDIFF_NORMED)
        loc3 = np.where(result3 <= threshold_scv_multi)

        # get mouse coordinates
        mouse_x, mouse_y = pyautogui.position()
        adj_mouse_x = mouse_x - 320

        # update count for the scv
        scv = len(loc2[0])

        # update count for the scv_multi
        scv_multi = len(loc3[0])

        # Draw rectangles around the matched regions for the minerals
        for pt_candidate in zip(*loc1[::-1]):
            bottom_right = (pt_candidate[0] + template_width1, pt_candidate[1] + template_height1)
            cv2.rectangle(current_frame, pt_candidate, bottom_right, (0, 255, 0), 2)
            
            # check for the mouse inside the green rectangle
            if pt_candidate[0] <= adj_mouse_x <= pt_candidate[0] + template_width1 and \
                pt_candidate[1] <= mouse_y <= pt_candidate[1] + template_height1:
                mouse_in_green = True
                break
            else:
                mouse_in_green = False
        
        if mouse_in_green and right_click == True:
            working_count += scv + scv_multi
            time.sleep(0.25)

        if right_click == True:
            right_clicks += 1
            
        # Display the processed frame (optional)
        resized_frame = cv2.resize(current_frame, (1280, 720))
        cv2.imshow("Live Desktop Video", resized_frame)

        print(scv, "scv count")
        print(scv_multi, "multi scv count")
        print(working_count, 'working count')
        print(right_clicks, 'right clicks')
        print()

        # Stop displaying when 'q' key is pressed
        if cv2.waitKey(1) == ord("q"):
            break

    except KeyboardInterrupt:
        break

# Close any open windows
cv2.destroyAllWindows()