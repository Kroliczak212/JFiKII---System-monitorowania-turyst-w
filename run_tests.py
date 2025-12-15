"""
Automated Test Runner for Threat Rules
=======================================

Runs comprehensive tests from test_signals_comprehensive.txt
and validates the results against expected values.

Usage:
    python run_tests.py
"""

from pathlib import Path
from src.parser.rule_parser import parse_rules_file
from src.evaluator.threat_matcher import ThreatMatcher
from src.evaluator.signal import parse_signal


def run_comprehensive_tests():
    """Run all tests from test_signals_comprehensive.txt"""

    # Load rules
    print("="  * 80)
    print("AUTOMATED TEST SUITE - Mountain Monitor Threat Rules")
    print("=" * 80)
    print()

    rules_path = Path("data/rules.txt")
    if not rules_path.exists():
        print(f"[FAIL] Rules file not found: {rules_path}")
        return

    print(f"Loading rules from: {rules_path}")
    rules_db = parse_rules_file(rules_path)
    matcher = ThreatMatcher(rules_db)
    print(f"[OK] Loaded {len(rules_db.blocks)} threat blocks")
    print()

    # Load test cases
    test_file = Path("test_signals_comprehensive.txt")
    if not test_file.exists():
        print(f"[FAIL] Test file not found: {test_file}")
        return

    print(f"Loading test cases from: {test_file}")
    print()

    # Parse test cases
    test_cases = []
    with open(test_file, 'r', encoding='utf-8') as f:
        for line_no, line in enumerate(f, 1):
            line = line.strip()

            # Skip comments and empty lines
            if not line or line.startswith('#'):
                continue

            # Parse: signal,expected,description
            parts = line.split(',', 7)  # Split max 8 parts
            if len(parts) < 7:
                continue

            signal_str = ','.join(parts[:6])  # w,f,t,r,a,d
            expected = parts[6]
            description = parts[7] if len(parts) > 7 else ""

            test_cases.append({
                'line': line_no,
                'signal': signal_str,
                'expected': expected,
                'description': description
            })

    print(f"[OK] Loaded {len(test_cases)} test cases")
    print()
    print("="  * 80)
    print("RUNNING TESTS")
    print("=" * 80)
    print()

    # Run tests
    passed = 0
    failed = 0
    errors = []

    current_level = None

    for test in test_cases:
        signal_str = test['signal']
        expected = test['expected']
        description = test['description']

        # Print section headers
        if expected != current_level:
            current_level = expected
            print()
            print(f"--- Testing {current_level} cases ---")
            print()

        try:
            # Parse signal
            signal = parse_signal(signal_str)

            # Evaluate
            assessment = matcher.assess_threat(signal)
            actual = assessment.threat_level.value

            # Check result (BEFORE printing)
            if actual == expected:
                passed += 1
                status = "[OK] PASS"
            else:
                failed += 1
                status = f"[FAIL] FAIL (got {actual})"
                errors.append({
                    'line': test['line'],
                    'signal': signal_str,
                    'expected': expected,
                    'actual': actual,
                    'description': description
                })

            # Print result (encoding errors won't affect test counts)
            try:
                print(f"{status} | {signal_str} => {expected} | {description}")
            except UnicodeEncodeError:
                # Fallback for encoding issues
                print(f"{status} | {signal_str} => {expected} | [description omitted]")

        except Exception as e:
            # Only count as failure if evaluation itself failed
            failed += 1
            status = f"[FAIL] ERROR: {e}"
            errors.append({
                'line': test['line'],
                'signal': signal_str,
                'expected': expected,
                'actual': 'ERROR',
                'error': str(e),
                'description': description
            })
            try:
                print(f"{status} | {signal_str} | {description}")
            except UnicodeEncodeError:
                print(f"{status} | {signal_str} | [description omitted]")

    # Print summary
    print()
    print("=" * 80)
    print("TEST SUMMARY")
    print("=" * 80)
    print()
    print(f"Total tests:  {len(test_cases)}")
    print(f"[OK] Passed:     {passed} ({100 * passed // len(test_cases)}%)")
    print(f"[FAIL] Failed:     {failed} ({100 * failed // len(test_cases)}%)")
    print()

    # Print failures
    if errors:
        print("=" * 80)
        print("FAILED TESTS")
        print("=" * 80)
        print()
        for error in errors:
            print(f"Line {error['line']}: {error['signal']}")
            print(f"  Expected: {error['expected']}")
            print(f"  Actual:   {error['actual']}")
            print(f"  Description: {error['description']}")
            if 'error' in error:
                print(f"  Error: {error['error']}")
            print()

    return passed, failed


if __name__ == "__main__":
    try:
        passed, failed = run_comprehensive_tests()

        # Exit with appropriate code
        if failed > 0:
            exit(1)
        else:
            print(" ALL TESTS PASSED! ")
            exit(0)

    except Exception as e:
        print(f"[FAIL] Fatal error: {e}")
        import traceback
        traceback.print_exc()
        exit(2)
