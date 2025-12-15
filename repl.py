"""
ThreatRules Interactive REPL (Read-Eval-Print Loop)
====================================================

Interactive shell for testing ThreatRules grammar and evaluation.

Features:
  - Parse rules and see AST structure
  - Evaluate rules against test signals
  - Show parse trees and derivations
  - Test logical expressions

Commands:
  :parse <rule>          - Parse a rule and show AST
  :eval <rule> <signal>  - Evaluate rule against signal
  :test <signal>         - Test signal against loaded rules file
  :load <file>           - Load rules from file
  :help                  - Show help
  :examples              - Show example rules
  :quit                  - Exit REPL

Examples:
  >>> :parse E5 { d4: w2 | w3; }
  >>> :eval "E5 { d4: w3 & f3; }" w3,f3,t1,r1,a1,d4
  >>> :load data/rules.txt
  >>> :test w2,f2,t1,r1,a1,d3
"""

import sys
import re
from pathlib import Path
from typing import Optional, List

from src.parser.rule_parser import parse_rules_string, parse_rules_file
from src.parser.models import ThreatBlock, RulesDatabase
from src.evaluator.threat_matcher import ThreatMatcher
from src.evaluator.signal import parse_signal


class ThreatRulesREPL:
    """Interactive REPL for ThreatRules"""

    def __init__(self):
        self.loaded_rules: Optional[RulesDatabase] = None
        self.rules_file: Optional[str] = None
        self.prompt = ">>> "

    def run(self):
        """Main REPL loop"""
        self.print_banner()

        while True:
            try:
                # Read input
                line = input(self.prompt).strip()

                if not line:
                    continue

                # Process command
                if line.startswith(':'):
                    self.process_command(line)
                else:
                    print("Unknown input. Use :help for commands or :parse <rule> to parse a rule.")

            except KeyboardInterrupt:
                print("\nUse :quit to exit")
            except EOFError:
                print("\nBye!")
                break

    def print_banner(self):
        """Print welcome banner"""
        print("=" * 70)
        print("ThreatRules Interactive REPL")
        print("=" * 70)
        print()
        print("Type :help for commands or :examples for example rules")
        print()

    def process_command(self, line: str):
        """Process REPL command"""
        parts = line.split(maxsplit=1)
        cmd = parts[0].lower()
        args = parts[1] if len(parts) > 1 else ""

        if cmd == ':quit' or cmd == ':exit' or cmd == ':q':
            print("Bye!")
            sys.exit(0)

        elif cmd == ':help' or cmd == ':h':
            self.show_help()

        elif cmd == ':examples' or cmd == ':ex':
            self.show_examples()

        elif cmd == ':parse' or cmd == ':p':
            if not args:
                print("Usage: :parse <rule>")
                print("Example: :parse E5 { d4: w2 | w3; }")
            else:
                self.parse_rule(args)

        elif cmd == ':eval' or cmd == ':e':
            self.eval_rule(args)

        elif cmd == ':test' or cmd == ':t':
            if not args:
                print("Usage: :test <signal>")
                print("Example: :test w2,f2,t1,r1,a1,d3")
            else:
                self.test_signal(args)

        elif cmd == ':load' or cmd == ':l':
            if not args:
                print("Usage: :load <file>")
                print("Example: :load data/rules.txt")
            else:
                self.load_rules(args)

        elif cmd == ':show' or cmd == ':s':
            self.show_loaded_rules()

        else:
            print(f"Unknown command: {cmd}")
            print("Type :help for available commands")

    def show_help(self):
        """Show help message"""
        print()
        print("Available Commands:")
        print("=" * 70)
        print()
        print("  :parse <rule>          Parse a single rule and show AST")
        print("  :eval <rule> <signal>  Evaluate a rule against a signal")
        print("  :test <signal>         Test signal against loaded rules")
        print("  :load <file>           Load rules from file")
        print("  :show                  Show currently loaded rules")
        print("  :examples              Show example rules")
        print("  :help                  Show this help message")
        print("  :quit                  Exit REPL")
        print()
        print("Shortcuts:")
        print("  :p  = :parse")
        print("  :e  = :eval")
        print("  :t  = :test")
        print("  :l  = :load")
        print("  :s  = :show")
        print("  :h  = :help")
        print("  :q  = :quit")
        print()

    def show_examples(self):
        """Show example rules"""
        print()
        print("Example Rules:")
        print("=" * 70)
        print()
        print("1. Simple OR:")
        print("   :parse E5 { d4: w2 | w3; }")
        print()
        print("2. Simple AND:")
        print("   :parse E5 { d4: w3 & f3; }")
        print()
        print("3. NOT expression:")
        print("   :parse E3 { d2: !w1; }")
        print()
        print("4. Precedence (& binds tighter than |):")
        print("   :parse E5 { d4: w1 | w2 & w3; }")
        print()
        print("5. Parentheses:")
        print("   :parse E5 { d4: (w1 | w2) & w3; }")
        print()
        print("6. Complex nested:")
        print("   :parse E5 { d4: (w3 & f3) | (w2 & t2); }")
        print()
        print("7. Multiple difficulties:")
        print("   :parse E3 { d4: w3; d3: w2; d2: w1; d1: others; }")
        print()
        print("8. Real-world avalanche combinations:")
        print("   :parse E5 { d4: (a4 & w3) | (a4 & f3) | a5; }")
        print()
        print("Example Evaluation:")
        print("=" * 70)
        print()
        print("1. Evaluate extreme weather:")
        print('   :eval "E5 { d4: w3 & f3; }" w3,f3,t1,r1,a1,d4')
        print()
        print("2. Test with loaded rules:")
        print("   :load data/rules.txt")
        print("   :test w2,f2,t1,r1,a1,d3")
        print()

    def parse_rule(self, rule_text: str):
        """Parse a rule and show AST"""
        print()
        print(f"Parsing: {rule_text}")
        print("-" * 70)

        try:
            rules_db = parse_rules_string(rule_text)

            if not rules_db or not rules_db.blocks:
                print("✗ Failed to parse rule")
                return

            print("✓ Parse successful!")
            print()

            for i, (threat_level, block) in enumerate(rules_db.blocks.items(), 1):
                print(f"Threat Block {i}:")
                print(f"  Level: {block.threat_level.value}")
                print(f"  Rules: {len(block.rules)}")
                print()

                for rule in block.rules.values():
                    print(f"  Difficulty: {rule.difficulty.value}")
                    print(f"  Expression: {self._expr_to_string(rule.expression)}")
                    print()

        except Exception as e:
            print(f"✗ Parse error: {e}")

        print()

    def eval_rule(self, args: str):
        """Evaluate a rule against a signal"""
        # Parse args: expect "rule" signal or rule signal
        match = re.match(r'^"([^"]+)"\s+(.+)$', args) or re.match(r'^(\S+.*?)\s+([a-z0-9,]+)$', args)

        if not match:
            print("Usage: :eval <rule> <signal>")
            print('Example: :eval "E5 { d4: w3 & f3; }" w3,f3,t1,r1,a1,d4')
            return

        rule_text = match.group(1)
        signal_text = match.group(2)

        print()
        print(f"Rule: {rule_text}")
        print(f"Signal: {signal_text}")
        print("-" * 70)

        try:
            # Parse rule
            rules_db = parse_rules_string(rule_text)
            if not rules_db or not rules_db.blocks:
                print("✗ Failed to parse rule")
                return

            # Parse signal
            signal = parse_signal(signal_text)
            print(f"✓ Signal parsed: {signal}")
            print()

            # Evaluate
            matcher = ThreatMatcher(rules_db)
            assessment = matcher.assess_threat(signal)

            print(f"Result: {assessment.threat_level.value}")
            print()

        except Exception as e:
            print(f"✗ Error: {e}")
            print()

    def test_signal(self, signal_text: str):
        """Test signal against loaded rules"""
        if self.loaded_rules is None:
            print("No rules loaded. Use :load <file> first.")
            return

        print()
        print(f"Signal: {signal_text}")
        print(f"Rules: {self.rules_file}")
        print("-" * 70)

        try:
            # Parse signal
            signal = parse_signal(signal_text)
            print(f"✓ Signal parsed: {signal}")
            print()

            # Evaluate
            matcher = ThreatMatcher(self.loaded_rules)
            assessment = matcher.assess_threat(signal)

            print(f"Result: {assessment.threat_level.value}")
            print()

        except Exception as e:
            print(f"✗ Error: {e}")
            print()

    def load_rules(self, file_path: str):
        """Load rules from file"""
        print()
        print(f"Loading: {file_path}")
        print("-" * 70)

        try:
            # Read file
            path = Path(file_path)
            if not path.exists():
                print(f"✗ File not found: {file_path}")
                return

            # Parse rules
            rules_db = parse_rules_file(path)

            if not rules_db or not rules_db.blocks:
                print("✗ No rules parsed")
                return

            self.loaded_rules = rules_db
            self.rules_file = file_path

            print(f"✓ Loaded {len(rules_db.blocks)} threat blocks")

            for block in rules_db.blocks.values():
                print(f"  - {block.threat_level.value}: {len(block.rules)} difficulty levels")

            print()

        except Exception as e:
            print(f"✗ Error: {e}")
            print()

    def show_loaded_rules(self):
        """Show currently loaded rules"""
        if self.loaded_rules is None:
            print("No rules loaded. Use :load <file> first.")
            return

        print()
        print(f"Loaded Rules: {self.rules_file}")
        print("=" * 70)
        print()

        for block in self.loaded_rules.blocks.values():
            print(f"{block.threat_level.value} {{")
            for rule in block.rules.values():
                expr_str = self._expr_to_string(rule.expression)
                print(f"  {rule.difficulty.value}: {expr_str};")
            print("}")
            print()

    def _expr_to_string(self, expr) -> str:
        """Convert expression AST to string"""
        from src.parser.models import LogicalExpression

        if isinstance(expr, str):
            return expr

        if not isinstance(expr, LogicalExpression):
            return str(expr)

        # Use the built-in to_simple_string method
        return expr.to_simple_string()


def main():
    """Entry point"""
    repl = ThreatRulesREPL()
    repl.run()


if __name__ == "__main__":
    main()
