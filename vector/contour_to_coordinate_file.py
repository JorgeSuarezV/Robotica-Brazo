import cv2
import numpy as np
import matplotlib.pyplot as plt
import cv2.ximgproc as xipg

from cobot.cobot_connector import draw
from vector.reduced_coords import reduced_coords, approximate_coords


class ContourProcessor:
    def __init__(self, image_path):
        self.image_path = image_path
        self.image = cv2.imread(image_path)
        self.processed_image = None
        self.flipped_image = None
        self.filtered_contours = []
        self.frame_top_right = (78, 43)
        self.frame_bottom_left = (23, -35)
        self.frame_width_cm = self.frame_top_right[0] - self.frame_bottom_left[0]
        self.frame_height_cm = self.frame_top_right[1] - self.frame_bottom_left[1]

    def process(self):
        self._preprocess_image()
        self._detect_and_filter_contours()
        self._draw_contours()
        self._convert_and_draw_coords()
        self._show_result()

    def _preprocess_image(self):
        rotated = cv2.rotate(self.image, cv2.ROTATE_90_CLOCKWISE)
        self.flipped_image = cv2.flip(rotated, 1)
        gray = cv2.cvtColor(self.flipped_image, cv2.COLOR_BGR2GRAY)
        blurred = cv2.GaussianBlur(gray, (5, 5), 0)
        edges = cv2.Canny(blurred, 100, 200)
        self.processed_image = xipg.thinning(edges)

    def _detect_and_filter_contours(self):
        contours, _ = cv2.findContours(
            self.processed_image, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE
        )
        similarity_threshold = 0.01
        for contour in contours:
            if all(
                cv2.matchShapes(contour, filtered, cv2.CONTOURS_MATCH_I1, 0.0) >= similarity_threshold
                for filtered in self.filtered_contours
            ):
                self.filtered_contours.append(contour)

    def _draw_contours(self):
        cv2.drawContours(self.flipped_image, self.filtered_contours, -1, (0, 255, 0), 2)

    def _convert_and_draw_coords(self):
        image_height, image_width = self.flipped_image.shape[:2]
        total_points = 0

        for contour in self.filtered_contours:
            x_coords, y_coords = [], []

            for point in contour:
                x_pixel, y_pixel = point[0]

                x_cm = self.frame_top_right[0] - (x_pixel / image_width) * self.frame_width_cm
                y_cm = self.frame_top_right[1] - (y_pixel / image_height) * self.frame_height_cm

                x_m, y_m = x_cm / 100.0, y_cm / 100.0
                x_coords.append(x_m)
                y_coords.append(y_m)

            reduced_x, reduced_y, n_points = reduced_coords(x_coords, y_coords, 0.25)
            avg_x, avg_y, _ = approximate_coords(reduced_x, reduced_y, 2, 0.05)

            avg_x.append(avg_x[0])
            avg_y.append(avg_y[0])

            self._show_points(x_coords, y_coords)
            self._show_points(reduced_x, reduced_y)
            self._show_points(avg_x, avg_y)

            draw(avg_x, avg_y)
            total_points += n_points

        print(f"Total number of points after reduction: {total_points}")

    def _show_points(self, x, y):
        plt.figure()
        plt.scatter(x, y, c='blue', marker='o')
        plt.title('Coordinates')
        plt.xlabel('X (meters)')
        plt.ylabel('Y (meters)')
        plt.grid(True)
        plt.show()

    def _show_result(self):
        cv2.imshow("Filtered Contours", self.flipped_image)
        cv2.waitKey(0)
        cv2.imshow("Detected Curves", self.flipped_image)
        cv2.waitKey(0)
        cv2.destroyAllWindows()
