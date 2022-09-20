import cv2
import numpy as np
from math import sqrt
from skimage.feature import blob_dog, blob_log, blob_doh

#img = cv2.imread('/Volumes/Aligned_data/tect_seg/Good_seg_test_cropped.tif')
img = cv2.imread('1.jpg')
# plt.figure(figsize=(10,10))
# plt.imshow(img)
cv2.imshow('img',img)
cv2.waitKey(0)

gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
# plt.figure(figsize=(10,10))
# plt.imshow(gray, cmap = "gray")
cv2.imshow('gray',gray)
cv2.waitKey(0)


# th = cv2.adaptiveThreshold(gray,255, cv2.ADAPTIVE_THRESH_MEAN_C,cv2.THRESH_BINARY_INV,3,5)
# # cv2.adaptiveThreshold(image, 255, 自適應二值化算法, 閥值類型, 參考局部大小, 偏移量)
# plt.figure(figsize=(10,10))
# plt.imshow(th)

thre,cell_bw=cv2.threshold(gray,80,255,cv2.THRESH_BINARY)#二值化
cv2.imshow('THRESH',cell_bw)
cv2.waitKey(0)


blobs_log = blob_log(cell_bw,min_sigma = 4, max_sigma=5.5, num_sigma=10, threshold=.0001,overlap=0.7)
# Compute radii in the 3rd column.
blobs_log[:, 2] = blobs_log[:, 2] * sqrt(2)


# fig, ax = plt.subplots(figsize=(20, 20), sharex=True, sharey=True)


# ax.imshow(cell_bw, interpolation='nearest')
# # cv2_imshow(gray)
# for i in range(blobs_log.shape[0]):
#     y, x, r = blobs_log [i,]
#     c = plt.Circle((x, y), r, color='r', linewidth=1, fill=False)
#     ax.add_patch(c)

# fig, ax = plt.subplots(figsize=(20, 20), sharex=True, sharey=True)
# font = {'family': 'serif',
#         'color':  (1,1,1),
#         'weight': 'bold',
#         'size': 8
#         }

# ax.imshow(img, interpolation='nearest')
# cv2_imshow(gray)
output1img=img.copy()
for i in range(blobs_log.shape[0]):
    y, x, r = blobs_log [i,]
    # c = plt.Circle((x, y), r, color='r', linewidth=1, fill=False)
    cv2.circle(output1img,(int(x), int(y)), int(r), color=(0,0,255), thickness=2)
    # y=10 if x<10 else x #防止編號到圖片之外
    # ax.text(x, y, str(i))
    # ax.text(x,y, str(i), fontdict=font)
    cv2.putText(output1img,str(i), (int(x), int(y)), cv2.FONT_HERSHEY_COMPLEX, 0.4, (255, 255, 255), 1) #在左上角寫上編號
    # ax.add_patch(c)

# fig, ax = plt.subplots(figsize=(20, 20), sharex=True, sharey=True)
cv2.imshow('output1img',output1img)
cv2.waitKey(0)
output2img = gray.copy()
# ax.imshow(gray, interpolation='nearest',cmap="gray")
for i in range(blobs_log.shape[0]):
    y, x, r = blobs_log [i,]
    # ax.text(x,y, str(i), fontdict=font)

    if r > 1.5:
        # c = plt.Circle((x, y), r, color="red", alpha = 0.4, linewidth=2, fill=True)
        cv2.circle(output2img,(int(x), int(y)), int(r), color=(0,0,0), thickness=2)

        # ax.add_patch(c)
    else:
        # c = plt.Circle((x, y), r, color="cyan", linewidth=2, fill=False)
        cv2.circle(output2img,(int(x), int(y)), int(r), color=(0,255,0), thickness=-1)

        # ax.add_patch(c)

cv2.imshow('output2img',output2img)
cv2.waitKey(0)
print(blobs_log.shape [0])
