"""
Silnik ewaluacji logicznej wyrażeń

Publiczne API:
    Signal, parse_signal               - Model sygnału wejściowego
    LogicEvaluator, evaluate_expression - Ewaluator wyrażeń
    ThreatMatcher, assess_threat        - Dopasowanie zagrożeń
    ThreatAssessment                    - Wynik oceny
"""

from .signal import (
    Signal,
    WindSignal,
    FogSignal,
    TemperatureSignal,
    RainSignal,
    AvalancheSignal,
    DifficultySignal,
    parse_signal,
)
from .logic_evaluator import (
    LogicEvaluator,
    evaluate_expression,
    EvaluationError,
)
from .threat_matcher import (
    ThreatMatcher,
    ThreatAssessment,
    assess_threat,
)

__all__ = [
    # Signal
    'Signal',
    'WindSignal',
    'FogSignal',
    'TemperatureSignal',
    'RainSignal',
    'AvalancheSignal',
    'DifficultySignal',
    'parse_signal',
    # Evaluator
    'LogicEvaluator',
    'evaluate_expression',
    'EvaluationError',
    # Matcher
    'ThreatMatcher',
    'ThreatAssessment',
    'assess_threat',
]
