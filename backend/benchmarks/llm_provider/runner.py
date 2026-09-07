from collections.abc import Iterable
from pathlib import Path
from time import perf_counter

from pydantic import BaseModel

from app.ai.providers.base import PreferenceProvider
from app.ai.schemas import PreferenceFeatures
from benchmarks.llm_provider.cases import BenchmarkCase


class BenchmarkResult(BaseModel):
    provider: str
    model: str
    case_id: str
    run_no: int

    schema_valid: bool
    latency_ms: float

    output: PreferenceFeatures | None = None
    error: str | None = None


def run_case(
    provider: PreferenceProvider,
    case: BenchmarkCase,
    run_no: int,
) -> BenchmarkResult:
    started_at = perf_counter()

    try:
        output = provider.extract(
            name=case.name,
            category=case.category,
            comment=case.comment,
        )

        latency_ms = (perf_counter() - started_at) * 1000

        return BenchmarkResult(
            provider=provider.provider_name,
            model=provider.model_name,
            case_id=case.case_id,
            run_no=run_no,
            schema_valid=True,
            latency_ms=latency_ms,
            output=output,
        )

    except Exception as exc:
        latency_ms = (perf_counter() - started_at) * 1000

        return BenchmarkResult(
            provider=provider.provider_name,
            model=provider.model_name,
            case_id=case.case_id,
            run_no=run_no,
            schema_valid=False,
            latency_ms=latency_ms,
            error=str(exc),
        )


def run_benchmark(
    provider: PreferenceProvider,
    cases: Iterable[BenchmarkCase],
    runs_per_case: int = 3,
) -> list[BenchmarkResult]:
    results: list[BenchmarkResult] = []

    for case in cases:
        for run_no in range(1, runs_per_case + 1):
            result = run_case(
                provider=provider,
                case=case,
                run_no=run_no,
            )
            results.append(result)

    return results


def save_results(
    results: Iterable[BenchmarkResult],
    output_path: Path,
) -> None:
    output_path.parent.mkdir(parents=True, exist_ok=True)

    with output_path.open("w", encoding="utf-8") as file:
        for result in results:
            file.write(result.model_dump_json())
            file.write("\n")
