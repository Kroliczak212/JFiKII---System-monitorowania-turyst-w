"""
Evaluator wyrażeń logicznych - silnik SAT-like

Ten moduł implementuje ewaluację formuł logicznych z reguł zagrożeń.
Działa na zasadzie rekurencyjnego przejścia po AST wyrażenia.

Algorytm:
1. Jeśli wyrażenie to atom -> sprawdź wartość w sygnale
2. Jeśli wyrażenie to NOT -> zaneguj wynik pod-wyrażenia
3. Jeśli wyrażenie to OR -> zwróć TRUE jeśli którekolwiek pod-wyrażenie TRUE
4. Jeśli wyrażenie to AND -> zwróć TRUE jeśli wszystkie pod-wyrażenia TRUE
"""

from typing import List, Tuple, Optional

# Import modeli parsera
from src.parser.models import LogicalExpression, LogicalOperator
from .signal import Signal


class EvaluationError(Exception):
    """Błąd podczas ewaluacji wyrażenia"""
    pass


class LogicEvaluator:
    """
    Ewaluator wyrażeń logicznych

    Użycie:
        evaluator = LogicEvaluator()
        signal = Signal(wind=WindSignal.W2, ...)
        expression = ...  # LogicalExpression z parsera
        result = evaluator.evaluate(expression, signal)
    """

    def __init__(self, debug: bool = False):
        """
        Inicjalizacja ewaluatora

        Args:
            debug: Jeśli True, wypisuje kroki ewaluacji
        """
        self.debug = debug
        self.evaluation_steps: List[str] = []

    def evaluate(self, expression: LogicalExpression, signal: Signal) -> bool:
        """
        Ewaluuje wyrażenie logiczne dla danego sygnału

        Args:
            expression: Wyrażenie logiczne do ewaluacji
            signal: Sygnał wejściowy z aktualnymi warunkami

        Returns:
            bool: True jeśli wyrażenie jest spełnione, False w przeciwnym razie

        Przykład:
            expr = LogicalExpression(operator=OR, left="w2", right="w3")
            signal = Signal(wind=WindSignal.W2, ...)
            evaluator.evaluate(expr, signal)  # True
        """
        self.evaluation_steps = []
        result = self._evaluate_recursive(expression, signal, depth=0)

        if self.debug:
            print("Evaluation steps:")
            for step in self.evaluation_steps:
                print(step)
            print(f"Final result: {result}")

        return result

    def _evaluate_recursive(
        self,
        expression: LogicalExpression,
        signal: Signal,
        depth: int = 0
    ) -> bool:
        """
        Rekurencyjna ewaluacja wyrażenia

        Args:
            expression: Wyrażenie do ewaluacji
            signal: Sygnał wejściowy
            depth: Głębokość rekurencji (do debugowania)

        Returns:
            bool: Wynik ewaluacji
        """
        indent = "  " * depth

        # PRZYPADEK 1: ATOM (zmienna lub "others")
        if expression.operator is None:
            atom = str(expression.left)
            result = signal.get_value(atom)

            if self.debug:
                self.evaluation_steps.append(
                    f"{indent}ATOM: {atom} = {result}"
                )

            return result

        # PRZYPADEK 2: NOT (negacja)
        elif expression.operator == LogicalOperator.NOT:
            if self.debug:
                self.evaluation_steps.append(f"{indent}NOT:")

            inner_result = self._evaluate_recursive(expression.left, signal, depth + 1)
            result = not inner_result

            if self.debug:
                self.evaluation_steps.append(
                    f"{indent}NOT result: !{inner_result} = {result}"
                )

            return result

        # PRZYPADEK 3: OR (alternatywa)
        elif expression.operator == LogicalOperator.OR:
            if self.debug:
                self.evaluation_steps.append(f"{indent}OR:")

            left_result = self._evaluate_recursive(expression.left, signal, depth + 1)

            # Short-circuit evaluation dla OR
            # Jeśli left jest TRUE, nie musimy sprawdzać right
            if left_result:
                if self.debug:
                    self.evaluation_steps.append(
                        f"{indent}OR short-circuit: left=TRUE -> TRUE"
                    )
                return True

            right_result = self._evaluate_recursive(expression.right, signal, depth + 1)
            result = left_result or right_result

            if self.debug:
                self.evaluation_steps.append(
                    f"{indent}OR result: {left_result} | {right_result} = {result}"
                )

            return result

        # PRZYPADEK 4: AND (koniunkcja)
        elif expression.operator == LogicalOperator.AND:
            if self.debug:
                self.evaluation_steps.append(f"{indent}AND:")

            left_result = self._evaluate_recursive(expression.left, signal, depth + 1)

            # Short-circuit evaluation dla AND
            # Jeśli left jest FALSE, nie musimy sprawdzać right
            if not left_result:
                if self.debug:
                    self.evaluation_steps.append(
                        f"{indent}AND short-circuit: left=FALSE -> FALSE"
                    )
                return False

            right_result = self._evaluate_recursive(expression.right, signal, depth + 1)
            result = left_result and right_result

            if self.debug:
                self.evaluation_steps.append(
                    f"{indent}AND result: {left_result} & {right_result} = {result}"
                )

            return result

        else:
            raise EvaluationError(f"Unknown operator: {expression.operator}")

    def evaluate_with_trace(
        self,
        expression: LogicalExpression,
        signal: Signal
    ) -> Tuple[bool, List[str]]:
        """
        Ewaluuje wyrażenie i zwraca trace ewaluacji

        Args:
            expression: Wyrażenie do ewaluacji
            signal: Sygnał wejściowy

        Returns:
            Tuple[bool, List[str]]: (wynik, kroki ewaluacji)

        Przykład:
            result, trace = evaluator.evaluate_with_trace(expr, signal)
            for step in trace:
                print(step)
        """
        original_debug = self.debug
        self.debug = True
        result = self.evaluate(expression, signal)
        self.debug = original_debug
        return result, self.evaluation_steps.copy()

    def get_matching_atoms(
        self,
        expression: LogicalExpression,
        signal: Signal
    ) -> List[str]:
        """
        Zwraca listę atomów z wyrażenia, które są TRUE w sygnale

        Args:
            expression: Wyrażenie do sprawdzenia
            signal: Sygnał wejściowy

        Returns:
            List[str]: Lista atomów które są TRUE

        Przykład:
            # Wyrażenie: w2 | w3 | f3
            # Sygnał: wind=w2, fog=f3
            # Wynik: ["w2", "f3"]
        """
        matching_atoms = []
        self._collect_matching_atoms(expression, signal, matching_atoms)
        return matching_atoms

    def _collect_matching_atoms(
        self,
        expression: LogicalExpression,
        signal: Signal,
        result: List[str]
    ):
        """Pomocnicza metoda do zbierania pasujących atomów"""
        if expression.operator is None:
            # To jest atom
            atom = str(expression.left)
            if signal.get_value(atom):
                result.append(atom)
        else:
            # Rekurencyjnie sprawdź pod-wyrażenia
            if isinstance(expression.left, LogicalExpression):
                self._collect_matching_atoms(expression.left, signal, result)
            if expression.right and isinstance(expression.right, LogicalExpression):
                self._collect_matching_atoms(expression.right, signal, result)


# ============================================================================
# Funkcje pomocnicze
# ============================================================================

def evaluate_expression(
    expression: LogicalExpression,
    signal: Signal,
    debug: bool = False
) -> bool:
    """
    Szybka ewaluacja wyrażenia

    Args:
        expression: Wyrażenie do ewaluacji
        signal: Sygnał wejściowy
        debug: Czy wypisywać kroki ewaluacji

    Returns:
        bool: Wynik ewaluacji

    Przykład:
        result = evaluate_expression(expr, signal)
    """
    evaluator = LogicEvaluator(debug=debug)
    return evaluator.evaluate(expression, signal)
