import cv2
import cvzone
from cvzone.SelfiSegmentationModule import SelfiSegmentation
import os
import numpy as np


cap = cv2.VideoCapture(0)
cap.set(3, 640)
cap.set(4, 480)


segmentor = SelfiSegmentation()

listImg = os.listdir("images")
imgList = []
for imgPath in listImg:
    img = cv2.imread(f'images/{imgPath}')
    img = cv2.resize(img, (640, 480))
    imgList.append(img)
indexImg = 0

while True:
    success, img = cap.read()
    if not success:
        continue
    img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    results = segmentor.selfieSegmentation.process(img_rgb)
    mask = results.segmentation_mask
    mask_blurred = cv2.GaussianBlur(mask, (9, 9), 0)
    
    alpha = np.stack([mask_blurred] * 3, axis=-1)
    bg_image = imgList[indexImg]
    
    foreground = img.astype(np.float32)
    background = bg_image.astype(np.float32)
    
    imgOut = cv2.multiply(alpha, foreground) + cv2.multiply(1.0 - alpha, background)
    imgOut = imgOut.astype(np.uint8)


    imgStacked = cvzone.stackImages([img, imgOut], 2, 1)
    cv2.imshow("Image", imgStacked)
    key = cv2.waitKey(1)

# Navigation controls
    if key == ord('a'):
        if indexImg > 0:
            indexImg -= 1

    elif key == ord('d'):
        if indexImg < len(imgList) - 1:
            indexImg += 1

    elif key == ord('q'):
        break


cap.release()
cv2.destroyAllWindows()
