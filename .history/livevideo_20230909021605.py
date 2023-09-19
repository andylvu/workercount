import cv2
import pyautogui
import numpy as np

# Load the template image of the minerals
object_image1 = cv2.imread("minerals.png", cv2.IMREAD_COLOR)
object_image2 = cv2.imread("scv.png", cv2.IMREAD_COLOR)
object_image3 = cv2.imread("scvmulti.png", cv2.IMREAD_COLOR)
# Get the template's width and height
template_width1, template_height1, _ = object_image1.shape
template_width2, template_height2, _ = object_image2.shape
template_width3, template_height3, _ = object_image3.shape

# Set the threshold for matching results 
threshold = 0.6

# Define the size of the center region to capture 
center_width = 1920  # Width of the center region
center_height = 1080  # Height of the center region

# Calculate the top-left corner of the center region
screen_width, screen_height = pyautogui.size()
x = (screen_width - center_width) // 2
y = (screen_height - center_height) // 2

# get screen coordinates
def get_screen_coordinates(rectangle_coordinates):
    # Calculate the actual screen coordinates by adding the offset of the center region
    screen_x = rectangle_coordinates[0] + x
    screen_y = rectangle_coordinates[1] + y
    return screen_x, screen_y

# object counts
object2_count = 0
object3_count = 0

# workers on minerals count
working_count = 0

# flag to track right click events
right_click = False

# flag to check if t he mouse is inside the green rectangle
mouse_in_green = False

# Create initial display frame
img = pyautogui.screenshot(region=(x, y, center_width, center_height))
display_frame = np.array(img)
display_frame = cv2.cvtColor(display_frame, cv2.COLOR_BGR2RGB)
display_frame = cv2.resize(display_frame, (center_width, center_height))

while True:
    try:

        # Capture the screen
        img = pyautogui.screenshot(region=(x, y, center_width, center_height))

        # Convert the screenshot to an array and then to RGB format
        current_frame = np.array(img)
        current_frame = cv2.cvtColor(current_frame, cv2.COLOR_BGR2RGB)
        current_frame = cv2.resize(current_frame, (center_width, center_height))

        # Resize the frame to the desired video dimensions
        video_width = center_width
        video_height = center_height
        current_frame = cv2.resize(current_frame, (video_width, video_height))

       # Perform template matching for the minerals
        result1 = cv2.matchTemplate(current_frame, object_image1, cv2.TM_CCOEFF_NORMED)
        loc1 = np.where(result1 >= threshold)

        # Perform template matching for the second object
        result2 = cv2.matchTemplate(current_frame, object_image2, cv2.TM_CCOEFF_NORMED)
        loc2 = np.where(result2 >= threshold)

        # Perform template matching for the third object
        result3 = cv2.matchTemplate(current_frame, object_image3, cv2.TM_CCOEFF_NORMED)
        loc3 = np.where(result3 >= threshold)

        # get mouse coordinates
        mouse_x, mouse_y = pyautogui.position()

        # update count for the second object
        object2_count = len(loc2[0])

        # update count for the third object
        object3_count = len(loc3[0])

        # Draw rectangles around the matched regions for the minerals
        for pt in zip(*loc1[::-1]):
            bottom_right = (pt[0] + template_width1, pt[1] + template_height1)
            cv2.rectangle(current_frame, pt, bottom_right, (0, 255, 0), 2)
            screen_x, screen_y = get_screen_coordinates(pt)
            
            # check for the mouse inside the green rectangle
            if pt[0] <= mouse_x <= pt[0] + template_width1 and pt[i] <=mouse_y <= pt[i] + template_height1:
                mouse_in_green = True
            else:
                mouse_in_green = False

        # Draw rectangles around the matched regions for the second object
        for pt in zip(*loc2[::-1]):
            bottom_right = (pt[0] + template_width2, pt[1] + template_height2)
            cv2.rectangle(current_frame, pt, bottom_right, (0, 0, 255), 2)

        # Draw rectangles around the matched regions for the third object
        for pt in zip(*loc3[::-1]):
            bottom_right = (pt[0] + template_width3, pt[1] + template_height3)
            cv2.rectangle(current_frame, pt, bottom_right, (0, 0, 255), 2)

        if pyautogui.mouseInfo().get('rightButton'):
            right_click = True
        else:
            right_click = False

        if mouse_in_green and right_click:
            working_count += object2_count + object3_count

        # Show the live video with detected minerals
        cv2.imshow("Live Desktop Video", display_frame)

        # print total count of workers at given time
        print("worker count = ", object3_count)
        print("single worker count = ", object2_count)


    

        # Stop displaying when 'q' key is pressed
        if cv2.waitKey(1) == ord("q"):
            break

        # Swap the frames for double buffering
        display_frame = current_frame

    except KeyboardInterrupt:
        break

# Close any open windows
cv2.destroyAllWindows()