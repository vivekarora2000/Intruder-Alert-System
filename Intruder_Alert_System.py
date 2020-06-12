import cv2
import numpy as np
import os
from twilio.rest import Client
from IPython.display import Audio
from threading import Thread
from playsound import playsound

def alarm():
    playsound("/home/vivek/file.mp3")
   
def call_owner():
    account_sid = 'ACcab5297d792518fd02fd69e3f11f538f'
    auth_token = '2703e1bc5f8851d7d241cfa1d7f9e858'
    client = Client(account_sid, auth_token)

    call = client.calls.create(
                            twiml='<Response><Say voice="Man">ALERT</Say><Pause length="1"/><Say voice="Man">ALERT</Say><Pause length="1"/><Say voice="Man">ALERT</Say><Say voice="Man">Someone has breached the perimeter</Say><Pause length="1"/><Say voice="Man">Someone has breached the perimeter</Say></Response>',
                            to='+919381404759',
                            from_='+13172862035'
                        )

    print(call.sid)

    
def main():
    
    total_mov=0
    count=0
    
    cap = cv2.VideoCapture(0)
    

    if cap.isOpened():
        ret, frame = cap.read()
    else:
        ret = False

    ret, frame1 = cap.read()
    ret, frame2 = cap.read()


    while ret:
        
        d = cv2.absdiff(frame1, frame2)
        
        grey = cv2.cvtColor(d, cv2.COLOR_BGR2GRAY)
        
        blur = cv2.GaussianBlur(grey, (5, 5), 0)
        
        ret, th = cv2.threshold( blur, 25, 255, cv2.THRESH_BINARY)
    
        dilated = cv2.dilate(th, np.ones((3, 3), np.uint8), iterations=1 )
        
        eroded = cv2.erode(dilated, np.ones((3, 3), np.uint8), iterations=1 )
        
        img, c, h = cv2.findContours(eroded, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        
        cv2.drawContours(frame1, c, -1, (0, 0, 255), 2)
        
        cv2.imshow("Output", frame1)
        
        if(th.sum()>100):
            total_mov+=1
            print("movement detected")
        else:
            if(total_mov>0):
                total_mov-=1
            print("No movement")

        if(count==0 or count>1):
            alarm()
            count+=1
            
        if(count==1):    
            if(total_mov>100):
                print("Alerting Owner")
                count+=1
                call_owner()   

        if cv2.waitKey(1) == 27: # exit on ESC
            break
        
        frame1 = frame2
        ret, frame2 = cap.read()

    cv2.destroyAllWindows()
    cap.release()
    

if __name__ == "__main__":
    main()