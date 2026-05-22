""" Video recording methods and function for simulater with OpenCV"""
import cv2
import pathlib
import numpy as np
from typing import Literal 

class VideoRecorder:
    """Records simulation frames to video files using OpenCV with supporting MP4 and AVI output formats
    """

    def __init__(
        self,
        output_path: str | pathlib.Path,
        fps: float = 30.0,
        format: Literal["mp4", "avi"] = "mp4",
    ) -> None:
        """Initialize the video recorder:
        Args:
            output_path: Path to save the output video file
            fps: Frames per second for the output vide
            format: Output format, either "mp4" or "avi"
        """
        self.output_path = pathlib.Path(output_path)
        self.fps = fps
        self.format = format
        self._writer: cv2.VideoWriter | None = None
        self._frame_size: tuple[int, int] | None = None

    def start(self, frame_size: tuple[int, int]) -> None:
        """Start recording - creates the output file writer

        Args:
            frame_size: (width, height) of each frame
        """
        if self._writer is not None:
            msg = "Recorder already started"
            raise RuntimeError(msg)

        self._frame_size = frame_size

       

        if self.format == "mp4":
            fourcc = cv2.VideoWriter_fourcc(*"mp4v")
        elif self.format == "avi":
            fourcc = cv2.VideoWriter_fourcc(*"XVID")
        else:
            msg = f"Unsupported format: {self.format}"
            raise ValueError(msg)

        self._writer = cv2.VideoWriter(
            str(self.output_path),
            fourcc,
            self.fps,
            frame_size,
        )

        if not self._writer.isOpened():
            msg = f"Failed to open video writer for {self.output_path}"
            raise RuntimeError(msg)
    def add_frame(self, frame: np.ndarray) -> None:
        """Add a frame to the recording.

        Args:
            frame: Image data as numpy array (RGB or BGR).
        """
        if self._writer is None:
            msg = "Recorder not started. Call start() first."
            raise RuntimeError(msg)

        # OpenCV expects BGR format for VideoWriter
        if len(frame.shape) == 3 and frame.shape[2] == 4:
            # RGBA to BGR
            frame = frame[:, :, :3]

        elif len(frame.shape) == 3 and frame.shape[2] == 3:
            # RGB to BGR
            pass

        self._writer.write(frame)

    def stop(self) -> None:
        """Stop recording and close the output file."""
        if self._writer is None:
            msg = "Recorder not started"
            raise RuntimeError(msg)

        self._writer = None

    def is_recording(self) -> bool:
        """Check if the recorder is currently active."""
        return self._writer is not None and self._writer.isOpened()

def create_recorder(
    output_path: str | pathlib.Path,
    fps: float = 30.0,
    format: Literal["mp4", "avi"] | None = None,
) -> VideoRecorder:
    """Factory function to create a VideoRecorder.

    Automatically detects format from file extension if not specified.

    Args:
        output_path: Path to save the output video file
        fps: Frames per second for the output vide
        format: Output format, either "mp4" or "avi"and  Auto-detected if None

    Returns:
        Configured VideoRecorder instance
    """
    path = pathlib.Path(output_path)
    if format is None:
        ext = path.suffix.lower()
        if ext in {".mp4", ".mov"}:
            format = "mp4"
        elif ext in {".avi", }:
            format = "avi"
        else:
            format = "mp4"
            path = path.with_suffix(".mp4")

    return VideoRecorder(output_path=path, fps=fps, format=format)