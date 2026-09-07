from pathlib import Path

from benchmarks.llm_provider.cases import CASES
from benchmarks.llm_provider.fake_provider import FakeProvider
from benchmarks.llm_provider.runner import run_benchmark, save_results


def main() -> None:
    provider = FakeProvider()

    results = run_benchmark(
        provider=provider,
        cases=CASES,
        runs_per_case=3,
    )

    output_path = Path("benchmarks/llm_provider/results/fake-model.jsonl")

    save_results(results, output_path)

    print(f"Completed: {len(results)} runs")
    print(f"Saved to: {output_path}")


if __name__ == "__main__":
    main()
