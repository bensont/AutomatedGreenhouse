import time
from picamera import PiCamera
from time import sleep


# there is only support for one offical CSI camera port. This facade is needed for adding more
# cameras usigng a Multi-Camera Adapter Module or using webcams via USB input in the future
class CameraFacade:
    # initialize needed values for communication
    def __init__(self):
        self.camera = Camera()

    # Take a picture
    def Take_Picture(self):
        self.camera.take_picture()

    # Take a recording
    def Take_Recording(self, time):
        self.camera.take_recording(time)

# Camera class. Currently only handling the Raspberry Pi camera port
class Camera:
    # initialize needed values for communication
    def __init__(self):
        self.camera = PiCamera()

    # Take a single picture. Store it locally for timelapse with a timestamp in
    # the file name. Store in static folder for photo shown on webapp
    def take_picture(self):
        stamp = time.time()
        self.camera.start_preview()
        sleep(3)
        self.camera.capture('/home/pi/Desktop/CSCI_4448/AutomatedGreenhouse/Images/image%s.jpg' % stamp)
        self.camera.capture('/home/pi/Desktop/CSCI_4448/AutomatedGreenhouse/static/photo/plant.jpg')
        self.camera.stop_preview()

    # Take a single recording for a given time. Store it locally for timelapse.
    def take_recording(self, time):
        stamp = time.time()
        self.camera.start_preview()
        self.camera.start_recording('/home/pi/Desktop/CSCI_4448/AutomatedGreenhouse/Images/recording%s.jpg' % stamp)
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
