# Morocco Retail Intelligence --- Project Handoff & Learning Guide

> **Purpose:** This document is the single source of truth for
> continuing this project in a new ChatGPT conversation. Keep it in the
> repository root as `PROJECT_CONTEXT.md`. If a conversation is lost,
> upload this file and say: "Continue the Morocco Retail Intelligence
> project from this handoff. Keep the same step-by-step teaching
> approach and current progress."

## 1. Project identity

**Project name:** Morocco Retail Intelligence\
**Repository/folder name:** `morocco-retail-intelligence`\
**Project type:** Portfolio-grade data analytics and backend
application\
**Business scenario:** A fictional Moroccan e-commerce retailer wants to
understand sales, customers, products, delivery performance, payments,
and customer satisfaction.

The project must be valuable as a GitHub portfolio project, not merely a
set of unrelated exercises. It should demonstrate the ability to
investigate imperfect business data, clean and combine datasets, derive
useful business insights, communicate findings through visualizations,
and expose selected analytics through a documented API.

All provided data is synthetic. It does not represent real Moroccan
businesses, customers, or transactions.

## 2. Learning objectives

By completing the project, the learner should be able to:

-   Use Python in a structured, reproducible project.
-   Inspect, clean, validate, join, aggregate, and analyze tabular data
    with Pandas.
-   Perform exploratory data analysis (EDA) and translate business
    questions into measurable KPIs.
-   Create clear, honest, professional visualizations with Matplotlib
    and Seaborn.
-   Explain analytical decisions, assumptions, limitations, and
    findings.
-   Build REST endpoints with FastAPI and validate data with Pydantic.
-   Work with PostgreSQL and SQLAlchemy.
-   Write automated tests with Pytest.
-   Use Git/GitHub, documentation, environment configuration, and
    Docker.
-   Optionally add a predictive analytics extension later.

### NumPy learning decision

Do **not** teach NumPy as a standalone subject at this stage. Pandas
depends on NumPy internally, so NumPy may be installed transitively and
may appear indirectly in stack traces or package metadata. That is fine.
Avoid NumPy-specific lessons and exercises until the learner reaches the
relevant algebra or LLM foundations lessons. Do not attempt to uninstall
NumPy if another library requires it.

## 3. Teaching and collaboration rules

The learner wants to work **step by step**, with explanations, practice,
and feedback---not receive a complete solution to copy.

For each phase:

1.  Explain the business purpose and the concepts needed for the current
    step.
2.  Give a small, clearly scoped task.
3.  Provide the relevant dataset and explain its columns/relationships
    when needed.
4.  Let the learner write the code.
5.  Review the learner's code and output; explain errors and
    improvements.
6.  Ask for interpretation, not only code output.
7.  Agree on a deliverable before moving to the next step.

Do not skip ahead or dump the entire implementation. Do not provide
solutions immediately when an exercise is intended for practice. Give
hints first when appropriate. Keep the project technically coherent and
update this handoff whenever major decisions or progress change.

The learner prefers professional project practices, including TOML
configuration and a clean repository structure.

## 4. Technology choices

  Technology               Planned role                                      Introduction
  ------------------------ ------------------------------------------------- ----------------------
  Python 3.12              Main language                                     Setup
  `uv`                     Project, environment, and dependency management   Setup
  `pyproject.toml`         Project metadata and tool configuration           Setup
  `uv.lock`                Reproducible dependency lockfile                  Setup
  Pandas                   Data inspection, cleaning, joins, analysis        Phases 1--3
  Matplotlib               Foundational plotting                             Phase 4
  Seaborn                  Statistical and analytical plots                  Phase 4
  JupyterLab / IPykernel   Interactive exploration                           Phases 1--4
  Ruff                     Linting and formatting                            Setup and throughout
  Pytest                   Automated tests                                   Setup and throughout
  FastAPI                  Analytics REST API                                Phase 5
  Pydantic                 API input/output validation                       Phase 5
  PostgreSQL               Persistent relational storage                     Phase 6
  SQLAlchemy               Python database integration                       Phase 6
  Docker                   Reproducible packaging/deployment                 Phase 7
  Scikit-learn             Optional predictive analytics                     Optional extension

Install libraries when their phase begins, rather than installing every
possible dependency on day one. Use `uv add <package>` for runtime
dependencies and `uv add --dev <package>` for development tools. Use
`uv sync` after dependency/configuration changes. Commit
`pyproject.toml` and `uv.lock`; do not commit `.venv`.

