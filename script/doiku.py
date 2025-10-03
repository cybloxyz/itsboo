import cv2

name = input("name: ")

cam = cv2.VideoCapture(0)

while True:
    ret, img = cam.read()
    
    cv2.imshow('Image', img)
    if cv2.waitKey(1) == ord('c'):
        cv2.imwrite('faces/' + name + ".jpg", img)
        print(f"{name} saved to faces/")
        break
    
cam.release()
cv2.destroyAllWindows()