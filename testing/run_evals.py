import json

from datetime import datetime
from pathlib import Path
from typing import List, Dict, Any
from dataclasses import dataclass
from enum import Enum


class TestResult(Enum):
    PASS = "PASS"
    FAIL = "FAIL"
    SKIP = "SKIP"
    ERROR = "ERROR"


@dataclass
class TestExecution:
    test_id: str
    name: str
    result: TestResult
    expected_references: List[str]
    actual_references: List[str]
    missing_references: List[str]
    extra_references: List[str]
    forbidden_found: List[str]
    execution_time_ms: float
    error_message: str = None
    reasoning: str = None


class ReferenceAnalyzer:
    """
    Analyzes user queries to determine which reference files should be loaded.

    This simulates the decision-making logic that Claude should follow
    when presented with a user query.
    """

    def __init__(self, skill_path: Path):
        self.skill_path = skill_path
        self.reference_keywords = self._load_reference_keywords()

    def _load_reference_keywords(self) -> Dict[str, List[str]]:
        """
        Load keyword mappings for each reference file.

        These keywords are extracted from the "When to load" column
        in SKILL.md's reference index.
        """
        return {
            "core.md": [
                "always",
                "auth",
                "api key",
                "rate limit",
                "methodology",
                "set up",
                "setup",
            ],
            "coins.md": [
                "coin price",
                "market data",
                "metadata",
                "tickers",
                "gainers",
                "losers",
                "current price",
                "market cap",
                "what's the",
            ],
            "coin-history.md": [
                "historical",
                "ohlc",
                "chart",
                "time-range",
                "candle",
                "past price",
                "historical price",
                "history",
            ],
            "coin-supply.md": [
                "supply",
                "circulating supply",
                "total supply",
                "supply chart",
                "circulating",
            ],
            "contract.md": [
                "contract address",
                "token address",
                "0x",
                "contract lookup",
                "by address",
                "address",
            ],
            "asset-platforms.md": [
                "platform id",
                "blockchain platform",
                "token list",
                "network id",
                "asset platform",
            ],
            "categories.md": ["category", "sector", "coin category"],
            "exchanges.md": [
                "exchange",
                "spot exchange",
                "cex",
                "binance",
                "coinbase",
                "kraken",
                "exchange volume",
                "exchange ticker",
                "ftx",
                "okx",
                "bybit",
            ],
            "derivatives.md": [
                "derivative",
                "futures",
                "perpetual",
                "swap",
                "options",
                "open interest",
            ],
            "treasury.md": [
                "treasury",
                "corporate",
                "institution",
                "company holdings",
                "microstrategy",
                "hold",
            ],
            "nfts.md": ["nft", "collection", "floor price", "nft market", "bored ape"],
            "global.md": [
                "global",
                "market stats",
                "dominance",
                "defi",
                "total market cap",
                "bitcoin dominance",
                "total crypto",
            ],
            "utils.md": [
                "search",
                "trending",
                "supported currencies",
                "exchange rate",
                "api status",
                "search for",
                "matching",
            ],
            "onchain-networks.md": [
                "network",
                "dex",
                "supported networks",
                "chain id",
                "dex id",
            ],
            "onchain-pools.md": [
                "pool",
                "liquidity pool",
                "dex pool",
                "trending pool",
                "new pool",
                "uniswap",
                "curve",
            ],
            "onchain-tokens.md": [
                "onchain token",
                "holder",
                "trader",
                "on-chain data",
                "token holder",
                "including holder",
            ],
            "onchain-ohlcv-trades.md": [
                "onchain ohlcv",
                "dex trade",
                "swap history",
                "pool candle",
            ],
            "onchain-categories.md": ["onchain category", "pool category"],
        }

    def analyze_query(self, query: str) -> List[str]:
        """
        Analyze a user query and return expected reference files.

        Args:
            query: User's natural language query

        Returns:
            List of reference file names that should be loaded
        """
        query_lower = query.lower()
        matched_refs = set()

        # Core is ALWAYS loaded
        matched_refs.add("core.md")

        # Check for keyword matches
        match_scores = {}
        for ref_file, keywords in self.reference_keywords.items():
            score = 0
            for keyword in keywords:
                if keyword in query_lower:
                    score += 1
            if score > 0:
                match_scores[ref_file] = score

        # Add all matched references
        for ref_file in match_scores:
            matched_refs.add(ref_file)

        # Apply routing logic: CoinGecko vs GeckoTerminal
        onchain_indicators = [
            "pool",
            "dex",
            "onchain",
            "on-chain",
            "liquidity pool",
            "uniswap",
            "pancakeswap",
            "curve",
            "sushiswap",
        ]
        is_onchain_query = any(
            indicator in query_lower for indicator in onchain_indicators
        )

        # Special cases for contract addresses
        if "0x" in query or "contract" in query_lower or "address" in query_lower:
            # If query mentions holders or on-chain, use GeckoTerminal
            if (
                "holder" in query_lower
                or "on-chain" in query_lower
                or "onchain" in query_lower
            ):
                matched_refs.add("onchain-tokens.md")
                # Remove contract.md if it was added
                matched_refs.discard("contract.md")
            else:
                # Use CoinGecko contract.md
                matched_refs.add("contract.md")
                matched_refs.discard("onchain-tokens.md")

        # Exchange routing: CEX vs DEX
        cex_names = [
            "binance",
            "coinbase",
            "kraken",
            "ftx",
            "okx",
            "bybit",
            "kucoin",
            "bitfinex",
            "huobi",
            "gate.io",
        ]
        has_cex = any(cex in query_lower for cex in cex_names)

        if has_cex:
            matched_refs.add("exchanges.md")
            # Don't add onchain-pools.md for CEX queries
            matched_refs.discard("onchain-pools.md")
            matched_refs.discard("onchain-ohlcv-trades.md")

        # If it's clearly an on-chain query but no specific reference matched
        if is_onchain_query and not any(r.startswith("onchain") for r in matched_refs):
            matched_refs.add("onchain-pools.md")

        # Remove core.md from analysis for cleaner logic, will re-add at end
        # (it's already in matched_refs, just don't match it again)

        # Special handling for auth/setup queries
        if (
            "api key" in query_lower
            or "rate limit" in query_lower
            or "set up" in query_lower
            or "setup" in query_lower
        ) and "how" in query_lower:
            # Pure auth query - only core.md needed
            # Remove other refs that might have been matched by keywords
            if "api key" in query_lower and "rate limit" in query_lower:
                # This is purely about authentication
                matched_refs = {"core.md"}

        # Trending/search queries
        if (
            "search" in query_lower or "trending" in query_lower
        ) and "coin" in query_lower:
            matched_refs.add("utils.md")
            # Remove coins.md if it was added just for "coin" keyword
            if "price" not in query_lower and "market" not in query_lower:
                matched_refs.discard("coins.md")

        return sorted(list(matched_refs))


