"""
Premium Web Security Scanner - Celery Tasks
"""

from . import scan_tasks
from . import report_tasks

__all__ = [
    "scan_tasks",
    "report_tasks"
]
