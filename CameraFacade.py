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
        image_count = 0
        
    def take_picture(self):
        image_count += 1
        camera.start_preview()
        sleep(3)
        camera.capture('/home/pi/Documents/Image_Captures/image%s.jpg' % image_count)
        camera.stop_preview()        
    
    def take_recording(self, time):
        camera.start_preview()
        camera.start_recording()
        sleep(time)
        camera.stop_recording()
        camera.stop_preview()
# Added a main to test the facade independently
def main():
    cameraFacade = CameraFacade()
    print("In main")
    cameraFacade.Take_Picture()


if __name__ == "__main__":
    main()     