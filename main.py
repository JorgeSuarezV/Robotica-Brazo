import sys
import PIL
import pytesseract
from PIL import Image
import cv2 as cv
import numpy as np

# Import ImageGrab if possible, might fail on Linux
try:
    from PIL import ImageGrab
    use_grab = True
except Exception as ex:
    # Some older versions of pillow don't support ImageGrab on Linux
    # In which case we will use XLib
    if sys.platform == 'linux':
        from Xlib import display, X
        use_grab = False
    else:
        raise ex


def screenGrab(rect):
    """ Given a rectangle, return a PIL Image of that part of the screen.
        Handles a Linux installation with an older Pillow by falling back
        to using XLib """
    global use_grab
    x, y, width, height = rect

    if use_grab:
        image = PIL.ImageGrab.grab(bbox=[x, y, x + width, y + height])
    else:
        # ImageGrab can be missing under Linux
        dsp = display.Display()
        root = dsp.screen().root
        raw_image = root.get_image(x, y, width, height, X.ZPixmap, 0xffffffff)
        image = Image.frombuffer("RGB", (width, height), raw_image.data, "raw", "BGRX", 0, 1)
    return image


def pil_to_cv(image):
    """Convert PIL Image to OpenCV format"""
    open_cv_image = np.array(image)
    open_cv_image = cv.cvtColor(open_cv_image, cv.COLOR_RGB2BGR)
    return open_cv_image


if __name__ == "__main__":
    # Hardcoded values
    x = 100  # X-coordinate of the top-left corner
    y = 200  # Y-coordinate of the top-left corner
    width = 500  # Width of the area to capture
    height = 300  # Height of the area to capture

    # Area of screen to monitor
    screen_rect = [x, y, width, height]
    print("Watching screen area: " + str(screen_rect))

    cap = cv.VideoCapture(0)  # Initialize camera

    while True:
        # Capture screen area
        screen_image = screenGrab(screen_rect)  # Grab the area of the screen
        cv_screen_image = pil_to_cv(screen_image)  # Convert PIL Image to OpenCV format

        # Capture camera feed
        ret, camera_frame = cap.read()

        if ret:
            # Display camera feed
            cv.imshow('Camera Feed', camera_frame)

        # Display the screen capture
        cv.imshow('Screen Capture', camera_frame)

        # OCR the screen image
        text = pytesseract.image_to_string(camera_frame)

        # If the OCR found anything, write it to stdout
        text = text.strip()
        if len(text) > 0:
            print(text)

        # Break the loop if 'q' is pressed
        if cv.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv.destroyAllWindows()
