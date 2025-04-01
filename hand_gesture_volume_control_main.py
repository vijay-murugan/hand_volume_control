import cv2
import mediapipe as mp
import pyautogui

webcam = cv2.VideoCapture(0)
# Used to capture hands
my_hands = mp.solutions.hands.Hands()
# Used to draw content in the image captured
drawing_utils = mp.solutions.drawing_utils
x1 = y1 = x2 = y2 = 0
while True:
    _ , image = webcam.read()
    # flip the image so that it is easily perceived
    image = cv2.flip(image, 1)
    output = my_hands.process(image)
    # collect hands from the output
    hands = output.multi_hand_landmarks
    # get frame sizes for the coordinate estimation
    frame_height, frame_width, depth = image.shape
    if hands:
        for hand in hands:
            # draws landmarks on the hand
            drawing_utils.draw_landmarks(image, hand)
            landmarks = hand.landmark
            for id, landmark in enumerate(landmarks):
                x = int(landmark.x * frame_width)
                y = int(landmark.y * frame_height)
                # Forefinger's id
                if id == 8:
                    cv2.circle(img=image, center=(x, y), radius=8, color=(0,255,255), thickness=3)
                    x1, y1 = x, y
                # Thumb's id
                if id == 4:
                    cv2.circle(img=image, center=(x, y), radius=8, color=(0,255,255), thickness=3)
                    x2, y2 = x, y
        distance = ((x2-x1)**2 +(y2-y1)**2) ** 0.5
        # Draw line as per distance
        cv2.line(image, (x1, y1), (x2, y2), (0, 255, 255), 5)
        if distance > 50:
            pyautogui.press("volumeup")
        else:
            pyautogui.press("volumedown")

    cv2.imshow("Hand volume control", image) # webcam window
    key = cv2.waitKey(10) # captures images every 10 ms
    if key == 27: # break when escape key is pressed
        break
webcam.release()
cv2.destroyAllWindows()