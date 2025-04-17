# Robotica-Brazo

**Robotica-Brazo** is a project that transforms an image into instructions for a collaborative robotic arm (cobot) and executes them.

A user sends an image to a local server, which processes it using OCR, vector transformations, or predefined tracing logic, then generates movement instructions for the cobot arm. The system is designed to handle simple shape drawing or text reproduction using robotic movement.

## How it Works

1. The user sends an image (e.g. handwritten text or shapes) to the server.
2. The image is processed and converted into coordinates.
3. The coordinates are translated into movement instructions.
4. The cobot arm executes the movements.

## Components

- **OCR and Text Handling** – Extracts characters using Tesseract and maps them to known traces.
- **Vector Conversion** – Detects shapes and converts contours to coordinates.
- **Cobot Control** – Sends commands to a URX-compatible robot arm.
- **Web Server** – Receives images and triggers the workflow.

## Setup

Install dependencies:

```bash
pip install -r requirements.txt
```

Make sure Tesseract is installed and the cobot is connected.

## Running

Start the server:

```bash
python app/server.py
```

Then send an image to the appropriate endpoint.

## Demo


[File in project](./live_demo.mp4)

or here

[Google photos link](https://photos.app.goo.gl/iE7DRAco7QvLQTo17)


