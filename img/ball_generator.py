import cv2,numpy


# cv2.circle(n,(4,4),4,[0,0,0],-1)
i=7
n=cv2.merge(numpy.ones([1,i+1,i+1])*255)
cv2.circle(n,(i,i),i,0,-1,shift=1)

nn=cv2.merge(numpy.zeros([1,i+1,i+1]))
cv2.circle(nn,(i,i),i,255,-1,shift=1)

n=cv2.merge([n,n,n,nn])
cv2.imwrite("ball1.png",n)