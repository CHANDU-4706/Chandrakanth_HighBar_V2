# Kasparro Analysis Report

## Query
Analyze why ROAS dropped last week

## Data Analysis


### Data Output (Get Daily Metrics):
| date                |   roas |       cpm |    ctr |   spend |
|:--------------------|-------:|----------:|-------:|--------:|
| 2025-03-17 00:00:00 |  44.24 |  0.677654 | 0.0273 |  328.12 |
| 2025-03-18 00:00:00 |  36.7  |  0.325904 | 0.0161 |   99.02 |
| 2025-03-19 00:00:00 |   9.18 |  0.827264 | 0.014  |  378.57 |
| 2025-03-20 00:00:00 |   1.64 |  3.41958  | 0.0088 |  914.33 |
| 2025-03-21 00:00:00 |  28.25 |  0.51666  | 0.0169 |  170.95 |
| 2025-03-22 00:00:00 |   4.91 |  3.45815  | 0.0194 |  589.11 |
| 2025-03-23 00:00:00 |  48.93 |  0.458093 | 0.0174 |   97.95 |
| 2025-03-24 00:00:00 |   2.99 |  2.68004  | 0.0091 |  502.81 |
| 2025-03-25 00:00:00 | 128.09 |  0.191466 | 0.0254 |   92.96 |
| 2025-03-26 00:00:00 |   3.11 |  4.18051  | 0.0172 |  950.89 |
| 2025-03-27 00:00:00 |  17.65 |  0.353687 | 0.0101 |   64.47 |
| 2025-03-28 00:00:00 |   4.9  |  0.977421 | 0.0099 |  377.92 |
| 2025-03-29 00:00:00 |   2.3  |  2.19034  | 0.011  |  672.3  |
| 2025-03-30 00:00:00 |   0.56 | 16.3107   | 0.014  |  751.5  |
| 2025-03-31 00:00:00 |   1.13 |  3.9858   | 0.0143 |  965.64 |

### Data Output (Segment Data):
|                             |     roas |
|:----------------------------|---------:|
| ('Carousel', 'Broad')       |  0.485   |
| ('Carousel', 'Retargeting') | 36.7     |
| ('Image', 'Broad')          |  4.193   |
| ('Image', 'Lookalike')      |  2.84    |
| ('Image', 'Retargeting')    |  4.36333 |
| ('UGC', 'Broad')            |  2.32333 |
| ('UGC', 'Lookalike')        |  3.11    |
| ('UGC', 'Retargeting')      |  3.52    |
| ('Video', 'Broad')          |  2.83091 |
| ('Video', 'Lookalike')      |  3.71    |
| ('Video', 'Retargeting')    |  7.0175  |

## Insights


### Insights (Identify Correlated Metrics):
### Hypotheses and Insights
Based on the provided data, the following observations, analyses, and conclusions can be drawn:

1. **Observation**: ROAS dropped significantly on certain days (e.g., 2025-03-19, 2025-03-20, 2025-03-22, 2025-03-24, 2025-03-26, 2025-03-30).
2. **Analysis**: On these days, CPM increased substantially (e.g., 0.827264 to 3.41958, 3.45815, 2.68004, 4.18051, 16.3107).
3. **Conclusion/Hypothesis**: The increase in CPM likely led to the drop in ROAS, as higher costs per thousand impressions (CPM) would decrease the return on ad spend (ROAS) if the conversion rate or revenue generated does not increase proportionally.

4. **Observation**: Spend amounts varied significantly across days.
5. **Analysis**: Higher spend days (e.g., 2025-03-20, 2025-03-22, 2025-03-24, 2025-03-26, 2025-03-30, 2025-03-31) often correlated with lower ROAS and higher CPM.
6. **Conclusion/Hypothesis**: Increased spend may be leading to audience saturation, driving up CPM and subsequently decreasing ROAS. This could indicate that the advertising budget is being inefficiently allocated on certain days.

7. **Observation**: CTR (click-through rate) also varied but did not show a clear correlation with ROAS drops.
8. **Analysis**: Despite fluctuations, CTR does not seem to directly influence the significant drops in ROAS observed.
9. **Conclusion/Hypothesis**: The impact of CTR on ROAS may be secondary to the effects of CPM and spend. Optimizing for CTR alone may not mitigate the drops in ROAS.

10. **Observation**: There are days with high ROAS (e.g., 2025-03-17, 2025-03-23, 2025-03-25) that have lower CPM and sometimes lower spend.
11. **Analysis**: These days suggest that when CPM is lower and spend is optimized, ROAS can be significantly higher.
12. **Conclusion/Hypothesis**: Efficient allocation of the advertising budget to avoid audience saturation and keeping CPM low could be key strategies to maintain or improve ROAS.

### Recommendations for Further Analysis
- Investigate the audience targeting strategies to identify potential saturation points.
- Analyze the ad creative performance to see if certain ads are more efficient in terms of ROAS.
- Consider implementing a dynamic budget allocation strategy that adjusts spend based on real-time CPM and ROAS performance.
- Evaluate the possibility of optimizing ad campaigns for specific days of the week or times of the day when ROAS tends to be higher.

### Insights (Determine Root Cause):
### Hypotheses and Insights
Based on the provided data, the following hypotheses and insights can be derived:

1. **Observation**: ROAS dropped significantly on certain days (e.g., 2025-03-19, 2025-03-20, 2025-03-22, 2025-03-24, 2025-03-26, 2025-03-30).
   **Analysis**: On these days, CPM increased substantially (e.g., 0.827264 to 3.41958, and up to 16.3107 on 2025-03-30).
   **Conclusion/Hypothesis**: The increase in CPM likely led to the drop in ROAS, possibly due to audience saturation or increased competition for ad space.

2. **Observation**: Certain creative types and audience segments have significantly lower ROAS (e.g., ('Carousel', 'Broad'), ('Image', 'Broad'), ('UGC', 'Broad')).
   **Analysis**: These segments have lower ROAS compared to their retargeting counterparts.
   **Conclusion/Hypothesis**: Broad targeting might be less effective than retargeting or lookalike targeting for these creative types, suggesting that targeting warmer audiences could improve ROAS.

3. **Observation**: Retargeting segments tend to have higher ROAS across most creative types (e.g., ('Carousel', 'Retargeting'), ('Video', 'Retargeting')).
   **Analysis**: This is consistent with the general understanding that retargeting ads are more effective because they target users who have already shown interest in the product or service.
   **Conclusion/Hypothesis**: Focusing more on retargeting campaigns could potentially increase overall ROAS.

4. **Observation**: There is a significant variation in ROAS across different days and segments.
   **Analysis**: This variability could be due to numerous factors including audience behavior, ad fatigue, or changes in bidding strategies.
   **Conclusion/Hypothesis**: Continuous monitoring and adjustment of ad campaigns, including creative assets and targeting strategies, are necessary to optimize performance.

5. **Observation**: The ('Carousel', 'Retargeting') segment has a notably high ROAS of 36.7.
   **Analysis**: This suggests that carousel ads perform particularly well when used for retargeting.
   **Conclusion/Hypothesis**: Allocating more budget to carousel retargeting ads could be an effective strategy to improve overall campaign performance.

These hypotheses and insights suggest that a combination of factors, including audience targeting, ad creative type, and bidding strategies, contribute to the variability in ROAS. Further analysis and experimentation are needed to confirm these hypotheses and optimize campaign performance.

## Creative Recommendations
