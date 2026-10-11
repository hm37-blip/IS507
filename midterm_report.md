
# Investigating the Nonlinear Relationship Between Scheduled Airport Traffic Volume and Flight Delays at Chicago O’Hare International Airport (ORD)

**IS507 Midterm Team Project**

## 1. Motivation

Flight delays can disrupt travel plans, especially for international students who need to travel long distances to return to school. Before the start of a new semester, many international students travel back to their universities, which may increase air travel demand during this period. This potential increased demand raises questions about how airport traffic volume is related to flight delays.

## 2. Your Problem

Our goal is to investigate whether scheduled airport traffic volume has a nonlinear relationship with flight delays at Chicago O'Hare International Airport (ORD).

Using January 2026 flight data from the Bureau of Transportation Statistics (BTS), we examine `TOTAL_SCHEDULED_TRAFFIC` as the independent variable (X) and arrival and departure delays as separate dependent variables (Y).

We plan to compare linear and quadratic regression models using mean squared error (MSE) as the fitting objective. Our findings may provide insights into flight delay patterns and the relationship between scheduled traffic volume and delays.

## 3. Related Work

Hsiao and Hansen (2006) analyzed U.S. airline flight delays using econometric regression models. Their findings showed that scheduled arrivals significantly affect average flight delays and that the impact of queuing delays varies by time of day.

Unlike their study, which considered multiple factors across 32 airports, our research focuses on whether scheduled traffic volume has a nonlinear relationship with arrival and departure delays at Chicago O'Hare International Airport (ORD).

## 4. Data

### 4.1 Data Description

We obtained the **Reporting Carrier On-Time Performance Data** from the Bureau of Transportation Statistics (BTS), covering flights associated with Chicago O'Hare International Airport (ORD) in January 2026.

The original dataset contains **61,446 rows and 23 columns**, with each row representing one flight record.

The dataset includes the following variable types:

- **Numerical:** Arrival and departure delays, flight distance, and taxi times.
- **Categorical:** Airline carrier, origin and destination airports, and day of the week.
- **Date and Time:** Flight date and scheduled departure and arrival times.
- **Binary:** Cancellation, diversion, and 15-minute delay indicators.

### 4.2 Data Preprocessing

We created separate departure and arrival datasets by excluding cancelled flights and records with missing relevant delay values. Diverted arrivals were also excluded.

After preprocessing:

- **Departure dataset:** 24,192 records
- **Arrival dataset:** 24,019 records

We checked for duplicate records and extreme delay values, retaining negative and extreme delays.

Using the original dataset, we also calculated scheduled departures and arrivals for each date and hourly time block, including flights that were later cancelled or diverted.

We then combined these counts into `TOTAL_SCHEDULED_TRAFFIC` as a proxy for airport congestion.

## 5. Preliminary EDA & Findings

### 5.1 Delay Distribution and Descriptive Statistics

We first examined the distributions of arrival and departure delays at Chicago O'Hare International Airport (ORD).

As shown in Table 1, the analysis includes 24,019 arrival flights and 24,192 departure flights.

Departure flights experienced a higher mean delay (**22.50 minutes**) than arrival flights (**16.25 minutes**). However, arrival delays exhibited greater variability, with a standard deviation of **80.71 minutes** compared with **67.46 minutes** for departures.

The median delays were **−4 minutes** for arrivals and **0 minutes** for departures, indicating that at least half of arrival flights arrived four or more minutes ahead of schedule, while at least half of departure flights departed on time or earlier.

**Table 1. Descriptive Statistics of Arrival and Departure Delays**

| Statistic | Arrival Delay (min) | Departure Delay (min) |
|---|---:|---:|
| Count | 24,019 | 24,192 |
| Mean | 16.25 | 22.50 |
| Median | -4.00 | 0.00 |
| Standard Deviation | 80.71 | 67.46 |
| Minimum | -64 | -28 |
| Maximum | 1,927 | 1,610 |
| Skewness | 7.71 | 7.56 |

The visualizations further reveal substantial departures from normality.

Figure 1 illustrates the wide dispersion and numerous extreme positive delays in both groups, particularly among arrival flights.

Figure 2, which focuses on delays between −60 and 180 minutes, shows that most flights were concentrated near their scheduled times, while both distributions exhibited long right tails.

The large differences between the means and medians, together with skewness values exceeding 7.5, indicate strongly right-skewed distributions.

These findings suggest that extreme delays substantially influence average delay estimates, motivating the use of both mean- and median-based measures in subsequent analyses.

**Figure 1. Arrival vs. Departure Delay Comparison**

Boxplots illustrating differences in delay variability, medians, and extreme observations.

<!-- Insert Figure 1 here -->
<!-- ![Figure 1](figures/figure1.png) -->

**Figure 2. Distribution of Arrival and Departure Delays**

