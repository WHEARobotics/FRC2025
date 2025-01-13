from typing import Optional, List

import commands2
import ntcore
import wpilib
import limelight
import limelightresults
from pycparser.c_ast import Union

from util.ntloggerutility import NTLoggerUtility

# See https://docs.limelightvision.io/docs/docs-limelight/apis/limelightlib-python#websocket-based
class VisionSubsystem(commands2.Subsystem):
    def __init__(self):
        super().__init__()  # Call the Subsystem class's (the "super" part) init.

        # ---------------------------------------------------------------------
        # Set up the logging facility for this subsystem. This uses the
        # NetworkTables logger utility class that we created.
        # ---------------------------------------------------------------------
        self.logger = NTLoggerUtility("VisionSubsystem")

        discovered_limelights = limelight.discover_limelights(debug=True)
        if len(discovered_limelights) == 0:
            self.logger.log("ERROR", "Status", "No Limelights found!")
            self.limelight = None
            self.limelight_result = None
            self.result_timestamp = None
        else:
            self.logger.log("INFO", "Status", "Found Limelight!")
            limelight_address = limelight.Limelight(discovered_limelights[0])
            self.limelight = limelight.Limelight(limelight_address)
            self.logger.log("INFO", "Status", f"Using Limelight at {limelight_address}")
            status = self.limelight.get_status()
            self.logger.log("INFO", "Limelight Status", status)
            self.limelight.enable_websocket()
            self.limelight_result = None
            self.result_timestamp = None

    def periodic(self) -> None:
        self._limelightPeriodic()

    def getBotPose(self) -> Optional[List[float]]:
        if self.limelight_result is not None:
            return self.limelight_result.botpose
        else:
            return None

    def diagnose(self) -> str:
        found_limelight = "Limelight found!" if self.limelight is not None else "No Limelight found!"
        getting_status = "Getting results..." if self.limelight is not None and self.limelight_result is not None else "No results available."
        time_status = f"Last result at {self.result_timestamp}" if self.result_timestamp is not None else ""
        return f"{found_limelight} {getting_status} {time_status}"

    def logPeriodic(self):
        self.logger.log("DEBUG", "BotPose", str(self.getBotPose()))
        self.logger.log("DEBUG", "Result_timestamp", self.result_timestamp)

    def _limelightPeriodic(self) -> Optional[limelightresults.GeneralResult]:
        if self.limelight is None:
            return None

        # Several results available. See https://docs.limelightvision.io/docs/docs-limelight/apis/limelightlib-python#websocket-based
        generalResult = self.limelight.get_results()
        if generalResult is None:
            return None

        self.limelight_result = generalResult
        self.result_timestamp = generalResult.timestamp

class GeneralResult:
    def __init__(self, results):
        self.barcode = results.get("Barcode", [])
        self.classifierResults = [ClassifierResult(item) for item in results.get("Classifier", [])]
        self.detectorResults = [DetectorResult(item) for item in results.get("Detector", [])]
        self.fiducialResults = [FiducialResult(item) for item in results.get("Fiducial", [])]
        self.retroResults = [RetroreflectiveResult(item) for item in results.get("Retro", [])]
        self.botpose = results.get("botpose", [])
        self.botpose_wpiblue = results.get("botpose_wpiblue", [])
        self.botpose_wpired = results.get("botpose_wpired", [])
        self.capture_latency = results.get("cl", 0)
        self.pipeline_id = results.get("pID", 0)
        self.robot_pose_target_space = results.get("t6c_rs", [])
        self.targeting_latency = results.get("tl", 0)
        self.timestamp = results.get("ts", 0)
        self.validity = results.get("v", 0)
        self.parse_latency = 0.0

# Not used in 2025, but kept for reference
class RetroreflectiveResult:
    def __init__(self, retro_data):
        self.points = retro_data["pts"]
        self.camera_pose_target_space = retro_data["t6c_ts"]
        self.robot_pose_field_space = retro_data["t6r_fs"]
        self.robot_pose_target_space = retro_data["t6r_ts"]
        self.target_pose_camera_space = retro_data["t6t_cs"]
        self.target_pose_robot_space = retro_data["t6t_rs"]
        self.target_area = retro_data["ta"]
        self.target_x_degrees = retro_data["tx"]
        self.target_x_pixels = retro_data["txp"]
        self.target_y_degrees = retro_data["ty"]
        self.target_y_pixels = retro_data["typ"]

class FiducialResult:
    def __init__(self, fiducial_data):
        self.fiducial_id = fiducial_data["fID"]
        self.family = fiducial_data["fam"]
        self.points = fiducial_data["pts"]
        self.skew = fiducial_data["skew"]
        self.camera_pose_target_space = fiducial_data["t6c_ts"]
        self.robot_pose_field_space = fiducial_data["t6r_fs"]
        self.robot_pose_target_space = fiducial_data["t6r_ts"]
        self.target_pose_camera_space = fiducial_data["t6t_cs"]
        self.target_pose_robot_space = fiducial_data["t6t_rs"]
        self.target_area = fiducial_data["ta"]
        self.target_x_degrees = fiducial_data["tx"]
        self.target_x_pixels = fiducial_data["txp"]
        self.target_y_degrees = fiducial_data["ty"]
        self.target_y_pixels = fiducial_data["typ"]

class DetectorResult:
    def __init__(self, detector_data):
        self.class_name = detector_data["class"]
        self.class_id = detector_data["classID"]
        self.confidence = detector_data["conf"]
        self.points = detector_data["pts"]
        self.target_area = detector_data["ta"]
        self.target_x_degrees = detector_data["tx"]
        self.target_x_pixels = detector_data["txp"]
        self.target_y_degrees = detector_data["ty"]
        self.target_y_pixels = detector_data["typ"]

class ClassifierResult:
    def __init__(self, classifier_data):
        self.class_name = classifier_data["class"]
        self.class_id = classifier_data["classID"]
        self.confidence = classifier_data["conf"]