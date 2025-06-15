import dlib
import cv2


detector = dlib.get_frontal_face_detector()
predictor = dlib.shape_predictor("../models/shape_predictor_68_face_landmarks.dat")

# Capture video from webcam
cap = cv2.VideoCapture(0)

while True:
    ret, frame = cap.read()

    # Convert the frame to grayscale
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Detect faces in the frame
    faces = detector(gray)

    for face in faces:
        # Get facial landmarks
        shape = predictor(gray, face)

        # Draw circles around facial landmarks
        for i in range(68):
            x, y = shape.part(i).x, shape.part(i).y
            cv2.circle(frame, (x, y), 1, (0, 0, 255), -1)

    # Display the result
    cv2.imshow("Facial Landmark Detection", frame)

    if cv2.waitKey(1) & 0xFF == 27:  
        break

cap.release()
cv2.destroyAllWindows()