class EvalRunner:
    """Main test runner class"""

    def __init__(self, evals_path: Path, skill_path: Path, output_dir: Path):
        self.evals_path = evals_path
        self.skill_path = skill_path
        self.output_dir = output_dir
        self.analyzer = ReferenceAnalyzer(skill_path)

    def load_tests(self) -> Dict[str, Any]:
        """Load test cases from evals.json"""
        with open(self.evals_path, "r") as f:
            return json.load(f)

    def run_test(self, test_case: Dict[str, Any]) -> TestExecution:
        """
        Execute a single test case.

        Args:
            test_case: Test case dictionary from evals.json

        Returns:
            TestExecution result
        """
        start_time = datetime.now()

        try:
            # Analyze the user query
            actual_refs = self.analyzer.analyze_query(test_case["user_query"])
            expected_refs = set(test_case["expected_references"])
            required_refs = set(test_case.get("required_references", []))
            forbidden_refs = set(test_case.get("forbidden_references", []))

            # Calculate differences
            actual_set = set(actual_refs)
            missing = list(required_refs - actual_set)
            extra = list(actual_set - expected_refs)
            forbidden_found = list(actual_set & forbidden_refs)

            # Determine pass/fail
            if forbidden_found:
                result = TestResult.FAIL
            elif missing:
                result = TestResult.FAIL
            elif len(extra) > 0 and test_case.get("priority") == "critical":
                # For critical tests, extra references are failures
                result = TestResult.FAIL
            else:
                result = TestResult.PASS

            execution_time = (datetime.now() - start_time).total_seconds() * 1000

            return TestExecution(
                test_id=test_case["test_id"],
                name=test_case["name"],
                result=result,
                expected_references=sorted(list(expected_refs)),
                actual_references=actual_refs,
                missing_references=missing,
                extra_references=extra,
                forbidden_found=forbidden_found,
                execution_time_ms=execution_time,
                reasoning=test_case.get("reasoning"),
            )

        except Exception as e:
            return TestExecution(
                test_id=test_case["test_id"],
                name=test_case["name"],
                result=TestResult.ERROR,
                expected_references=[],
                actual_references=[],
                missing_references=[],
                extra_references=[],
                forbidden_found=[],
                execution_time_ms=0,
                error_message=str(e),
            )

    def run_all_tests(self, filters: Dict[str, Any] = None) -> List[TestExecution]:
        """
        Run all tests with optional filtering.

        Args:
            filters: Dict with optional keys: category, priority, tags

        Returns:
            List of TestExecution results
        """
        evals_data = self.load_tests()
        results = []

        for suite in evals_data.get("test_suites", []):
            for test_case in suite.get("tests", []):
                # Apply filters
                if filters:
                    if (
                        "category" in filters
                        and test_case.get("category") != filters["category"]
                    ):
                        continue
                    if (
                        "priority" in filters
                        and test_case.get("priority") != filters["priority"]
                    ):
                        continue
                    if "tags" in filters:
                        test_tags = set(test_case.get("tags", []))
                        filter_tags = set(filters["tags"])
                        if not test_tags & filter_tags:
                            continue

                result = self.run_test(test_case)
                results.append(result)

        return results

    def generate_report(
        self, results: List[TestExecution], format: str = "markdown"
    ) -> str:
        """
        Generate test report in specified format.

        Args:
            results: List of test execution results
            format: 'markdown' or 'json'

        Returns:
            Formatted report string
        """
        if format == "markdown":
            return self._generate_markdown_report(results)
        elif format == "json":
            return self._generate_json_report(results)
        else:
            raise ValueError(f"Unsupported format: {format}")

    def _generate_markdown_report(self, results: List[TestExecution]) -> str:
        """Generate markdown test report"""
        # Calculate statistics
        total = len(results)
        passed = sum(1 for r in results if r.result == TestResult.PASS)
        failed = sum(1 for r in results if r.result == TestResult.FAIL)
        errors = sum(1 for r in results if r.result == TestResult.ERROR)
        skipped = sum(1 for r in results if r.result == TestResult.SKIP)
        pass_rate = (passed / total * 100) if total > 0 else 0

        # Build report
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        report = f"""# CoinGecko Skill Evaluation Report

**Generated:** {timestamp}

## Summary

| Metric | Value |
|--------|-------|
| Total Tests | {total} |
| Passed | {passed} ✓ |
| Failed | {failed} ✗ |
| Errors | {errors} ⚠ |
| Skipped | {skipped} ⊘ |
| Pass Rate | {pass_rate:.1f}% |

## Test Results

"""
        # Group by result type
        for result_type in [TestResult.FAIL, TestResult.ERROR, TestResult.PASS]:
            filtered = [r for r in results if r.result == result_type]
            if not filtered:
                continue

            report += f"\n### {result_type.value} ({len(filtered)})\n\n"

            for exec_result in filtered:
                status_icon = {
                    TestResult.PASS: "✓",
                    TestResult.FAIL: "✗",
                    TestResult.ERROR: "⚠",
                    TestResult.SKIP: "⊘",
                }[exec_result.result]

                report += (
                    f"#### {status_icon} {exec_result.test_id}: {exec_result.name}\n\n"
                )

                if exec_result.result == TestResult.ERROR:
                    report += f"**Error:** {exec_result.error_message}\n\n"
                    continue

                report += f"**Expected References:** {', '.join(exec_result.expected_references)}\n\n"
                report += f"**Actual References:** {', '.join(exec_result.actual_references)}\n\n"

                if exec_result.missing_references:
                    report += (
                        f"**Missing:** {', '.join(exec_result.missing_references)}\n\n"
                    )

                if exec_result.extra_references:
                    report += (
                        f"**Extra:** {', '.join(exec_result.extra_references)}\n\n"
                    )

                if exec_result.forbidden_found:
                    report += f"**Forbidden (Found):** {', '.join(exec_result.forbidden_found)}\n\n"

                if exec_result.reasoning:
                    report += f"**Reasoning:** {exec_result.reasoning}\n\n"

                report += (
                    f"**Execution Time:** {exec_result.execution_time_ms:.2f}ms\n\n"
                )
                report += "---\n\n"

        return report

    def _generate_json_report(self, results: List[TestExecution]) -> str:
        """Generate JSON test report"""
        report_data = {
            "timestamp": datetime.now().isoformat(),
            "summary": {
                "total": len(results),
                "passed": sum(1 for r in results if r.result == TestResult.PASS),
                "failed": sum(1 for r in results if r.result == TestResult.FAIL),
                "errors": sum(1 for r in results if r.result == TestResult.ERROR),
                "skipped": sum(1 for r in results if r.result == TestResult.SKIP),
            },
            "results": [
                {
                    "test_id": r.test_id,
                    "name": r.name,
                    "result": r.result.value,
                    "expected_references": r.expected_references,
                    "actual_references": r.actual_references,
                    "missing_references": r.missing_references,
                    "extra_references": r.extra_references,
                    "forbidden_found": r.forbidden_found,
                    "execution_time_ms": r.execution_time_ms,
                    "error_message": r.error_message,
                    "reasoning": r.reasoning,
                }
                for r in results
            ],
        }

        report_data["summary"]["pass_rate"] = (
            report_data["summary"]["passed"] / report_data["summary"]["total"] * 100
            if report_data["summary"]["total"] > 0
            else 0
        )

        return json.dumps(report_data, indent=2)