## 5. Business questions the project should answer

The final analysis should answer questions such as:

1.  What is the total value of delivered sales, and how is it defined?
2.  How do sales and order volume change over time?
3.  Which product categories and products perform best?
4.  Which cities contribute most to sales and order volume?
5.  What is the average order value (AOV)?
6.  What are the customer segments and repeat-purchase patterns?
7.  Which payment methods are used, and what are their payment outcomes?
8.  How long does delivery take, and does it vary by city?
9.  What is the distribution of customer ratings?
10. Are there patterns between delivery performance and customer
    satisfaction?

**Important analytical rule:** Never silently treat every order as
revenue. Cancelled and returned orders must be handled explicitly.
Define the population and metric for each KPI, document assumptions, and
check that joins do not multiply amounts unexpectedly.

## 6. Dataset supplied for the project

Download archive: `morocco_retail_intelligence_dataset.zip`\
The archive contains the six CSV files, `README_DATA.md`, and a starter
`README.md`.

The files should be extracted into the project at `data/raw/`.

  ------------------------------------------------------------------------
  File                              Approximate rows Columns / purpose
  --------------------- ---------------------------- ---------------------
  `customers.csv`                              1,000 Customer profile,
                                                     city, segment, signup
                                                     date

  `products.csv`                                 100 Product catalog,
                                                     category, unit/cost
                                                     prices, stock status

  `orders.csv`                                 3,205 Orders, customer,
                                                     date, status,
                                                     delivery, city,
                                                     shipping fee

  `order_items.csv`                            5,376 Products and
                                                     quantities per order,
                                                     unit price, discount,
                                                     line total

  `payments.csv`                               3,200 Payment method,
                                                     status, payment
                                                     amount

  `reviews.csv`                                2,019 Review, order,
                                                     customer, rating,
                                                     date, comment
  ------------------------------------------------------------------------

The order count includes five deliberately duplicated rows in
`orders.csv`. The row counts are the original generated counts and
should be verified by the learner after extraction.

### Dataset relationships

-   `customers.customer_id` → `orders.customer_id`
-   `orders.order_id` → `order_items.order_id`
-   `products.product_id` → `order_items.product_id`
-   `orders.order_id` → `payments.order_id`
-   `orders.order_id` → `reviews.order_id`

### Data notes and intentional quality issues

-   Currency: Moroccan dirham (MAD).
-   Dates cover 2024 and 2025.
-   Data is synthetic and generated for this learning project.
-   `orders.csv` contains five duplicated rows.
-   Some customer ages are missing.
-   Some shipping fees are missing.
-   Some review comments are missing.
-   Order statuses include `Delivered`, `Cancelled`, `Returned`, and
    `Processing`.
-   Payment statuses include `Paid`, `Refunded`, and `Failed`.
-   `order_items.line_total_mad` is the line total after discount and
    excludes shipping.
-   An order can contain multiple order items.
-   There is one generated payment row per original order.
-   Reviews exist only for a subset of delivered or returned orders.
-   Do not "fix" the raw files directly. Preserve raw data and create
    cleaned/processed outputs separately.
-   Verify primary-key uniqueness and referential integrity rather than
    assuming they are valid.

### Dataset acquisition

The original archive was supplied in the conversation as a downloadable
attachment. If it is not available in a new conversation, ask the
learner to upload it again or regenerate a compatible synthetic dataset.
Do not pretend to have access to a previous sandbox file if it is not
attached or available.

## 7. Project setup --- completed

The learner reports that the initial setup is now working.

### Environment

-   Operating system: Windows.
-   Editor: VS Code.
-   Shell examples: PowerShell.
-   Python target: 3.12.
-   Package/environment manager: `uv`.
-   Project initialized with:

``` powershell
uv init --package --python 3.12
```

### Dependency commands used

``` powershell
uv add pandas
uv add --dev jupyterlab ipykernel ruff pytest
uv sync
```

### Current intended Ruff and Pytest configuration

These sections were added to `pyproject.toml`:

``` toml
[tool.ruff]
line-length = 88
target-version = "py312"

[tool.ruff.lint]
select = ["E", "F", "I", "UP", "B"]

[tool.pytest.ini_options]
testpaths = ["tests"]
pythonpath = ["src"]
```

`uv` owns the project metadata and dependency sections in
`pyproject.toml`. Do not overwrite those sections blindly; inspect the
existing file before suggesting changes.

