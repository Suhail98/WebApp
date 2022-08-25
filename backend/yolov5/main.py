#from PyQt5.QtWidgets import QMainWindow, QApplication, QPushButton, QTextEdit, QFileDialog, QWidget
from PyQt5 import uic, QtWidgets
import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5 import *
import sys
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5 import QtWidgets, QtMultimediaWidgets, QtMultimedia, QtCore, QtGui, Qt
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QPushButton, QLineEdit, QComboBox
from PyQt5.QtGui import QTransform
import sys
import random
import requests
from xml.etree import ElementTree
import socket
from detect import run
import time
import os
from pathlib import Path
import cv2
from PIL import Image
import torch
import gc
ip = socket.gethostbyname(socket.gethostname())

model_choice = ""

#Form = QtWidgets.QWidget()


#ui.setupUi(Form)




gc.collect()
torch.cuda.empty_cache()

with requests.Session() as session:
    query = {
    "userName":"yangyoujian","password":"Huawei@2021"
    }
    session.get('https://186.1.16.32:18531/loginInfo/login/v1.0',verify=False)
    response = session.post('https://186.1.16.32:18531/loginInfo/login/v1.0', json  = query,verify=False)
    if response.json()['resultCode'] == 0:
        print("login sucess")
    else:
        print("login failed")

