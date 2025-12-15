"""
Prezentacja wyników i interfejs CLI

Publiczne API:
    ThreatPresenter         - Formatowanie wyników
    show_assessment         - Szybkie wyświetlenie oceny
    show_multiple_assessments - Wyświetlenie wielu ocen
"""

from .presenter import (
    ThreatPresenter,
    show_assessment,
    show_multiple_assessments,
)

__all__ = [
    'ThreatPresenter',
    'show_assessment',
    'show_multiple_assessments',
]
