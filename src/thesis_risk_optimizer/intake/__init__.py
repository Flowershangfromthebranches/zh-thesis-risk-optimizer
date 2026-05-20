"""Intake gate: validates user-provided information before optimization."""

from .intake_gate import IntakeGate, IntakeResult
from .required_fields import REQUIRED_FIELDS, MATERIAL_EXAMPLES, MATERIAL_PURPOSE
from .confirmation import PermissionGate, PermissionResult
