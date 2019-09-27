import cv2, time

while True:
    video = cv2.VideoCapture(0)
    check, frame = video.read()
    cv2.imshow("Capturing",frame)
    key = cv2.waitKey(1)

    if key == ord('q'):
        break


video.release()
