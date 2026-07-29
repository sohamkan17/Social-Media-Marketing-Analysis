# Marketing Campaign Performance — Social Media Advertising Analysis

> # An end-to-end analytics project: loading raw ad-funnel CSVs into a relational SQLite database with Python, answering business questions in SQL, and publishing the results as an interactive Tableau dashboard.



# Highlights

- Four raw CSVs loaded into a clean, joinable SQLite database.
- Business questions answered in SQL using JOINs, CTEs, and window functions.
- Headline finding: cost-per-acquisition varies 55× across campaigns — a clear signal for where to reallocate ad spend.
- Results published as an interactive [Tableau dashboard](https://public.tableau.com/app/profile/soham.kandalgaonkar/viz/MarketingCampaignPerformance-SocialMediaAdvertisingKaggle/MarketingCampaignPerformance?publish=yes).

[![Marketing Campaign Performance dashboard](Dashboard-Tableau-Social-Media-Analysis.webp)](https://public.tableau.com/app/profile/soham.kandalgaonkar/viz/MarketingCampaignPerformance-SocialMediaAdvertisingKaggle/MarketingCampaignPerformance?publish=yes)

*Interactive Tableau dashboard — click to explore campaign-level cost-per-acquisition.*

# Overview

This project explores a social-media advertising dataset to answer one core question: which campaigns and platforms actually turn ad spend into purchases, and at what cost?

 I took the raw data through a full pipeline: loading it into a relational database, validating that the tables join cleanly, writing SQL to answer specific marketing questions, and visualizing the results.

The data comes from the [Social Media Advertisement Performance](https://www.kaggle.com/datasets/alperenmyung/social-media-advertisement-performance) dataset on Kaggle. It is synthetic/simulated, so the findings demonstrate the analytics process rather than report on any real company.

The data models a four-table ad funnel, joined on `campaign_id`, `ad_id`, and `user_id`:

| Table | Rows | Description |
|---|---:|---|
| `users` | 10,000 | Demographics: age, gender, country, interests |
| `campaigns` | 50 | Budget, start/end dates, duration |
| `ads` | 200 | Platform, ad type, targeting parameters |
| `ad_events` | 400,000 | Every interaction (impression → click → purchase) with timestamp |

Key findings:

- Cost per acquisition varies by 55×. The cheapest campaign acquired a purchase for \$118.18 (*Campaign_42_Summer*); the most expensive cost \$6,511.53 (*Campaign_35_Launch*).
- Facebook narrowly out-converts Instagram — 0.613% vs 0.572% of impressions — and drove 1,323 of the 2,031 total purchases.
- The funnel is steep (339,812 impressions → 2,031 purchases), so findings are framed around cost-per-purchase rather than dollar ROI, since the data records purchase events, not amounts.
- Reallocate spend toward low-CAC campaigns. Cost-per-acquisition ranges 55× — from \$118 (*Campaign_42_Summer*) to \$6,512 (*Campaign_35_Launch*). Move budget off the high-CAC outliers and toward *Campaign_42*-tier campaigns, then audit what makes the cheap ones efficient (targeting, ad type, platform) and replicate it.
- Lean on Facebook for volume. Facebook drove 1,323 of 2,031 purchases (~65%) and converted slightly better than Instagram (0.613% vs 0.572%), making it the stronger default for broad-reach spend.
  Investigate Campaign_35_Launch before renewing it. At \$6,512 per purchase it's the single biggest source of wasted spend — review its creative and targeting instead of re-funding it as-is.

Since this data records purchase *events* but not purchase *amounts*, these are cost-per-acquisition calls, not full ROI. The natural next step is to join revenue/LTV data and weigh acquisition cost against customer value.


### Author

Soham Kandalgaonkar
- [Tableau Public profile](https://public.tableau.com/app/profile/soham.kandalgaonkar)
- [GitHub profile](https://github.com/sohamkan17)
- [LinkedIn profile](https://www.linkedin.com/in/soham-kandalgaonkar-34296a2a4)


## Usage

Build the database and run the analysis in two steps:

```bash
python python/getdata.py     # loads the 4 CSVs into marketing.db
python python/analyze.py     # runs the SQL analysis, prints findings, saves charts
```

Each business question also lives as a standalone file in `/sql`, runnable against `marketing.db` in any SQLite client:

| File | Question |
|---|---|
| `purchases_per_platform.sql` | Which platform drives more purchases? |
| `conversion_rate_by_platform.sql` | What % of impressions convert and how many per platform? |
| `cost_per_purchase.sql` | Cost-per-acquisition per campaign |
| `customer_segmentation.sql` | RFM-style buyer segmentation with `ntile()` |


## Installation

Clone the repository and install the dependencies (Python 3.9+):

```bash
git clone https://github.com/sohamkan17/Social-Media-Marketing-Analysis.git
cd Social-Media-Marketing-Analysis
pip install -r requirements.txt
```
The raw CSVs live in `/data` and are never edited by hand — running `python/getdata.py` regenerates `marketing.db` from them.

## Limitations & Next Steps

- This is synthetic data, therefore this is more to practice the analytical process rather than reflecting an analysis on real consumer behavior
- 'ad_events' can give cost-per-acquisition but it doesn't necessarily resemble ROI which would be useful information in a full marketing analysis
- In the future, I'd like to use my Tableau dashboard to reflect live data rather than a set marketing dashboard


## Feedback and Contributing

This is a learning project, so if you spot something or have a suggestion, feel free to open an issue or start a discussion in the repo.
