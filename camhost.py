import os
from re import M
import time
import numpy as np
import cv2
import sys
from pypylon import genicam
from pypylon import pylon
import imghost
import threading
import os.path
import requests
import shutil
import json

converter = pylon.ImageFormatConverter()
converter.OutputPixelFormat = pylon.PixelType_Mono8 
converter.OutputBitAlignment = pylon.OutputBitAlignment_MsbAligned

global gGrabOk
gGrabOk = False
global gImg
global g_grabResult

filename = 'img'

class SampleImageEventHandler(pylon.ImageEventHandler):
    def OnImageGrabbed(self, camera, grabResult): 
        if camera.IsGrabbing():
            if grabResult.GrabSucceeded():
                g_grabResult = grabResult
                image = converter.Convert(g_grabResult)
                img = image.GetArray()      
                cv2.imwrite('./image/' + filename + '.bmp', img)       
                print(img.shape)
                # return img   

def camshot(expos, fname):  
    try:
        print('Camstep1')
        tlFactory = pylon.TlFactory.GetInstance()
        devices = tlFactory.EnumerateDevices()
        if len(devices) == 0:
            raise pylon.RUNTIME_EXCEPTION("No camera present.")
        for i in range(len(devices)):
            if devices[i].GetSerialNumber() == '24044347':
            # if devices[i].GetSerialNumber() == '23683422':
                camera = pylon.InstantCamera(tlFactory.CreateDevice(devices[i]))
                camera.RegisterImageEventHandler(SampleImageEventHandler(), pylon.RegistrationMode_Append, pylon.Cleanup_Delete)

        camera.Open()
        camera.TriggerMode.SetValue('On')
        camera.TriggerSource.SetValue('Software')
        camera.ExposureTimeAbs.SetValue(int(expos))

        camera.StartGrabbing(pylon.GrabStrategy_OneByOne, pylon.GrabLoop_ProvidedByInstantCamera)
        if camera.IsGrabbing(): 
            camera.ExecuteSoftwareTrigger()
            time.sleep(0.2)
            return 'CamshotOK'    
        else:
            return 'CamshotError'
                            
    except genicam.GenericException as e:
        # Error handling.
        print("An exception occurred.", e.GetDescription())
        return 'CameraError'
