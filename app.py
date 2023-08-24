import cv2
import dlib
import face_recognition
from flask import Flask, render_template, Response

app = Flask(__name__)

# Load the face detection model from dlib
detector = dlib.get_frontal_face_detector()

# Load your reference image and encode it
reference_image_path = "photo_of_mine.jpg"  # Replace with the path to your image
reference_image = face_recognition.load_image_file(reference_image_path)
reference_encoding = face_recognition.face_encodings(reference_image)[0]

# Initialize the video capture from the default camera
cap = cv2.VideoCapture(0)

def generate_frames():
    while True:
        # Read a frame from the video
        ret, frame = cap.read()
        if not ret:
            break

        # Convert the frame to grayscale for face detection
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        # Detect faces in the grayscale frame
        faces = detector(gray)

        for face in faces:
            # Calculate the coordinates for drawing the circle
            x, y, w, h = face.left(), face.top(), face.width(), face.height()
            center = (x + w // 2, y + h // 2)
            radius = int((w + h) // 3)

            # Draw a circle around the detected face
            cv2.circle(frame, center, radius, (0, 255, 0), 2)

            # Perform face recognition
            face_locations = [(y, x + w, y + h, x)]
            face_encodings = face_recognition.face_encodings(frame, face_locations)

            if len(face_encodings) > 0:
                face_encoding = face_encodings[0]
                results = face_recognition.compare_faces([reference_encoding], face_encoding)
                if results[0]:
                    name = "Oqiljon Islomov"
                else:
                    name = "Hechkim topilmadi"

                # Write the name above the circle
                text_position = (x + 10, y + 280)
                cv2.putText(frame, name, text_position, cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

        ret, buffer = cv2.imencode('.jpg', frame)
        frame = buffer.tobytes()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/video_feed')
def video_feed():
    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == '__main__':
    app.run(debug=True)
