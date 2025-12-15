"""
Mountain Tourist Monitoring System - Main Entry Point

System monitorowania turystów górskich oparty na analizie danych mobilnych
i automatycznym wnioskowaniu logicznym.

Autorzy: Szymon Adamczyk, Bartłomiej Król
Akademia Tarnowska - Języki formalne i kompilatory II
Rok: 2025/2026

Użycie:
    python main.py --rules data/rules.txt --signals examples/signals.txt
    python main.py --interactive
    python main.py --single "w3,f3,t1,r1,a1,d4"
"""

import sys
import argparse
from pathlib import Path

from rich.console import Console

from src.parser.rule_parser import parse_rules_file
from src.evaluator.signal import parse_signal
from src.evaluator.threat_matcher import ThreatMatcher
from src.stream import StreamProcessor, SignalReader
from src.ui import ThreatPresenter

console = Console()


def main():
    """Główna funkcja programu"""
    parser = argparse.ArgumentParser(
        description="Mountain Tourist Monitoring System",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Process signals from file
  python main.py --rules data/rules.txt --signals examples/signals.txt

  # Interactive mode (manual signal input)
  python main.py --rules data/rules.txt --interactive

  # Single signal assessment
  python main.py --rules data/rules.txt --single "w3,f3,t1,r1,a1,d4"

  # Compact output
  python main.py --rules data/rules.txt --signals examples/signals.txt --compact

  # Show evaluation trace
  python main.py --rules data/rules.txt --single "w2,f3,t1,r2,a1,d3" --trace
        """
    )

    parser.add_argument(
        '--rules',
        type=str,
        default='data/rules.txt',
        help='Path to rules file (default: data/rules.txt)'
    )

    parser.add_argument(
        '--signals',
        type=str,
        help='Path to signals file (CSV format)'
    )

    parser.add_argument(
        '--single',
        type=str,
        help='Single signal to assess (format: w1,f1,t1,r1,a1,d1)'
    )

    parser.add_argument(
        '--interactive',
        action='store_true',
        help='Interactive mode (enter signals manually)'
    )

    parser.add_argument(
        '--compact',
        action='store_true',
        help='Compact output (one line per signal)'
    )

    parser.add_argument(
        '--trace',
        action='store_true',
        help='Show evaluation trace (debug)'
    )

    parser.add_argument(
        '--no-stats',
        action='store_true',
        help='Do not show statistics'
    )

    parser.add_argument(
        '--debug',
        action='store_true',
        help='Debug mode'
    )

    args = parser.parse_args()

    # Banner
    console.print("\n[bold cyan]Mountain Tourist Monitoring System[/bold cyan]")
    console.print("[dim]Akademia Tarnowska - Jezyki formalne i kompilatory II[/dim]\n")

    try:
        # 1. Load rules
        console.print(f"[yellow]Loading rules from:[/yellow] {args.rules}")
        rules_db = parse_rules_file(args.rules)
        console.print("[green]Rules loaded successfully![/green]\n")

        # 2. Create components
        presenter = ThreatPresenter(console)
        matcher = ThreatMatcher(rules_db, debug=args.debug)

        # 3. Process based on mode
        if args.single:
            # Single signal mode
            process_single_signal(args.single, matcher, presenter, args)

        elif args.interactive:
            # Interactive mode
            process_interactive(matcher, presenter, args)

        elif args.signals:
            # File processing mode
            process_signals_file(args.signals, matcher, presenter, args)

        else:
            console.print("[red]Error: Please specify --signals, --single, or --interactive[/red]")
            console.print("Use --help for more information")
            sys.exit(1)

    except FileNotFoundError as e:
        console.print(f"\n[bold red]File Not Found:[/bold red] {str(e)}\n")
        sys.exit(1)
    except KeyboardInterrupt:
        console.print("\n\n[yellow]Interrupted by user[/yellow]")
        sys.exit(0)
    except Exception as e:
        console.print(f"\n[bold red]Unexpected Error:[/bold red] {str(e)}\n")
        if args.debug:
            import traceback
            traceback.print_exc()
        sys.exit(1)


def process_single_signal(signal_str: str, matcher, presenter, args):
    """Process a single signal"""
    console.print(f"[yellow]Processing signal:[/yellow] {signal_str}\n")

    try:
        signal = parse_signal(signal_str)
        assessment = matcher.assess_threat(signal, include_trace=args.trace)

        if args.compact:
            presenter.show_compact(assessment)
        else:
            presenter.show_assessment(
                assessment,
                show_trace=args.trace,
                show_recommendations=True
            )

    except ValueError as e:
        console.print(f"[red]Invalid signal format:[/red] {str(e)}")
        console.print("Expected format: w1,f1,t1,r1,a1,d1")
        sys.exit(1)


def process_interactive(matcher, presenter, args):
    """Interactive mode - read signals from stdin"""
    console.print("[cyan]Interactive Mode[/cyan]")
    console.print("Enter signals in format: w1,f1,t1,r1,a1,d1")
    console.print("Type 'q' to quit\n")

    assessments = []

    try:
        for signal in SignalReader.read_stdin():
            assessment = matcher.assess_threat(signal, include_trace=args.trace)
            assessments.append(assessment)

            if args.compact:
                presenter.show_compact(assessment)
            else:
                presenter.show_assessment(
                    assessment,
                    show_trace=args.trace,
                    show_recommendations=True
                )

            console.print()  # Empty line between assessments

    except KeyboardInterrupt:
        console.print("\n[yellow]Exiting interactive mode...[/yellow]")

    # Show statistics if we processed any signals
    if assessments and not args.no_stats:
        console.print("\n")
        presenter.show_statistics(assessments)


def process_signals_file(file_path: str, matcher, presenter, args):
    """Process signals from file"""
    console.print(f"[yellow]Processing signals from:[/yellow] {file_path}\n")

    # Create processor with callback for real-time display
    assessments = []

    def on_signal(signal, assessment):
        assessments.append(assessment)
        if not args.compact:
            # Show detailed assessment
            presenter.show_assessment(
                assessment,
                show_trace=args.trace,
                show_recommendations=False  # Don't show recs in batch mode
            )
            console.print()
        else:
            # Show compact
            presenter.show_compact(assessment)

    processor = StreamProcessor(
        matcher.rules_db,
        on_signal=on_signal if not args.compact else None,
        debug=args.debug
    )

    # Process file
    result = processor.process_file(file_path)

    # If compact mode and we didn't show during processing, show now
    if args.compact and not on_signal:
        for assessment in result.assessments:
            presenter.show_compact(assessment)

    # Show summary
    console.print(f"\n[bold]Processing Summary:[/bold]")
    console.print(f"  Total signals: {result.total_signals}")
    console.print(f"  Successfully processed: {len(result.assessments)}")
    console.print(f"  Errors: {len(result.errors)}")
    console.print(f"  Processing time: {result.processing_time:.3f}s")

    if result.errors and args.debug:
        console.print("\n[red]Errors:[/red]")
        for error in result.errors:
            console.print(f"  - {error}")

    # Show statistics
    if result.assessments and not args.no_stats:
        console.print()
        presenter.show_statistics(result.assessments)


if __name__ == "__main__":
    main()
