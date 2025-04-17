import cv2
import cv2.ximgproc as xipg

from cobot.cobot_connector import draw
from vector.reduced_coords import reduced_coords, approximate_coords


class ImageDrawer:
    @staticmethod
    def draw_image(image):
        print("DRAWING IMAGE")

        processed_image = ImageDrawer._preprocess_image(image)
        contours = ImageDrawer._get_filtered_contours(processed_image)
        ImageDrawer._draw_contours(processed_image, contours)
        ImageDrawer._convert_and_draw_coords(processed_image, contours)

    @staticmethod
    def _preprocess_image(image):
        rotated = cv2.rotate(image, cv2.ROTATE_90_CLOCKWISE)
        flipped = cv2.flip(rotated, 1)
        gray = cv2.cvtColor(flipped, cv2.COLOR_BGR2GRAY)
        blurred = cv2.GaussianBlur(gray, (5, 5), 0)
        edges = cv2.Canny(blurred, 100, 200)
        thinned = xipg.thinning(edges)
        return thinned, flipped

    @staticmethod
    def _get_filtered_contours(processed_data):
        thinned_edges, _ = processed_data
        contours, _ = cv2.findContours(thinned_edges, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)

        filtered_contours = []
        similarity_threshold = 0.05

        for contour in contours:
            is_unique = True
            for filtered in filtered_contours:
                similarity = cv2.matchShapes(contour, filtered, cv2.CONTOURS_MATCH_I1, 0.0)
                if similarity < similarity_threshold:
                    is_unique = False
                    break
            if is_unique:
                filtered_contours.append(contour)

        return filtered_contours

    @staticmethod
    def _draw_contours(image_data, contours):
        _, flipped = image_data
        cv2.drawContours(flipped, contours, -1, (0, 255, 0), 2)

    @staticmethod
    def _convert_and_draw_coords(image_data, contours):
        _, flipped = image_data
        image_height, image_width = flipped.shape[:2]

        frame_top_right = (78, 43)
        frame_bottom_left = (23, -35)

        frame_width_cm = frame_top_right[0] - frame_bottom_left[0]
        frame_height_cm = frame_top_right[1] - frame_bottom_left[1]

        for contour in contours:
            x_coords, y_coords = [], []

            for point in contour:
                x_pixel, y_pixel = point[0]

                x_cm = frame_top_right[0] - (x_pixel / image_width) * frame_width_cm
                y_cm = frame_top_right[1] - (y_pixel / image_height) * frame_height_cm

                x_m = x_cm / 100.0
                y_m = y_cm / 100.0

                x_coords.append(x_m)
                y_coords.append(y_m)

            reduced_x, reduced_y, _ = reduced_coords(x_coords, y_coords, 0.75)
            avg_x, avg_y, _ = approximate_coords(reduced_x, reduced_y, 3, 0.003)

            avg_x.append(avg_x[0])
            avg_y.append(avg_y[0])

            draw(avg_x, avg_y)
