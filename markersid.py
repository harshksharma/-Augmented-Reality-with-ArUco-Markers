import cv2
import numpy as np

def generate_aruco_marker(marker_id, marker_size, border_bits, dictionary, save_path):
    # Create the ArUco marker
    marker_image = cv2.aruco.drawMarker(dictionary, marker_id, marker_size, borderBits=border_bits)
    
    # Save the marker image
    cv2.imwrite(save_path, marker_image)
    print(f"Marker ID {marker_id} saved to {save_path}")

# Parameters
marker_size = 200  # Size of the marker in pixels
border_bits = 1    # Width of the marker border (default is 1)
save_dir = "./markers"  # Directory to save markers

# Ensure the save directory exists
import os
if not os.path.exists(save_dir):
    os.makedirs(save_dir)

# Load the dictionary that was used to generate the markers.
aruco_dict = cv2.aruco.Dictionary_get(cv2.aruco.DICT_6X6_250)

# Marker IDs to generate
marker_ids = [0]

# Generate and save each marker
for marker_id in marker_ids:
    save_path = os.path.join(save_dir, f"marker_{marker_id}.png")
    generate_aruco_marker(marker_id, marker_size, border_bits, aruco_dict, save_path)
