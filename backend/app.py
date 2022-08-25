import flask
from flask import Flask,request, jsonify, render_template, request, redirect, url_for, send_file, Response
import os
import requests
from app5 import OD
import torch
import numpy as np
import cv2
from time import time
from datetime import datetime
import math
import websockets
from threading import Thread
import asyncio
import time
from flask_cors import CORS
'''
with requests.Session() as session:
    query = {
    "userName":"yangyoujian","password":"Huawei@22q22"
    }
    session.get('https://186.1.16.32:18531/loginInfo/login/v1.0',verify=False)
    response = session.post('https://186.1.16.32:18531/loginInfo/login/v1.0', json  = query,verify=False)
    if response.json()['resultCode'] == 0:
        print("login sucess")
    else:
        print("login failed")
        '''
'''
async def time2(websocket, path):
        
        while True:    
                cap = cv2.VideoCapture('rtsp://186.1.16.32:1161/02010533754159250101?DstCode=01&ServiceType=1&ClientType=1&StreamID=1&SrcTP=2&DstTP=2&SrcPP=1&DstPP=1&MediaTransMode=0&BroadcastType=0&SV=1&Token=H3QJhAtJ8Hu1Mm3uMqeoaPPBnbltrb8Ln4hdxwnWzxs=&DomainCode=da30d0eb264e47968184273537e16acf&UserId=12&')
                cap.set(cv2.CAP_PROP_FPS,24)
                video_fps = cap.get(cv2.CAP_PROP_FPS),
                total_frames = cap.get(cv2.CAP_PROP_FRAME_COUNT)
                height = cap.get(cv2.CAP_PROP_FRAME_HEIGHT)
                width = cap.get(cv2.CAP_PROP_FRAME_WIDTH)
                try:
                    #v = VideoStreamWidget()
                    #v.ops()
                    
                    while(vid.isOpened()):
                        
                        img, frame = vid.read()
                        
                        #frame = cv2.resize(frame, (640, 480))
                        encode_param = [int(cv2.IMWRITE_JPEG_QUALITY), 65]
                        man = cv2.imencode('.jpg', frame, encode_param)[1]
                        #sender(man)
                        #print(len(man.tobytes()))
                        #cv2.imshow('img',man)
                        await websocket.send(man.tobytes())
                
                except :
                    pass
          '''

def do_something():
  print('MyFlaskApp is starting up!')


class MyFlaskApp(Flask):
  def run(self, host=None, port=None, debug=True, load_dotenv=True, **options):
    if not self.debug or os.getenv('WERKZEUG_RUN_MAIN') == 'true':
      with self.app_context():
        do_something()
    super(MyFlaskApp, self).run(host=host, port=port, debug=debug, load_dotenv=load_dotenv, **options)


app = Flask(__name__)
CORS(app)
app.run(debug=True,host="0.0.0.0")



@app.route('/localFile', methods=['POST'])
def upload_file():
    print("hi2")
    uploaded_file = request.files['file']
    print("hi1")
    if uploaded_file.filename != '':
        uploaded_file.save(uploaded_file.filename)
    print("ops")
    #ip1 = request.remote_addr
    
    #detector = OD(capture_index=uploaded_file.filename, model_name='Analytics-_App-main/model/container_only_train.pt', ip=ip1)
    ip1 = request.remote_addr
    print(ip1)
    print("ops2")
    response = Response(ip1)
    @response.call_on_close
    def sendStream():
        #print(response1.content)
        #source = response1.json()['rtspURL']
            source = uploaded_file.filename
            detector = OD(capture_index=source, model_name='Analytics-_App-main/container_only_train.pt',ip=ip1)
            print("entered")
            detector()
    return response

@app.route("/get_my_ip", methods=["GET"])
def get_my_ip():
    return jsonify({'ip': request.remote_addr}), 200