class Ui_Form(object):
    def __init__(self, Form,dict):
        print("ops")
        '''
        response = session.post('https://186.1.16.32:18531/video/rtspurl/v1.0', json = query, verify=False)
        if response.json()['resultCode'] == 0:
            print("Stream begun")
        else:
            print("Stream failed")
        print(response.content)
        '''
        Form.setObjectName("Form")
        Form.resize(622, 300)
        #Form.setStyleSheet("background-color: rgb(0,11,25);")
        #Form.background-color = rgb(0,0,0);
        '''
        self.label = QtWidgets.QLabel(Form)
        self.label.setGeometry(QtCore.QRect(110, 60, 161, 20))
        self.label.setAutoFillBackground(True)
        self.label.setObjectName("label")
        self.pushButton = QtWidgets.QPushButton(Form)
        self.pushButton.setGeometry(QtCore.QRect(360, 50, 75, 41))
        self.pushButton.setObjectName("pushButton")
        '''
        self.tableWidget = QtWidgets.QTableWidget(Form)
        self.tableWidget.setGeometry(QtCore.QRect(10, 50, 591, 192))
        self.tableWidget.setObjectName("tableWidget")
        self.tableWidget.setColumnCount(20)
        self.tableWidget.setRowCount(0)
        self.tableWidget.setEditTriggers(QtWidgets.QTableWidget.NoEditTriggers)
        #self.tableWidget.setStyleSheet("color: white")
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(1, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(2, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(3, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(4, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(5, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(6, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(7, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(8, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(9, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(10, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(11, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(12, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(13, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(14, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(15, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(16, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(17, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(18, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(19, item)
        print(model_choice)
        
        print(model_choice)
        #self.pushButton.clicked.connect(self.click1)
        print(self.tableWidget)
        self.retranslateUi(Form)
        self.load_data(dict)
        QtCore.QMetaObject.connectSlotsByName(Form)
        self.tableWidget.doubleClicked.connect(self.double_click)
        print("hii")

    def double_click(self, it):
        #for item in self.tableWidget.selectedItems() :
        #    item.text()
        global model_choice
        conf_thres = 0.25
        #print(self.tableWidget.item(self.tableWidget.currentRow(), 0).text())
        '''
        if model_choice == "model\\Weapon\\gun-model.pt":
            conf_thres = 0.25
        else:
            conf_thres = 0.6
        '''
        CameraCode = self.tableWidget.item(self.tableWidget.currentRow(), 0).text()
        query = {
        "cameraCode": CameraCode,
        "mediaURLParam": {
        "serviceType": 1,
        "streamType": 1,
        "clientType": 1,
        "protocolType": 2
        }
        }

        response = session.post('https://186.1.16.32:18531/video/rtspurl/v1.0', json = query, verify=False)
        if response.json()['resultCode'] == 0:
            print("Stream begun")
        else:
            print("Stream failed")
        source = response.json()['rtspURL']
        print(response.content)
        #source = "rtsp://186.1.16.32:1161/02010533755583570101?DstCode=01&ServiceType=1&ClientType=1&StreamID=2&SrcTP=2&DstTP=2&SrcPP=1&DstPP=1&MediaTransMode=0&BroadcastType=0&SV=1&Token=RJqeYTkxhBcHPj52gah5GJyZv0URtqKZcs+Tuk4RosI=&DomainCode=da30d0eb264e47968184273537e16acf&UserId=12&"
        
        run(weights= model_choice, source = source,conf_thres=conf_thres)
        gc.collect()
        torch.cuda.empty_cache()
        self.tableWidget.clearSelection()
        
        
    def click1(self, item):
        
        print("You clicked on {0}x{1}".format(item.column(), item.row()), item.text())
    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        #self.label.setText(_translate("Form", " Name of Camera"))
        #self.pushButton.setText(_translate("Form", "Camera"))
        item = self.tableWidget.horizontalHeaderItem(0)
        item.setText(_translate("Form", "code"))
        item = self.tableWidget.horizontalHeaderItem(1)
        item.setText(_translate("Form", "Name"))
        item = self.tableWidget.horizontalHeaderItem(2)
        item.setText(_translate("Form", "Device Group Code"))
        item = self.tableWidget.horizontalHeaderItem(3)
        item.setText(_translate("Form", "Parent Code"))
        item = self.tableWidget.horizontalHeaderItem(4)
        item.setText(_translate("Form", "Domain Code"))
        item = self.tableWidget.horizontalHeaderItem(5)
        item.setText(_translate("Form", "Device model type"))
        item = self.tableWidget.horizontalHeaderItem(6)
        item.setText(_translate("Form", "vendor type"))
        item = self.tableWidget.horizontalHeaderItem(7)
        item.setText(_translate("Form", "Device form type"))
        item = self.tableWidget.horizontalHeaderItem(8)
        item.setText(_translate("Form", "Type"))
        item = self.tableWidget.horizontalHeaderItem(9)
        item.setText(_translate("Form", "Camera location"))
        item = self.tableWidget.horizontalHeaderItem(10)
        item.setText(_translate("Form", "Camera status"))
        item = self.tableWidget.horizontalHeaderItem(11)
        item.setText(_translate("Form", "Status"))
        item = self.tableWidget.horizontalHeaderItem(12)
        item.setText(_translate("Form", "Net type"))
        item = self.tableWidget.horizontalHeaderItem(13)
        item.setText(_translate("Form", "Support Intelligent"))
        item = self.tableWidget.horizontalHeaderItem(14)
        item.setText(_translate("Form", "Enable voide"))
        item = self.tableWidget.horizontalHeaderItem(15)
        item.setText(_translate("Form", "nvr Code"))
        item = self.tableWidget.horizontalHeaderItem(16)
        item.setText(_translate("Form", "Device create time"))
        item = self.tableWidget.horizontalHeaderItem(17)
        item.setText(_translate("Form", "Ex Domain "))
        item = self.tableWidget.horizontalHeaderItem(18)
        item.setText(_translate("Form", "Device IP"))
        item = self.tableWidget.horizontalHeaderItem(19)
        item.setText(_translate("Form", "reserve"))
        print("hi2")
    def load_data(self,dict):
        col = 0
        row = 0
        self.tableWidget.setRowCount(len(dict))
        for i in range(len(dict)) :
            col = 0
            for j in dict[i] :
                self.tableWidget.setItem(row,col,QtWidgets.QTableWidgetItem(str(dict[i][j])))
                col+=1

            row+=1

#if _name_ == "_main_":
#    app = QtWidgets.QApplication(sys.argv)
    

    
   
    #sys.exit(app.exec_())
    
class AnotherWindow(QFrame):
    def __init__(self):
        print(model_choice)
        super().__init__()
        self.Form = None
        self.w = None
        self.ui = None
        win = uic.loadUi("untitled4.ui",self)
        self.pushButton.clicked.connect(self.open_file)
        self.pushButton_2.clicked.connect(self.show_new_window2)
        self.pushButton_3.clicked.connect(self.back)
        self.pushButton_4.clicked.connect(self.close)
        self.opacity_effect = QGraphicsOpacityEffect()
        self.opacity_effect.setOpacity(0.1)
        self.graphicsView.setGraphicsEffect(self.opacity_effect)
        
        self.opacity_effect2 = QGraphicsOpacityEffect()
        self.opacity_effect2.setOpacity(0.1)
        self.graphicsView_3.setGraphicsEffect(self.opacity_effect2)
    def open_file(self):
        '''
        path = QFileDialog.getOpenFileName(self, 'Open a file', '',
                                        'All Files (*.*)')
        if path != ('', ''):
            print(path[0])
        '''
        options = QFileDialog.Options()
        #options.setStyleSheet("color:white;background:black")
        #options |= QFileDialog.DontUseNativeDialog
        files, _ = QFileDialog.getOpenFileNames(self,"QFileDialog.getOpenFileNames()", "","All Files (*);;Python Files (*.py)", options=options)
        print(files)
        if len(files) > 0:
            path = run(weights= model_choice, source = files[0])
            path = str(path)
            file = str(files[0])
            print(path+"\\"+os.path.basename(file))
            print(path+"\\"+os.path.basename(file))
            print("hi1")
            try:
                 im=Image.open(os.path.basename(path+"\\"+file))
                 im.close()
                 print("hi2")
                 # Load an color image in grayscale
                 img = cv2.imread(path+"\\"+os.path.basename(file))
                 print("hi3")
                 # show image

                 cv2.imshow('image',img)
                 print("hi4")
                 cv2.waitKey(0)
                 print("hi5")
                 cv2.destroyAllWindows()
            except IOError:
                # filename not an image file
                cap = cv2.VideoCapture(path+"\\"+os.path.basename(file))
                print("hi6")
                cap.set(cv2.CAP_PROP_FPS, 30)
        
                while(cap.isOpened()):
                    print("hi7")
                    #if(not cap.isOpened()):
                    #    continue
                    #print("hi7")
                    ret, frame = cap.read()
                    if not ret:
                        break
                    print("hi8")
                    #print(frame)
                    if(frame is None):
                        continue
                    print("hi9")
                   
                    print("hi10")
                    #width = 800
                    #height = 600
                    #dim = (width, height)
                    #img = cv2.resize(frame, dim, interpolation = cv2.INTER_AREA)
                    cv2.imshow('frame', frame)
                    print("hi11")
                    if cv2.waitKey(20) & 0xFF == ord('q'):
                        break
                    print("hi12")
                    if (path+"\\"+os.path.basename(file)).endswith("jpg"):
                        break
                    print("hi13")
                cv2.waitKey(0)
                print("hi14")
                cap.release()
                print("hi15")
                cv2.destroyAllWindows()
                gc.collect()
                torch.cuda.empty_cache()
        
    def show_info_messagebox(self):
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Information)
      
        # setting message for Message Box
        msg.setText("Data was processed successfully")
          
        # setting Message box window title
        msg.setWindowTitle("Information ")
          
        # declaring buttons on Message Box
        msg.setStandardButtons(QMessageBox.Ok)
          
        # start the app
        retval = msg.exec_()        
    def show_new_window2(self, checked):
        
        query = {"deviceType":2,"fromIndex":1,"toIndex":1000}
        response = session.get('https://186.1.16.32:18531/device/deviceList/v1.0', params = query, verify=False)
        if response.json()['resultCode'] == 0:
            print("camera list sucess")
        else:
            print("camera list failed")
        dict = {}
        dict = response.json()['cameraBriefInfos']['cameraBriefInfoList']['cameraBriefInfo']
        
        #dict = [{'code': '02010533750398980101#da30d0eb264e47968184273537e16acf', 'name': 'تقاطع شارع احمد فؤاد مع مصطفى محمود', 'deviceGroupCode': '6#da30d0eb264e47968184273537e16acf', 'parentCode': '02010533750398980000', 'domainCode': 'da30d0eb264e47968184273537e16acf', 'deviceModelType': 'M2141-EVL(2.8-12mm)', 'vendorType': 'HUAWEI', 'deviceFormType': 1, 'type': 0, 'cameraLocation': '', 'cameraStatus': 1, 'status': 0, 'netType': 0, 'isSupportIntelligent': 1, 'enableVoice': 0, 'nvrCode': '6c72ce6c5fde481d9da1718b34aebeb0', 'deviceCreateTime': '20220201173701', 'isExDomain': 0, 'deviceIP': '186.1.1.120', 'reserve': None}, {'code': '02010533750560480101#da30d0eb264e47968184273537e16acf', 'name': '186.1.11.9', 'deviceGroupCode': '5#da30d0eb264e47968184273537e16acf', 'parentCode': '02010533750560480000', 'domainCode': 'da30d0eb264e47968184273537e16acf', 'deviceModelType': 'IPC6325-WD-VR', 'vendorType': 'HUAWEI', 'deviceFormType': 1, 'type': 0, 'cameraLocation': '', 'cameraStatus': 1, 'status': 1, 'netType': 0, 'isSupportIntelligent': 1, 'enableVoice': 0, 'nvrCode': '6c72ce6c5fde481d9da1718b34aebeb0', 'deviceCreateTime': '20220206102213', 'isExDomain': 0, 'deviceIP': '186.1.11.9', 'reserve': None}, {'code': '02010533751775080101#da30d0eb264e47968184273537e16acf', 'name': '186.1.1.144', 'deviceGroupCode': '5#da30d0eb264e47968184273537e16acf', 'parentCode': '02010533751775080000', 'domainCode': 'da30d0eb264e47968184273537e16acf', 'deviceModelType': 'X2391-20-T', 'vendorType': 'HUAWEI', 'deviceFormType': 1, 'type': 0, 'cameraLocation': '', 'cameraStatus': 1, 'status': 1, 'netType': 0, 'isSupportIntelligent': 1, 'enableVoice': 0, 'nvrCode': '6c72ce6c5fde481d9da1718b34aebeb0', 'deviceCreateTime': '20220201173116', 'isExDomain': 0, 'deviceIP': '186.1.1.144', 'reserve': None}]
        if self.Form is None:
            self.Form = QtWidgets.QWidget()
            self.ui  = Ui_Form(self.Form,dict)
        self.Form.show()    
        
        #Form.show()
    def back(self, checked):
        if self.w is None:
            self.w = Appdemo()
        self.w.showFullScreen()
        self.close()
   # def close(self):
    #    self.close()
class Appdemo(QMainWindow) : 
    def __init__(self) : 
        self.w = None
        super().__init__()   
        win = uic.loadUi("untitled3.ui",self)
        #self.setCentralWidget(self.form_widget)
        #self.resize(200, 400)
        self.pushButton.clicked.connect(self.show_new_window)
        self.pushButton_2.clicked.connect(self.show_new_window2)
        self.pushButton_4.clicked.connect(self.close)
        x = "C:\\Users\\Suhail\\Downloads\\Untitled Folder 3\\kBPPK.gif"
        y = "F:\\New folder (3)\\AjarJaggedClumber.gif"
        z = "AjarJaggedClumber (4) (1).gif"
        '''
        self.movie = QMovie(z)
        
        self.movie.frameChanged.connect(self.repaint)
        self.movie.start()
        '''
        self.opacity_effect = QGraphicsOpacityEffect()
        self.opacity_effect.setOpacity(0.1)
        self.graphicsView.setGraphicsEffect(self.opacity_effect)
        
        self.opacity_effect2 = QGraphicsOpacityEffect()
        self.opacity_effect2.setOpacity(0.1)
        self.graphicsView_3.setGraphicsEffect(self.opacity_effect2)
        self.showFullScreen()
    def show_new_window(self, checked):
        global model_choice
        model_choice = "model\\UAV\\best.pt"
        #print("mohsen", model_choice)
        #model_choice = 1
        if self.w is None:
            self.w = AnotherWindow()
        self.w.showFullScreen()
        
        self.close()
    def show_new_window2(self, checked):
        global model_choice
        model_choice = "model\\Weapon\\best.pt"
        #model_choice = 2
        if self.w is None:
            self.w = AnotherWindow()
        self.w.showFullScreen()
        
        self.close()
   # def close(self):
    #    self.close()
    '''
    def paintEvent(self, event):
        currentFrame = self.movie.currentPixmap()
        frameRect = currentFrame.rect()
        frameRect.moveCenter(self.rect().center())
        if frameRect.intersects(event.rect()):
            painter = QPainter(self)
            painter.drawPixmap(frameRect.left(), frameRect.top(), currentFrame)
'''

'''

if __name__ == '__main__' :
    app = QApplication(sys.argv) 
    demo = Appdemo()
    #demo.show()
    try : 
        sys.exit(app.exec_())
    except SystemExit : 
        print("Closing Window")
        '''
        
'''
app = QtWidgets.QApplication(sys.argv)
window = Appdemo()
sys.exit(app.exec_())

'''

app = QtWidgets.QApplication(sys.argv)
window = Appdemo()
#Form.show()
sys.exit(app.exec_())
