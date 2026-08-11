# ERRORS.md — error journal

Every error logged in plain English: what it said, what caused it, how it was fixed. Built so future me can self-diagnose faster.

---

## 2026-06-30 — "invalid identifier" on a fully qualified table name

**Where:** dbt Cloud, `dbt build --select customers` on the Fundamentals quickstart.

**What Snowflake said:**
`000904 (42000): SQL compilation error ... invalid identifier 'ANALYTICS.DBT_GADEBAYO.STG_JAFFLE_SHOP__ORDERS'`

**Plain-English cause:**
The orders CTE inside `customers.sql` read `select {{ ref('stg_jaffle_shop__orders') }}` with no `* from` in front of it. `ref()` does not return a query, it returns a plain table name. So once compiled, the line became `select ANALYTICS.DBT_GADEBAYO.STG_JAFFLE_SHOP__ORDERS`, and Snowflake assumed that three-part name was a column to select. It went looking for a column by that name, found none, and called it an invalid identifier. Same mistake class as writing `select orders` instead of `select * from orders`.

**Fix:**
Added the missing clause so the CTE reads `select * from {{ ref('stg_jaffle_shop__orders') }}`, matching the customers CTE above it. Saved, then reran. Green.

**Lesson to keep:**
"Invalid identifier" naming a full `DATABASE.SCHEMA.OBJECT` path usually means a `ref()` with no `from` in front of it. Snowflake is reading the table name as a column. Also: in the dbt Cloud IDE you must Save before Run, because run/build use the saved file, not the editor buffer.

---

## 2026-07-10 — "unexpected 'limit'" when building fct_orders

**What Snowflake said:** `syntax error line 1 at position 0 unexpected 'limit'`

**Cause:** The model ended with a trailing semicolon (`group by 1,2;`). dbt wraps a model's SQL inside a bigger statement, and the IDE appends a `limit` for previews. The `;` closed the statement early, stranding the appended `limit` as its own invalid statement.

**Fix:** Removed the trailing semicolon. **dbt models never end with `;`.**

**Lesson:** "unexpected 'limit'" almost always means a trailing semicolon in a dbt model.

---

## 2026-07-10 — "invalid identifier 'O.USER_ID'" in fct_orders

**Cause:** Selected `o.user_id` from the orders staging model, but staging had renamed that column (to `customer_id`). A staging model's output columns are its `select` aliases; downstream models must use the new names, not the raw ones.

**Fix:** Referenced the actual staging column name.

**Lesson:** Two flavours of "invalid identifier" now seen. If it names a full **table path**, suspect a missing `from`. If it names a **table.column**, suspect a wrong or renamed column. Read *which kind* of identifier it points at.

---

## 2026-07-10 — "source named 'stripe.payment' which was not found"

**Cause:** `stg_stripe__payments` called `{{ source('stripe','payment') }}` but no sources YAML declared that source. `source()` is a pointer to a declaration that must exist.

**Fix:** Created `_src_stripe_sources.yml` declaring the stripe source (database `raw`, schema `stripe`, table `payment`).

**Lesson:** A "source not found" error means the `source()` call has no matching declaration in a sources `.yml`.

---

## 2026-07-10 — "ERROR STALE" on jaffle_shop / stripe (NOT a bug)

**Cause:** `dbt source freshness` reported the source as stale because `max(loaded_at_field)` was older than the `error_after` threshold. The course data is **frozen training data**, so it is always old.

**Fix:** None needed. The config is correct; the data is just static.

**Lesson:** ERROR STALE on the course data is expected. In a real company it would mean the pipeline stopped loading fresh data. The freshness check working is the point.

---

## 2026-07-28 — Snowflake trial expired, models could not build (infra, not code)

**Where:** dbt Cloud. Builds stopped working after the 30-day Snowflake trial ended.

**Plain-English cause:**
The trial warehouse was the compute + storage behind every model. When it expired, dbt Cloud still had all my code but had nothing to build against. The raw `jaffle_shop` and `stripe` tables lived *inside* that account and died with it. The dbt project (models, tests, commits) was untouched in the repo. What I lost was the rented engine and the raw data, not my work.

**Fix (four moves):**
1. Started a fresh Snowflake trial with a `+alias` email (`...+snow2@gmail.com`).
2. Re-ran the Fundamentals setup SQL to recreate `raw` + `analytics` databases, the `jaffle_shop`/`stripe` schemas, and reload the CSVs from `s3://dbt-tutorial-public/`. A NEW ACCOUNT IS EMPTY — the raw data does not come back on its own.
3. Re-pointed dbt Cloud: new account identifier on the **Connection** screen; new username/password on the **Development Credentials** screen (two separate places). Kept db/warehouse/schema names identical (`analytics` / `transforming` / `dbt_gadebayo`) so nothing downstream had to change.
4. Test Connection (green), then `dbt build` to repopulate `dbt_gadebayo`.

**Lesson:** Code and data are separate concerns. A dead warehouse is recoverable because the code is the source of truth and the raw data is reproducible from a load script. Also: dbt Cloud splits settings across two screens — shared **Connection** (account, db, warehouse) vs personal **Credentials** (username, password, schema). Also reconfirmed: raw columns are `user_id` and `orderid`; staging is where they become `customer_id` and `order_id`. That is what staging is for.
