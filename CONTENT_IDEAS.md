# CONTENT_IDEAS.md — LinkedIn / blog moments

Captured moments worth posting about, with the angle. I do not write the posts, just flag them.

---

## 2026-06-30 — "Reading a dbt error as a BI person"
**Angle:** A senior Tableau/SQL analyst learning dbt hits `invalid identifier 'ANALYTICS.DBT_GADEBAYO.STG_JAFFLE_SHOP__ORDERS'`. Instead of panicking, decode it: it is Snowflake saying it read a table name as a column, because a CTE was missing its `from`. The transferable skill is not dbt trivia, it is learning to read compiled SQL and trace an error back to one line. Good story about how BI fundamentals (you already read SQL errors all day) make the AE transition faster than it looks.
**Format:** short carousel or text post with the error screenshot and the one-line fix.

## 2026-07-28 — "My data warehouse expired mid-course. Nothing was lost."
**Angle:** The Snowflake trial died and for a second it felt like the project was gone. It was not. The models, tests and git history were untouched, because in analytics engineering your *code* is the source of truth and the *data* is reproducible from a load script. Rebuilding meant: new warehouse, re-run the seed SQL, re-point the connection, `dbt build`. The mindset shift for a BI person: dashboards feel fragile because they are welded to a live data source; a dbt project is portable because the transformation logic lives in version control, independent of any one warehouse. That separation of code from compute is the whole point of the discipline.
**Format:** short reflective text post. Strong because it reframes a "disaster" as a demonstration of why the AE way is more robust than the classic BI way.

## 2026-08-05 — "Two teams want the same metric. They mean different things."
**Angle:** Marketing and Product both ask for customer lifetime value, with quietly different definitions. The junior move is to pick one and ship. The right move is to make the disagreement explicit: get both definitions stated as arithmetic, and if they genuinely differ, they are two metrics that need two names (`clv_predicted_12m` vs `clv_realised_net`), each owned and documented. The cardinal sin is two things with the same name returning different numbers. As a BI person I have sat in the "which number is right" meeting many times; analytics engineering does not make that disagreement disappear, it makes it *visible and versioned* instead of buried in a calculated field. Ties to why the semantic layer exists.
**Format:** text post. Strong because it is about judgement and stakeholder handling, not syntax, which is what actually separates senior from junior.

## 2026-06-30 — "Save is not Commit (and neither is typing)"
**Angle:** The three gates in the dbt Cloud IDE — type, save, commit — mapped to a Tableau mental model (editing a calc field vs clicking OK vs publishing to Server). A small thing that trips up every newcomer, explained by someone who just tripped on it.
