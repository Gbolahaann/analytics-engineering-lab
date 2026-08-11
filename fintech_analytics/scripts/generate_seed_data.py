"""
Generate synthetic raw data for the fintech analytics dbt project.

The output is deliberately messy in ways real source systems are messy:
inconsistent key naming across tables, amounts in minor units, inconsistent
casing on status fields, legitimate nulls, a duplicated row, and a few
orphaned foreign keys. Cleaning this up is the job of the staging layer.

Deterministic: same seed in, same CSVs out.
"""

import csv
import random
from datetime import datetime, timedelta
from pathlib import Path

random.seed(42)

# Anchor everything to a fixed date so regenerating gives identical output.
ANCHOR = datetime(2026, 8, 11)
SEEDS = Path(__file__).resolve().parents[1] / "seeds"
SEEDS.mkdir(parents=True, exist_ok=True)

FIRST = ["Amara", "Tolu", "James", "Priya", "Ade", "Sarah", "Chen", "Fatima",
         "Oliver", "Ngozi", "Daniel", "Aisha", "Marcus", "Yemi", "Hannah",
         "Ibrahim", "Grace", "Leo", "Zara", "Femi"]
LAST = ["Okafor", "Bello", "Wright", "Sharma", "Adeyemi", "Hughes", "Wang",
        "Hassan", "Clarke", "Eze", "Murphy", "Khan", "Bennett", "Ogun",
        "Reid", "Ali", "Thompson", "Rossi", "Ahmed", "Balogun"]

MERCHANTS = ["Tesco", "Amazon UK", "Shell", "Pret A Manger", "Uber", "Netflix",
             "Sainsburys", "TfL", "Deliveroo", "Boots", "John Lewis", "Spotify"]


def d(dt):
    return dt.strftime("%Y-%m-%d")


def ts(dt):
    return dt.strftime("%Y-%m-%d %H:%M:%S")


def write(name, header, rows):
    path = SEEDS / name
    with open(path, "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(header)
        w.writerows(rows)
    print(f"{name}: {len(rows)} rows")


# ---------------------------------------------------------------- customers
# Messy: key is cust_id here but referenced as cust_ref elsewhere.
# Status and country casing is inconsistent. Some emails missing.
customers = []
for i in range(1, 61):
    fn = random.choice(FIRST)
    ln = random.choice(LAST)
    signup = ANCHOR - timedelta(days=random.randint(30, 900))
    dob = datetime(random.randint(1960, 2004), random.randint(1, 12), random.randint(1, 28))
    email = f"{fn.lower()}.{ln.lower()}{i}@example.com" if random.random() > 0.05 else ""
    customers.append([
        i, fn, ln, email, d(dob), d(signup),
        random.choice(["GB", "GB", "GB", "gb", "IE", "US"]),
        random.choice(["verified", "VERIFIED", "verified", "pending", "rejected"]),
    ])

write("raw_customers.csv",
      ["cust_id", "fname", "lname", "email", "dob", "signup_dt", "country_cd", "kyc_status"],
      customers)


# ----------------------------------------------------------------- accounts
# Messy: foreign key to customers is called cust_ref, not cust_id.
accounts = []
acct_id = 1000
for c in customers:
    for _ in range(random.randint(1, 3)):
        acct_id += 1
        opened = ANCHOR - timedelta(days=random.randint(10, 850))
        accounts.append([
            acct_id, c[0],
            random.choice(["current", "savings", "credit", "current"]),
            d(opened),
            random.choice(["ACTIVE", "active", "active", "closed", "frozen"]),
            random.choice(["GBP", "GBP", "GBP", "EUR", "USD"]),
        ])

write("raw_accounts.csv",
      ["acct_id", "cust_ref", "acct_type", "opened_dt", "acct_status", "currency_cd"],
      accounts)


# ------------------------------------------------------------- transactions
# Messy: foreign key is acct_no here. Amounts in PENCE (minor units).
# merchant_nm and mcc_code are legitimately null for transfers.
# One row is duplicated on purpose (a double-posted transaction).
transactions = []
txn_id = 500000
for _ in range(600):
    txn_id += 1
    acct = random.choice(accounts)
    when = ANCHOR - timedelta(days=random.randint(0, 400),
                              hours=random.randint(0, 23),
                              minutes=random.randint(0, 59))
    kind = random.choices(["card_purchase", "transfer_in", "transfer_out",
                           "direct_debit", "refund"],
                          weights=[55, 12, 12, 16, 5])[0]
    is_merchant = kind in ("card_purchase", "direct_debit", "refund")
    amount_p = random.randint(150, 45000)
    if kind in ("card_purchase", "transfer_out", "direct_debit"):
        amount_p = -amount_p
    transactions.append([
        txn_id, acct[0], amount_p, acct[5], kind, ts(when),
        random.choice(MERCHANTS) if is_merchant else "",
        random.randint(5411, 7999) if is_merchant else "",
        ts(ANCHOR - timedelta(hours=random.randint(1, 8))),
    ])

# Deliberate duplicate: the same transaction posted twice.
transactions.append(list(transactions[10]))

write("raw_transactions.csv",
      ["txn_id", "acct_no", "txn_amt_pence", "txn_ccy", "txn_type", "txn_ts",
       "merchant_nm", "mcc_code", "_loaded_at"],
      transactions)


# ----------------------------------------------------------------- payments
# Messy: foreign key is txn_ref. Status casing inconsistent.
# Three rows deliberately reference transactions that do not exist (orphans).
payments = []
pmt_id = 900000
settled = random.sample(transactions[:600], 380)
for t in settled:
    pmt_id += 1
    processed = datetime.strptime(t[5], "%Y-%m-%d %H:%M:%S") + timedelta(hours=random.randint(1, 72))
    payments.append([
        pmt_id, t[0],
        random.choice(["card", "direct_debit", "bank_transfer", "standing_order"]),
        random.choice(["completed", "COMPLETED", "completed", "completed",
                       "failed", "pending", "refunded"]),
        abs(t[2]),
        ts(processed),
        ts(ANCHOR - timedelta(hours=random.randint(1, 12))),
    ])

for orphan in (999901, 999902, 999903):
    pmt_id += 1
    payments.append([
        pmt_id, orphan, "card", "completed", random.randint(500, 20000),
        ts(ANCHOR - timedelta(days=random.randint(1, 60))),
        ts(ANCHOR - timedelta(hours=random.randint(1, 12))),
    ])

write("raw_payments.csv",
      ["pmt_id", "txn_ref", "pmt_method", "pmt_status", "pmt_amt_pence",
       "processed_at", "_batched_at"],
      payments)

print(f"\nWritten to {SEEDS}")
