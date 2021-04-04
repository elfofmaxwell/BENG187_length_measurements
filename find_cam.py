import cv2
cap = cv2.VideoCapture(2)
ret, frame = cap.read()
cv2.imshow('r', frame)
cv2.waitKey()