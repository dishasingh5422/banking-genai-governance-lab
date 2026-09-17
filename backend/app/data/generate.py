from __future__ import annotations

from pathlib import Path

import numpy as np
import pandas as pd


def generate_banking_data(output_dir: Path, seed: int = 20260917, customers: int = 5000) -> dict[str, Path]:
    rng = np.random.default_rng(seed)
    output_dir.mkdir(parents=True, exist_ok=True)

    customer_ids = np.array([f"CUS-{i:06d}" for i in range(1, customers + 1)])
    age = rng.integers(21, 76, customers)
    tenure = rng.integers(1, 181, customers)
    digital_adoption = rng.beta(2.4, 1.8, customers).round(4)
    utilization = np.clip(rng.beta(2.1, 3.2, customers) * 1.15, 0, 1).round(4)
    payment_ratio = np.clip(rng.normal(0.86, 0.17, customers), 0.1, 1.2).round(4)
    complaints = rng.poisson(0.55, customers)
    late_payments = rng.poisson(0.65 + utilization * 1.5, customers)
    service_calls = rng.poisson(1.1 + complaints * 0.7, customers)
    digital_sessions = rng.poisson(8 + digital_adoption * 24, customers)

    logit = (
        -1.4
        + 2.0 * utilization
        - 1.5 * payment_ratio
        + 0.33 * complaints
        + 0.28 * late_payments
        + 0.16 * service_calls
        - 0.018 * tenure
        - 0.65 * digital_adoption
    )
    attrition_probability = 1 / (1 + np.exp(-logit))
    attrited = rng.binomial(1, attrition_probability)

    customer_frame = pd.DataFrame(
        {
            "customer_id": customer_ids,
            "age": age,
            "age_group": pd.cut(age, bins=[20, 34, 49, 64, 80], labels=["21-34", "35-49", "50-64", "65+"]).astype(str),
            "region": rng.choice(["NORTH", "SOUTH", "EAST", "WEST"], customers),
            "segment": rng.choice(["MASS", "AFFLUENT", "EMERGING"], customers, p=[0.58, 0.18, 0.24]),
            "tenure_months": tenure,
            "digital_adoption": digital_adoption,
            "credit_utilization": utilization,
            "payment_ratio": payment_ratio,
            "complaints_90d": complaints,
            "late_payments_6m": late_payments,
            "service_calls_90d": service_calls,
            "digital_sessions_30d": digital_sessions,
            "attrited": attrited,
        }
    )

    transaction_count = int(customers * 12)
    transaction_customers = rng.choice(customer_ids, transaction_count)
    transaction_frame = pd.DataFrame(
        {
            "transaction_id": [f"TXN-{i:08d}" for i in range(1, transaction_count + 1)],
            "customer_id": transaction_customers,
            "transaction_date": pd.Timestamp("2026-08-31") - pd.to_timedelta(rng.integers(0, 90, transaction_count), unit="D"),
            "channel": rng.choice(["CARD", "MOBILE", "WEB", "ATM"], transaction_count, p=[0.48, 0.25, 0.17, 0.10]),
            "amount": np.round(rng.lognormal(4.0, 0.85, transaction_count), 2),
            "declined": rng.binomial(1, 0.035, transaction_count),
        }
    )

    paths = {"customers": output_dir / "customers.csv", "transactions": output_dir / "transactions.csv"}
    customer_frame.to_csv(paths["customers"], index=False)
    transaction_frame.to_csv(paths["transactions"], index=False)
    return paths
