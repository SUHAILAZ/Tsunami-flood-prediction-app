# -*- coding: utf-8 -*-
"""
Created on Thu Mar 28 00:13:36 2019

@author: CodersMine
Team CARDIOCODERS
"""

from skimage.measure import compare_ssim
import imutils
import cv2
                   
import requests
import time

from firebase import firebase


#to make the buzzer beeeepppppp OFF mode 
try:
    r=requests.get("http://192.168.43.70/LED=OFF")
except:
    print("things are not good yet")

firebase = firebase.FirebaseApplication('https://sih2019-f0d6c.firebaseio.com/latLong', None)

imageA = cv2.imread("map - Copy.png")
imageB = cv2.imread("map.png")
imageC=cv2.imread("tsunami case.png")

grayA = cv2.cvtColor(imageA, cv2.COLOR_BGR2GRAY)
grayB = cv2.cvtColor(imageB, cv2.COLOR_BGR2GRAY)
grayC = cv2.cvtColor(imageC, cv2.COLOR_BGR2GRAY)


(score, diff) = compare_ssim(grayA, grayB, full=True)
diff = (diff * 255).astype("uint8")

#print("SSIM: {}".format(score))
(score1, diffMain) = compare_ssim(grayB, grayC, full=True)
diffMain = (diffMain * 255).astype("uint8")

thresh = cv2.threshold(diff, 0, 255,
    cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU)[1]
cnts = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL,
    cv2.CHAIN_APPROX_SIMPLE)
cnts = imutils.grab_contours(cnts)

for c in cnts:
    # compute the bounding box of the contour and then draw the
    # bounding box on both input images to represent where the two
    # images differ
    (x, y, w, h) = cv2.boundingRect(c)
    cv2.rectangle(imageA, (x, y), (x + w, y + h), (0, 0, 255), 2)
    cv2.rectangle(imageB, (x, y), (x + w, y + h), (0, 0, 255), 2)

w=len(imageA[0,:])#1920
h=len(imageB[:,0])#1080

a=[[ 55.06347656249999,32.80574473290688 ], 
   [101.77734374999998,32.84267363195431],
   [55.06347656249999,9.88227549342994],
   [101.77734374999998,10.14193168613103]]       

x0=(a[0][0]+a[2][0])/2
x1=(a[1][0]+a[3][0])/2

y0=(a[2][1]+a[3][1])/2
y1=(a[0][1]+a[1][1])/2

xm=0;
ym=0;
m=0;
n=0;




def pix_to_alt(x,y):
	m=x/w
	n=y/h
	xm=(m*(x1)+(1-m)*(x0))
	ym=(n*(y0)+(1-n)*(y1))
	return(xm,ym)
    
    
#led on during plotting
try:
    r=requests.get("http://192.168.43.70/LED=ON")
except:
    print("things are not good yet")
    

	
	
ct=0
for i in range(0,len(diff),4):
    for j in range(0,len(diff[0]),12):
        if(diff[i][j]<7):
                if(ct<10):
                    print(i,j)
                    ct+=1
                    lon,lat=pix_to_alt(i,j)
                    print(lat,lon)
                    #lon,lat=pix_to_alt(1920/2-240,1080/2-300)
                    data =  { 'latitude': lat+2,'longitude': lon+5} 
                    result = firebase.post('latLong/',data)
					



time.sleep(1)

try:
    r=requests.get("http://192.168.43.70/LED=OFF")
except:
    print("things are not good yet")
    
k=0
l=0

# -*- coding: utf-8 -*-
"""
Created on Sun Mar 31 10:59:24 2019

@author: CodersMine
"""

# Python program to play a video 
# in reverse mode using opencv 

# import cv2 library 
import cv2 
import time
# videoCapture method of cv2 return video object 
# Pass absolute address of video file 
cap = cv2.VideoCapture("open.avi") 


check , vid = cap.read() 

counter = 0


check = True

frame_list = [] 

while(check == True): 
    

    cv2.imwrite("frame%d.jpg" %counter , vid) 
    check , vid = cap.read() 
    frame_list.append(vid) 
    
    # increment the counter by 1 
    counter += 1

frame_list.pop() 

frame_list.reverse() 


for frame in frame_list: 
    

    cv2.imshow("Frame" , frame) 
    time.sleep(0.03)

    if cv2.waitKey(25) and 0xFF == ord("q"): 
        break

cap.release() 

# close any open windows 
cv2.destroyAllWindows() 

frame_list.reverse() 

for frame in frame_list: 
    cv2.imshow("Frame" , frame) 
    time.sleep(0.3)
    if cv2.waitKey(25) and 0xFF == ord("q"): 
        break

cap.release() 
cv2.destroyAllWindows()

new=diff-diffMain
for i in range(len(diff)):
    for j in range(len(diff[0])):
        l+=1
        if (new[i][j]):
            k+=1
matching=(l-k)/l


match="The value of matching percentage is "+str(matching*100)
emails=["vermavinay982@gmail.com","vanikakansal456@gmail.com","sachinpr0001@gmail.com","pmn.bhatnagar@gmail.com","sachinpr2015@gmail.com","alankritgupta091099@gmail.com"]

import smtplib, ssl
import pandas as pd

port = 465  # For SSL
smtp_server = "smtp.gmail.com"
sender_email = "verma.rohan017@gmail.com"  # Enter your address
password = "521998Yaniv1234"
#input("Type your password and press enter: ")


message = """\
"""+match+"""
Subject:Tsunami Alert

Please get to safest point 
things may get worse 

Contact: 123456
Name : Regional Officer

Contact: 100
Name:Police Headquarters

Indian Tsunami Early Warning Centre (ITEWC) Indian National Centre for Ocean Information Services (INCOIS) Address: Ocean Valley , Pragathi Nagar (BO), Nizampet (SO), Hyderabad 500 090, India. 
Tel: 914023895011
 Fax: 914023895012 Email:tsunami@incois.gov.in
Website: www.incois.gov.in

"""

for email in emails:    
    receiver_email =  email # Enter receiver address
    context = ssl.create_default_context()
    with smtplib.SMTP_SSL(smtp_server, port, context=context) as server:
        server.login(sender_email, password)
        print("Sending Mail to "+email);
        server.sendmail(sender_email, receiver_email, message)
    
	

"""Using with smtplib.SMTP_SSL() as server: makes sure that the connection is automatically closed at the end of the indented code block. If port is zero, or not specified, .SMTP_SSL() will use the standard port for SMTP over SSL (port 465)."""

import matplotlib.pyplot as plt 
  
# x axis values 
x = [1,2,3] 
# corresponding y axis values 
#matching=90
y = [matching,100,70] 
# labels for bars 
tick_label = ['Matching', 'Total', 'Danger Value'] 
def color(x,y):
    if(x[0]>3):
        return "green"
    else:
        return "blue"
    
# plotting the points  
plt.bar(x, y, color=["green","blue","red"], tick_label = tick_label) 

  
# naming the x axis 
plt.xlabel('x - axis') 
# naming the y axis 
plt.ylabel('y - axis') 
  
# giving a title to my graph 
plt.title('Representation of DATA!') 
  
# function to show the plot 
plt.show() 



dim=(int(w/2),int(h/2))
rez=cv2.resize(imageA,dim)
cv2.imshow("Original",cv2.resize(imageA,dim))
cv2.imshow("Modified",cv2.resize(imageB,dim))
cv2.imshow("Diff", cv2.resize(diff,dim))
cv2.imshow("Thresh",cv2.resize(thresh,dim))
cv2.waitKey(0)




    
    
    
    