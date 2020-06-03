import cv2,numpy

n=cv2.imread("tank21.jpg")
a,b,c=cv2.split(n)
# nn=numpy.zeros(numpy.shape(a))
nn=numpy.copy(a)
nn[0:50,0:50]=255
nn[0:7,0:8]=0
nn[0:7,-8:]=0

# print(a,nn)
# print(a.shape,nn.shape)
n=cv2.merge([c,a,b,nn])
cv2.imwrite("tank23.png",n)