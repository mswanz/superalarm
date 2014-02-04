#imprt librerrys
import RPi.GPIO as GPIO
import time
import os
import smtplib
import mimetypes
from email.MIMEMultipart import MIMEMultipart
from email.MIMEBase import MIMEBase
from email.MIMEText import MIMEText
from email.MIMEAudio import MIMEAudio
from email.MIMEImage import MIMEImage
from email.Encoders import encode_base64
#funtion to send an email
def sendMail(subject, text):
  #change identety to username and password
  gmailUser = 'user@domain.net'
  gmailPassword = 'pa55Word'
  recipient = 'otheruser@domain.net'
  msg = MIMEMultipart()
  msg['From'] = gmailUser
  msg['To'] = recipient
  msg['Subject'] = subject
  msg.attach(MIMEText(text))
  #gmails mail server
  mailServer = smtplib.SMTP('smtp.gmail.com', 587)
  mailServer.ehlo()
  mailServer.starttls()
  mailServer.ehlo()
  mailServer.login(gmailUser, gmailPassword)
  mailServer.sendmail(gmailUser, recipient, msg.as_string())
  mailServer.close()
  print'Sent email to %s' % recipient

#set up the general perpose input output
GPIO.setmode(GPIO.BOARD)
GPIO.setup (11, GPIO.IN)
GPIO.setup (12, GPIO.OUT)
GPIO.setup (13, GPIO.IN)
GPIO.setup (15, GPIO.OUT)


while True:
      if not GPIO.input(11):
            if GPIO.input(13):
                  print "The door is open - please close the door and try again."
                  GPIO.output(15, True)
                  time.sleep(.3)
                  GPIO.output(15, False)
                  flash = 3
                  while flash > 0:
                        GPIO.output(12, True)
                        time.sleep(.3)
                        GPIO.output(12, False)
                        time.sleep(.3)
                        flash -= 1
            else:
                  active = 'true'
                  activated = 'false'
                  time.sleep(.1)
                  if GPIO.input(11):
                        print "Alarm Armed"
                        while active == 'true':
                              GPIO.output(12,False)
                              if not GPIO.input(11):
                                    time.sleep(.1)
                                    if GPIO.input(11):
                                          print "Alarm Disarmed"
                                          time.sleep(.1)
                                          active = 'false'
                              if GPIO.input(13):
                                    print "**** Alarm !!! ****"
                                    sendMail('alarm', 'intruder alert!')
                                    activated = 'true'
                                    GPIO.output(15, True)
                                    time.sleep(10)
                                    GPIO.output(15, False)
                                    while activated == 'true':
                                          if not GPIO.input(11):
                                                time.sleep(.1)
                                                if GPIO.input(11):
                                                      print "Alarm Disarmed"
                                                      time.sleep(.1)
                                                      active = 'false'
                                                      activated = 'false'
                                          else:
                                                GPIO.output(12, True)
                                                time.sleep(.3)
                                                GPIO.output(12, False)
                                                time.sleep(.3)
      else:
            GPIO.output(12,True)
