import sys
import time
from statistics import mean

import cv2
import numpy as np


class Detector:
    videoTest = "none"
    videoSource = "none"
    rows = 5
    cols = 5

    def __init__(self):
        self.psnrTriggerValue = 30
        self.delay = 20
        self.fps = 30
        self.numLength = 10
        self.logs = ""
        self.reportMsg = ""

    def getPSNR(self, I1, I2):
        s1 = cv2.absdiff(I1, I2)  # |I1 - I2|
        s1 = np.float32(s1)  # cannot make a square on 8 bits
        s1 = s1 * s1  # |I1 - I2|^2
        sse = s1.sum()  # sum elements per channel
        if sse <= 1e-10:  # sum channels
            return 0  # for small values return zero
        else:
            shape = I1.shape
            mse = 1.0 * sse / (shape[0] * shape[1] * shape[2])
            psnr = 10.0 * np.log10((255 * 255) / mse)
            return psnr

    def getMSSISM(self, i1, i2):
        C1 = 6.5025
        C2 = 58.5225
        # INITS
        I1 = np.float32(i1)  # cannot calculate on one byte large values
        I2 = np.float32(i2)
        I2_2 = I2 * I2  # I2^2
        I1_2 = I1 * I1  # I1^2
        I1_I2 = I1 * I2  # I1 * I2
        # END INITS
        # PRELIMINARY COMPUTING
        mu1 = cv2.GaussianBlur(I1, (11, 11), 1.5)
        mu2 = cv2.GaussianBlur(I2, (11, 11), 1.5)
        mu1_2 = mu1 * mu1
        mu2_2 = mu2 * mu2
        mu1_mu2 = mu1 * mu2
        sigma1_2 = cv2.GaussianBlur(I1_2, (11, 11), 1.5)
        sigma1_2 -= mu1_2
        sigma2_2 = cv2.GaussianBlur(I2_2, (11, 11), 1.5)
        sigma2_2 -= mu2_2
        sigma12 = cv2.GaussianBlur(I1_I2, (11, 11), 1.5)
        sigma12 -= mu1_mu2
        t1 = 2 * mu1_mu2 + C1
        t2 = 2 * sigma12 + C2
        t3 = t1 * t2  # t3 = ((2*mu1_mu2 + C1).*(2*sigma12 + C2))
        t1 = mu1_2 + mu2_2 + C1
        t2 = sigma1_2 + sigma2_2 + C2
        t1 = t1 * t2  # t1 =((mu1_2 + mu2_2 + C1).*(sigma1_2 + sigma2_2 + C2))
        ssim_map = cv2.divide(t3, t1)  # ssim_map =  t3./t1;
        mssim = cv2.mean(ssim_map)  # mssim = average of ssim map
        return mssim

    def checkFrameSequence(self,numPred,numCurr): # 0 - все ок, 1 - пропуск, 2 - повтор
        #print("Проверка",numPred,numCurr)
        if  numPred == numCurr:
            return 2
        if numCurr == 0: # если текущий номер 0, делаем его 10 для цикличности
            numCurr = self.numLength
        if numCurr != numPred + 1:
            return 1
        else:
            return 0


    def newLog(self,msg):
        self.logs+=msg
        print(msg)

    def newReport(self,msg):
        self.reportMsg+=msg

    def detectDefect(self,numType):

        calibrationDelta = 0
        capTest = cv2.VideoCapture(cv2.samples.findFileOrKeep(self.videoTest))
        capSource = cv2.VideoCapture(cv2.samples.findFileOrKeep(self.videoSource))

        framenum = -1

        if not capSource.isOpened():
            print("Could not open the source " + self.videoSource)
            sys.exit(-1)
        if not capTest.isOpened():
            print("Could not open case test " + self.videoTest)
            sys.exit(-1)

        sizeTest = (int(capSource.get(cv2.CAP_PROP_FRAME_WIDTH)), int(capSource.get(cv2.CAP_PROP_FRAME_HEIGHT)))
        sizeSource = (int(capTest.get(cv2.CAP_PROP_FRAME_WIDTH)), int(capTest.get(cv2.CAP_PROP_FRAME_HEIGHT)))

        if sizeTest != sizeSource:
            print("Inputs have different size!!! Closing.")
            sys.exit(-1)

        red_banner = cv2.imread('red_cell.jpg')
        red_banner = cv2.resize(red_banner, sizeSource)

        WIN_UT = "Under Test"
        WIN_RF = "Source"

        # cv2.namedWindow(WIN_RF, cv2.WINDOW_AUTOSIZE)
        # cv2.namedWindow(WIN_UT, cv2.WINDOW_AUTOSIZE)
        # cv2.moveWindow(WIN_RF, 400, 0)  # 750,  2 (bernat =0)
        # cv2.moveWindow(WIN_UT, sizeSource[0], 0)  # 1500, 2

        #print("Reference frame resolution: Width={} Height={} of nr#: {}".format(sizeSource[0], sizeSource[1],
        #                                                                         capSource.get(
        #                                                                             cv2.CAP_PROP_FRAME_COUNT)))
        #print("PSNR trigger value {}".format(self.psnrTriggerValue))

        startFlag = False
        psnrlist = []
        missindex = 0
        outText = ""
        intervalFlag = False
        startFrame = 0
        qrDetector = cv2.QRCodeDetector()
        prev_num = -1

        while True:

            _, frameTest = capTest.read()

            if not startFlag:  # если не начали, пока сравниваем с красным баннером
                frameSource = red_banner
            else:
                _, frameSource = capSource.read()

            if frameTest is None or frameSource is None:
                print(" END! ")
                with open('report.txt','w') as file:
                    file.write(self.reportMsg)
                with open('logs.txt', 'w') as file:
                    file.write(self.logs)
                break

            framenum += 1
            psnrv = self.getPSNR(frameSource, frameTest)
            value = -1
            startAnalyzeFrame = -1

            if numType == 0 and startFlag:
                value, points, straight_qrcode = qrDetector.detectAndDecode(frameTest)
                value = "none" if value == "" else value
                if prev_num == -1:
                    prev_num = value
                else:
                    if prev_num != "none" and value != "none":
                        result = self.checkFrameSequence(int(prev_num),int(value))
                        if result == 1:
                            self.newLog("Пропуск кадров")
                            res1 = time.gmtime(round(framenum / self.fps))
                            timeStamp = time.strftime("%H:%M:%S", res1)
                            self.newReport("Пропуск кадров, кадр: {}, время: {}\n".format(framenum,timeStamp))
                        if result == 2:
                            self.newLog("Повтор кадров")
                            res1 = time.gmtime(round(framenum / self.fps))
                            timeStamp = time.strftime("%H:%M:%S", res1)
                            self.newReport("Повтор кадров, кадр: {}, время: {}\n".format(framenum, timeStamp))
                    prev_num = value


            self.newLog("Кадр: {}# {}dB# номер: {} ".format(framenum, round(psnrv, 3),value))
            #print("Кадр: {}# {}dB# номер: {}".format(framenum, round(psnrv, 3),value), end=" ")

            if startFlag and len(psnrlist) != 15: # до сравнения
                if missindex != 2:
                    missindex += 1 # пропускаем первые пару кадров
                else:
                    psnrlist.append(psnrv) # добавляем в список для калибровки
                if len(psnrlist) == 15:
                    self.psnrTriggerValue = mean(psnrlist)
                    calibrationDelta = round(self.psnrTriggerValue) / 10 # здесь высчитываем порог для дефекта
                    self.newLog("calibration done")
            else:
                if (psnrv < self.psnrTriggerValue-calibrationDelta and psnrv and startFlag):
                    if not intervalFlag:
                        intervalFlag = True
                        startFrame = framenum # здесь дефект начинается
                    self.newLog("Испорчено изображение\n")
                else:
                    if intervalFlag: # здесь дефект закончился
                        intervalFlag = False
                        endFrame = framenum

                        ty_res1 = time.gmtime(round(startFrame/self.fps))
                        startTime = time.strftime("%H:%M:%S",ty_res1)
                        ty_res2 = time.gmtime(round(endFrame/self.fps))
                        endTime = time.strftime("%H:%M:%S",ty_res2)

                        self.newLog("Интервал дефекта: начало - {}, (кадр - {}); конец - {}, (кадр - {})\n".format(startTime,startFrame,endTime,endFrame))
                        self.newReport("Дефект изображения: начало - {}, (кадр - {}); конец - {}, (кадр - {})\n".format(startTime,startFrame,endTime,endFrame))

            if psnrv < 10 and not startFlag:  # значит, красный баннер закончился
                print("starting...")
                for i in range(self.fps * 2 - 1):
                    _, frameSource = capSource.read()
                startFlag = True

            print()
            cv2.imshow(WIN_RF, frameSource)
            cv2.imshow(WIN_UT, frameTest)
            k = cv2.waitKey(self.delay)
            if k == 27:
                break