### Verification commands

``` powershell
uv sync
uv run ruff check .
uv run python --version
uv run python -c "import pandas; print(pandas.__version__)"
```

The learner says everything is OK. Exact installed package versions have
not been recorded in this handoff; the authoritative versions are in the
project's `uv.lock`.

### Git commands already recommended

``` powershell
git init
git add .
git commit -m "chore: initialize professional project structure"
```

The learner was asked to initialize Git and make the first commit.
Confirm whether the commit was actually made before assuming it exists.

## 8. Target repository structure

The intended structure is:

``` text
morocco-retail-intelligence/
│
├── .python-version
├── .gitignore
├── pyproject.toml
├── uv.lock
├── README.md
├── PROJECT_CONTEXT.md
│
├── data/
│   ├── raw/
│   │   ├── customers.csv
│   │   ├── products.csv
│   │   ├── orders.csv
│   │   ├── order_items.csv
│   │   ├── payments.csv
│   │   └── reviews.csv
│   └── processed/
│
├── notebooks/
│   ├── 01_data_understanding.ipynb
│   ├── 02_data_cleaning.ipynb
│   ├── 03_exploratory_analysis.ipynb
│   └── 04_visualization.ipynb
│
├── src/
│   └── morocco_retail_intelligence/
│       ├── __init__.py
│       ├── main.py
│       ├── analysis/
│       ├── visualization/
│       ├── api/
│       ├── database/
│       └── schemas/
│
├── tests/
├── reports/
│   └── figures/
└── docs/
```

The exact structure can evolve as the implementation becomes clearer.
Keep importable application code under
`src/morocco_retail_intelligence/`. Notebooks are for exploration and
reporting; reusable business logic should gradually move into the
package.

### Git and data hygiene

-   Commit source code, notebooks, documentation, configuration, and
    lockfile.
-   Do not commit `.venv/`, cache folders, secrets, or local environment
    files.
-   Decide whether to commit the synthetic raw CSV files based on
    repository size and licensing/portfolio needs; these supplied files
    are small and synthetic, so they can normally be committed.
-   Never overwrite the raw dataset with cleaned data.
-   Add generated temporary files and notebook checkpoints to
    `.gitignore`.
-   Do not commit credentials, database passwords, API keys, or `.env`
    files.

## 9. Full roadmap: phases and steps

### Phase 0 --- Professional project setup

**Status: Reported complete; setup verification details not yet
reviewed.**

Objectives: - Create a modern Python package. - Use Python 3.12 and
`uv`. - Understand `pyproject.toml` and `uv.lock`. - Separate runtime
and development dependencies. - Configure Ruff and Pytest. - Create
repository folders. - Place the supplied CSVs under `data/raw/`. -
Initialize Git and create an initial commit.

Deliverable: - Reproducible project skeleton with working environment
and configuration.

### Phase 1 --- Data understanding and quality audit

**Next phase.**

Notebook: `notebooks/01_data_understanding.ipynb`

Objectives: - Understand the business context and each CSV. - Load CSV
files with Pandas using clear variable names. - Understand DataFrames
and Series. - Inspect `head()`, `tail()`, `sample()`, `shape`,
`columns`, `index`, `dtypes`, `info()`, and `describe()`. - Inspect
missing values with `isna()` and `isna().sum()`. - Detect duplicates
with `duplicated()` and `duplicated().sum()`. - Count unique values with
`nunique()` and inspect categories with `value_counts()`. - Identify
candidate primary keys and foreign keys. - Check uniqueness and
referential integrity across related tables. - Parse date columns and
inspect date ranges. - Distinguish data-quality problems from valid
business cases.

Suggested exercise sequence: 1. Load all six CSV files. 2. Display the
first five rows of each. 3. Record the shape of each DataFrame. 4.
Inspect columns and data types. 5. Generate descriptive statistics. 6.
Count missing values per column. 7. Detect duplicate rows and duplicate
IDs. 8. Count unique customers, products, orders, and categories. 9.
Identify primary and foreign keys. 10. Explain the relationships between
the six tables in the learner's own words. 11. Write a short initial
data-quality report.

Deliverable: - A notebook documenting the dataset structure,
relationships, and quality issues. - A concise summary of risks to later
analysis.

Do not clean the data in Phase 1. First understand and document it.

### Phase 2 --- Data cleaning and preparation

Notebook: `notebooks/02_data_cleaning.ipynb`

