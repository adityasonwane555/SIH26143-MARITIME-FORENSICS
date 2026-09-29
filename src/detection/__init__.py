"""Detection package."""
from src.detection.threshold import BaseSpillDetector, AdaptiveThresholdDetector
from src.detection.lookalike import LookalikeDetector

__all__ = ["BaseSpillDetector", "AdaptiveThresholdDetector", "LookalikeDetector"]
