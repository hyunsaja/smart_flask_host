#flask
from flask import Flask, request, render_template, url_for
from flask_restx import Resource, Api
import os
import random
import camhost
import imghost
import urllib
import json
from flask import send_file

app = Flask(__name__)
api = Api(app)

# API 
@api.route('/smart',  methods = ['POST'])
class SmartPost(Resource):
    def post(self):
        print(request.json)
        fname = request.json.get('fname')
        cmd = request.json.get('cmd')
        expos = request.json.get('expos')
        thickness = request.json.get('thickness')
        try:
            if 'camshot' in cmd:
                print(cmd)
                msg = camhost.camshot(expos, thickness)
                print('CamshotOK')
                if 'CamshotOK' in msg:
                    print('camimgshot')
                    msg2 = imghost.imgshot(fname)
                    print(msg2)
                    msg = msg2
                
            elif 'imgshot' in cmd:
                print(cmd)
                msg2 = imghost.imgshot(fname)
                print(msg2)
                msg = msg2
                
            elif 'ncfile' in cmd:
                print(cmd)
                from requests import get
                import shutil
                url = 'http://smart-robot.kr/ncfile'
                with open('./point.txt', "wb") as file:   # open in binary mode
                    res = get(url)               # get request
                    file.write(res.content)      # write to file
                    # shutil.copy('./point.txt', './nc.cnc')   
                    shutil.copy('./point.txt', '/home/pi/nc.cnc')   
                msg = "ShotOK"
            else:
                return {'message':'nomatch'}
        except:
            return {'message':'commandError'}
        
if __name__ == "__main__":
    app.run(host="127.0.0.1", port=int("3000"), debug=True)