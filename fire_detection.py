import cv2
import numpy as np
import smtplib
from datetime import datetime
#import playsound
import threading

#Alarm_Status = False
Email_Status = False
Fire_Reported = 0

#def play_alarm_sound_function():
#	while True:
#		playsound.playsound('alarm-sound.mp3',True)

def send_mail_function():

    recipientEmail = "saptajitbanerjee2002@gmail.com"
    recipientEmail = recipientEmail.lower()

    try:
        smtpUser='jcomponentrasberrypibot@gmail.com'
        smtpPass='waumkjgbiebmgmua'
        toAdd='saptajitbanerjee2002@gmail.com'
        fromAdd = smtpUser
        subject='WARNING! FIRE Detected!'
        header='To:'+toAdd+'\n'+'From:'+fromAdd+'\n'+'Subject:'+subject
        now = datetime.now()
        body='Fire has been detected at time: '+now.strftime("%m/%d/%Y, %H:%M:%S")
        print(header+'\n'+body)
        s = smtplib.SMTP('smtp.gmail.com',587)
        s.ehlo()
        s.starttls()
        s.ehlo()
        s.login(smtpUser,smtpPass)
        print("Login Successful")
        s.sendmail(fromAdd,toAdd,header+'\n\n'+body)
        s.quit()
    except Exception as e:
    	print(e)


video = cv2.VideoCapture("http://192.168.215.45:8000/stream.mjpg") # If you want to use webcam use Index like 0,1.

while True:
    (grabbed, frame) = video.read()
    if not grabbed:
        break

    frame = cv2.resize(frame, (960, 540))

    blur = cv2.GaussianBlur(frame, (21, 21), 0)
    hsv = cv2.cvtColor(blur, cv2.COLOR_BGR2HSV)

    lower = [18, 50, 50]
    upper = [35, 255, 255]
    lower = np.array(lower, dtype="uint8")
    upper = np.array(upper, dtype="uint8")

    mask = cv2.inRange(hsv, lower, upper)

    #output = cv2.bitwise_and(frame, hsv, mask=mask)

    no_red = cv2.countNonZero(mask)

    if int(no_red) > 20000:
        Fire_Reported = Fire_Reported + 1

    #cv2.imshow("output", output)
    #ret, frame = video.read()
    #cv2.imshow('frame', frame)
    
    if Fire_Reported >= 1:
        print("Fire Detected")
    	#if Alarm_Status == False:
    		#threading.Thread(target=play_alarm_sound_function).start()
    		#Alarm_Status = True
        if Email_Status == False:
            threading.Thread(target=send_mail_function).start()
            Email_Status = True
            break

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cv2.destroyAllWindows()
video.release()