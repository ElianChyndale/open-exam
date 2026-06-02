# OpenExam workflows package
# Re-exports all public symbols from core.py for backward compatibility.
# Subsystem modules will be extracted from core.py in subsequent iterations.

from app.workflows.core import *

# Private symbols needed by tests
from app.workflows.core import _as_source_refs as _as_source_refs

# Todo is event sourced. Import it after the compatibility module so the CLI
# keeps its public write_todo entry point while using the V2 reducer.
from app.workflows.todo import *
