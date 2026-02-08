"""
Generate simulated Student Services Operations dataset (3,000 rows)
for Student Services Operations Analytics project.
Simulates data from a university one-stop enrollment services center
handling Financial Aid, Registrar, Admissions, and Student Business Services.
"""

import numpy as np
import pandas as pd

np.random.seed(42)
n = 3000

# ---- Inquiry/Interaction Records ----
inquiry_ids = range(10001, 10001 + n)

# Service departments (mirrors a one-stop shop)
departments = np.random.choice(
    ["Financial Aid", "Registrar", "Student Business Services", "Admissions", "General Inquiry"],
    n, p=[0.30, 0.25, 0.20, 0.15, 0.10]
)

# Channel
channel = np.random.choice(
    ["Walk-In", "Phone", "Email", "Virtual Appointment"],
    n, p=[0.45, 0.25, 0.20, 0.10]
)

# Quarter and month
quarter = np.random.choice(
    ["Fall 2024", "Winter 2025", "Spring 2025", "Summer 2025"],
    n, p=[0.35, 0.25, 0.25, 0.15]
)
month_map = {
    "Fall 2024": ["Sep", "Oct", "Nov", "Dec"],
    "Winter 2025": ["Jan", "Feb", "Mar"],
    "Spring 2025": ["Apr", "May", "Jun"],
    "Summer 2025": ["Jul", "Aug"],
}
months = [np.random.choice(month_map[q]) for q in quarter]

# Day of week
day_of_week = np.random.choice(
    ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"],
    n, p=[0.22, 0.20, 0.20, 0.20, 0.18]
)

# Peak hours
hour = np.random.choice(
    ["8-10 AM", "10-12 PM", "12-2 PM", "2-4 PM"],
    n, p=[0.20, 0.35, 0.25, 0.20]
)

# Staff member
staff = np.random.choice(
    ["Staff A", "Staff B", "Staff C", "Staff D", "Staff E",
     "Staff F", "Staff G", "Staff H"], n
)

# Inquiry type
inquiry_type_map = {
    "Financial Aid": ["FAFSA Status", "Award Letter", "Scholarship Inquiry", "Loan Questions", "Work-Study"],
    "Registrar": ["Transcript Request", "Enrollment Verification", "Grade Change", "Graduation Check", "Add/Drop"],
    "Student Business Services": ["Tuition Payment", "Refund Status", "Payment Plan", "Account Hold", "1098-T"],
    "Admissions": ["Application Status", "Admission Decision", "Transfer Credits", "Orientation", "Residency"],
    "General Inquiry": ["Campus Resources", "Department Referral", "Hours/Location", "General Question", "Complaint"],
}
inquiry_types = [np.random.choice(inquiry_type_map[d]) for d in departments]

# Student type
student_type = np.random.choice(
    ["Undergraduate", "Graduate", "Prospective", "Parent/Guardian"],
    n, p=[0.55, 0.20, 0.15, 0.10]
)

# ---- Operational Metrics ----
# Wait time (minutes) - influenced by channel and quarter
base_wait = np.random.exponential(8, n)
wait_adj = np.where(channel == "Walk-In", 5, 0) + \
           np.where(quarter == "Fall 2024", 4, 0) + \
           np.where(np.isin(months, ["Sep", "Jan"]), 3, 0)
wait_time_min = np.clip(base_wait + wait_adj, 0, 45).round(1)

# Service time (minutes)
base_service = np.random.normal(12, 5, n)
service_adj = np.where(departments == "Financial Aid", 5, 0) + \
              np.where(departments == "Student Business Services", 3, 0) + \
              np.where(channel == "Email", -4, 0)
service_time_min = np.clip(base_service + service_adj, 2, 40).round(1)

# Resolution status
resolution = np.random.choice(
    ["Resolved on First Contact", "Follow-Up Required", "Escalated to Department", "Referred to Another Office"],
    n, p=[0.55, 0.20, 0.15, 0.10]
)

# First contact resolution influenced by inquiry complexity
fcr_boost = np.where(departments == "General Inquiry", 0.15, 0) + \
            np.where(departments == "Registrar", 0.05, 0)

# Satisfaction score (1-5)
base_sat = np.random.normal(3.8, 0.8, n)
sat_adj = np.where(resolution == "Resolved on First Contact", 0.5, 0) + \
          np.where(resolution == "Escalated to Department", -0.3, 0) + \
          np.where(wait_time_min > 20, -0.4, 0) + \
          np.where(wait_time_min < 5, 0.3, 0)
satisfaction = np.clip(base_sat + sat_adj, 1, 5).round(1)

# Escalated flag
escalated = np.where(resolution == "Escalated to Department", "Yes", "No")

# Callback required
callback = np.where(resolution == "Follow-Up Required",
                    np.random.choice(["Yes", "No"], n, p=[0.70, 0.30]),
                    "No")

# ---- BUILD DATAFRAME ----
df = pd.DataFrame({
    "inquiry_id": inquiry_ids,
    "department": departments,
    "inquiry_type": inquiry_types,
    "channel": channel,
    "student_type": student_type,
    "quarter": quarter,
    "month": months,
    "day_of_week": day_of_week,
    "time_slot": hour,
    "staff_member": staff,
    "wait_time_min": wait_time_min,
    "service_time_min": service_time_min,
    "resolution": resolution,
    "escalated": escalated,
    "callback_required": callback,
    "satisfaction_score": satisfaction,
})

# Save
df.to_csv("C:/Users/Deepanshi/Desktop/student-services-analytics/data/student_services_data.csv", index=False)
print(f"Dataset created: {len(df)} student service interactions")
print(f"\nDepartments:\n{df['department'].value_counts()}")
print(f"\nChannels:\n{df['channel'].value_counts()}")
print(f"\nResolution:\n{df['resolution'].value_counts()}")
print(f"\nAvg Wait Time: {df['wait_time_min'].mean():.1f} min")
print(f"Avg Service Time: {df['service_time_min'].mean():.1f} min")
print(f"Avg Satisfaction: {df['satisfaction_score'].mean():.2f}/5.0")
print(f"First Contact Resolution: {(df['resolution'] == 'Resolved on First Contact').mean()*100:.1f}%")
