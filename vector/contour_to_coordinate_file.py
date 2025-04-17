import cv2
import numpy as np
import matplotlib.pyplot as plt
from cobot.cobot_connector import draw
from vector.reduced_coords import reduced_coords, approximate_coords
import cv2.ximgproc as xipg



def show_points(x_coords_local, y_coords_local):
    plt.figure()
    plt.scatter(x_coords_local, y_coords_local, c='blue', marker='o')
    plt.title('Reduced X, Y Coordinates of All Contours')
    plt.xlabel('X (meters)')
    plt.ylabel('Y (meters)')
    plt.grid(True)
    plt.show()


# Load the image
image = cv2.imread('/home/jorgesuarez/PycharmProjects/Robotica-Brazo/vector/rectilineas.jpg')

rotated_image = cv2.rotate(image, cv2.ROTATE_90_CLOCKWISE)
flipped_image = cv2.flip(rotated_image, 1)

# Convert the image to grayscale
gray = cv2.cvtColor(flipped_image, cv2.COLOR_BGR2GRAY)

# Apply Gaussian blur to reduce noise
blurred = cv2.GaussianBlur(gray, (5, 5), 0)

# Apply edge detection (Canny) with different thresholds if necessary
edges = cv2.Canny(blurred, 100, 200)

# Apply thinning to reduce lines to single-pixel width
thinned_edges = xipg.thinning(edges)

# Find contours using RETR_TREE to get both internal and external contours with hierarchy
contours, _ = cv2.findContours(thinned_edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

filtered_contours = []

# Threshold for similarity comparison
similarity_threshold = 0.01

for contour in contours:
    is_unique = True

    # Compare against all previously filtered contours
    for filtered_contour in filtered_contours:
        similarity = cv2.matchShapes(contour, filtered_contour, cv2.CONTOURS_MATCH_I1, 0.0)

        if similarity < similarity_threshold:
            is_unique = False
            break

    # If the contour is unique enough, add it to the filtered_contours list
    if is_unique:
        filtered_contours.append(contour)

# Draw filtered contours on the image
cv2.drawContours(flipped_image, filtered_contours, -1, (0, 255, 0), 2)

cv2.imshow("Filtered Contours", flipped_image)
cv2.waitKey(0)

# Define the frame limits (in centimeters)
frame_top_right = (78, 43)  # x=78, y=43
frame_bottom_left = (23, -35)  # x=23, y=-35

# 55 x / 9
# 78 y / 6

# Extract frame width and height in real-world units (centimeters)
frame_width_cm = frame_top_right[0] - frame_bottom_left[0]  # x difference
frame_height_cm = frame_top_right[1] - frame_bottom_left[1]  # y difference

# Get image dimensions (in pixels)
image_height, image_width = flipped_image.shape[:2]

# Initialize lists to hold all contours' reduced coordinates
all_x_coords = []
all_y_coords = []
n = 0

# Iterate over each filtered contour
for contour in filtered_contours:
    x_coords = []
    y_coords = []

    for point in contour:
        x_pixel, y_pixel = point[0]

        # Scale pixel coordinates to real-world coordinates in centimeters
        x_cm = frame_top_right[0] - (x_pixel / image_width) * frame_width_cm
        y_cm = frame_top_right[1] - (y_pixel / image_height) * frame_height_cm

        # Convert centimeters to meters
        x_m = x_cm / 100.0
        y_m = y_cm / 100.0

        # Append the real-world coordinates to the lists
        x_coords.append(x_m)
        y_coords.append(y_m)

    # Apply reduced_coords to the current contour
    reduced_x, reduced_y, n_points = reduced_coords(x_coords, y_coords, 0.25)
    avg_coords_x, avg_coords_y, _ = approximate_coords(reduced_x, reduced_y, 2, 0.05)
    avg_coords_x.append(avg_coords_x[0])
    avg_coords_y.append(avg_coords_y[0])

    show_points(x_coords, y_coords)
    show_points(reduced_x, reduced_y)
    show_points(avg_coords_x, avg_coords_y)
    # skip if key c is pressed:
    # key = input('')
    # if key != 'c':
    #     draw(avg_coords_x, avg_coords_y)

    draw(avg_coords_x, avg_coords_y)

    n += n_points

print(f'Total number of points after reduction: {n}')

# Display the image with detected curves
cv2.imshow('Detected Curves', flipped_image)
cv2.waitKey(0)
cv2.destroyAllWindows()