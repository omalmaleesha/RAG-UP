import time
from pathlib import Path
from datetime import datetime
import requests
from metrics.performance_reporter import PerformanceReporter
API_URL = "http://127.0.0.1:8000/chat"
WAIT_SECONDS = 5
CACHE_HIT_WAIT_SECONDS = 1
REPORT_FILE = Path("metrics/test_metrics.txt")
QUESTIONS = [
    "In what year was Apex Horizon University founded?",
    "How many total acres does the campus cover?",
    "What is the faculty-to-student ratio at the university?",
    "Which organization fully accredits Apex Horizon University?",
    "What is the university's rank in global innovation?",
    "Which college offers the Undergraduate Major in Robotics?",
    "How many students are annually enrolled in the School of Business & Leadership?",
    "In which school or faculty is the M.F.A. in Creative Writing offered?",
    "What graduate degree in cybersecurity is offered by the College of Engineering & Computing?",
    "Which college or school has an annual enrollment of 3,800 students?",
    "What is the minimum GPA requirement on a 4.0 scale for undergraduate admission?",
    "What minimum TOEFL iBT score is required for non-native English speakers?",
    "What is the minimum IELTS score required for non-native English speakers?",
    "What minimum undergraduate GPA is required for graduate admission?",
    "What is the annual undergraduate tuition for an in-state resident?",
    "What is the annual graduate tuition for out-of-state or international students?",
    "How much does housing and campus dining cost annually per student?",
    "What percentage of undergraduates receive financial assistance?",
    "What annual living stipend is provided with Graduate Research & Teaching Assistantships?",
    "How many print volumes are hosted in the Central Founders Library?",
    "What is the seating capacity of the athletics stadium?",
    "How many modern residence halls does the university operate?",
    "What is the Early Action application deadline for the Fall Semester 2026?",
    "On what date do classes commence for the Spring Semester 2027?",
    "What is the main phone number for the Office of Undergraduate Admissions?",
]
def check_api():
    print("\nChecking RAG AI Agent API...")
    try:
        response = requests.get(
            "http://127.0.0.1:8000/",
            timeout=5
        )
        if response.status_code == 200:
            print("✅ API is running")
            return True
        print(
            f"❌ API returned status code "
            f"{response.status_code}"
        )
        return False
    except requests.exceptions.RequestException as e:
        print("❌ Could not connect to API")
        print(f"Error: {e}")
        print(
            "\nStart your RAG AI Agent first with:"
        )
        print(
            "uv run python main.py"
        )
        return False
def clear_old_report():
    if REPORT_FILE.exists():
        REPORT_FILE.unlink()
        print(
            f"🗑️ Deleted old report: "
            f"{REPORT_FILE}"
        )
    else:
        print(
            "No previous test report found."
        )
def run_query(
    question: str,
    test_number: int,
    phase: str
):
    print("\n")
    print("=" * 70)
    print(
        f"TEST {test_number}/25"
    )
    print(
        f"PHASE: {phase}"
    )
    print("=" * 70)
    print(
        f"Question: {question}"
    )
    print(
        f"Started : "
        f"{datetime.now().strftime('%H:%M:%S')}"
    )
    start = time.perf_counter()
    try:
        response = requests.post(
            API_URL,
            json={
                "query": question
            },
            timeout=120
        )
        elapsed = (
            time.perf_counter()
            - start
        )
        if response.status_code != 200:
            print(
                f"\n❌ HTTP ERROR "
                f"{response.status_code}"
            )
            print(
                response.text
            )
            return None
        data = response.json()
        cache_hit = data.get(
            "cache_hit",
            False
        )
        llm_calls = data.get(
            "llm_calls",
            0
        )
        total_time = data.get(
            "total_time",
            elapsed
        )
        answer = data.get(
            "answer",
            ""
        )
        print("\nRESULT")
        print("-" * 70)
        print(
            f"Cache Hit : {cache_hit}"
        )
        print(
            f"LLM Calls : {llm_calls}"
        )
        print(
            f"Total Time: {total_time:.3f}s"
        )
        print(
            f"HTTP Time : {elapsed:.3f}s"
        )
        print(
            f"Answer    : {answer[:200]}"
        )
        result = {
            "user_query": question,
            "final_answer": answer,
            "total_time": total_time,
            "llm_calls": llm_calls,
            "cache_hit": cache_hit,
            "cached_answer": (
                answer
                if cache_hit
                else None
            ),
            "selected_tool": None,
            "enough_information": False,
            "reflection_passed": False,
            "retrieved_docs": [],
            "metrics": {}
        }
        PerformanceReporter.write(
            result
        )
        print(
            "\n✅ Report written"
        )
        return result
    except requests.exceptions.Timeout:
        print(
            "\n❌ Request timed out"
        )
        return None
    except requests.exceptions.RequestException as e:
        print(
            "\n❌ Request failed"
        )
        print(
            f"Error: {e}"
        )
        return None
    except Exception as e:
        print(
            "\n❌ Unexpected error"
        )
        print(
            f"Error: {e}"
        )
        return None
