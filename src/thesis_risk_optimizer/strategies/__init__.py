"""Discipline-specific rewrite strategies.

Provides a registry of all available strategies and a factory function
to get the right strategy for a given discipline.
"""

from .base import BaseStrategy, UniversalStrategy
from .computer import ComputerStrategy
from .management import ManagementStrategy
from .human_resource import HumanResourceStrategy
from .education import EducationStrategy
from .literature import LiteratureStrategy
from .law import LawStrategy
from .medicine import MedicineStrategy
from .universal import UniversalStrategy as UniversalFallback
from .contract import StrategyContract

# -- Strategy registry -------------------------------------------------------
STRATEGY_REGISTRY: dict[str, BaseStrategy] = {
    "computer": ComputerStrategy(),
    "human_resource": HumanResourceStrategy(),
    "management": ManagementStrategy(),
    "education": EducationStrategy(),
    "literature": LiteratureStrategy(),
    "law": LawStrategy(),
    "medicine": MedicineStrategy(),
    "universal": UniversalStrategy(),
}


def get_strategy(discipline: str) -> BaseStrategy:
    """Get the strategy instance for a discipline name.

    Args:
        discipline: One of 'computer', 'human_resource', 'management',
                    'education', 'literature', 'law', 'medicine', 'universal'.

    Returns:
        BaseStrategy instance, falling back to UniversalStrategy.
    """
    return STRATEGY_REGISTRY.get(discipline, STRATEGY_REGISTRY["universal"])


def list_strategies() -> list[dict]:
    """List all available strategies with their labels."""
    return [
        {"name": s.name, "label": s.label}
        for s in STRATEGY_REGISTRY.values()
    ]


# -- Discipline-to-strategy mapping ------------------------------------------
DISCIPLINE_STRATEGY_MAP: dict[str, str] = {
    "computer": "computer",
    "human_resource": "human_resource",
    "management": "management",
    "education": "education",
    "literature": "literature",
    "law": "law",
    "medicine": "medicine",
    "universal": "universal",
}


def get_strategy_name_for_discipline(discipline: str) -> str:
    """Get the strategy name for a given discipline."""
    return DISCIPLINE_STRATEGY_MAP.get(discipline, "universal")
