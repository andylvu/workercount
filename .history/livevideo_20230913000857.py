import cv2
import pyautogui
import numpy as np
from pynput.mouse import Listener, Button
import threading
import time

start_time = time.time()
print(start_time, 'start time')

# Load the template images
minerals_pic = cv2.imread("minerals.png", cv2.IMREAD_GRAYSCALE)
scv_pic = cv2.imread("scv.png", cv2.IMREAD_GRAYSCALE)
scv_multi_pic = cv2.imread("scvmulti.png", cv2.IMREAD_GRAYSCALE)

# Get the template's dimensions and thresholds
template_width1, template_height1 = minerals_pic.shape[::-1]  # Get width and height for grayscale image
template_width2, template_height2 = scv_pic.shape[::-1]  
template_width3, template_height3 = scv_multi_pic.shape[::-1]
threshold_minerals = 0.4
threshold_scv = 0.7
threshold_scv_multi = 0.7

# set timing variables and intervals
target_runtime = 0.020 # 20 milliseconds
last_matching_time = time.time()

# Create a video capture object for the screen
screen_capture = cv2.VideoCapture(0)  

# video resolution
screen_capture.set(3, 1920)
screen_capture.set(4, 1080)

# object counts and flags

scv = 0
scv_multi = 0
working_count = 0
right_clicks = 0
right_click = False
mouse_in_green = False



# Lock for synchronization
lock = threading.Lock()

# function to detect right clicks
def on_click(x,y, button, pressed):
    global right_click
    if button == Button.right and pressed:
        right_click = True
        print('right click')
    else:
        right_click = False

# initiialize mouse listener in separete thread
mouse_listener = Listener(on_click = on_click)
mouse_listener.start()

time1 = time.time()
print(time1, 'time1')

# while loop to run the live video
while True:
    try:
        time2 = time.time()
        print(time2, 'time2')
        # Capture the screen frame
        ret, current_frame = screen_capture.read()

        if not ret:
            break

        # Convert the current_frame to grayscale
        gray_frame = cv2.cvtColor(current_frame, cv2.COLOR_BGR2GRAY)    
        

        if time.time() - last_matching_time >= target_runtime:
        # Perform template matching for the minerals
            result1 = cv2.matchTemplate(gray_frame, minerals_pic, cv2.TM_CCOEFF_NORMED)
            loc1 = np.where(result1 >= threshold_minerals)
            # Perform template matching for the scv
            result2 = cv2.matchTemplate(gray_frame, scv_pic, cv2.TM_CCOEFF_NORMED)
            loc2 = np.where(result2 >= threshold_scv)

            # Perform template matching for the scv_multi
            result3 = cv2.matchTemplate(gray_frame, scv_multi_pic, cv2.TM_CCOEFF_NORMED)
            loc3 = np.where(result3 >= threshold_scv_multi)

            num_matches = len(loc1[0])
            print(num_matches)

        # get mouse coordinates
        mouse_x, mouse_y = pyautogui.position()
        adj_mouse_x = mouse_x - 320

        # update count for the scv
        scv = len(loc2[0])

        # update count for the scv_multi
        scv_multi = len(loc3[0])

        
        # Draw rectangles around the matched regions for the minerals
        for i in range(0, num_matches, 10):
            pt_candidate = (loc1[1][i], loc1[0][i])
            bottom_right = (pt_candidate[0] + template_width1, pt_candidate[1] + template_height1)
            cv2.rectangle(current_frame, pt_candidate, bottom_right, (0, 255, 0), 2)

            time3 = time.time()
            print(time3, 'time3')

            # check for the mouse inside the green rectangle
            if pt_candidate[0] <= adj_mouse_x <= pt_candidate[0] + template_width1 and \
                pt_candidate[1] <= mouse_y <= pt_candidate[1] + template_height1:
                mouse_in_green = True
                break
            else:
                mouse_in_green = False

        if mouse_in_green and right_click == True:
            working_count += scv + scv_multi

        if right_click == True:
            right_clicks += 1

        # Display the processed frame (optional)
        resized_frame = cv2.resize(current_frame, (1280, 720))
        cv2.imshow("Live Desktop Video", resized_frame)

        time4 = time.time()
        print(time4, 'time4')

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