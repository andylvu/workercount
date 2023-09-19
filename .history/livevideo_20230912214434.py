import cv2
import pyautogui
import numpy as np
from pynput.mouse import Listener, Button

# Load the template image of the minerals and workers
minerals_pic = cv2.imread("minerals.png", cv2.IMREAD_COLOR)
scv_pic = cv2.imread("scv.png", cv2.IMREAD_COLOR)
scv_multi_pic = cv2.imread("scvmulti.png", cv2.IMREAD_COLOR)

# Get the template's width and height
template_width1, template_height1, _ = minerals_pic.shape
template_width2, template_height2, _ = scv_pic.shape
template_width3, template_height3, _ = scv_multi_pic.shape

# Threshold values for each template
threshold_minerals = 0.4
threshold_scv = 0.7
threshold_scv_multi = 0.7

# Create a video capture object for the screen
screen_capture = cv2.VideoCapture(0)  

# video resolution
screen_capture.set(3, 1920)
screen_capture.set(4, 1080)

# object counts
scv = 0
scv_multi = 0

# workers on minerals count
working_count = 0

# number of right clicks
right_clicks = 0

# flag to track right click events
right_click = False

# flag to check if the mouse is inside the green rectangles
mouse_in_green = False

# function to catch right clicks and mark as true
def on_click(x,y, button, pressed):
    global right_click
    if button == Button.right and pressed:
        right_click = True
        print('right click')
    else:
        right_click = False

# initiialize mouse listener and start
mouse_listener = Listener(on_click = on_click)
mouse_listener.start()

# whiel loop to run the live video
while True:
    try:

        # Capture the screen frame
        ret, current_frame = screen_capture.read()

        if not ret:
            break

       # Perform template matching for the minerals
        result1 = cv2.matchTemplate(current_frame, minerals_pic, cv2.TM_CCOEFF_NORMED)
        loc1 = np.where(result1 >= threshold_minerals)

        # Perform template matching for the scv
        result2 = cv2.matchTemplate(current_frame, scv_pic, cv2.TM_CCOEFF_NORMED)
        loc2 = np.where(result2 >= threshold_scv)

        # Perform template matching for the scv_multi
        result3 = cv2.matchTemplate(current_frame, scv_multi_pic, cv2.TM_CCOEFF_NORMED)
        loc3 = np.where(result3 >= threshold_scv_multi)

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
            if pt_candidate[0] <= adj_mouse_x <= pt_candidate[0] + template_width1 and pt_candidate[1] <= mouse_y <= pt_candidate[1] + template_height1:
                mouse_in_green = True
                break
            else:
                mouse_in_green = False

        # Draw rectangles around the matched regions for the scv
        for pt in zip(*loc2[::-1]):
            bottom_right = (pt[0] + template_width2, pt[1] + template_height2)
            cv2.rectangle(current_frame, pt, bottom_right, (0, 0, 255), 2)

        # Draw rectangles around the matched regions for the scv_multi
        for pt in zip(*loc3[::-1]):
            bottom_right = (pt[0] + template_width3, pt[1] + template_height3)
            cv2.rectangle(current_frame, pt, bottom_right, (0, 0, 255), 2)

        if mouse_in_green and right_click == True:
            working_count += scv + scv_multi

        if right_click == True:
            right_clicks += 1

        # Display the processed frame (optional)
        cv2.imshow("Live Desktop Video", current_frame)

        print(scv, "scv count")
        print(scv_multi, "multi scv count")
        print(working_count, 'working count')
        print(right_clicks, 'right clicks')
        print(mouse_in_green, 'mouse in green')
        
        print(mouse_x, mouse_y)
        print()

        # Stop displaying when 'q' key is pressed
        if cv2.waitKey(1) == ord("q"):
            break

        # Swap the frames for double buffering
        display_frame = current_frame

    except KeyboardInterrupt:
        break

# Close any open windows
cv2.destroyAllWindows()