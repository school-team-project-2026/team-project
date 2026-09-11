from collections.abc import Iterable
from pathlib import Path
from time import perf_counter, sleep

from pydantic import BaseModel, ValidationError

from app.ai.providers.base import PreferenceProvider
from app.ai.schemas import PreferenceFeatures
from benchmarks.llm_provider.cases import BenchmarkCase


class BenchmarkResult(BaseModel):
    provider: str
    model: str
    case_id: str
    run_no: int

    request_success: bool
    schema_valid: bool | None
    latency_ms: float

    output: PreferenceFeatures | None = None
    error_type: str | None = None
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
            request_success=True,
            schema_valid=True,
            latency_ms=latency_ms,
            output=output,
        )

    except ValidationError as exc:
        latency_ms = (perf_counter() - started_at) * 1000

        return BenchmarkResult(
            provider=provider.provider_name,
            model=provider.model_name,
            case_id=case.case_id,
            run_no=run_no,
            request_success=True,
            schema_valid=False,
            latency_ms=latency_ms,
            error_type=type(exc).__name__,
            error=str(exc),
        )

    except Exception as exc:
        latency_ms = (perf_counter() - started_at) * 1000

        return BenchmarkResult(
            provider=provider.provider_name,
            model=provider.model_name,
            case_id=case.case_id,
            run_no=run_no,
            request_success=False,
            schema_valid=None,
            latency_ms=latency_ms,
            error_type=type(exc).__name__,
            error=str(exc),
        )


def run_benchmark(
    provider: PreferenceProvider,
    cases: Iterable[BenchmarkCase],
    runs_per_case: int = 3,
    request_interval_seconds: float = 0,
) -> list[BenchmarkResult]:
    case_list = list(cases)
    results: list[BenchmarkResult] = []

    for case_index, case in enumerate(case_list):
        for run_index in range(runs_per_case):
            result = run_case(
                provider=provider,
                case=case,
                run_no=run_index + 1,
            )
            results.append(result)

            is_last_run = (
                case_index == len(case_list) - 1 and run_index == runs_per_case - 1
            )

            if not is_last_run and request_interval_seconds > 0:
                sleep(request_interval_seconds)

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
