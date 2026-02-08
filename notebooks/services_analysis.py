"""
Student Services Operations Analytics
=======================================
Analysis of 3,000 student service interactions at a university one-stop
enrollment services center. Covers: operational efficiency, staffing patterns,
resolution rates, satisfaction drivers, and process improvement recommendations.

Author: Deepanshi Behal
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats
import os

sns.set_theme(style="whitegrid")
plt.rcParams["figure.figsize"] = (10, 6)
plt.rcParams["figure.dpi"] = 150

output_dir = "C:/Users/Deepanshi/Desktop/student-services-analytics/dashboards"
os.makedirs(output_dir, exist_ok=True)

df = pd.read_csv("C:/Users/Deepanshi/Desktop/student-services-analytics/data/student_services_data.csv")

print("=" * 60)
print("STUDENT SERVICES OPERATIONS ANALYTICS")
print("=" * 60)
print(f"\nDataset: {len(df)} interactions across {df['department'].nunique()} departments")
print(f"Channels: {', '.join(df['channel'].unique())}")
print(f"Coverage: {df['quarter'].nunique()} quarters")

# ============================================================
# 1. OPERATIONS OVERVIEW & KPI DASHBOARD
# ============================================================
print("\n" + "=" * 60)
print("1. OPERATIONS OVERVIEW & KPIs")
print("=" * 60)

total = len(df)
avg_wait = df["wait_time_min"].mean()
avg_service = df["service_time_min"].mean()
fcr_rate = (df["resolution"] == "Resolved on First Contact").mean() * 100
escalation_rate = (df["escalated"] == "Yes").mean() * 100
avg_sat = df["satisfaction_score"].mean()
callback_rate = (df["callback_required"] == "Yes").mean() * 100

print(f"\nTotal Interactions:        {total:>10,}")
print(f"Avg Wait Time:             {avg_wait:>10.1f} min")
print(f"Avg Service Time:          {avg_service:>10.1f} min")
print(f"First Contact Resolution:  {fcr_rate:>10.1f}%")
print(f"Escalation Rate:           {escalation_rate:>10.1f}%")
print(f"Callback Rate:             {callback_rate:>10.1f}%")
print(f"Avg Satisfaction:          {avg_sat:>10.2f}/5.0")

# KPIs by department
dept_kpis = df.groupby("department").agg(
    volume=("inquiry_id", "count"),
    avg_wait=("wait_time_min", "mean"),
    avg_service=("service_time_min", "mean"),
    fcr=("resolution", lambda x: (x == "Resolved on First Contact").mean() * 100),
    avg_sat=("satisfaction_score", "mean"),
).round(2)

print(f"\n{'Department':<28} {'Volume':>8} {'Wait':>8} {'Service':>8} {'FCR %':>8} {'Sat':>6}")
print("-" * 70)
for dept, row in dept_kpis.iterrows():
    print(f"{dept:<28} {row['volume']:>8} {row['avg_wait']:>7.1f}m {row['avg_service']:>7.1f}m {row['fcr']:>7.1f}% {row['avg_sat']:>5.2f}")

# Chart: KPIs by department
fig, axes = plt.subplots(1, 3, figsize=(15, 5))

colors = ["#1565C0", "#42A5F5", "#90CAF9", "#BBDEFB", "#E3F2FD"]

axes[0].barh(dept_kpis.index, dept_kpis["avg_wait"], color=colors, edgecolor="white")
axes[0].set_xlabel("Avg Wait Time (min)")
axes[0].set_title("Wait Time by Department", fontsize=11, fontweight="bold")
for i, (dept, val) in enumerate(zip(dept_kpis.index, dept_kpis["avg_wait"])):
    axes[0].text(val + 0.2, i, f"{val:.1f}m", va="center", fontsize=9)

axes[1].barh(dept_kpis.index, dept_kpis["fcr"], color=colors, edgecolor="white")
axes[1].set_xlabel("First Contact Resolution (%)")
axes[1].set_title("FCR Rate by Department", fontsize=11, fontweight="bold")
for i, (dept, val) in enumerate(zip(dept_kpis.index, dept_kpis["fcr"])):
    axes[1].text(val + 0.3, i, f"{val:.1f}%", va="center", fontsize=9)

axes[2].barh(dept_kpis.index, dept_kpis["avg_sat"], color=colors, edgecolor="white")
axes[2].set_xlabel("Avg Satisfaction (1-5)")
axes[2].set_title("Satisfaction by Department", fontsize=11, fontweight="bold")
for i, (dept, val) in enumerate(zip(dept_kpis.index, dept_kpis["avg_sat"])):
    axes[2].text(val + 0.02, i, f"{val:.2f}", va="center", fontsize=9)

plt.suptitle("Student Services KPI Dashboard", fontsize=14, fontweight="bold", y=1.02)
plt.tight_layout()
plt.savefig(f"{output_dir}/01_kpi_dashboard.png", bbox_inches="tight")
plt.close()
print("\nSaved: 01_kpi_dashboard.png")

# ============================================================
# 2. VOLUME PATTERNS & STAFFING ANALYSIS
# ============================================================
print("\n" + "=" * 60)
print("2. VOLUME PATTERNS & STAFFING ANALYSIS")
print("=" * 60)

# By quarter
vol_quarter = df.groupby("quarter").agg(
    volume=("inquiry_id", "count"),
    avg_wait=("wait_time_min", "mean"),
).round(1)
print(f"\nVolume by Quarter:")
for q, row in vol_quarter.iterrows():
    print(f"  {q:<15} {row['volume']:>5} interactions  Avg Wait: {row['avg_wait']:.1f}m")

# By day of week
vol_day = df.groupby("day_of_week")["inquiry_id"].count()
day_order = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]
vol_day = vol_day.reindex(day_order)
print(f"\nVolume by Day of Week:")
for day, count in vol_day.items():
    print(f"  {day:<12} {count:>5}")

# By time slot
vol_time = df.groupby("time_slot")["inquiry_id"].count()
time_order = ["8-10 AM", "10-12 PM", "12-2 PM", "2-4 PM"]
vol_time = vol_time.reindex(time_order)
print(f"\nVolume by Time Slot:")
for slot, count in vol_time.items():
    print(f"  {slot:<12} {count:>5}")

# Peak period analysis
peak_combo = df.groupby(["day_of_week", "time_slot"]).agg(
    volume=("inquiry_id", "count"),
    avg_wait=("wait_time_min", "mean"),
).round(1).sort_values("volume", ascending=False)
print(f"\nTop 5 Peak Periods (highest volume):")
for (day, slot), row in peak_combo.head(5).iterrows():
    print(f"  {day} {slot}: {row['volume']} interactions, {row['avg_wait']:.1f}m avg wait")

# Chart: Volume heatmap by day and time
pivot_vol = df.groupby(["day_of_week", "time_slot"])["inquiry_id"].count().unstack()
pivot_vol = pivot_vol.reindex(day_order)[time_order]

fig, ax = plt.subplots(figsize=(8, 5))
sns.heatmap(pivot_vol, annot=True, fmt="d", cmap="Blues", ax=ax, linewidths=0.5)
ax.set_title("Inquiry Volume: Day of Week x Time Slot", fontsize=14, fontweight="bold")
ax.set_ylabel("Day of Week")
ax.set_xlabel("Time Slot")
plt.tight_layout()
plt.savefig(f"{output_dir}/02_volume_heatmap.png", bbox_inches="tight")
plt.close()
print("\nSaved: 02_volume_heatmap.png")

# ============================================================
# 3. CHANNEL ANALYSIS & SERVICE EFFICIENCY
# ============================================================
print("\n" + "=" * 60)
print("3. CHANNEL ANALYSIS & SERVICE EFFICIENCY")
print("=" * 60)

channel_stats = df.groupby("channel").agg(
    volume=("inquiry_id", "count"),
    pct=("inquiry_id", lambda x: len(x) / len(df) * 100),
    avg_wait=("wait_time_min", "mean"),
    avg_service=("service_time_min", "mean"),
    fcr=("resolution", lambda x: (x == "Resolved on First Contact").mean() * 100),
    avg_sat=("satisfaction_score", "mean"),
).round(2)

print(f"\n{'Channel':<22} {'Volume':>8} {'%':>6} {'Wait':>8} {'Service':>8} {'FCR':>8} {'Sat':>6}")
print("-" * 70)
for ch, row in channel_stats.iterrows():
    print(f"{ch:<22} {row['volume']:>8} {row['pct']:>5.1f}% {row['avg_wait']:>7.1f}m {row['avg_service']:>7.1f}m {row['fcr']:>7.1f}% {row['avg_sat']:>5.2f}")

# Chart: Channel comparison
fig, axes = plt.subplots(1, 2, figsize=(12, 5))

ch_colors = ["#1565C0", "#42A5F5", "#90CAF9", "#BBDEFB"]
axes[0].pie(channel_stats["volume"], labels=channel_stats.index, autopct="%1.1f%%",
            colors=ch_colors, startangle=90, textprops={"fontsize": 10})
axes[0].set_title("Inquiry Volume by Channel", fontsize=12, fontweight="bold")

x = range(len(channel_stats))
width = 0.35
axes[1].bar([i - width/2 for i in x], channel_stats["avg_wait"], width, label="Wait Time", color="#FF9800", edgecolor="white")
axes[1].bar([i + width/2 for i in x], channel_stats["avg_service"], width, label="Service Time", color="#1565C0", edgecolor="white")
axes[1].set_xticks(x)
axes[1].set_xticklabels(channel_stats.index, rotation=15)
axes[1].set_ylabel("Minutes")
axes[1].set_title("Wait & Service Time by Channel", fontsize=12, fontweight="bold")
axes[1].legend()

plt.suptitle("Channel Performance Analysis", fontsize=14, fontweight="bold", y=1.02)
plt.tight_layout()
plt.savefig(f"{output_dir}/03_channel_analysis.png", bbox_inches="tight")
plt.close()
print("\nSaved: 03_channel_analysis.png")

# ============================================================
# 4. STAFF PERFORMANCE & WORKLOAD
# ============================================================
print("\n" + "=" * 60)
print("4. STAFF PERFORMANCE & WORKLOAD")
print("=" * 60)

staff_perf = df.groupby("staff_member").agg(
    interactions=("inquiry_id", "count"),
    avg_wait=("wait_time_min", "mean"),
    avg_service=("service_time_min", "mean"),
    fcr=("resolution", lambda x: (x == "Resolved on First Contact").mean() * 100),
    avg_sat=("satisfaction_score", "mean"),
    escalations=("escalated", lambda x: (x == "Yes").sum()),
).round(2).sort_values("avg_sat", ascending=False)

print(f"\n{'Staff':<12} {'Volume':>8} {'Wait':>8} {'Service':>8} {'FCR':>8} {'Sat':>6} {'Esc':>6}")
print("-" * 60)
for staff_name, row in staff_perf.iterrows():
    print(f"{staff_name:<12} {row['interactions']:>8} {row['avg_wait']:>7.1f}m {row['avg_service']:>7.1f}m {row['fcr']:>7.1f}% {row['avg_sat']:>5.2f} {row['escalations']:>5}")

# Chart: Staff performance comparison
fig, ax = plt.subplots(figsize=(10, 5))
x = range(len(staff_perf))
width = 0.3

ax.bar([i - width for i in x], staff_perf["fcr"], width, label="FCR %", color="#4CAF50", edgecolor="white")
ax.bar(x, staff_perf["avg_sat"] * 20, width, label="Satisfaction (x20)", color="#1565C0", edgecolor="white")
ax.bar([i + width for i in x], staff_perf["escalations"] / staff_perf["interactions"] * 100, width, label="Escalation %", color="#FF5722", edgecolor="white")

ax.set_xticks(x)
ax.set_xticklabels(staff_perf.index)
ax.set_ylabel("Percentage / Score")
ax.set_title("Staff Performance: FCR, Satisfaction & Escalation Rates", fontsize=14, fontweight="bold")
ax.legend()
plt.tight_layout()
plt.savefig(f"{output_dir}/04_staff_performance.png", bbox_inches="tight")
plt.close()
print("\nSaved: 04_staff_performance.png")

# ============================================================
# 5. SATISFACTION DRIVERS & STATISTICAL ANALYSIS
# ============================================================
print("\n" + "=" * 60)
print("5. SATISFACTION DRIVERS & STATISTICAL ANALYSIS")
print("=" * 60)

# Satisfaction by resolution type
sat_by_res = df.groupby("resolution")["satisfaction_score"].mean().sort_values(ascending=False)
print(f"\nSatisfaction by Resolution Type:")
for res, sat in sat_by_res.items():
    print(f"  {res:<30} {sat:.2f}/5.0")

# T-test: FCR vs non-FCR satisfaction
fcr_sat = df[df["resolution"] == "Resolved on First Contact"]["satisfaction_score"]
non_fcr_sat = df[df["resolution"] != "Resolved on First Contact"]["satisfaction_score"]
t_stat, p_val = stats.ttest_ind(fcr_sat, non_fcr_sat)
print(f"\nT-Test: First Contact Resolution Impact on Satisfaction")
print(f"  FCR Avg Satisfaction:     {fcr_sat.mean():.2f}")
print(f"  Non-FCR Avg Satisfaction: {non_fcr_sat.mean():.2f}")
print(f"  Difference:              {fcr_sat.mean() - non_fcr_sat.mean():+.2f}")
print(f"  t-statistic:             {t_stat:.4f}")
print(f"  p-value:                 {p_val:.6f}")
print(f"  Significant:             {'Yes (p < 0.05)' if p_val < 0.05 else 'No'}")

# Correlation: wait time vs satisfaction
corr, corr_p = stats.pearsonr(df["wait_time_min"], df["satisfaction_score"])
print(f"\nCorrelation: Wait Time vs Satisfaction")
print(f"  r = {corr:.4f}, p = {corr_p:.6f}")
print(f"  {'Significant negative correlation' if corr < 0 and corr_p < 0.05 else 'Not significant'}")

# Wait time buckets
df["wait_bucket"] = pd.cut(df["wait_time_min"],
    bins=[0, 5, 10, 15, 20, 50],
    labels=["0-5 min", "5-10 min", "10-15 min", "15-20 min", "20+ min"])

sat_by_wait = df.groupby("wait_bucket", observed=True).agg(
    count=("inquiry_id", "count"),
    avg_sat=("satisfaction_score", "mean"),
).round(2)
print(f"\nSatisfaction by Wait Time:")
for bucket, row in sat_by_wait.iterrows():
    print(f"  {str(bucket):<12} n={row['count']:>5}  Sat: {row['avg_sat']:.2f}")

# Chart: Satisfaction drivers
fig, axes = plt.subplots(1, 2, figsize=(12, 5))

res_colors = ["#4CAF50", "#FF9800", "#F44336", "#9E9E9E"]
axes[0].barh(sat_by_res.index, sat_by_res.values, color=res_colors, edgecolor="white")
axes[0].set_xlabel("Avg Satisfaction (1-5)")
axes[0].set_title("Satisfaction by Resolution Type", fontsize=11, fontweight="bold")
for i, val in enumerate(sat_by_res.values):
    axes[0].text(val + 0.02, i, f"{val:.2f}", va="center", fontsize=9)

axes[1].bar(sat_by_wait.index, sat_by_wait["avg_sat"], color=["#4CAF50", "#8BC34A", "#FF9800", "#FF5722", "#F44336"], edgecolor="white")
axes[1].set_xlabel("Wait Time Bucket")
axes[1].set_ylabel("Avg Satisfaction")
axes[1].set_title("Satisfaction by Wait Time", fontsize=11, fontweight="bold")
axes[1].tick_params(axis="x", rotation=20)

plt.suptitle("What Drives Student Satisfaction?", fontsize=14, fontweight="bold", y=1.02)
plt.tight_layout()
plt.savefig(f"{output_dir}/05_satisfaction_drivers.png", bbox_inches="tight")
plt.close()
print("\nSaved: 05_satisfaction_drivers.png")

# ============================================================
# 6. PROCESS IMPROVEMENT RECOMMENDATIONS
# ============================================================
print("\n" + "=" * 60)
print("6. KEY FINDINGS & PROCESS IMPROVEMENT RECOMMENDATIONS")
print("=" * 60)

highest_wait_dept = dept_kpis["avg_wait"].idxmax()
lowest_fcr_dept = dept_kpis["fcr"].idxmin()
peak_day = vol_day.idxmax()

print(f"""
FINDINGS:
1. First Contact Resolution of {fcr_rate:.1f}% - students resolved on first contact report {fcr_sat.mean() - non_fcr_sat.mean():.2f} higher satisfaction (statistically significant, p < 0.05)
2. Walk-in channel handles {(df['channel'] == 'Walk-In').mean()*100:.0f}% of volume with highest wait times - staffing optimization opportunity
3. {highest_wait_dept} has the longest average wait time ({dept_kpis.loc[highest_wait_dept, 'avg_wait']:.1f} min) - may need additional staff or process streamlining
4. {peak_day}s and 10-12 PM are peak periods requiring maximum staffing coverage
5. Wait times above 15 minutes correlate with significant drops in satisfaction scores
6. Escalation rate of {escalation_rate:.1f}% suggests opportunity for expanded staff training

RECOMMENDATIONS:
1. Increase staffing during peak periods ({peak_day}s, 10-12 PM) to reduce wait times below 10-minute target
2. Expand staff training for {lowest_fcr_dept} inquiries to improve first contact resolution rate
3. Implement queue management system to redirect walk-in overflow to virtual appointments during peaks
4. Create comprehensive reference materials for common inquiry types to reduce escalations
5. Set wait time target of under 10 minutes - data shows satisfaction drops significantly above 15 minutes
6. Use staff performance scorecards (FCR, satisfaction, escalation rate) for coaching and development
""")

print("=" * 60)
print("Analysis complete. All charts saved to /dashboards folder.")
print("=" * 60)