Overlaid histograms showing the central portions of both delay distributions (−60 to 180 minutes), with dashed and dotted lines indicating the respective medians.

<!-- Insert Figure 2 here -->
<!-- ![Figure 2](figures/figure2.png) -->

### 5.2 Scheduled Traffic Volume and Mean Flight Delay

To explore the relationship between airport congestion and flight delays, we examined total scheduled traffic volume, defined as the sum of scheduled departures and arrivals within each hourly interval.

Flights were grouped by traffic volume, and the mean delay was calculated for each group.

Figure 3 presents the resulting relationships separately for arrival and departure flights, with marker sizes representing the number of flights associated with each traffic volume level.

The scatterplots reveal considerable variation in mean delays across traffic levels, with no clear linear trend in either group.

Pearson correlation analysis at the individual-flight level further indicates:

- **Arrival delay:** r = 0.0488, p < 0.001
- **Departure delay:** r = −0.0039, p = 0.545

Although the arrival correlation is statistically significant under the conventional test, its small magnitude suggests limited practical explanatory value.

These preliminary findings indicate that scheduled traffic volume alone has little linear association with flight delays.

However, weak linear correlations do not rule out potentially nonlinear relationships, motivating further investigation using more flexible regression models.

**Figure 3. Scheduled Traffic Volume vs. Mean Flight Delay**

Scatterplots comparing mean arrival and departure delays across total scheduled traffic volume levels. Each point represents a traffic volume group, and marker size indicates the number of flights within that group.

<!-- Insert Figure 3 here -->
<!-- ![Figure 3](figures/figure3.png) -->

### 5.3 Median Delay as a Robustness Check

Given the strongly right-skewed delay distributions identified in Section 5.1, we further examined median delays to assess whether the patterns observed in mean delays were influenced by extreme observations.

Unlike the mean, the median is less sensitive to unusually long delays.

Figure 4 presents median arrival and departure delays across scheduled traffic volume levels, with marker sizes representing the number of flights in each group.

Compared with the mean-based results in Figure 3, median delays remain relatively concentrated near zero across most traffic levels, although some variation and isolated high values are observed.

Neither group exhibits a clear, consistent trend as traffic volume increases.

These findings suggest that extreme delays may contribute to fluctuations in mean delay estimates, while the relationship between scheduled traffic volume and typical flight delays remains unclear.

Further nonlinear modeling is therefore needed to determine whether meaningful patterns exist beyond simple linear associations.

**Figure 4. Scheduled Traffic Volume vs. Median Flight Delay**

Scatterplots showing median arrival and departure delays across total scheduled traffic volume levels. Marker sizes indicate the number of flights within each traffic volume group.

<!-- Insert Figure 4 here -->
<!-- ![Figure 4](figures/figure4.png) -->

## 6. Proposed Baseline Model

Based on the preliminary EDA, we propose **simple linear regression** as our baseline model to examine the relationship between scheduled airport traffic volume and flight delays.

The correlation analysis revealed weak linear associations for both arrival (r = 0.0488) and departure delays (r = −0.0039), while the scatterplots showed no clear linear trends.

These findings motivate the use of a simple linear model as a reference for evaluating whether more flexible models can capture additional patterns.

The baseline will use:

- **Independent variable (X):** `TOTAL_SCHEDULED_TRAFFIC`
- **Dependent variable (Y):** `ARR_DELAY` or `DEP_DELAY`
- **Fitting objective:** Mean Squared Error (MSE)
- **Evaluation metrics:** RMSE, MAE, and R²

Separate models will be fitted for arrival and departure flights to account for their different delay distributions.

In the next stage, we will introduce a quadratic traffic term to investigate potential nonlinear relationships.

By comparing the linear baseline with the quadratic model, we aim to determine whether allowing for nonlinearity meaningfully improves model fit and predictive performance.

## 7. Challenges and Limitations

Several challenges remain for the next stage of analysis.

First, both arrival and departure delays exhibit highly right-skewed distributions with substantial extreme values, which may disproportionately influence mean-based estimates and regression results.

Second, flight delays are affected by factors beyond scheduled traffic volume, including weather conditions, airline operations, and time-of-day effects. These potential confounding factors may complicate the interpretation of the relationship between congestion and delay.

Additionally, multiple flights within the same hourly interval share identical traffic volume measurements and may experience common operational conditions, introducing dependence among observations. Future analyses will need to account for this dependence when conducting statistical inference.

Finally, because this study uses observational data, any identified relationship should be interpreted as an **association rather than evidence of causation**.

## 8. Reference

Hsiao, C.-Y., & Hansen, M. (2006). Econometric analysis of U.S. airline flight delays with time-of-day effects. *Transportation Research Record: Journal of the Transportation Research Board, 1951*(1), 104–112.

https://doi.org/10.1177/0361198106195100113
