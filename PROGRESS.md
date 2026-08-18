# PROGRESS.md — analytics engineering learning tracker

Tracks the dbt / analytics engineering journey. Concepts covered, concepts shaky, what is next.
(SQL practice on Stratascratch is tracked separately.)

Plan: dbt Fundamentals in dbt Cloud first (Stage A), then mirror locally in dbt Core + DuckDB (Stage B).

---

## Concepts covered
- **Environment setup:** personal Snowflake trial (kept separate from employer), dbt Cloud connected to it. Account identifier format (`ORG-ACCOUNT`, no domain suffix). Role / Database / Warehouse fields and what each is for.
- **Project structure:** staging models vs marts; `models/` folder; `dbt_project.yml`.
- **`ref()`:** compiles to a plain table name and records the dependency, so dbt builds models in the right order. Bridge: pointing a workbook at a published data source.
- **`ref()` graph operators:** `+model` builds it and its ancestors (upstream); `model+` builds it and descendants (downstream). Plus points the side data flows from.
- **`dbt run` / `dbt build`:** builds models in dependency order.
- **Reading errors:** decoding Snowflake compilation errors via dbt. Four distinct ones logged (see ERRORS.md): ref-with-no-from, trailing-semicolon, renamed-column, source-not-found.
- **Save vs commit:** three gates — type, Save (what runs), Commit (what reaches git history). main is protected, so commits go to a branch (branch-and-PR workflow).
- **Git model:** branch = a line of work / parallel copy; commit = a save point on it; many commits per branch, new branch per unit of work. Switching branches swaps which version the editor shows; main is untouched by experiment branches. File markers: A=added, M=modified; folder dots = changes inside; tab dot = unsaved.
- **`source()` vs `ref()`:** `source()` points at raw declared in a sources `.yml`; `ref()` points at a model dbt built. Staging reads from `source()`, everything else from `ref()`.
- **Staging conventions:** import CTE pattern (`source` CTE then `renamed` CTE then `select * from renamed`); rename/cast in staging so downstream inherits one clean vocabulary.
- **Source freshness:** `loaded_at_field` (the load-timestamp column — NO default, dataset-specific: jaffle_shop=`_etl_loaded_at`, stripe=`_batched_at`) + `warn_after`/`error_after` thresholds set to the load cadence + buffer. `dbt source freshness` checks only sources that declared it. `freshness: null` on a table opts it out. Source-level config = default for all tables; table-level = that table only.
- **Materializations:** view (stores the query, always fresh, slower = Tableau live connection) vs table (stores rows, fast, can go stale = extract). Views for staging, tables for heavily-queried marts.
- **Dimensional modelling:** fact (events/measures, one row per order = `fct_orders`) vs dimension (entities you slice by, one row per customer = `dim_customers`). Dimensions aggregate facts. Put measures in the fact so they are computed once and reused (DRY). Grain-first thinking (see MODELLING_MINDSET.md).
- **Packages / codegen:** a package = reusable macros installed via `packages.yml` + `dbt deps`. `codegen` auto-generates boilerplate (source YAML, staging SQL) as a draft to refine.
- **YAML styles:** block style (indented lines) vs flow style (`{count: 12, period: hour}`) are identical to dbt; flow is compact but braces must balance.
- **Deprecation:** a warning (not error) that an old way still works but is scheduled for removal; migrate before upgrading.
- **Warehouse portability / recovery:** re-pointed dbt Cloud at a new Snowflake account after the trial expired. Learned code and data are separate: the project survives, raw data is reloaded from a setup script. dbt Cloud settings split across shared **Connection** (account id, db, warehouse) vs personal **Credentials** (username, password, schema). Reuse the same db/warehouse/schema names to avoid downstream changes. Always Test Connection before running.

## Concepts shaky / to firm up
- The full save -> run -> commit -> PR -> merge loop end to end (done up to commit; PR/merge still to do).
- Whether the current dbt Cloud project is a dbt-managed repo or my own public GitHub repo (needs checking for portfolio visibility).
- Intermediate models (between staging and marts) — not covered yet.

## The Apply Loop (agreed 2026-07-31)

For every milestone of the dbt Certified Developer path, do a hands-on application project. **One growing fintech project**, not a fresh one per milestone, so the lineage graph and portfolio value compound.

**The repeatable loop:**
1. I finish the dbt Learn course(s) for a milestone and say so.
2. Mentor generates a fintech mock dataset exercising that milestone, plus the Snowflake load SQL.
3. Mentor hands over a challenge brief: ordered tasks with acceptance criteria, no answers.
4. I build the models and tests myself. Mentor reviews, questions, hints. Mentor does not write them.
5. Debrief: teach-back, update PROGRESS/ERRORS, capture content moments, commit and push.

**Domain:** fintech (customers, accounts, transactions, payments, card events). Data grows over time so snapshots have changing records, incremental models have timestamped events, exposures have downstream consumers.

**The path's 5 milestones** (from dbt Learn, study guide now v1.11):
1. Build a Foundation: Fundamentals, Materializations, Refactoring SQL for Modularity, Analyses & Seeds, Python Models, Grants, Snapshots, Incremental Models, Jinja/Macros/Packages
2. Govern and Debug: dbt Mesh, Debug Errors
3. Resilient Pipelines at Scale: Advanced Testing, Exposures, Unit Testing, State, dbt retry, dbt Clone
4. Exam Preparation: study guide v1.11
5. Exam Registration

Note: most courses ship in both dbt Studio and VS Code flavours. The VS Code versions are a built-in on-ramp to Stage B (local dbt Core).

