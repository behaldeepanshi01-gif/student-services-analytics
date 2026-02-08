# Student Services Operations Analytics

End-to-end operational analysis of 3,000 student service interactions at a university one-stop enrollment services center. Covers KPI tracking, staffing optimization, channel efficiency, satisfaction drivers, and process improvement recommendations across Financial Aid, Registrar, Student Business Services, and Admissions.

## Project Structure

```
student-services-analytics/
├── data/
│   └── student_services_data.csv           # 3,000-row interaction dataset
├── scripts/
│   ├── generate_data.py                    # Simulates one-stop service data
│   └── services_queries.sql                # 7 SQL queries for operations analysis
├── notebooks/
│   └── services_analysis.py                # Full analysis with statistical tests
├── dashboards/
│   ├── 01_kpi_dashboard.png
│   ├── 02_volume_heatmap.png
│   ├── 03_channel_analysis.png
│   ├── 04_staff_performance.png
│   └── 05_satisfaction_drivers.png
└── README.md
```

## Analysis Sections

1. **Operations Overview & KPIs** - Department-level KPI dashboard (wait time, FCR, satisfaction)
2. **Volume Patterns & Staffing** - Peak period identification, day/time heatmap for scheduling
3. **Channel Analysis** - Walk-in, phone, email, virtual appointment efficiency comparison
4. **Staff Performance** - Individual scorecards with FCR, satisfaction, and escalation rates
5. **Satisfaction Drivers** - Statistical testing (t-tests, correlation) on what drives student satisfaction
6. **Process Improvement Recommendations** - Data-backed operational improvements

## Key Findings

- First Contact Resolution of **55.7%** - students resolved on first contact report **+0.55 higher satisfaction** (p < 0.05)
- Walk-in channel handles **46%** of volume with highest wait times (15.1 min avg)
- **Mondays, 10-12 PM** are peak periods with 241 interactions
- Wait times above **15 minutes** correlate with significant satisfaction drops
- Escalation rate of **15.3%** - training opportunity to improve first contact resolution

## Tools Used

- **Python**: pandas, numpy, matplotlib, seaborn, scipy.stats
- **SQL**: KPI queries, staffing analysis, escalation tracking
- **Statistical Methods**: Independent t-tests, Pearson correlation, satisfaction modeling

## Author

Deepanshi Behal | [LinkedIn](https://linkedin.com/in/bdeepanshi) | [GitHub](https://github.com/behaldeepanshi01-gif)
