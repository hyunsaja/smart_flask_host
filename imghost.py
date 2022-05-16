import os
import requests
import json

def imgshot(filename):   
    try:        
        posturl = 'http://smart-robot.kr/camshot'
        fimg = open('./image/'+filename+'.bmp', 'rb')
        upload = {'file': fimg}
        print('reading..')
        msg = requests.post(posturl, files= upload, timeout = 50).text
        return msg
    except:
        msg='ImgshotError'   
        return msg 
    finally:
        pass