import cv2
import numpy as np
from moviepy.editor import VideoFileClip
import threading

# Initialize video capture for webcam and the video to be projected
cap = cv2.VideoCapture(0)  # Webcam

# Load the video file using moviepy
video_path = 'tnm.mp4'
clip = VideoFileClip(video_path)
video_cap = cv2.VideoCapture(video_path)  # Video to be projected

# Function to detect ArUco markers
def detect_markers(frame, aruco_dict, parameters):
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    corners, ids, rejectedImgPoints = cv2.aruco.detectMarkers(gray, aruco_dict, parameters=parameters)
    if ids is not None:
        cv2.aruco.drawDetectedMarkers(frame, corners, ids)
    return corners, ids

# Camera calibration parameters (example values, you should calibrate your own camera)
camera_matrix = np.array([[1000, 0, 640],
                          [0, 1000, 360],
                          [0, 0, 1]], dtype=float)
dist_coeffs = np.array([0, 0, 0, 0], dtype=float)

def warp_video_onto_marker(frame, video_frame, marker_corners):
    marker_corners = np.array(marker_corners).reshape((4, 2))
    h, w, _ = video_frame.shape

    # Define the destination points for the homography
    dst_pts = np.array([
        [0, 0],
        [w - 1, 0],
        [w - 1, h - 1],
        [0, h - 1]
    ], dtype="float32")

    # Compute the homography
    H, _ = cv2.findHomography(dst_pts, marker_corners)

    # Warp the video frame to fit the marker
    warped_frame = cv2.warpPerspective(video_frame, H, (frame.shape[1], frame.shape[0]))

    # Create a mask for the warped video frame
    mask = np.zeros_like(frame, dtype=np.uint8)
    cv2.fillConvexPoly(mask, marker_corners.astype(int), (255, 255, 255))

    # Combine the warped video frame with the original frame
    frame = cv2.bitwise_and(frame, cv2.bitwise_not(mask))
    frame = cv2.bitwise_or(frame, warped_frame)
    
    return frame

# Function to play audio
def play_audio():
    clip.audio.preview()

# ArUco dictionary and parameters
aruco_dict = cv2.aruco.getPredefinedDictionary(cv2.aruco.DICT_6X6_250)
parameters = cv2.aruco.DetectorParameters()

audio_playing = False
audio_thread = None

while cap.isOpened() and video_cap.isOpened():
    ret, frame = cap.read()
    ret_video, video_frame = video_cap.read()

    if not ret or not ret_video:
        break

    corners, ids = detect_markers(frame, aruco_dict, parameters)

    if corners is not None and ids is not None:
        for corner, id_ in zip(corners, ids):
            if id_ == 0:  # Check for marker ID 0
                frame = warp_video_onto_marker(frame, video_frame, corner[0])
                if not audio_playing:
                    audio_thread = threading.Thread(target=play_audio)
                    audio_thread.start()
                    audio_playing = True
    else:
        if audio_playing:
            clip.audio.reader.close_proc()
            audio_playing = False

    cv2.imshow('AR with ArUco Marker', frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
video_cap.release()
cv2.destroyAllWindows()

# Ensure the audio thread is terminated
if audio_thread is not None:
    audio_thread.join()
