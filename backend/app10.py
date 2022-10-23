from textwrap import fill
import torch
import numpy as np
import cv2 
from time import time
from datetime import datetime
import math
import arabic_reshaper
from bidi.algorithm import get_display
from PIL import ImageFont, ImageDraw, Image
import globals2
dir = []

class OD3:
    def __init__(self, capture_index, model_name, ip):
        """
        Initializes the class with youtube url and output file.
        :param url: Has to be as youtube URL,on which prediction is made.
        :param out_file: A valid output file name.
        """
        self.capture_index = capture_index
        self.model = self.load_model(model_name)
        self.classes = self.model.names
        self.device = 'cuda' if torch.cuda.is_available() else 'cpu'
        print("Using Device: ", self.device)
        self.frame_count = []
        self.count = 0
        self.is_container = False
        self.left_corner = []
        self.last_container = 0
        self.ip = ip
    def get_video_capture(self):
        """
        Creates a new video streaming object to extract video frame by frame to make prediction on.
        :return: opencv2 video capture object, with lowest quality frame available for video.
        #cv2.VideoCapture(self.capture_index , cv2.CAP_FFMPEG)
        """
        #rtsp = "rtsp://186.1.16.32:1161/02010533754159250101?DstCode=01&ServiceType=1&ClientType=1&StreamID=1&SrcTP=2&DstTP=2&SrcPP=1&DstPP=1&MediaTransMode=0&BroadcastType=0&SV=1&Token=pVt4XpuQUFvFTND0UIc6ZCCe4OF0Dj/zOz7G+RKAix8=&DomainCode=da30d0eb264e47968184273537e16acf&UserId=12"
        cap = cv2.VideoCapture(self.capture_index)
        #cap.set(cv2.CAP_PROP_BUFFERSIZE, 1)
        cap.set(cv2.CAP_PROP_FPS, 30)
        assert cap is not None
        return cap

    def load_model(self, model_name):
        model = torch.hub.load("yolov5",'custom' ,'Analytics-_App-main/container_only_train.pt' , source='local')
        model.conf = 0.80  
        model.iou = 0.50 
        #model.classes = 0
        return model
    
    def check_if_all_zero(self,arr):
        for elem in arr:
            if elem != 0:
                return False
        return True
        
    def check_if_all_ones(self,arr):
        for elem in arr:
            if elem != 1:
                return False
        return True 

    def score_frame(self, frame):
        """
        Takes a single frame as input, and scores the frame using yolo5 model.
        :param frame: input frame in numpy/list/tuple format.
        :return: Labels and Coordinates of objects detected by model in the frame.
        """
        
        self.model.to(self.device)
        frame = [frame]
        results = self.model(frame)
        
        labels, cord ,confidence = results.xyxyn[0][:, -1], results.xyxy[0][:,:-1],results.xyxyn[0][:, -2]
        
        try:
            if labels.size()[0] == 0:
                self.frame_count.append(0)
                
            if labels.size()[0] == 1:
                if self.count == 0 or (self.left_corner[-2] - self.left_corner[-1] >= 150): 
                    print("here")
                    self.is_container = True
                self.frame_count.append(1)
                self.left_corner.append(cord[0][0].item())
                print(self.left_corner[-2] , self.left_corner[-1])
            """if self.left_corner[-1] < self.left_corner[-2]:
                print(self.left_corner)"""
                
            if self.check_if_all_zero(self.frame_count[-30:]):
                if self.is_container == True:
                    self.count +=1
                    #self.left_corner = []
                    self.is_container = False          
        except :
            pass
        
        return labels, cord ,confidence
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
        labels, cord, confidence = results
        n = len(labels)
        x_shape, y_shape = frame.shape[1], frame.shape[0]
        for i in range(n):
            row = cord[i]
            if row[4] >= 0.3:
                x1, y1, x2, y2 = int(row[0]), int(row[1]), int(row[2]), int(row[3])
                bgr = (0, 0, 255)
                cv2.rectangle(frame, (x1, y1), (x2, y2), bgr, 2)
                cv2.putText(frame, self.class_to_label(labels[i]) + " " +str([round(x.item(),2) for x in confidence][i]),\
                            (x1, y1), cv2.FONT_HERSHEY_SIMPLEX , 0.7 , bgr, 1 ,cv2.LINE_AA)  
                
        return frame
    '''
    def __call__(self):
        """
        This function is called when class is executed, it runs the loop to read the video frame by frame,
        and write the output into a new file.
        :return: void
        """
        cap = self.get_video_capture()
        assert cap.isOpened()
        
        # we are using x264 codec for mp4
        cap.set(cv2.CAP_PROP_FPS, 30)
        video_fps = cap.get(cv2.CAP_PROP_FPS),
        total_frames = cap.get(cv2.CAP_PROP_FRAME_COUNT)
        height = cap.get(cv2.CAP_PROP_FRAME_HEIGHT)
        width = cap.get(cv2.CAP_PROP_FRAME_WIDTH)
        fourcc = cv2.VideoWriter_fourcc(*'mp4v')
        writer = cv2.VideoWriter('out2.mp4', apiPreference=0, fourcc=fourcc,
                                fps=video_fps[0], frameSize=(int(width), int(height)))
        while (cap.isOpened()):
            ret, frame = cap.read()
            if not ret:
                break
            if(frame is None):
                continue
            #print(1)
            #frame = frame[200:800,200:1000]
            results = self.score_frame(frame)
            #print(2)
            
            cv2.putText(img = frame,
                            #text = f'Number of Containers: {int(len(results[0]))}',
                            text = f'Number of Containers: {self.count}',
                            org = (20, 300),
                            fontFace = cv2.FONT_HERSHEY_SIMPLEX,
                            fontScale = 0.7,
                            color = (0, 0, 255),
                            thickness = 2,
                            lineType =cv2.LINE_AA)  
            
            #print(3)
            frame = self.plot_boxes(results, frame)
            #cv2.imshow('img',frame)
            writer.write(frame)
            #print(4)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        cap.release()
        cv2.destroyAllWindows()
    '''       
    async def time1(self,websocket, path):
    
      
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
                    while (cap.isOpened()):
                        #start_time = time()
                         
                        (grabbed, frame) = cap.read()
                        if not grabbed:
                                break
                        #print(2)
                        i+=1
                        if(i%3 != 0):
                                continue
                        #frame = cv2.resize(frame, (640, 480))
                        results = self.score_frame(frame)
                        cv2.putText(img = frame,
                                        #text = f'Number of Containers: {int(len(results[0]))}',
                                        text = f'Number of Containers: {self.count}',
                                        org = (1400, 300),
                                        fontFace = cv2.FONT_HERSHEY_SIMPLEX,
                                        fontScale = 0.68,
                                        color = (0, 0, 255),
                                        thickness = 2,
                                        lineType =cv2.LINE_AA)  
                        frame = self.plot_boxes(results, frame)
                        encode_param = [int(cv2.IMWRITE_JPEG_QUALITY), 65]
                        man = cv2.imencode('.jpg', frame, encode_param)[1]         
                        timeout = 10
                        #print("FUCK YOU")
                        #cv2.imshow('img',frame)
                        await websocket.send(man.tobytes())
                        #print(3)
                                                      
                        #writer.write(frame)
                        #clientsocket.sendall(message_size + data)
                except Exception as e:              
                        print("hey")
                        globals2.server.close()
    '''
    def __call__(self):
    
        """
        This function is called when class is executed, it runs the loop to read the video frame by frame,
        and write the output into a new file.
        :return: void
        """
        cap = self.get_video_capture()
        assert cap.isOpened()
        cap.set(cv2.CAP_PROP_FPS, 30)
        video_fps = cap.get(cv2.CAP_PROP_FPS),
        total_frames = cap.get(cv2.CAP_PROP_FRAME_COUNT)
        height = cap.get(cv2.CAP_PROP_FRAME_HEIGHT)
        width = cap.get(cv2.CAP_PROP_FRAME_WIDTH)
        #print(f"Frame Per second: {video_fps } \nTotal Frames: {total_frames} \nHeight: {height} \nWidth: {width}")

        # we are using x264 codec for mp4
        fourcc = cv2.VideoWriter_fourcc(*'mp4v')
        writer = cv2.VideoWriter("out.mp4", apiPreference=0, fourcc=fourcc,
                                fps=video_fps[0], frameSize=(int(width), int(height)))

        while (True):

            ret, frame = cap.read()
            if not ret:
                break
            #frame = cv2.resize(frame, (int(width), int(height)) , interpolation = cv2.INTER_AREA)

            start_time = time()
            results = self.score_frame(frame)
            frame = self.plot_boxes(results, frame)
                                             
            #cv2.imshow('img',frame)
            writer.write(frame)
            
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        cap.release()
        cv2.destroyAllWindows()
      '''

#detector = OD(capture_index="rtsp://186.1.16.32:1161/02010533754159250101?DstCode=01&ServiceType=1&ClientType=1&StreamID=1&SrcTP=2&DstTP=2&SrcPP=1&DstPP=1&MediaTransMode=0&BroadcastType=0&SV=1&Token=63B64Rsp7ATaAf+HE1JcN8AyXqntsSjNwjQb2Tupy90=&DomainCode=da30d0eb264e47968184273537e16acf&UserId=12&", model_name='Analytics-_App-main/model/best.pt')
#print("before")
#detector()
