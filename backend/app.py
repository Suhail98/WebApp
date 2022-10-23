import flask
from flask import Flask,request, jsonify, render_template, request, redirect, url_for, send_file, Response
import os
import requests
#from app5 import OD
from app9 import OD2
from app10 import OD3
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
import globals2
loop = None

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
    print("ljljljl")
    uploaded_file = request.files['file']
    model = request.args.get('model')
    model_name = ""
    print(model, 0)
    if int(model) == int(0):
      print("wtf?")
      model_name = "yolov5\\model\\Weapon\\best.pt"
    elif int(model) == int(1):
      model_name = "yolov5/model/UAV/best.pt"
    else:
      model_name = "Analytics-_App-main/container_only_train.pt"
    
    print("hi")
    print(model)
    print(model_name)
    if uploaded_file.filename != '':
        uploaded_file.save(uploaded_file.filename)
    print("ops")
    #ip1 = request.remote_addr
    
    #detector = OD(capture_index=uploaded_file.filename, model_name='Analytics-_App-main/model/container_only_train.pt', ip=ip1)
    ip1 = request.remote_addr
    print(ip1)
    print("ops2")
    response = jsonify(success=True)
    #print(response1.content)
    #source = response1.json()['rtspURL']
    print(1)
    source = uploaded_file.filename
    print(2)
    global loop
    global server2
    print(loop)
    #if loop is not None:
      #loop.close()
      #loop = None
      #print("laaaaaaaaaaaaaaa")
      #server2.close()
      #loop.run_until_complete(server.wait_closed())
      #loop.stop()
      #loop = None
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    detector = None
    #global server
    if int(model) == int(2):
      print("in if model == 2")
      detector = OD3(capture_index=source, model_name=model_name,ip=ip1)
    else:    
      detector = OD2(capture_index=source, model_name=model_name,ip=ip1,loop=loop)
    print(3)
    if globals2.server is not None:
      globals2.server.close()
      globals2.server = None
    #start_server = websockets.serve(detector.time1, port=8585)
  
    async def serve():
        try:
          print("hi44")
          #global server
          globals2.server = await websockets.serve(detector.time1, port=8585)
          #server.close()
          print("hi33")
          await globals2.server.wait_closed()
          print("after awaint server.wait_closed()")
        except WindowsError as e:
                  print("windows error catched")
                  #server = await websockets.serve(detector.time1, port=8585)
                  #await server.wait_closed()
        except OSError as error :
                  print(error)
                  print("File descriptor is not associated with any terminal device")
        except websockets.exceptions.ConnectionClosedError:
                  print("ops1")
                  print("Client disconnected.  Do cleanup")
                  websockets.legacy.protocol.WebSocketCommonProtocol.close()
                  globals2.server.close()
                  websockets.terminate()
                  loop.stop()
                  loop.close()
                  #self.loop.stop()
        except Exception as e:
                  print("ops2")
                  #websockets.legacy.protocol.WebSocketCommonProtocol.close()
                  print("Client disconnected.  Do cleanup")
                  websockets.legacy.protocol.WebSocketCommonProtocol.close()
                  globals2.server.close()
                  websockets.terminate()
                  loop.stop()
                  loop.close()
                  '''
                  server.close()
                  websockets.terminate()
                  loop.stop()
                  loop.close()
                  '''
                  #self.loop.stop()
        except:
                  print("op3")
                  #websockets.legacy.protocol.WebSocketCommonProtocol.close()
                  print("Client disconnected.  Do cleanup")
                  websockets.legacy.protocol.WebSocketCommonProtocol.close()
                  globals2.server.close()
                  websockets.terminate()
                  loop.stop()
                  loop.close()
                  '''
                  server.close()
                  websockets.terminate()
                  loop.stop()
                  loop.close()
                  '''
                  #self.loop.stop()
        print("ops not done")  
    @response.call_on_close
    def sendStream():
          
            asyncio.run(serve())
            print("send stream final?")
            # Start the server, add it to the event loop
            # Registered our websocket connection handler, thus run event loop forever
            '''
            try:
                  server2 = asyncio.get_event_loop().run_until_complete(start_server)
                  asyncio.get_event_loop().run_forever()
            except asyncio.CancelledError:
              print('Tasks has been canceled')
            except websockets.exceptions.ConnectionClosed:
              #start_server.cancel()
              #loop.stop()
              print("Shutdown complete ...") 
              #loop.close()
            #loop.stop()
            print(4)
            print("entered")
            #detector()
            '''
    return response

@app.route("/get_my_ip", methods=["GET"])
def get_my_ip():
    return jsonify({'ip': request.remote_addr}), 200
