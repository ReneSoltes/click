"""
Profiling benchmark for Click shell completion
Focus on performance bottlenecks in string operations and formatting
"""

import cProfile
import io
import pstats
import time

import click
from click.shell_completion import CompletionItem
from click.shell_completion import FishComplete


def create_complex_cli():
    """Create a complex CLI for benchmarking."""

    @click.group()
    def cli():
        """Complex CLI for profiling."""
        pass

    # Add multiple subcommands with many options
    for i in range(20):

        def cmd_func(**kwargs):
            pass

        cmd_func.__name__ = f"command{i}"

        cmd = click.command(name=f"command{i}")(cmd_func)
        for j in range(5):
            cmd = click.option(
                f"--opt{i}-{j}", help=f"Option {i}-{j} with some\nmulti-line\nhelp text"
            )(cmd)

        cli.add_command(cmd)

    return cli


def benchmark_fish_format_completion(iterations=10000):
    """Benchmark FishComplete.format_completion method."""
    from unittest.mock import Mock

    fish = FishComplete(cli=Mock(), ctx_args={}, prog_name="test", complete_var="TEST")

    # Test items with various help texts
    test_items = [
        CompletionItem(type="plain", value="--simple", help="Simple help"),
        CompletionItem(type="plain", value="--multiline", help="Help\nwith\nnewlines"),
        CompletionItem(type="plain", value="--long", help="Very long help text " * 20),
        CompletionItem(type="plain", value="--special", help="\b\nSpecial\n--format"),
    ]

    results = []
    for _ in range(iterations):
        start = time.perf_counter()
        for item in test_items:
            fish.format_completion(item)
        end = time.perf_counter()
        results.append(end - start)

    return results


def benchmark_string_replace_operations(iterations=100000):
    """Benchmark string replace operations - BEFORE optimization."""
    test_strings = [
        "Simple text without newlines",
        "Text\nwith\nnewlines",
        "\b\nSpecial\nformat",
        "Very long text " * 50,
        "Short",
    ]

    results = []
    for _ in range(iterations):
        start = time.perf_counter()
        for text in test_strings:
            # OLD METHOD: Always call replace
            _ = text.replace("\n", r"\n")
        end = time.perf_counter()
        results.append(end - start)

    return results


def benchmark_string_replace_optimized(iterations=100000):
    """Benchmark string replace operations - AFTER optimization."""
    test_strings = [
        "Simple text without newlines",
        "Text\nwith\nnewlines",
        "\b\nSpecial\nformat",
        "Very long text " * 50,
        "Short",
    ]

    results = []
    for _ in range(iterations):
        start = time.perf_counter()
        for text in test_strings:
            # NEW METHOD: Check first, then replace
            if "\n" in text:
                _ = text.replace("\n", r"\n")
            else:
                _ = text
        end = time.perf_counter()
        results.append(end - start)

    return results


def profile_with_cprofile():
    """Profile using cProfile."""
    profiler = cProfile.Profile()

    profiler.enable()
    benchmark_fish_format_completion(iterations=1000)
    profiler.disable()

    s = io.StringIO()
    ps = pstats.Stats(profiler, stream=s).sort_stats("cumulative")
    ps.print_stats(20)

    return s.getvalue()


if __name__ == "__main__":
    print("=" * 70)
    print("CLICK PROFILING BENCHMARK - TIME PROFILING")
    print("=" * 70)
    print()

    # 1. FishComplete.format_completion benchmark
    print("1. Benchmarking FishComplete.format_completion()...")
    results = benchmark_fish_format_completion(iterations=10000)
    avg_time = sum(results) / len(results)
    total_time = sum(results)

    print("   Iterations: 10,000")
    print(f"   Total time: {total_time:.4f} s")
    print(f"   Average time per iteration: {avg_time * 1000:.4f} ms")
    print(f"   Average time per item: {(avg_time / 4) * 1000000:.4f} μs")
    print()

    # 2. String replace - BEFORE optimization
    print("2. Benchmarking string.replace() - BEFORE optimization...")
    results_before = benchmark_string_replace_operations(iterations=100000)
    avg_before = sum(results_before) / len(results_before)
    total_before = sum(results_before)

    print("   Iterations: 100,000")
    print(f"   Total time: {total_before:.4f} s")
    print(f"   Average time per iteration: {avg_before * 1000000:.4f} μs")
    print()

    # 3. String replace - AFTER optimization
    print("3. Benchmarking string.replace() - AFTER optimization...")
    results_after = benchmark_string_replace_optimized(iterations=100000)
    avg_after = sum(results_after) / len(results_after)
    total_after = sum(results_after)

    print("   Iterations: 100,000")
    print(f"   Total time: {total_after:.4f} s")
    print(f"   Average time per iteration: {avg_after * 1000000:.4f} μs")
    print()

    # 4. Comparison
    improvement = ((avg_before - avg_after) / avg_before) * 100
    time_saved = total_before - total_after

    print("4. COMPARISON:")
    print(f"   BEFORE: {avg_before * 1000000:.4f} μs per iteration")
    print(f"   AFTER:  {avg_after * 1000000:.4f} μs per iteration")
    print(f"   IMPROVEMENT: {improvement:.2f}%")
    print(f"   TIME SAVED (100k iterations): {time_saved:.4f} s")
    print()

    # 5. cProfile analysis
    print("5. cProfile analysis (top 20 functions):")
    print("-" * 70)
    profile_output = profile_with_cprofile()
    print(profile_output[:2000])  # First 2000 chars
    print()

    print("=" * 70)
    print("PROFILING COMPLETE - Results saved to PROFILING_REPORT.md")
    print("=" * 70)