def main():
    """Main entry point with CLI interface"""
    import argparse

    parser = argparse.ArgumentParser(description="CoinGecko Skill Evaluation Runner")
    parser.add_argument(
        "--evals",
        type=Path,
        default=Path(__file__).parent / "evals.json",
        help="Path to evals.json file",
    )
    parser.add_argument(
        "--skill",
        type=Path,
        default=Path(__file__).parent.parent / "coingecko",
        help="Path to skill directory",
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=Path(__file__).parent / "output",
        help="Output directory for reports",
    )
    parser.add_argument(
        "--format",
        choices=["markdown", "json", "both"],
        default="markdown",
        help="Report format",
    )
    parser.add_argument("--category", help="Filter by test category")
    parser.add_argument("--priority", help="Filter by test priority")
    parser.add_argument("--tags", nargs="+", help="Filter by tags")

    args = parser.parse_args()

    # Create output directory
    args.output.mkdir(parents=True, exist_ok=True)

    # Build filters
    filters = {}
    if args.category:
        filters["category"] = args.category
    if args.priority:
        filters["priority"] = args.priority
    if args.tags:
        filters["tags"] = args.tags

    # Run tests
    runner = EvalRunner(args.evals, args.skill, args.output)
    print(f"Loading tests from {args.evals}...")
    results = runner.run_all_tests(filters)
    print(f"Executed {len(results)} tests")

    # Generate reports
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

    if args.format in ["markdown", "both"]:
        md_report = runner.generate_report(results, "markdown")
        md_path = args.output / f"eval_report_{timestamp}.md"
        with open(md_path, "w") as f:
            f.write(md_report)
        print(f"Markdown report saved to {md_path}")

    if args.format in ["json", "both"]:
        json_report = runner.generate_report(results, "json")
        json_path = args.output / f"eval_report_{timestamp}.json"
        with open(json_path, "w") as f:
            f.write(json_report)
        print(f"JSON report saved to {json_path}")

    # Print summary to console
    passed = sum(1 for r in results if r.result == TestResult.PASS)
    failed = sum(1 for r in results if r.result == TestResult.FAIL)
    pass_rate = (passed / len(results) * 100) if results else 0

    print(f"\nResults: {passed} passed, {failed} failed ({pass_rate:.1f}% pass rate)")

    # Exit with error code if tests failed
    return 0 if failed == 0 else 1


if __name__ == "__main__":
    exit(main())
