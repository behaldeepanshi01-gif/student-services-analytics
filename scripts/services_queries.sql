-- ============================================================
-- Student Services Operations Analytics - SQL Queries
-- Dataset: 3,000 student service interactions
-- Departments: Financial Aid, Registrar, SBS, Admissions
-- ============================================================

-- 1. Operational KPIs by Department
SELECT
    department,
    COUNT(*) AS volume,
    ROUND(AVG(wait_time_min), 1) AS avg_wait,
    ROUND(AVG(service_time_min), 1) AS avg_service,
    ROUND(100.0 * SUM(CASE WHEN resolution = 'Resolved on First Contact' THEN 1 ELSE 0 END) / COUNT(*), 1) AS fcr_pct,
    ROUND(AVG(satisfaction_score), 2) AS avg_satisfaction
FROM student_services
GROUP BY department
ORDER BY volume DESC;

-- 2. Volume by Channel with Efficiency Metrics
SELECT
    channel,
    COUNT(*) AS volume,
    ROUND(100.0 * COUNT(*) / (SELECT COUNT(*) FROM student_services), 1) AS pct_total,
    ROUND(AVG(wait_time_min), 1) AS avg_wait,
    ROUND(AVG(service_time_min), 1) AS avg_service,
    ROUND(AVG(satisfaction_score), 2) AS avg_sat
FROM student_services
GROUP BY channel
ORDER BY volume DESC;

-- 3. Peak Period Staffing Analysis
SELECT
    day_of_week,
    time_slot,
    COUNT(*) AS volume,
    ROUND(AVG(wait_time_min), 1) AS avg_wait,
    ROUND(AVG(satisfaction_score), 2) AS avg_sat
FROM student_services
GROUP BY day_of_week, time_slot
ORDER BY volume DESC
LIMIT 10;

-- 4. Staff Performance Scorecards
SELECT
    staff_member,
    COUNT(*) AS interactions,
    ROUND(AVG(wait_time_min), 1) AS avg_wait,
    ROUND(AVG(service_time_min), 1) AS avg_service,
    ROUND(100.0 * SUM(CASE WHEN resolution = 'Resolved on First Contact' THEN 1 ELSE 0 END) / COUNT(*), 1) AS fcr_pct,
    ROUND(AVG(satisfaction_score), 2) AS avg_sat,
    SUM(CASE WHEN escalated = 'Yes' THEN 1 ELSE 0 END) AS escalations
FROM student_services
GROUP BY staff_member
ORDER BY avg_sat DESC;

-- 5. Resolution Type Distribution
SELECT
    resolution,
    COUNT(*) AS volume,
    ROUND(AVG(satisfaction_score), 2) AS avg_sat,
    ROUND(AVG(wait_time_min), 1) AS avg_wait
FROM student_services
GROUP BY resolution
ORDER BY avg_sat DESC;

-- 6. Quarterly Volume and Wait Time Trends
SELECT
    quarter,
    COUNT(*) AS volume,
    ROUND(AVG(wait_time_min), 1) AS avg_wait,
    ROUND(AVG(satisfaction_score), 2) AS avg_sat,
    ROUND(100.0 * SUM(CASE WHEN resolution = 'Resolved on First Contact' THEN 1 ELSE 0 END) / COUNT(*), 1) AS fcr_pct
FROM student_services
GROUP BY quarter
ORDER BY quarter;

-- 7. Escalation Analysis by Department and Inquiry Type
SELECT
    department,
    inquiry_type,
    COUNT(*) AS total,
    SUM(CASE WHEN escalated = 'Yes' THEN 1 ELSE 0 END) AS escalated,
    ROUND(100.0 * SUM(CASE WHEN escalated = 'Yes' THEN 1 ELSE 0 END) / COUNT(*), 1) AS esc_rate
FROM student_services
GROUP BY department, inquiry_type
HAVING COUNT(*) > 20
ORDER BY esc_rate DESC
LIMIT 15;