def run_cache_miss_phase():
    print("\n")
    print("#" * 70)
    print("# PHASE 1 — CACHE MISS")
    print("#" * 70)
    print(
        "\n25 unique questions will be sent."
    )
    print(
        "Expected behavior:"
    )
    print(
        "CACHE MISS → RAG → LLM → CACHE WRITE"
    )
    print(
        f"\nWaiting {WAIT_SECONDS}s "
        "between requests to respect rate limits."
    )
    results = []
    for index, question in enumerate(
        QUESTIONS,
        start=1
    ):
        result = run_query(
            question=question,
            test_number=index,
            phase="CACHE MISS"
        )
        results.append(
            result
        )
        if index < len(QUESTIONS):
            print(
                f"\n⏳ Waiting "
                f"{WAIT_SECONDS} seconds..."
            )
            time.sleep(
                WAIT_SECONDS
            )
    return results
def run_cache_hit_phase():
    print("\n")
    print("#" * 70)
    print("# PHASE 2 — CACHE HIT")
    print("#" * 70)
    print(
        "\nThe same 25 questions will be sent again."
    )
    print(
        "Expected behavior:"
    )
    print(
        "CACHE HIT → RETURN CACHED ANSWER"
    )
    print(
        "\nExpected LLM calls: 0"
    )
    results = []
    for index, question in enumerate(
        QUESTIONS,
        start=1
    ):
        result = run_query(
            question=question,
            test_number=index,
            phase="CACHE HIT"
        )
        results.append(
            result
        )
        if index < len(QUESTIONS):
            time.sleep(
                CACHE_HIT_WAIT_SECONDS
            )
    return results
def calculate_statistics(
    phase1_results,
    phase2_results
):
    phase1_valid = [
        result
        for result in phase1_results
        if result is not None
    ]
    phase1_cache_hits = sum(
        1
        for result in phase1_valid
        if result.get(
            "cache_hit",
            False
        )
    )
    phase1_llm_calls = sum(
        result.get(
            "llm_calls",
            0
        )
        for result in phase1_valid
    )
    phase1_time = sum(
        result.get(
            "total_time",
            0
        )
        for result in phase1_valid
    )
    phase2_valid = [
        result
        for result in phase2_results
        if result is not None
    ]
    phase2_cache_hits = sum(
        1
        for result in phase2_valid
        if result.get(
            "cache_hit",
            False
        )
    )
    phase2_llm_calls = sum(
        result.get(
            "llm_calls",
            0
        )
        for result in phase2_valid
    )
    phase2_time = sum(
        result.get(
            "total_time",
            0
        )
        for result in phase2_valid
    )
    average_miss_time = 0
    average_hit_time = 0
    if phase1_valid:
        average_miss_time = (
            phase1_time
            / len(phase1_valid)
        )
    if phase2_valid:
        average_hit_time = (
            phase2_time
            / len(phase2_valid)
        )
    speedup = 0
    if average_hit_time > 0:
        speedup = (
            average_miss_time
            / average_hit_time
        )
    time_saved = (
        average_miss_time
        - average_hit_time
    )
    llm_calls_avoided = (
        phase1_llm_calls
        - phase2_llm_calls
    )
    cache_hit_rate = 0
    if phase2_valid:
        cache_hit_rate = (
            phase2_cache_hits
            / len(phase2_valid)
        ) * 100
    return {
        "phase1_queries": len(
            phase1_valid
        ),
        "phase1_cache_hits": (
            phase1_cache_hits
        ),
        "phase1_llm_calls": (
            phase1_llm_calls
        ),
        "phase1_total_time": (
            phase1_time
        ),
        "phase2_queries": len(
            phase2_valid
        ),
        "phase2_cache_hits": (
            phase2_cache_hits
        ),
        "phase2_llm_calls": (
            phase2_llm_calls
        ),
        "phase2_total_time": (
            phase2_time
        ),
        "average_miss_time": (
            average_miss_time
        ),
        "average_hit_time": (
            average_hit_time
        ),
        "speedup": speedup,
        "time_saved": time_saved,
        "llm_calls_avoided": (
            llm_calls_avoided
        ),
        "cache_hit_rate": (
            cache_hit_rate
        )
    }
