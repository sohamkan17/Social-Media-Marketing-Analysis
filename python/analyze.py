from pathlib import Path
import pandas as pd
import sqlite3

ROOT = Path(__file__).resolve().parent.parent
conn = sqlite3.connect(ROOT / "marketing.db")

q = """
SELECT a.ad_platform,
       SUM(CASE WHEN e.event_type = 'Impression' THEN 1 ELSE 0 END) AS impressions,
       SUM(CASE WHEN e.event_type = 'Purchase'   THEN 1 ELSE 0 END) AS purchases,
       ROUND(
         SUM(CASE WHEN e.event_type = 'Purchase'   THEN 1 ELSE 0 END) * 100.0 /
         SUM(CASE WHEN e.event_type = 'Impression' THEN 1 ELSE 0 END), 3
       ) AS conversion_pct
FROM ad_events e
JOIN ads a ON a.ad_id = e.ad_id
GROUP BY a.ad_platform
ORDER BY conversion_pct DESC
"""

df = pd.read_sql(q, conn)
print(df)



import seaborn as sns
import matplotlib.pyplot as plt

# bar chart of conversion rate by platform 
sns.barplot(x="ad_platform", y="conversion_pct", data=df)
plt.title("Purchase Conversion Rate by Platform")
plt.ylabel("Conversion %")
plt.xlabel("Platform")
plt.savefig(ROOT / "dashboard" / "conversion_by_platform.png", dpi=150, bbox_inches="tight")
plt.show()


#Cost per purchase by campaign (CAC)
cac_q = """
SELECT c.name,
       c.total_budget,
       COUNT(*) AS purchases,
       ROUND(c.total_budget * 1.0 / COUNT(*), 2) AS cost_per_purchase
FROM campaigns c
JOIN ads a        ON a.campaign_id = c.campaign_id
JOIN ad_events e  ON e.ad_id = a.ad_id
WHERE e.event_type = 'Purchase'
GROUP BY c.name, c.total_budget
ORDER BY cost_per_purchase ASC
"""
cac = pd.read_sql(cac_q, conn)
print(cac)

best  = cac.iloc[0]    # cheapest cost per purchase
worst = cac.iloc[-1]   # most expensive
print(f"\nCheapest:  {best['name']} at ${best['cost_per_purchase']} per purchase")
print(f"Most expensive: {worst['name']} at ${worst['cost_per_purchase']} per purchase")
ratio = worst['cost_per_purchase'] / best['cost_per_purchase']
print(f"That's a {ratio:.1f}x difference.")

cac.to_csv(ROOT / "dashboard" / "cost_per_purchase.csv", index=False)

# Tableau
df.to_csv(ROOT / "dashboard" / "platform_summary.csv", index=False)

cac.to_csv(ROOT / "dashboard" / "cost_per_purchase.csv", index=False)

conn.close()
