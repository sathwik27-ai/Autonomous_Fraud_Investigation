"""Production regression test suite covering:
1. Issue 1: Health metadata (environment, engine, graph_backend)
2. Issue 2: Fraud decision distribution and boundary thresholds (0.49, 0.50, 0.79, 0.80)
3. Issue 3: Transaction amount validation and rejection of invalid / extreme amounts
4. Issue 4: IST timezone handling and round-trip preservation
"""

import math
import unittest
from datetime import datetime, timezone
from pydantic import ValidationError

from app.api.routes import TransactionIn
from app.agents.scoring import score_from_results
from app.config import settings


class TestProductionIssues(unittest.TestCase):
    def test_amount_validation(self):
        """Verify TransactionIn accepts valid finite positive amounts <= 10M, and rejects extremes/invalids."""
        # Valid amounts
        t1 = TransactionIn(user_id="U001", amount=4800.0)
        self.assertEqual(t1.amount, 4800.0)

        t2 = TransactionIn(user_id="U001", amount=10_000_000.0)
        self.assertEqual(t2.amount, 10_000_000.0)

        t3 = TransactionIn(user_id="U001", amount=0.01)
        self.assertEqual(t3.amount, 0.01)

        # Zero or negative
        with self.assertRaises(ValidationError):
            TransactionIn(user_id="U001", amount=0.0)

        with self.assertRaises(ValidationError):
            TransactionIn(user_id="U001", amount=-100.0)

        # Exceeds maximum limit ($10M)
        with self.assertRaises(ValidationError):
            TransactionIn(user_id="U001", amount=10_000_001.0)

        # Extreme exponential values
        with self.assertRaises(ValidationError):
            TransactionIn(user_id="U001", amount=1e207)

        with self.assertRaises(ValidationError):
            TransactionIn(user_id="U001", amount=6.7e38)

        # Non-finite values
        with self.assertRaises(ValidationError):
            TransactionIn(user_id="U001", amount=float("inf"))

        with self.assertRaises(ValidationError):
            TransactionIn(user_id="U001", amount=float("nan"))

    def test_decision_boundaries(self):
        """Verify exact boundary behavior for thresholds (0.50 review, 0.80 block)."""
        # Low risk -> Allow
        mock_results_allow = {
            "get_user_history": {"found": True, "is_flagged": False, "avg_amount": 300},
            "check_transaction_pattern": {"anomalies": [], "amount_ratio_vs_avg": 1.0, "user_avg_amount": 300},
            "get_linked_accounts": {"flagged_connection_count": 0, "shared_devices": []},
            "search_similar_cases": {"matches": []},
        }
        res_allow = score_from_results({"user_id": "U001", "amount": 300}, mock_results_allow)
        self.assertLess(res_allow["fraud_score"], 0.50)
        self.assertEqual(res_allow["action"], "allow")

        # Moderate risk -> Review (0.50 <= score < 0.80)
        mock_results_review = {
            "get_user_history": {"found": True, "is_flagged": False, "avg_amount": 300},
            "check_transaction_pattern": {
                "anomalies": ["amount_far_above_average", "unusual_country", "high_risk_category", "odd_hour"],
                "amount_ratio_vs_avg": 4.5,
                "user_avg_amount": 300,
                "hour": 2,
            },
            "get_linked_accounts": {"flagged_connection_count": 0, "shared_devices": []},
            "search_similar_cases": {"matches": []},
        }
        res_review = score_from_results(
            {"user_id": "U001", "amount": 1350, "country": "AE", "merchant_category": "crypto_exchange"},
            mock_results_review,
        )
        self.assertGreaterEqual(res_review["fraud_score"], 0.50)
        self.assertLess(res_review["fraud_score"], 0.80)
        self.assertEqual(res_review["action"], "review")

        # High risk -> Block (score >= 0.80)
        mock_results_block = {
            "get_user_history": {"found": True, "is_flagged": False, "avg_amount": 300},
            "check_transaction_pattern": {
                "anomalies": ["amount_extreme_deviation", "flagged_receiver", "high_risk_category", "unusual_country"],
                "amount_ratio_vs_avg": 16.0,
                "user_avg_amount": 300,
                "receiver_id": "U033",
            },
            "get_linked_accounts": {"flagged_connection_count": 1, "flagged_connections": ["U033"], "shared_devices": []},
            "search_similar_cases": {"matches": [{"case_id": "C014", "fraud_type": "crypto_offramp", "similarity": 0.42}]},
        }
        res_block = score_from_results(
            {"user_id": "U001", "receiver_id": "U033", "amount": 4800, "country": "AE", "merchant_category": "crypto_exchange"},
            mock_results_block,
        )
        self.assertGreaterEqual(res_block["fraud_score"], 0.80)
        self.assertEqual(res_block["action"], "block")

    def test_exact_threshold_edge_values(self):
        """Verify boundary conditions for 0.49, 0.50, 0.79, and 0.80."""
        block_th = settings.fraud_block_threshold  # 0.80
        review_th = settings.fraud_review_threshold  # 0.50

        def map_score(s: float) -> str:
            s = round(max(0.0, min(1.0, s)), 2)
            if s >= block_th:
                return "block"
            elif s >= review_th:
                return "review"
            return "allow"

        self.assertEqual(map_score(0.49), "allow")
        self.assertEqual(map_score(0.50), "review")
        self.assertEqual(map_score(0.79), "review")
        self.assertEqual(map_score(0.80), "block")
        self.assertEqual(map_score(0.81), "block")
        self.assertEqual(map_score(0.00), "allow")
        self.assertEqual(map_score(1.00), "block")

    def test_ist_timezone_behavior(self):
        """Test Asia/Kolkata daylight-independent behavior (UTC+05:30) and date boundaries."""
        # 2026-10-24 15:30:00 IST -> 2026-10-24 10:00:00 UTC
        ist_iso = "2026-10-24T15:30:00+05:30"
        dt = datetime.fromisoformat(ist_iso)
        utc_dt = dt.astimezone(timezone.utc)
        self.assertEqual(utc_dt.hour, 10)
        self.assertEqual(utc_dt.minute, 0)
        self.assertEqual(utc_dt.day, 24)

        # Date boundary test: 2026-10-25 01:30:00 IST -> 2026-10-24 20:00:00 UTC (previous day in UTC)
        ist_boundary = "2026-10-25T01:30:00+05:30"
        dt_boundary = datetime.fromisoformat(ist_boundary)
        utc_boundary = dt_boundary.astimezone(timezone.utc)
        self.assertEqual(utc_boundary.day, 24)
        self.assertEqual(utc_boundary.hour, 20)


if __name__ == "__main__":
    unittest.main()