Objectives: - Define cleaning rules before applying them. - Handle
duplicate records using justified business keys. - Handle missing values
based on meaning, not by blindly filling everything. - Convert dates and
numeric/categorical columns to appropriate types. - Standardize text and
category values where justified. - Validate numeric ranges and
impossible values. - Filter and sort data. - Use `groupby()`, `agg()`,
`transform()`, `merge()`, `concat()`, and `pivot_table()`. - Understand
join types and prevent row multiplication. - Build clean, reusable
tables for analysis. - Save processed datasets under `data/processed/`.

Suggested steps: 1. Write a data-cleaning plan. 2. Preserve raw data
unchanged. 3. Investigate and resolve duplicate orders. 4. Investigate
missing customer ages, shipping fees, and review comments. 5. Parse
dates and validate date ranges. 6. Validate IDs and relationships. 7.
Join tables carefully and verify row counts. 8. Derive useful fields
such as delivery duration where valid. 9. Save cleaned outputs and
document each transformation.

Deliverable: - Reproducible cleaning notebook or Python module. -
Processed datasets. - Data-quality decisions documented in `docs/` or
the notebook.

### Phase 3 --- Exploratory data analysis (EDA) and business KPIs

Notebook: `notebooks/03_exploratory_analysis.ipynb`

Objectives: - Translate business questions into analytical questions. -
Define metrics and their denominators precisely. - Analyze orders,
sales, products, customers, cities, delivery, payments, and reviews. -
Use Pandas aggregation, grouping, sorting, merging, and reshaping. -
Compare time periods and segments. - Identify outliers and unusual
patterns. - Distinguish correlation from causation. - Write
evidence-based business observations.

Potential KPIs: - Delivered order count. - Cancelled and returned order
rates. - Gross item sales and net item sales, with explicit
definitions. - Shipping revenue/cost only if the dataset supports a
defensible definition. - Average order value. - Units sold. - Revenue by
category/product/city/month. - Repeat-customer rate. - Average delivery
time for delivered orders. - Average review rating and rating
distribution. - Payment-method share and payment failure rate.

Important: - Decide how returned orders affect sales metrics. - Avoid
counting cancelled orders as completed sales. - Avoid double-counting
order-level values after joining to multiple order items. - Document all
formulas and assumptions.

Deliverable: - Business KPI tables. - Written answers to the business
questions. - A concise findings report.

### Phase 4 --- Data visualization and storytelling

Notebook: `notebooks/04_visualization.ipynb`

Install when this phase begins:

``` powershell
uv add matplotlib seaborn
```

Objectives: - Learn Matplotlib's figure/axes model. - Learn Seaborn's
statistical plotting interface. - Select chart types that fit the
question and data. - Label axes, units, legends, titles, and time
periods. - Avoid misleading scales and clutter. - Create consistent,
publication-quality charts. - Save important figures under
`reports/figures/`. - Write interpretations beneath charts.

Potential charts: - Monthly sales trend: line chart. - Sales by
city/category: bar chart. - Order status proportions: bar chart or
carefully justified composition chart. - Order value distribution:
histogram and boxplot. - Ratings distribution: count plot. - Delivery
duration by city: boxplot. - Product/category performance: ranked bar
chart. - Correlation heatmap only where numeric relationships are
meaningful.

Deliverable: - A curated set of professional figures. - A narrative
report explaining what each chart reveals and what it does not prove.

### Phase 5 --- Analytics REST API with FastAPI

Install when this phase begins:

``` powershell
uv add fastapi "uvicorn[standard]"
```

Add any additional testing tools when required.

Objectives: - Understand HTTP, REST, methods, status codes, and JSON. -
Understand FastAPI application structure and route handlers. - Use
Pydantic models for request/response validation. - Build endpoints that
expose previously implemented analytics. - Add query parameters,
filtering, sorting, and pagination. - Handle invalid input and errors. -
Document endpoints using generated OpenAPI/Swagger documentation. - Test
endpoints.

Potential endpoints: - `GET /health` - `GET /analytics/overview` -
`GET /analytics/sales/monthly` - `GET /analytics/sales/by-city` -
`GET /analytics/products/top` - `GET /analytics/orders/status` -
`GET /analytics/delivery/performance` - `GET /analytics/reviews/summary`

Deliverable: - A documented, working API exposing meaningful business
analytics.

### Phase 6 --- Database and SQL integration