## Milestones
- **2026-08-11: dbt Fundamentals (dbt Studio) COMPLETED.** Certificate issued by dbt Labs. Covered: connections, sources, staging/marts modelling, ref/source, tests, docs, deployment environments and jobs.

- **2026-08-12: Full project scaffolding assembled.** Public repo live (github.com/Gbolahaann/analytics-engineering-lab) with journals, README, Fundamentals export, and the fintech project. Neon Postgres connected to dbt platform (SSL via extended attributes, prod profile `neon-postgres-prod` → schema `analytics`, dev credentials → `dbt_gadebayo`). Production + Development environments configured. `dbt seed` green: 4 raw tables loaded into Neon.

## Concepts covered (additions)
- **Git from the terminal:** init, gitignore-before-first-commit, staging area, commit message conventions (imperative, ~50-char summary, body for detail; describe the diff, not actions taken elsewhere), gh repo create, push. Commit what you author; ignore what is generated or secret.
- **dbt platform settings hierarchy:** connection (where the warehouse is) → credentials (who logs in) → extended attributes (adapter options the UI lacks). Project/environment picks the connection; profiles bundle connection + deployment credentials for jobs.
- **Dev/prod schema separation in practice:** personal dev schema `dbt_gadebayo` vs deployment schema `analytics`; environment types (Development vs Deployment, and PROD designation).
- **Seeds:** version-controlled CSVs loaded with `dbt seed` — the data ships with the repo, so the whole project is reproducible by anyone who clones it.

## Concepts covered (2026-08-14)
- **Modelling without an ERD:** you derive the ERD from evidence — column-name clues, cardinality probes (`count(*)` vs `count(distinct)`), join success-rate tests, row-count ratios, and the business questions. The investigation becomes the first draft of the test suite.
- **Pull from remote:** every git clone (terminal, Studio IDE, GitHub) is a full independent copy; pull brings remote commits down, push sends local commits up. Habit: pull at session start, push at session end.
- **Freshness criterion sharpened:** freshness is only mechanically possible where a load timestamp exists (`_loaded_at`, `_batched_at`); it monitors an ingestion pipeline's heartbeat, not the data itself. Thresholds = load cadence + buffer. Seeds have no pipeline, and frozen CSV timestamps mean ERROR STALE forever — expected, not a bug.
- **Key vocabulary decided:** customer_id, account_id, transaction_id, payment_id — one canonical name per entity across all staging models, applied to both PK and FK columns.

## Concepts covered (2026-08-18) — Stage 1 COMPLETE
- **Sources declared across three source systems:** `crm`, `core_banking`, `payment_processor`, each in its own folder under `models/staging/` with its own `_src_*.yml`. Source `name:` is the logical alias used in code; `schema:` is the physical location. Decoupling them means raw data can move without touching any model.
- **`source()` vs `ref()` inside a sources file:** `ref()` claims dbt built the thing. Using it on a source does not just read oddly, it draws the wrong edge in the DAG and makes the lineage graph lie about provenance.
- **Freshness cadence, established not guessed:** ask the pipeline owner, read the ingestion tool's schedule, or measure gaps in `loaded_at` from the data itself. `warn_after` = cadence + one missed cycle (technical). `error_after` = when a stakeholder would act on something untrue (a business SLA).
- **Reading parse errors:** skip the dict dump, go to the last line, read `at path ['tables'][3]['freshness']` as zero-indexed coordinates, compare the flagged block against a working one. Runtime errors name a database problem; parse errors name a file and a path.
- **`dbt parse` covers the whole project**, always. Parsing is all-or-nothing; `--select` filters execution afterwards, never parsing. Parse never touches the warehouse, so it is free and fast.
- **`packages.yml` vs `package-lock.yml`:** what you asked for vs what you got (exact resolved versions). Commit both; `dbt_packages/` stays ignored. Same pattern as a requirements file vs a lockfile.
- **Generic tests are just SQL you already write.** `unique` = group by, count, having count > 1. `relationships` = anti-join for unmatched keys. dbt's value is not clever SQL, it is running the check automatically forever instead of it living in someone's head.
- **Read WHICH test failed, do not infer.** `source_unique_...` failing means duplicates, not nulls. Independent failures have independent causes; matching them by count (1 vs 3) disproves a shared cause. Then verify with the compiled SQL rather than theorising.

## Data quality defects found in the raw data (Stage 1 findings)
- **Duplicate:** `raw_transactions.txn_id = 500011` appears twice (failed `unique`).
- **Orphans:** `raw_payments.txn_ref` values `999901`, `999902`, `999903` reference transactions that do not exist (failed `relationships`).
- Both sources permanently ERROR STALE, as expected: seed timestamps are frozen in the CSVs, so even re-running `dbt seed` cannot freshen them.

## Next
- Migrate generic test args to the new `arguments:` nesting (deprecation warning on parse).
- **DECISIONS.md:** the duplicate — where to handle it and why there? The orphans — alert-worthy bug or fact of life to filter?
- Then Stage 2: staging models using the agreed vocabulary (customer_id / account_id / transaction_id / payment_id).
- Grain decisions for marts come to the mentor BEFORE building.
- Commit the uncommitted work on `Gbolahaann-patch-1` (stripe staging + source, fct_orders, dim_customers refactor, freshness config).
- Confirm where the dbt Cloud project pushes to (managed vs my own public GitHub repo).
- Continue Fundamentals: tests, then `dbt docs generate` and the lineage graph.
- Later: open the PR and merge the branch to main, to complete the git loop.
