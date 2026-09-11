from pathlib import Path

from app.ai.providers.gemini import GeminiProvider
from benchmarks.llm_provider.cases import CASES
from benchmarks.llm_provider.runner import run_benchmark, save_results


def main() -> None:
    provider = GeminiProvider()

    results = run_benchmark(
        provider=provider,
        cases=CASES,
        runs_per_case=1,
        request_interval_seconds=13,
    )

    output_path = Path(
        "benchmarks/llm_provider/results/google-gemini-3.8-flash-preliminary.jsonl"
    )

    save_results(results, output_path)

    success_count = sum(
        result.request_success and result.schema_valid is True for result in results
    )

    api_failure_count = sum(not result.request_success for result in results)

    schema_failure_count = sum(
        result.request_success and result.schema_valid is False for result in results
    )

    print(f"Completed: {len(results)} runs")
    print(f"Success: {success_count}")
    print(f"API Failure: {api_failure_count}")
    print(f"Schema Failure: {schema_failure_count}")
    print(f"Saved to: {output_path}")


if __name__ == "__main__":
    main()
