"""
Procesor strumienia sygnałów wejściowych

Publiczne API:
    SignalReader        - Czytanie sygnałów z różnych źródeł
    StreamProcessor     - Przetwarzanie strumienia
    ProcessingResult    - Wynik przetwarzania
"""

from .processor import (
    SignalReader,
    StreamProcessor,
    ProcessingResult,
    process_signals_file,
)

__all__ = [
    'SignalReader',
    'StreamProcessor',
    'ProcessingResult',
    'process_signals_file',
]