Objectives: - Learn relational database concepts and PostgreSQL. -
Design tables and relationships. - Understand primary keys, foreign
keys, constraints, indexes, and transactions. - Import the cleaned
data. - Write SQL queries for key analytical questions. - Integrate
PostgreSQL with Python using SQLAlchemy. - Separate database access from
business logic and API routes. - Manage configuration and secrets
through environment variables. - Test database-dependent behavior.

Deliverable: - A persistent PostgreSQL-backed analytics application. -
Documented schema and reproducible database setup.

### Phase 7 --- Testing, quality, Docker, and deployment

Objectives: - Add unit tests for cleaning and analytical functions. -
Add API tests with Pytest and FastAPI's test client. - Test edge cases
and invalid inputs. - Improve logging and error handling. - Run Ruff
consistently. - Add Docker and a reproducible deployment
configuration. - Document environment variables without committing
secrets. - Improve README with setup, architecture, sample outputs, API
examples, and screenshots. - Deploy if a suitable free/low-cost platform
is available at the time.

Deliverable: - Tested, documented, reproducible, portfolio-ready
application.

### Optional Phase 8 --- Predictive analytics

Only after the core project is solid, consider: - Sales forecasting. -
Customer segmentation. - Product demand prediction. - Customer churn or
repeat-purchase propensity, if the data supports a meaningful
definition.

Potential technology: Scikit-learn. NumPy should still not be taught as
a standalone topic until the learner reaches the relevant algebra/LLM
lessons. Explain any mathematical prerequisites before implementing
models. Do not claim predictive accuracy without proper train/test
methodology and evaluation.

## 10. Current immediate task

The learner has confirmed: **"now everything ok"** after the
professional environment setup.

Continue by confirming that the six CSV files are in `data/raw/` and
that the initial notebook can be created. Do not repeat the entire setup
unless a problem is reported.

Start Phase 1 with `notebooks/01_data_understanding.ipynb`.

First exercise: 1. Import Pandas. 2. Load all six CSV files from
`../data/raw/`. 3. Display the first five rows of each DataFrame. 4.
Display each DataFrame's shape. 5. Display column names and data types.
6. Use `info()` and `describe()`. 7. Count missing values. 8. Detect
duplicate rows. 9. Count unique identifiers. 10. Identify candidate keys
and explain relationships.

The learner should share their code and outputs for review. Review the
work before proceeding to the next exercise.

Example initial loading code:

``` python
import pandas as pd

customers = pd.read_csv("../data/raw/customers.csv")
products = pd.read_csv("../data/raw/products.csv")
orders = pd.read_csv("../data/raw/orders.csv")
order_items = pd.read_csv("../data/raw/order_items.csv")
payments = pd.read_csv("../data/raw/payments.csv")
reviews = pd.read_csv("../data/raw/reviews.csv")
```

This relative path assumes the notebook is in `notebooks/` and the CSVs
are in `data/raw/`.

## 11. GitHub portfolio expectations

The finished repository should have: - A clear README explaining the
business problem and project value. - Setup instructions using `uv`. - A
clear architecture overview. - Dataset documentation and synthetic-data
disclaimer. - Reproducible notebooks and reusable source modules. -
Well-named charts and analytical reports. - A documented KPI
dictionary/formula definitions. - API documentation and example
requests/responses. - Tests and code-quality configuration. -
Screenshots or sample outputs where useful. - No secrets or unnecessary
generated files.

The README should communicate business value and analytical reasoning,
not merely list technologies.

## 12. How to resume in a new conversation

Upload this file and, if possible, the current `pyproject.toml`,
repository tree, and any notebook/code that has been completed.

Use this message:

> We are continuing my Morocco Retail Intelligence project. Read
> `PROJECT_CONTEXT.md` carefully and treat it as the project handoff.
> Keep the same step-by-step teaching approach: explain concepts, give
> me exercises, let me implement them, review my code and outputs, and
> only then move forward. The project uses Python 3.12, uv,
> pyproject.toml, Pandas, Matplotlib, Seaborn, FastAPI, PostgreSQL, and
> related tools. Do not teach NumPy as a standalone subject until my
> algebra or LLM lessons. My Phase 0 setup is complete. Continue with
> the current immediate task in Phase 1, without restarting completed
> work.

------------------------------------------------------------------------

**Handoff maintenance:** Update the "Current immediate task" and the
status of each phase as the project progresses. Record important design
decisions, completed deliverables, dependency changes, and unresolved
issues here so this document remains useful across conversations.
