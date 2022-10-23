import torch
import numpy as np
import cv2
from time import time
from datetime import datetime
import math
import numpy as np
import socket
import sys
import pickle
import struct
import websockets
from threading import Thread
import asyncio
import time
#from vidgear.gears import NetGear
import cv2
from concurrent.futures import TimeoutError as ConnectionTimeoutError
# timeout in seconds
import globals2
dir = []
async def time1(websocket, path,loop):
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
                    stop = False
                    while(vid.isOpened()):
                        
                        img, frame = vid.read()
                        
                        #frame = cv2.resize(frame, (640, 480))
                        encode_param = [int(cv2.IMWRITE_JPEG_QUALITY), 65]
                        man = cv2.imencode('.jpg', frame, encode_param)[1]
                        #sender(man)
                        #print(len(man.tobytes()))
                        #cv2.imshow('img',man)
                        try:
                                await websocket.send(man.tobytes())
                        except websockets.exceptions.ConnectionClosed:
                                stop = True
                                log("Socket closed")
                    if stop:
                            break
                
                except :
                    pass
class OD2:
    def __init__(self, capture_index, model_name, ip,loop):
        self.loop = loop
        """
        Initializes the class with youtube url and output file.
        :param url: Has to be as youtube URL,on which prediction is made.
        :param out_file: A valid output file name.
        """
        self.ip = ip
        self.capture_index = capture_index
        self.model = self.load_model(model_name)
        print(model_name)
        self.classes = self.model.names
        self.device = 'cuda' if torch.cuda.is_available() else 'cpu'
        print("Using Device: ", self.device)

    def get_video_capture(self):
        """
        Creates a new video streaming object to extract video frame by frame to make prediction on.
        :return: opencv2 video capture object, with lowest quality frame available for video.
        """
        return cv2.VideoCapture(self.capture_index)

    def load_model(self, model_name):
        model = torch.hub.load("yolov5",'custom' ,model_name , source='local')
        model.conf = 0.45  # confidence threshold (0-1)
        model.iou = 0.45  # NMS IoU threshold (0-1)
        return model

    def direction(self,lis):
      dirx = ''
      if len(lis)<2:
          
          for i in range(len(lis)-1):
              if lis[i] > lis[i + 1]:
                 if (np.array(lis[i]) - np.array(lis[i + 1])) > 5:
                     dirx = "Left"
              elif lis[i] < lis[i + 1]:
                 #if (np.array(lis[i+1]) - np.array(lis[i])) < 5:
                    #print((np.array(lis[i+1]) - np.array(lis[i])),'sec')
                    dirx = "Right"      
      return dirx

    def score_frame(self, frame):
        """
        Takes a single frame as input, and scores the frame using yolo5 model.
        :param frame: input frame in numpy/list/tuple format.
        :return: Labels and Coordinates of objects detected by model in the frame.
        """
        self.model.to(self.device)
        frame = [frame]
        results = self.model(frame)
        labels, cord ,confidence = results.xyxyn[0][:, -1], results.xyxyn[0][:, :-1],results.xyxyn[0][:, -2]
        dir.append([lis.item() for lis in results.xyxy[0][:,0:1]])
        tep=self.direction(dir)
        return labels, cord,confidence,tep

    def class_to_label(self, x):
        """
        For a given label value, return corresponding string label.
        :param x: numeric label
        :return: corresponding string label
        """
        return self.classes[int(x)]

    def plot_boxes(self, results, frame):
        """
        Takes a frame and its results as input, and plots the bounding boxes and label on to the frame.
        :param results: contains labels and coordinates predicted by model on the given frame.
        :param frame: Frame which has been scored.
        :return: Frame with bounding boxes and labels ploted on it.
        """
        labels, cord, confidence,dir = results
        n = len(labels)
        x_shape, y_shape = frame.shape[1], frame.shape[0]
        for i in range(n):
            row = cord[i]
            if row[4] >= 0.3:
                x1, y1, x2, y2 = int(row[0]*x_shape), int(row[1]*y_shape), int(row[2]*x_shape), int(row[3]*y_shape)
                bgr = (0, 0, 255)
                cv2.rectangle(frame, (x1, y1), (x2, y2), bgr, 2)
                cv2.putText(frame, self.class_to_label(labels[i]) + " " +str([round(x.item(),2) for x in confidence][i]),\
                            (x1, y1), cv2.FONT_HERSHEY_SIMPLEX , 0.7 , bgr, 1 ,cv2.LINE_AA)
                
                cv2.putText(img = frame,
                        text = f'Number of Objects: {int(len(results[0]))}',
                        org = (20, 60),
                        fontFace = cv2.FONT_HERSHEY_SIMPLEX,
                        fontScale = 0.7,
                        color = (0, 0, 255),
                        thickness = 1,
                        lineType =cv2.LINE_AA)
                
                if int(len(results[0])) == 1:
                      cv2.putText(img = frame,
                            text = f'Direction: {dir}',
                            org = (20, 85),
                            fontFace = cv2.FONT_HERSHEY_SIMPLEX,
                            fontScale = 0.7,
                            color = (0, 0, 255),
                            thickness = 1,
                            lineType =cv2.LINE_AA)     

        return frame


    async def time1(self,websocket, path):
        #while True:
                ''' 
                cap = cv2.VideoCapture('rtsp://186.1.16.32:1161/02010533754159250101?DstCode=01&ServiceType=1&ClientType=1&StreamID=1&SrcTP=2&DstTP=2&SrcPP=1&DstPP=1&MediaTransMode=0&BroadcastType=0&SV=1&Token=H3QJhAtJ8Hu1Mm3uMqeoaPPBnbltrb8Ln4hdxwnWzxs=&DomainCode=da30d0eb264e47968184273537e16acf&UserId=12&')
                '''
                #print(5)
                cap = self.get_video_capture()
                cap.set(cv2.CAP_PROP_FPS,30)
                video_fps = cap.get(cv2.CAP_PROP_FPS),
                total_frames = cap.get(cv2.CAP_PROP_FRAME_COUNT)
                height = cap.get(cv2.CAP_PROP_FRAME_HEIGHT)
                width = cap.get(cv2.CAP_PROP_FRAME_WIDTH)
                #print(6)
                    #v = VideoStreamWidget()
                    #v.ops()
                i = 0
                try:
                        while(cap.isOpened()):
                                #print(7)
                                img, frame = cap.read()
                                i += 1
                                if i % 3 != 0:
                                        continue
                                frame = cv2.resize(frame, (640, 480))
                                #start_time = time()
                                results = self.score_frame(frame)
                                frame = self.plot_boxes(results, frame)
                                
                                encode_param = [int(cv2.IMWRITE_JPEG_QUALITY), 65]
                                man = cv2.imencode('.jpg', frame, encode_param)[1]
                                #sender(man)
                                #print(len(man.tobytes()))
                                #cv2.imshow('img',man)
                                #print(8)

                                timeout = 10
                                await websocket.send(man.tobytes())
                        
                except Exception as e:              
                        print("hey")
                        globals2.server.close()
  
    def __call__(self):
    
        """
        This function is called when class is executed, it runs the loop to read the video frame by frame,
        and write the output into a new file.
        :return: void
        """
        '''
        while True:
                    
                                    cap = cv2.VideoCapture('rtsp://186.1.16.32:1161/02010533754159250101?DstCode=01&ServiceType=1&ClientType=1&StreamID=1&SrcTP=2&DstTP=2&SrcPP=1&DstPP=1&MediaTransMode=0&BroadcastType=0&SV=1&Token                    =H3QJhAtJ8Hu1Mm3uMqeoaPPBnbltrb8Ln4hdxwnWzxs=&DomainCode=da30d0eb264e47968184273537e16acf&UserId=12&')
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
        #cap = self.get_video_capture()
        #assert cap.isOpened()
        #asyncio.set_event_loop_policy(AnyThreadEventLoopPolicy())
        '''
        '''
        #print(f"Frame Per second: {video_fps } \nTotal Frames: {total_frames} \nHeight: {height} \nWidth: {width}")

        # we are using x264 codec for mp4
        #fourcc = cv2.VideoWriter_fourcc(*'x264')
        #writer = cv2.VideoWriter("out.mp4", apiPreference=0, fourcc=fourcc,
                                fps=video_fps[0], frameSize=(int(width), int(height)))
        # define tweak flags
        #options = {"flag": 0, "copy": False, "track": False}

        # Define Netgear Client at given IP address and define parameters 
        # !!! change following IP address '192.168.x.xxx' with yours !!!
        
        client = NetGear(
            address="192.168.1.11",
            port="5454",
            protocol="tcp",
            pattern=0,
            logging=True,
            **options
        )
        
        print("trying to")
        print(self.ip)
        #clientsocket=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        #clientsocket.connect(('192.168.1.11',8089))
        #clientsocket.connect((self.ip,8089))
        #print(self.ip)
        print("maybe succeeded?")
        while (True):
            #print(0)
            ret, frame = cap.read()
            if frame is None:
                continue
            start_time = time()
            results = self.score_frame(frame)
            frame = self.plot_boxes(results, frame)
            
            #print(len(frame))
            #print(1)
            #frame = cv2.resize(frame, (int(width), int(height)) , interpolation = cv2.INTER_AREA)
            #data = pickle.dumps(frame)
            #print(len(data))
            #print(data)
            #print(2)
            # Send message length first
            #message_size = struct.pack("L", len(data)) ### CHANGED
            #print(type(message_size))
            #print(3)
            # Then data
            #clientsocket.sendall(message_size + data)
            #print(4)
            
            #client.send(frame)                                 
            #cv2.imshow('img',frame)
            #writer.write(frame)
            #clientsocket.sendall(message_size + data)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        cap.release()
        cv2.destroyAllWindows()
        print(10)
        '''

#detector = OD(capture_index="rtsp://186.1.16.32:1161/02010533754159250101?DstCode=01&ServiceType=1&ClientType=1&StreamID=1&SrcTP=2&DstTP=2&SrcPP=1&DstPP=1&MediaTransMode=0&BroadcastType=0&SV=1&Token=63B64Rsp7ATaAf+HE1JcN8AyXqntsSjNwjQb2Tupy90=&DomainCode=da30d0eb264e47968184273537e16acf&UserId=12&", model_name='Analytics-_App-main/model/best.pt')
#print("before")
#detector()
