import cv2
import numpy as np

values = {}
with open('teste.txt') as f:
    lines = f.readlines()
    key_frame = None
    for l in lines:
        if "Frame" in l:
            l = l.replace("\n", "")
            key_frame = l
            values[key_frame] = []
        else:
            new_coordinate = list(map(float, l.split(",")))
            values[key_frame].append(new_coordinate)

# Create a VideoCapture object and read from input file
# If the input is the camera, pass 0 instead of the video file name
cap = cv2.VideoCapture('town10.mp4')

# Read until video is completed
frame_counter = 0
while cap.isOpened():
    # Capture frame-by-frame
    ret, image = cap.read()
    if ret:
        coordinates = values[f"Frame {frame_counter}"]
        for c in coordinates:
            width = image.shape[1]
            height = image.shape[0]
            if 0 < c[0] < width:
                x = int(c[0])
            else:
                continue
            if 0 < c[1] < height:
                y = int(c[1])
            else:
                continue

            image = cv2.circle(image, (x, y), radius=5, color=(0, 0, 255), thickness=-1)

        # percent by which the image is resized
        scale_percent = 50  # calculate the 50 percent of original dimensions
        new_width = int(image.shape[1] * scale_percent / 100)
        new_height = int(image.shape[0] * scale_percent / 100)
        dsize = (new_width, new_height)  # resize image
        image = cv2.resize(image, dsize)

        cv2.imshow('Frame', image)

        while not cv2.waitKey():
            pass
        frame_counter += 1
    else:
        break


# When everything done, release the video capture object
cap.release()

# Closes all the frames
cv2.destroyAllWindows()