import cv2
import numpy as np

# Initialize variables
x = 0
y = 0
temp_x = np.zeros(2)
temp_y = np.zeros(2)
temp_sum_row = 0
temp_sum_col = 0
row_pixel = np.zeros(360)
col_pixel = np.zeros(360)
prev_keypoints = [] # Initialize list to hold past key points

# Load video file
cap = cv2.VideoCapture('ECE2195_HW6.mp4')

# Define parameters for blob detection
params = cv2.SimpleBlobDetector_Params()
params.filterByColor = True  # We have grayscale
params.blobColor = 0 or 255  # blob color can be black (0) or white (255)
params.minArea = 6           # This can be adjusted, is working okay for the lasers
params.maxArea = 500         # This can be adjusted, is working okay for the lasers

# Create blob detector
detector = cv2.SimpleBlobDetector_create(params)

while True:
    # Read frame from video
    ret, frame = cap.read()

    # Test for a valid frame
    if not ret:
        break

    # Get the dimensions of the frame
    height, width, channels = frame.shape

    '''
    Loop through rows and cols and store sum of row/cols pixels. We have an NxN frame.
    This is mainly here to slow down the video, so we can closely observe the bounding boxes and direction indications.
    Don't need anymore, we can use cv2.waitKey() for the number of millisceonds for a frame to be displayed.
    '''
    # for i in range(width):
    #     for j in range(height):
    #         temp_sum_row += frame[i, j]
    #         temp_sum_col += frame[j, i]
    #         if j == height - 1:
    #             row_pixel[i] = int(np.average(temp_sum_row))
    #             col_pixel[i] = int(np.average(temp_sum_col))

    # Detect blobs from the frame
    key_points = detector.detect(frame)

    for i in range(2):
        # Draw bounding boxes around blobs in the frame
        for keypoint in key_points:
            # Get coordinates from key points
            x, y = int(keypoint.pt[0]), int(keypoint.pt[1])
            # Predict direction of movement by using the displacement between the current and previous blob(s)
            if len(prev_keypoints) > 0:
                prev_x, prev_y = prev_keypoints[0].pt
                dx = x - prev_x
                dy = y - prev_y
                ur = dy < 0 < dx
                ul = dy < 0 and dx < 0
                dr = dy > 0 and dx > 0
                dl = dy > 0 > dx
                sur = 'Up and Right'
                sul = 'Up and Left'
                sdr = 'Down and Right'
                sdl = 'Down and Left'
                # Condensed decision statement
                direction_xy = sur if ur else sul if ul else sdr if dr else sdl if dl else 'Stationary'
                # Draw arrow(s) indicating direction of movement
                cv2.arrowedLine(frame, (x, y), (int(x + dx), int(y + dy)), (0, 0, 255), 2)
                cv2.putText(frame, direction_xy, (x-15, y-15), 0, 0.5, (0, 0, 255), 2)

            # Box blob objects with adjustable shifts
            cv2.rectangle(frame, (x-10, y-10), (x + 35, y + 35), (255, 0, 0), 2)
            temp_x[i] = x
            temp_y[i] = y

    # Have the bounding box persist
    cv2.rectangle(frame, (x - 10, y - 10),  (x + 35, y + 35), (255, 0, 0), 2)

    # Update previous
    prev_keypoints = key_points

    # Display frame
    cv2.imshow('Object Tracking and Motion Detection', frame)

    # Quit with q
    if cv2.waitKey(50) & 0xFF == ord('q'):
        break

# Release video file and close windows
cap.release()
cv2.destroyAllWindows()