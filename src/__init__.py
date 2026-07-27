"""Social Media Engine - Autonomous social media campaign system."""

__version__ = "0.1.0"
__author__ = "Claude Code"
__description__ = "Data-driven social media campaign system with approval workflow"

from .status_calculator import StatusCalculator
from .data_importer import DataImporter
from .content_generator import ContentGenerator
from .approval_workflow import ApprovalWorkflow
from .scheduler import Scheduler
from .performance_tracker import PerformanceTracker

__all__ = [
    "StatusCalculator",
    "DataImporter",
    "ContentGenerator",
    "ApprovalWorkflow",
    "Scheduler",
    "PerformanceTracker",
]
