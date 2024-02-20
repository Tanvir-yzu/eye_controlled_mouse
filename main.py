import cv2
import mediapipe as mp
import pyautogui
cam = cv2.VideoCapture(0)  # Initialize the camera object to capture video from the first webcam.
face_mesh = mp.solutions.face_mesh.FaceMesh(refine_landmarks=True)  # Create a FaceMesh object with refined landmarks.
screen_w, screen_h = pyautogui.size()  # Get the width and height of the screen.
while True:
    _, frame = cam.read()  # Read a frame from the camera.
    frame = cv2.flip(frame, 1)  # Flip the frame horizontally for a mirror effect.
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)  # Convert the frame from BGR to RGB color space.
    output = face_mesh.process(rgb_frame)  # Process the RGB frame to find facial landmarks.
    landmark_points = output.multi_face_landmarks  # Extract the facial landmarks points.
    frame_h, frame_w, _ = frame.shape  # Get the height and width of the frame.
    if landmark_points:
        landmarks = landmark_points[0].landmark  # Get the landmarks of the first face detected.
        for id, landmark in enumerate(landmarks[474:478]):
            x = int(landmark.x * frame_w)  # Calculate the x-coordinate of the landmark.
            y = int(landmark.y * frame_h)  # Calculate the y-coordinate of the landmark.
            cv2.circle(frame, (x, y), 3, (0, 255, 0))  # Draw a circle at each landmark point.
            if id == 1:  # If the landmark is the second one in the subset.
                screen_x = screen_w * landmark.x  # Map the x-coordinate to the screen width.
                screen_y = screen_h * landmark.y  # Map the y-coordinate to the screen height.
                pyautogui.moveTo(screen_x, screen_y)  # Move the mouse to the mapped coordinates.
        left = [landmarks[145], landmarks[159]]  # Select landmarks for the left eye.
        for landmark in left:
            x = int(landmark.x * frame_w)  # Calculate the x-coordinate for the left eye landmarks.
            y = int(landmark.y * frame_h)  # Calculate the y-coordinate for the left eye landmarks.
            cv2.circle(frame, (x, y), 3, (0, 255, 255))  # Draw a circle at each left eye landmark.
        if (left[0].y - left[1].y) < 0.004:  # Check if the left eye is almost closed.
            pyautogui.click()  # Perform a mouse click.
            pyautogui.sleep(1)  # Pause for 1 second.
    cv2.imshow('Eye Controlled Mouse', frame)  # Display the frame with the landmark points.
    cv2.waitKey(1)  # Wait for 1 millisecond before moving to the next frame.