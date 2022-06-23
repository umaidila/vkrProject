import sys
import time
from statistics import mean

import cv2
import numpy as np


class Detector:
    videoTest = "none"
    rows = 5
    cols = 5

    def __init__(self):
        self.videoSource = "source.mp4"
        self.psnrTriggerValue = 30
        self.delay = 30
        self.fps = 30

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

    def detectDefect(self):

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

        print("Reference frame resolution: Width={} Height={} of nr#: {}".format(sizeSource[0], sizeSource[1],
                                                                                 capSource.get(
                                                                                     cv2.CAP_PROP_FRAME_COUNT)))
        print("PSNR trigger value {}".format(self.psnrTriggerValue))

        startFlag = False
        psnrlist = []
        missindex = 0
        outText = ""
        intervalFlag = False
        startFrame = 0

        while True:

            _, frameTest = capTest.read()

            if not startFlag:  # если не начали, пока сравниваем с красным баннером
                frameSource = red_banner
            else:
                _, frameSource = capSource.read()

            if frameTest is None or frameSource is None:
                print(" < < <  Game over!  > > > ")
                with open('resurts.txt','w') as file:
                    file.write(outText)
                break

            framenum += 1
            psnrv = self.getPSNR(frameSource, frameTest)

            print("Frame: {}# {}dB".format(framenum, round(psnrv, 3)), end=" ")

            if startFlag and len(psnrlist) != 15:
                if missindex != 2:
                    missindex += 1
                else:
                    psnrlist.append(psnrv)
                if len(psnrlist) == 15:
                    self.psnrTriggerValue = mean(psnrlist)
                    calibrationDelta = round(self.psnrTriggerValue) / 10
                    print("calibration done")
            else:
                if (psnrv < self.psnrTriggerValue-calibrationDelta and psnrv and startFlag):
                    if not intervalFlag:
                        intervalFlag = True
                        startFrame = framenum
                    print("defect detected")
                else:
                    if intervalFlag:
                        intervalFlag = False
                        endFrame = framenum

                        ty_res1 = time.gmtime(round(startFrame/self.fps))
                        startTime = time.strftime("%H:%M:%S",ty_res1)
                        ty_res2 = time.gmtime(round(endFrame/self.fps))
                        endTime = time.strftime("%H:%M:%S",ty_res2)
                        outstr = "Defect interval: start - {}, (frame - {}); end - {}, (frame - {})\n".format(startTime,startFrame,endTime,endFrame)
                        print(outstr)
                        outText += outstr+"\n"

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

