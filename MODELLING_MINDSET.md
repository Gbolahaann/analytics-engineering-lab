# MODELLING_MINDSET.md — the analytics engineering thinking checklist

A reference to run through every time I read or build a model. The mindset is not a book of patterns to memorise. It is a small set of questions asked every single time until they become automatic.

---

## The four questions

1. **What is the grain?**
   One row per *what*? Per order, per customer, per customer per day? If I cannot say it in one sentence, I do not understand the model yet.

2. **Is this a fact or a dimension?**
   Fact = events and measures I sum and count (orders, payments). Dimension = entities I describe and slice by (customers, products).

3. **Where does this calculation belong so it lives in exactly one place?**
   If two models would compute the same thing, one of them is wrong. Push shared logic down a layer.

4. **What does this depend on, and does the lineage read cleanly?**
   raw -> staging -> fact -> dimension, each layer leaning on the one below through `ref()`.

---

## The master habit: grain first, SQL second

Most modelling bugs are grain problems in disguise. Before writing anything, say out loud:

> "This model is one row per ___."

Then check that every join and every `group by` respects that answer. Get both sides of a join to the same grain before joining.

---

## The layers, and what each is for

- **Staging:** clean one raw source. Rename, cast, tidy. No joins, no business logic. One job per source.
- **Intermediate / fact:** reshape and combine. Joins and deliberate grain changes happen here. Measures get computed here.
- **Marts (facts + dimensions):** business-ready models people actually query. Dimensions aggregate facts.

Stuck? Ask "which layer does this belong in" and the mess usually sorts itself.

---

## Tableau bridges (my unfair advantage)

I already think this way from years in Tableau. dbt just makes it explicit and versioned.

- A `{ FIXED [Customer] : SUM([Amount]) }` LOD calc *is* a grain change.
- A published, governed data source *is* a mart.
- A star schema (fact surrounded by dimensions) *is* the fact/dimension split.
- Renaming a field in a prepped data source, and every workbook inheriting it, *is* how staging renames flow downstream.

When a dbt idea feels abstract, ask "what is this in Tableau." I usually already know it.

---

## How to build the muscle (reps, not reading)

- **Narrate grain on everything.** State the grain in one sentence before touching a model.
- **Play "where does this belong."** Any calc another model might need gets pushed down a layer.
- **Refactor my own work.** Compare my first attempt to a better version (like turning my dim_customers into the exemplar's fact-then-dimension design). Best single exercise.
- **Read good projects.** dbt Labs jaffle_shop and a few public dbt repos, asking "why is this its own model."
- **Phase 2 of the mentorship** (splitting a big messy query into staging + marts) is the deliberate practice for exactly this.

---

## The signal I have got it

I stop *thinking about* grain and layering and start *seeing* them. Given any model, the first thing my eye finds is its grain, and misplaced logic looks wrong the way a broken formula looks wrong in Tableau.
