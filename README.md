# Analytics Engineering Lab

Learning analytics engineering in public. This repository is the working record of a senior BI developer moving upstream into the data stack: the projects, the mistakes, and the reasoning behind both.

---

## Why I am doing this

I have spent my career at the **end** of the data lifecycle. As a Tableau developer and senior data analyst, I received data that was already loaded, already shaped, already decided, and my job was to turn it into dashboards and reports.

I want to understand what happens **before** that point.

How data is modelled and refined on its way through the warehouse. How raw source tables become something that actually resembles the business. How metrics get defined, and by whom, and what happens when two teams define the same one differently. The decisions that are already made by the time a dashboard exists, and that quietly determine whether the dashboard can be trusted.

There is also a forward-looking reason. As analytics moves toward agentic and natural-language interfaces, the **semantic layer** becomes the thing that makes those interfaces trustworthy. If a stakeholder asks a question in plain English, something has to know what "revenue" means, which tables relate to which, and which definition is authoritative. That is a modelling problem before it is an AI problem. Understanding how data connects, how context is captured, and how metrics are governed is what separates a useful answer from a confident wrong one.

Longer term, I want to lead a data team. That means understanding the whole pipeline, not just the last mile of it.

---

## What is in here

| File | Purpose |
|---|---|
| `PROGRESS.md` | Concepts covered, concepts still shaky, what is next |
| `ERRORS.md` | Every error hit, with the cause and fix in plain English |
| `CONTENT_IDEAS.md` | Moments worth writing about publicly |
| `MODELLING_MINDSET.md` | Notes on thinking in grain, facts, and dimensions |

The error journal is deliberate. Debugging is most of the job, and a record of how each error was reasoned through is more useful than a record of things that worked first time.

---

## The learning arc

**Stage A: dbt in the browser.** dbt Fundamentals via dbt Studio against Snowflake. Sources, staging and mart layers, `ref()` and `source()`, generic and singular tests, source freshness, documentation and lineage, deployment environments and jobs. **Completed August 2026.**

**Stage B: dbt Core locally.** The same projects run from the terminal against a local environment, to learn the plumbing that the browser IDE hides: virtual environments, `profiles.yml`, and running builds without a safety net.

**Applied projects.** After each milestone of the dbt Certified Developer path, a hands-on project applying it end to end, rather than a course exercise with the answer supplied.

**Ahead:** refactoring a large legacy analyst query into modular layers, MetricFlow semantic models and metrics, and connecting a natural-language interface to a governed semantic layer.

---

## Certifications

- **dbt Fundamentals**, dbt Labs, August 2026

---

## Current project

A fintech analytics project built on **dbt** against **Postgres**, applying everything from dbt Fundamentals to a dataset with no supplied answers. Customers, accounts, transactions, and payments, modelled from raw source tables through a staging layer into dimensional marts, with tests and documentation.

Architecture notes and lineage graphs will be added here as the project grows.

---

## Stack

dbt, Postgres, Snowflake, SQL, git. Previously and still: Tableau.
