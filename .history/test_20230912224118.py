import cv2

# Create a video capture object for the screen
screen_capture = cv2.VideoCapture(0)  

# video resolution
# video resolution
screen_capture.set(3, 1920)
screen_capture.set(4, 1080)

while True:
    # Capture the screen frame
    ret, frame = screen_capture.read()

    if not ret:
        break

    # Resize the frame
    resized_frame = cv2.resize(frame, (1280, 720))

    # Display the resized frame
    cv2.imshow("Live Desktop Video", resized_frame)

    # Stop displaying when 'q' key is pressed
    if cv2.waitKey(1) == ord("q"):
        break

# Release the video capture object and close any open windows
screen_capture.release()
cv2.destroyAllWindows()