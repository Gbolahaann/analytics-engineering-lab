# Apply Loop #1: Fintech Analytics

Applying dbt Fundamentals end to end, on a dataset with no supplied answers.

---

## The scenario

You have joined a UK digital bank as their first analytics engineer. Four raw tables have been dumped into the warehouse from three different source systems. Nobody has modelled them. The Head of Product and the Head of Risk both want answers, and right now every question requires someone to write bespoke SQL against raw tables.

Your job is to build the modelled layer that makes those questions routine.

---

## The raw data

Four CSVs in `seeds/`, loaded with `dbt seed`.

| Table | Roughly | From |
|---|---|---|
| `raw_customers` | 60 rows | CRM |
| `raw_accounts` | 123 rows | Core banking |
| `raw_transactions` | 601 rows | Core banking |
| `raw_payments` | 383 rows | Payment processor |

**This data is deliberately messy, in the ways real source data is messy.** Look at it before you write anything. Things you should expect to find and deal with, without me telling you where:

- The same entity is referenced by different column names in different tables.
- Money is not stored in the unit you want to report in.
- Status and country fields have inconsistent casing.
- Some nulls are genuine business facts, not errors. Some are not.
- There is at least one duplicated record.
- There are records referencing parents that do not exist.

**Do not fix the raw CSVs.** Raw data is what it is. Every fix belongs in a model.

---

## The questions the business needs answered

These drive your design. Do not start modelling until you can say which model answers which question.

1. How many customers do we have, split by KYC status and country?
2. What is total spend per customer per month?
3. Which merchants drive the most transaction volume and value?
4. What proportion of payments fail, and does that vary by payment method?
5. How many accounts does a typical customer hold, and how many are still active?

---

## Tasks

### Stage 1: sources

- [ ] Declare all four raw tables as sources in a properly named `.yml`.
- [ ] Configure **freshness** on the two tables that carry a load timestamp.
- [ ] Run `dbt source freshness` and be able to explain the result.

**Acceptance:** `dbt parse` succeeds, and `dbt source freshness` runs against exactly the tables that should have it.

### Stage 2: staging

- [ ] One staging model per raw table. No more, no less.
- [ ] Follow the import CTE pattern you learned in Fundamentals.
- [ ] Rename every key to a single consistent vocabulary across all four models.
- [ ] Cast types properly. Money should be reported in pounds, not pence.
- [ ] Clean the inconsistent categorical values.
- [ ] Materialise staging appropriately and be able to justify the choice.

**Acceptance:** every downstream model can join these together without a single rename or cast.

### Stage 3: marts

- [ ] Build the dimensional models needed to answer the five questions above.
- [ ] You decide how many, what grain, and what they are called. Justify each.
- [ ] Follow fact and dimension naming conventions.
- [ ] Materialise marts appropriately.

**Acceptance:** each of the five questions can be answered with a simple query against one mart, no joins back to staging.

### Stage 4: tests

- [ ] Every model has a primary key tested for `unique` and `not_null`.
- [ ] At least one `accepted_values` test on a cleaned categorical field.
- [ ] At least one `relationships` test between a fact and a dimension.
- [ ] At least one **singular** test expressing a business rule that generic tests cannot.
- [ ] Minimum twelve tests total.

**Acceptance:** `dbt build` runs and you can explain every failure. Some tests **should** fail on first run, because the data has real problems. Fixing a test to make it pass is only correct if the test was wrong.

### Stage 5: documentation

- [ ] Description on every model and every key column.
- [ ] `dbt docs generate`, then walk the lineage graph.
- [ ] Screenshot the lineage graph into the repo README.

### Stage 6: ship it

- [ ] Commit in logical chunks with your own messages, not one giant commit.
- [ ] Open a PR, merge to main.
- [ ] Deployment environment and a job that runs `dbt build` green.

---

## Design decisions to write down

Answer these in a `DECISIONS.md` in this folder as you go. This is the part that matters most, and the part a hiring manager will actually read.

1. What is the grain of each mart model, stated as "one row per ___"?
2. The duplicated record: how did you handle it, and where? Why there rather than somewhere else?
3. The orphaned records: are they a data quality bug to alert on, or a fact of life to filter? What did you choose and why?
4. Money in pence: which layer converted it, and why that layer?
5. Question 2 asks for spend per customer per month. Did you pre-aggregate that into a mart or leave it to the query? What did you trade off?
6. Which nulls did you decide were legitimate, and how did you stop a `not_null` test firing on them?

---

## Definition of done

- `dbt build` green, or every remaining failure explained and deliberate.
- All five business questions answerable from the marts.
- `DECISIONS.md` complete.
- Lineage graph in the README.
- Job running green in a deployment environment.

---

## Rules of engagement

I will not write your models. Bring me your SQL and I will review it, ask questions, and point at what you have not considered. Bring me your grain decisions before you build, because that is where the real thinking is and it is much cheaper to change on paper than in code.

Start with Stage 1. Do not skip ahead to marts.
