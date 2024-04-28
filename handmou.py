import cv2
import mediapipe as mp
import pyautogui

# Initialize OpenCV VideoCapture
cap = cv2.VideoCapture(0)

# Initialize MediaPipe Hands
hand_detector = mp.solutions.hands.Hands()

# Initialize MediaPipe Drawing Utilities
drawing_utils = mp.solutions.drawing_utils

# Get screen size
screen_width, screen_height = pyautogui.size()

# Initialize variables for index finger and thumb positions
index_x, index_y = 0, 0

while True:
    # Read frame from webcam
    ret, frame = cap.read()
    if not ret:
        break

    # Flip the frame horizontally for natural viewing
    frame = cv2.flip(frame, 1)

    # Get frame dimensions
    frame_height, frame_width, _ = frame.shape

    # Convert BGR frame to RGB for MediaPipe
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    # Process the frame to detect hands
    output = hand_detector.process(rgb_frame)
    hands = output.multi_hand_landmarks

    # If hands are detected
    if hands:
        for hand in hands:
            # Draw landmarks on the frame
            drawing_utils.draw_landmarks(frame, hand)
            landmarks = hand.landmark

            # Iterate through each landmark
            for id, landmark in enumerate(landmarks):
                x = int(landmark.x * frame_width)
                y = int(landmark.y * frame_height)

                # Index finger landmark (ID: 8)
                if id == 8:
                    # Draw a circle around the index finger
                    cv2.circle(img=frame, center=(x, y), radius=10, color=(0, 255, 255))
                    
                    # Convert finger position to screen coordinates
                    index_x = screen_width / frame_width * x
                    index_y = screen_height / frame_height * y

                # Thumb landmark (ID: 4)
                if id == 4:
                    # Draw a circle around the thumb
                    cv2.circle(img=frame, center=(x, y), radius=10, color=(0, 255, 255))
                    
                    # Convert thumb position to screen coordinates
                    thumb_x = screen_width / frame_width * x
                    thumb_y = screen_height / frame_height * y

                    # Check if the thumb is close to the index finger
                    if abs(index_y - thumb_y) < 20:
                        # Perform a click action
                        pyautogui.click()
                        pyautogui.sleep(1)
                    elif abs(index_y - thumb_y) < 100:
                        # Move the mouse cursor
                        pyautogui.moveTo(index_x, index_y)

    # Display the frame
    cv2.imshow('Virtual Mouse', frame)

    # Check for key press
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the webcam and close all windows
cap.release()
cv2.destroyAllWindows()
