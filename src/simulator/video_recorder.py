""" Video recording methods and function for simulater with OpenCV"""
import cv2
import pathlib
import numpy as np
import Literal from typing
class VideoRecorder:
     """Records simulation frames to video files using OpenCV.
    Supports MP4 and AVI output formats.
    """
     def __init__(
        self,
        output_path: str |pathlib.Path,
        fps: float =30.0,
        format: Literal["mp4", "avi"] = "mp4",
                  
                  )->None:
          pass