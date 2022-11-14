#! /usr/bin/env python3
import argparse
import cv2 as cv
import numpy as np
import pyzed.sl as sl

class ZEDM():

    def __init__(self, fps: int=30, 
                        resolution=sl.RESOLUTION.HD1080,
                        brightness: int=-1,
                        contrast: int=-1,
                        hue: int=-1,
                        gamma: int=-1,
                        exposure: int=-1,
                        saturation: int=-1,
                        sharpness: int=-1
                        ):

        self.zed = sl.Camera()

        self.init_params = sl.InitParameters()
        self.init_params.camera_resolution = resolution
        self.init_params.camera_fps = fps
        

        err = self.zed.open(self.init_params)
        if err != sl.ERROR_CODE.SUCCESS:
            print('[ERROR] ZED failed to initialize')
            exit(-1)

        # set camera settings, if no value passed to constructor, then set to default/auto value
        self.zed.set_camera_settings(sl.VIDEO_SETTINGS.BRIGHTNESS, brightness)
        self.zed.set_camera_settings(sl.VIDEO_SETTINGS.CONTRAST, contrast)
        self.zed.set_camera_settings(sl.VIDEO_SETTINGS.HUE, hue)
        self.zed.set_camera_settings(sl.VIDEO_SETTINGS.GAMMA, gamma)
        self.zed.set_camera_settings(sl.VIDEO_SETTINGS.EXPOSURE, exposure)
        self.zed.set_camera_settings(sl.VIDEO_SETTINGS.SATURATION, saturation)
        self.zed.set_camera_settings(sl.VIDEO_SETTINGS.SHARPNESS, sharpness)

    def capture(self):
        # allocate memory for the captured images
        # Mat class simply allocates a matrix container with special memory management properties 
        #   which can hold up to 4 channel images.
        left_img = sl.Mat()
        right_img = sl.Mat()
        depth_view = sl.Mat()

        runtime_parameters = sl.RuntimeParameters()
        if self.zed.grab(runtime_parameters) == sl.ERROR_CODE.SUCCESS:
            self.zed.retrieve_image(left_img, sl.VIEW.LEFT) # rectified left image
            self.zed.retrieve_image(right_img, sl.VIEW.RIGHT) # rectified right image
            self.zed.retrieve_image(depth_view, sl.VIEW.DEPTH) # grayscale depth map

            # get numpy arrays of data so we can use imshow()
            np_left = left_img.get_data()
            np_right = right_img.get_data()
            concat_horizontal = np.concatenate((np_left, np_right), axis=1)

            cv.imshow('left', concat_horizontal)

            cv.waitKey(-1)



if __name__ == '__main__':
    parser = argparse.ArgumentParser(
                                        prog='ZEDMTester',
                                        description='Tool kit for checking out a ZED camera, default mode capturing one image on each image sensor and comparing them. Press any key to close the images.'
                                    )

    parser.add_argument(
                            '-b',
                            '--brightness',
                            action='store',
                            choices=range(1,8),
                            default=-1,
                            dest='brightness',
                            type=int,
                            help='if set, then camera brightness will be set to the specified param'
                        )

    parser.add_argument(
                            '-c',
                            '--contrast',
                            action='store',
                            choices=range(1,8),
                            default=-1,
                            dest='contrast',
                            type=int,
                            help='defines the contrast control'
                        )

    parser.add_argument(
                            '--hue',
                            action='store',
                            choices=range(1,12),
                            default=-1,
                            dest='hue',
                            type=int,
                            help='defines the hue of the image'
                        )
    
    parser.add_argument(
                            '-g',
                            '--gamma',
                            action='store',
                            choices=range(2,10),
                            default=-1,
                            dest='gamma',
                            type=int,
                            help='defines the gamma of the image'
                        )

    parser.add_argument(
                            '-e',
                            '--exposure',
                            action='store',
                            choices=range(1,100),
                            default=-1,
                            dest='exposure',
                            type=int,
                            help='defines the exposure/shutter speed'
                        )

    parser.add_argument(
                            '-sh',
                            '--sharpness',
                            action='store',
                            choices=range(1,8),
                            default=-1,
                            dest='sharpness',
                            type=int,
                            help='defines the digital sharpening amount'
                        )

    parser.add_argument(
                            '-sa',
                            '--saturation',
                            action='store',
                            choices=range(1,8),
                            default=-1,
                            dest='saturation',
                            type=int,
                            help='defines the saturation control'
                        )




    parser.add_argument(
                            '--fps',
                            action='store',
                            choices=[15,30,60,100],
                            default=60,
                            dest='fps',
                            type=int,
                            help='specify the frames per second video capture rate, the higher the frame rate the lower the resolution'
                        )


    args = parser.parse_args()

    zed = ZEDM(
                fps=args.fps,
                brightness=args.brightness,
                contrast=args.contrast,
                hue=args.hue,
                gamma=args.gamma,
                exposure=args.exposure,
                saturation=args.saturation,
                sharpness=args.sharpness
            )

    zed.capture()
