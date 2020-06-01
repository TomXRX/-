import cv2,numpy

n=cv2.imread("tank21.jpg")
a,b,c=cv2.split(n)
nn=numpy.ones(numpy.shape(a))*0

n=cv2.merge([a,b,c,nn])
cv2.imwrite("tank21.png",n)