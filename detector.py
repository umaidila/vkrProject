import cv2


class Detector:

    path = "none"
    rows = 13
    cols = 18

    def detectDefect(self):

        cap  = cv2.VideoCapture(self.path)
        success,image = cap.read()

        while success:
            info,corners = cv2.findChessboardCornersSB(image,(self.cols,self.rows))
            print(info,corners)
            success,image = cap.read()




        cap.release()
        cv2.destroyAllWindows()

