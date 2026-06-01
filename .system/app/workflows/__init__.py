# OpenExam workflows package
# Re-exports all public symbols from core.py for backward compatibility.
# Subsystem modules will be extracted from core.py in subsequent iterations.

from app.workflows.core import *

# Private symbols needed by tests
from app.workflows.core import _as_source_refs