def print_summary(stats):
    print("\n\n")
    print("=" * 70)
    print("RAG AI AGENT BENCHMARK SUMMARY")
    print("=" * 70)
    print()
    print("CACHE MISS PHASE")
    print("-" * 70)
    print(
        f"Queries              : "
        f"{stats['phase1_queries']}"
    )
    print(
        f"Cache Hits           : "
        f"{stats['phase1_cache_hits']}"
    )
    print(
        f"LLM Calls            : "
        f"{stats['phase1_llm_calls']}"
    )
    print(
        f"Total Time           : "
        f"{stats['phase1_total_time']:.3f}s"
    )
    print()
    print("CACHE HIT PHASE")
    print("-" * 70)
    print(
        f"Queries              : "
        f"{stats['phase2_queries']}"
    )
    print(
        f"Cache Hits           : "
        f"{stats['phase2_cache_hits']}"
    )
    print(
        f"LLM Calls            : "
        f"{stats['phase2_llm_calls']}"
    )
    print(
        f"Total Time           : "
        f"{stats['phase2_total_time']:.3f}s"
    )
    print()
    print("OVERALL PERFORMANCE")
    print("-" * 70)
    total_queries = (
        stats["phase1_queries"]
        + stats["phase2_queries"]
    )
    total_llm_calls = (
        stats["phase1_llm_calls"]
        + stats["phase2_llm_calls"]
    )
    print(
        f"Total Queries        : "
        f"{total_queries}"
    )
    print(
        f"Total LLM Calls      : "
        f"{total_llm_calls}"
    )
    print(
        f"LLM Calls Avoided    : "
        f"{stats['llm_calls_avoided']}"
    )
    print(
        f"Cache Hit Rate       : "
        f"{stats['cache_hit_rate']:.2f}%"
    )
    print()
    print("LATENCY")
    print("-" * 70)
    print(
        f"Average Cache Miss   : "
        f"{stats['average_miss_time']:.3f}s"
    )
    print(
        f"Average Cache Hit    : "
        f"{stats['average_hit_time']:.3f}s"
    )
    print(
        f"Average Time Saved   : "
        f"{stats['time_saved']:.3f}s"
    )
    print(
        f"Average Speedup      : "
        f"{stats['speedup']:.2f}x"
    )
    print("=" * 70)
    print(
        "\nFull reports:"
    )
    print(
        "metrics/test_metrics.txt"
    )
def main():
    print("\n")
    print("=" * 70)
    print("RAG AI AGENT 50-QUERY BENCHMARK")
    print("=" * 70)
    print(
        f"\nTotal unique questions : "
        f"{len(QUESTIONS)}"
    )
    print(
        "Total executions       : 50"
    )
    print(
        "Maximum LLM calls      : 25"
    )
    print(
        f"LLM wait interval      : "
        f"{WAIT_SECONDS}s"
    )
    print(
        "\nBenchmark strategy:"
    )
    print(
        "Phase 1 → 25 unique queries"
    )
    print(
        "Phase 2 → same 25 queries"
    )
    print(
        "Expected LLM calls → 25"
    )
    print(
        "Expected cache-hit LLM calls → 0"
    )
    print("=" * 70)
    if not check_api():
        return
    clear_old_report()
    phase1_results = (
        run_cache_miss_phase()
    )
    phase2_results = (
        run_cache_hit_phase()
    )
    stats = calculate_statistics(
        phase1_results,
        phase2_results
    )
    print_summary(
        stats
    )
if __name__ == "__main__":
    main()