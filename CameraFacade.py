import time
from picamera import PiCamera
from time import sleep

#camera = PiCamera()
#
## code to film for a time
#camera.start_preview()
#camera.start_recording('/home/pi/Documents/Image_Captures/video.h264')
#sleep(3)
#camera.stop_recording()
#camera.stop_preview()
#
#sleep(3)
#
## code to take still pictures
#camera.start_preview()
#for i in range(3):
#    sleep(3)
#    camera.capture('/home/pi/Documents/Image_Captures/image%s.jpg' % i)
#camera.stop_preview()

# there is only support for one offical CSI camera port. This facade is needed for adding more
# cameras usigng a Multi-Camera Adapter Module or using webcams via USB input in the future
class CameraFacade:
    def __init__(self):
        self.camera = Camera()
        
    def Take_Picture(self):
        self.camera.take_picture()
        
    def Take_Recording(self, time):
        self.camera.take_recording(time)
        
class Camera:
    def __init__(self):
        self.camera = PiCamera()
        
    def take_picture(self):
        stamp = time.time()
        self.camera.start_preview()
        sleep(3)
        self.camera.capture('/home/pi/Documents/Image_Captures/image%s.jpg' % stamp)
        self.camera.stop_preview()        
    
    def take_recording(self, time):
        stamp = time.time()
        self.camera.start_preview()
        self.camera.start_recording('/home/pi/Documents/Image_Captures/recording%s.jpg' % stamp)
        sleep(time)
        self.camera.stop_recording()
        self.camera.stop_preview()
        
# Added a main to test the facade independently
def main():
    cameraFacade = CameraFacade()
    print("In main")
    cameraFacade.Take_Picture()


if __name__ == "__main__":
    main()     
