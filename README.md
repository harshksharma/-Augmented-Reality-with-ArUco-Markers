# -Augmented-Reality-with-ArUco-Markers
This project demonstrates how to use ArUco markers to project a video onto a marker in real-time using a webcam and play synchronized audio. Additionally, it includes a script for generating ArUco markers using OpenCV.

Project Structure
main.py: Detects ArUco markers in a webcam feed, warps a video onto the detected marker, and plays synchronized audio.
markersid.py: Generates and saves an ArUco marker as an image file.

Requirements
To run this project, you need the following:
Python 3.x
OpenCV
NumPy
MoviePy
ArUco markers (included in the OpenCV library)
pip install opencv-contrib-python==4.7.0.68 opencv-python==4.7.0.68

Step 1: Generate ArUco Markers
Before running the main AR projection, you need to generate the ArUco marker.
a)Run the Markers_id_generator.py script.
b)This will create a marker image (e.g., marker_0.png) inside the ./markers folder.

Step 2: Project Video onto ArUco Marker
a)Place the generated marker (e.g., marker_0.png) in front of your webcam.
b)Modify the video path in the main.py file to point to your video file: video_path = 'your-video.mp4'
c)Run the main.py script.

The webcam will detect the ArUco marker and project the video onto the marker. The audio from the video will also start playing.

Controls
q: Press this key to exit the video projection.

Explanation of Files:-

main.py
a)Webcam Capture: It opens the webcam feed and captures each frame.
b)ArUco Detection: It detects ArUco markers in the webcam feed using OpenCV.
c)Video Projection: Once a marker is detected (marker ID 0 in this case), it projects the corresponding video onto the marker.
d)Audio Playback: The video’s audio is played in sync with the projection using threading to ensure it runs independently of the video processing.
e)Warping Video: The video is warped onto the marker using homography transformation to give a perspective-correct appearance on the detected marker.

Markers_id_generator.py
a)ArUco Marker Generation: This script generates and saves an ArUco marker based on the provided ID and marker size.
b)Customization: You can modify the marker size, border width, and save path as needed.
