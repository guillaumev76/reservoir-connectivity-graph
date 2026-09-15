"""
Step 2 — Production correlation between wells.

Method: convert monthly oil volume to a rate (Oil / On Stream), which
naturally drops full shut-in months (0/0 -> NaN) instead of letting them
pollute the correlation as false zeros. Then take the month-over-month
change of that rate, per well, to remove the field-wide decline trend
(otherwise every well would look "correlated" just because they all
decline over the field's life). Pearson correlation is computed on this
detrended series, for every well pair, excluding water injectors (15/9-F-1
C and 15/9-F-4 never produce oil, so an oil-rate correlation is meaningless
for them).

Finding (15/09/2026): no well pair reaches significance at p < 0.05. But
sample sizes vary a lot between pairs (28-94 months for the well-sampled
wells, only 3-4 months for 15/9-F-5), so "not significant" means two very
different things here — genuine absence of correlation for the
well-sampled pairs, versus simply not enough data to conclude anything for
15/9-F-5 and, to a lesser extent, 15/9-F-15 D. Next steps: (1) build the
NetworkX graph reflecting this — no edges among the well-sampled wells,
data-limited wells flagged rather than shown as "confirmed unconnected";
(2) revisit 15/9-F-5 / 15/9-F-15 D using the daily sheet, which has far
more overlapping data points than the monthly aggregation.
"""

import pandas as pd
from scipy import stats
from itertools import combinations

from load_data import load_monthly

#Import data from the Excel file
df = load_monthly()
df = df.sort_values(['Wellbore name', 'Year', 'Month'])

injectors = ["15/9-F-1 C", "15/9-F-4"]

# Calcul the effective monthly production 
df['production']=df['Oil']/df['On Stream']

# Removing the natural declining trend to get the real correlation of the data
df['variation'] = df.groupby("Wellbore name")['production'].diff()

df_pivot = df.pivot(values = 'variation', index ='date', columns ='Wellbore name')

# Select both wells together, then drop a row if EITHER is missing, so the
# two series stay aligned on exactly the same set of months.

for colonne, colonne2 in combinations(df_pivot.drop(columns=injectors).columns, 2):
    
    pair = df_pivot [[colonne, colonne2]].dropna()
    corr, pval = stats.pearsonr(pair[colonne], pair[colonne2])
    print()
    print(f"{colonne} vs {colonne2}: n={len(pair)} months, corr={corr:.3f}, p-value={pval:.4f}")
