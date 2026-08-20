# Design decisions

The reasoning behind the modelling choices in this project. Each entry records what was found, what it means in business terms, what was decided, and why that layer rather than another.

---

## 1. Duplicated transaction: `txn_id = 500011`

**Found:** The `unique` test on `core_banking.raw_transactions.txn_id` failed on one row. Investigating the two rows showed they are **identical across every column**, including the amount, the timestamp and the load timestamp.

**What it means:** This is not two different transactions colliding on an ID, which would be serious. It is the same transaction recorded twice, most likely a retry that posted successfully on both attempts. The second row carries no information the first does not.

**Decision:** Deduplicate in the **staging** layer, keeping one row.

**Why dropping is safe:** Because the rows are identical, there is no question of which transaction survives. They are indistinguishable, so removing the repetition is lossless. Had the rows differed in any column, dropping one would have destroyed a real event, and the correct response would have been to escalate to the source system owner rather than resolve it here.

**Why staging:** Staging exists to present a clean, one-row-per-entity view of a source. Fixing it here means no downstream model needs to know that this source system double-posts. The alternative, leaving it to the marts, would mean every mart handling the same quirk independently, and eventually one of them forgetting.

**How it stays visible:**
- A `unique` test on the **staging model**, not only on the source. This proves the deduplication works, and will fail loudly if the source's behaviour ever changes into something the current logic does not handle.
- Documented in the staging model's description, so it surfaces in `dbt docs` where someone outside the codebase can find it.

---

## 2. Orphaned payments: `txn_ref` 999901, 999902, 999903

**Found:** The `relationships` test on `payment_processor.raw_payments.txn_ref` failed on three rows referencing transactions that do not exist in `core_banking.raw_transactions`.

**What it means, and there are two answers:** Checking `processed_at` on the three rows showed they are not a single problem.

- **Two are recent (August).** Payments and transactions arrive from two different source systems on two different load schedules, so a payment can legitimately land before the transaction it refers to. These are plausibly late-arriving and may resolve on the next load.
- **One is roughly a month older (June).** That is too old to be in flight. The transaction it refers to is not coming, so this is a genuinely broken reference rather than a timing artefact.

The general lesson: when a test fails on N rows, the N rows do not necessarily share a cause.

**Decision:** Do not filter silently. Instead:

1. **Downgrade the generic test to a warning with thresholds:** warn above 5 orphaned rows, error above 20. A handful of orphans is normal turbulence between two feeds on different schedules, assuming their processing times are not far apart. Twenty means the integration itself has broken. A build that fails every morning over two rows that resolve by lunchtime trains people to ignore alerts.

2. **Add a singular test for orphan age.** Row counts cannot distinguish the two causes: three orphans look identical to a `relationships` test whether they are three hours or three months old. Age is the real discriminator, and expressing it needs a bespoke query. An orphan older than **7 days** is treated as a genuine failure, on the basis that this is a high-volume business where transactions flow daily, so a week is far longer than any plausible load lag.

   The two tests cover different failure modes and are deliberately complementary. The generic test watches for a **volume spike**, meaning the integration has broken. The singular test watches for **staleness**, meaning a specific record never arrived. Note that today's three orphans sit below the generic test's warn threshold and pass it silently; the singular test is what surfaces the June row.
3. **Escalate the June row** to the owner of the payment feed. This project cannot fix a missing transaction, and raising it is the only route to it ever being fixed upstream.
4. **Handle it per mart, not globally.** This is the substantive modelling decision:
   - An orphaned payment **still happened**; money moved. It belongs in payment-level measures such as total payments processed by method.
   - It has **no path to a customer**, because the route runs payment → transaction → account → customer and the chain breaks at the first step. So it must be excluded from customer-level measures such as spend per customer.

   The same three rows are therefore included in one mart and excluded from another, and both are correct. The question is not "filter or keep" but "what is this model for."

**Principle applied:** Silent filtering is the worst available option. It makes warehouse totals disagree with the source system for reasons nobody can trace, and it guarantees the upstream bug is never fixed because nobody upstream is ever told. Where records are excluded, the exclusion is documented, tested and countable.

---

## 3. Source freshness reports permanent ERROR STALE

**Found:** `dbt source freshness` returns ERROR STALE for both configured sources.

**What it means:** Not a defect. The load timestamps live inside the seed CSVs and were written once when the data was generated, so no run can freshen them. Re-running `dbt seed` reloads the same frozen values.

**Why it is configured anyway:** Freshness monitors an ingestion pipeline's heartbeat. Seeds have no pipeline, so the check measures nothing real here. It is configured to exercise the mechanics, and because a production version of this project would read from continuously loaded sources where the check would be meaningful.
