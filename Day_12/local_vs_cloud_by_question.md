# Local vs cloud, by question (cells are local / cloud)

Questions whose retrieved context is identical in both runs: 20 of 20.

## Judge noise on identical contexts (mean and max |cloud - local|)

| Metric | Questions | Mean abs diff | Max abs diff |
|---|---|---|---|
| Contextual Relevancy | 20 | 0.040 | 0.101 |
| Contextual Recall | 20 | 0.075 | 0.500 |
| Contextual Precision | 20 | 0.019 | 0.160 |

## Scores and checks

| id | type | Faithfulness | Answer Relevancy | Contextual Relevancy | Contextual Recall | Contextual Precision | refusal phrase | hand passed | time (s) | finish |
|---|---|---|---|---|---|---|---|---|---|---|
| q01 | factual | 0.67 / 1.00 | 1.00 / 1.00 | 0.19 / 0.17 | 1.00 / 1.00 | 1.00 / 1.00 | no / no | T / T | 117.8 / 3.3 | stop / stop |
| q02 | factual | 1.00 / 1.00 | 1.00 / 1.00 | 0.12 / 0.12 | 1.00 / 1.00 | 1.00 / 0.84 | no / no | T / T | 79.1 / 1.1 | stop / stop |
| q03 | factual | 1.00 / 1.00 | 1.00 / 1.00 | 0.18 / 0.08 | 1.00 / 1.00 | 1.00 / 1.00 | no / no | T / T | 73.4 / 1.2 | stop / stop |
| q04 | factual | 0.67 / 1.00 | 1.00 / 1.00 | 0.11 / 0.21 | 1.00 / 1.00 | 0.75 / 0.75 | no / no | T / T | 84.9 / 0.8 | stop / stop |
| q05 | factual | 1.00 / 1.00 | 1.00 / 1.00 | 0.09 / 0.19 | 1.00 / 1.00 | 1.00 / 1.00 | no / no | T / T | 78.1 / 1.3 | stop / stop |
| q06 | comparison | 0.84 / 1.00 | 1.00 / 1.00 | 0.65 / 0.64 | 1.00 / 1.00 | 0.54 / 0.61 | no / no | F / T | 207.3 / 1.6 | stop / stop |
| q07 | comparison | 1.00 / 0.78 | 1.00 / 1.00 | 0.30 / 0.23 | 1.00 / 1.00 | 1.00 / 1.00 | no / no | T / T | 161.1 / 1.4 | stop / stop |
| q08 | synthesis | 1.00 / 1.00 | 1.00 / 1.00 | 0.11 / 0.14 | 1.00 / 1.00 | 1.00 / 1.00 | no / no | T / T | 97.0 / 1.0 | stop / stop |
| q09 | multi_document | 0.75 / 1.00 | 1.00 / 1.00 | 0.31 / 0.33 | 1.00 / 1.00 | 0.57 / 0.54 | no / no | T / T | 125.3 / 1.2 | stop / stop |
| q10 | multi_document | 0.86 / 1.00 | 1.00 / 1.00 | 0.26 / 0.35 | 1.00 / 1.00 | 0.93 / 0.93 | no / no | T / T | 107.3 / 3.2 | stop / stop |
| q11 | synthesis | 1.00 / 1.00 | 1.00 / 1.00 | 0.27 / 0.25 | 1.00 / 1.00 | 0.81 / 0.85 | no / no | T / T | 83.5 / 1.5 | stop / stop |
| q12 | conflict | 0.50 / 1.00 | 1.00 / 1.00 | 0.09 / 0.07 | 1.00 / 0.67 | 0.92 / 0.92 | no / no | T / F | 100.4 / 2.0 | stop / stop |
| q13 | partially_answerable | 0.80 / 1.00 | 1.00 / 0.33 | 0.04 / 0.04 | 1.00 / 0.50 | 0.67 / 0.67 | yes / no | T / T | 118.4 / 1.8 | stop / stop |
| q14 | table_reasoning | 0.00 / 0.00 | 1.00 / 1.00 | 0.11 / 0.08 | 1.00 / 1.00 | 1.00 / 1.00 | no / yes | F / F | 106.3 / 0.8 | stop / stop |
| q15 | conflict | 0.00 / 0.00 | 1.00 / 1.00 | 0.11 / 0.10 | 0.00 / 0.00 | 0.54 / 0.54 | no / no | T / T | 91.5 / 0.8 | stop / stop |
| q16 | conflict | 0.86 / 1.00 | 0.88 / 0.75 | 0.41 / 0.45 | 1.00 / 1.00 | 0.75 / 0.75 | no / no | T / T | 104.8 / 1.3 | stop / stop |
| q17 | conflict | 1.00 / 1.00 | 1.00 / 0.67 | 0.32 / 0.28 | 0.67 / 0.50 | 0.93 / 1.00 | no / no | T / T | 94.8 / 1.0 | stop / stop |
| q18 | partially_answerable | 0.00 / 0.00 | 1.00 / 1.00 | 0.00 / 0.00 | 0.50 / 1.00 | 0.00 / 0.00 | yes / yes | F / F | 80.1 / 1.6 | stop / stop |
| q19 | unanswerable | 0.83 / 0.00 | 0.57 / 1.00 | 0.35 / 0.26 | 0.50 / 0.50 | 0.97 / 0.97 | yes / yes | T / T | 82.9 / 3.5 | stop / stop |
| q20 | unanswerable | 0.00 / 0.00 | 1.00 / 1.00 | 0.00 / 0.00 | 0.00 / 0.00 | 1.00 / 1.00 | yes / yes | T / T | 75.2 / 1.0 | stop / stop |

## Differences of at least 0.2 on one metric (compare with the judge noise above)

- q19, Faithfulness: local 0.83, cloud 0.00 (-0.83)
- q13, Answer Relevancy: local 1.00, cloud 0.33 (-0.67)
- q18, Contextual Recall: local 0.50, cloud 1.00 (+0.50)
- q13, Contextual Recall: local 1.00, cloud 0.50 (-0.50)
- q12, Faithfulness: local 0.50, cloud 1.00 (+0.50)
- q19, Answer Relevancy: local 0.57, cloud 1.00 (+0.43)
- q17, Answer Relevancy: local 1.00, cloud 0.67 (-0.33)
- q12, Contextual Recall: local 1.00, cloud 0.67 (-0.33)
- q04, Faithfulness: local 0.67, cloud 1.00 (+0.33)
- q01, Faithfulness: local 0.67, cloud 1.00 (+0.33)
- q09, Faithfulness: local 0.75, cloud 1.00 (+0.25)
- q07, Faithfulness: local 1.00, cloud 0.78 (-0.22)

## Answers side by side

### q01 (factual): What is the annual price per user for the Professional tier?
- Expected: The Professional tier costs 66 EUR per user per month when billed annually (79 EUR per user per month when billed monthly).
- Local: Based on the provided context, the **annual price per user** for the **Professional tier** is **€66**. This information can be found in the "Per-Product Pricing" table under section 5.1 of the product guide: * **Tier:** Professional * **Annual Price (per user):** €66/user/month (billed annually) *Note: There is also a bundled annual price for the …
- Cloud: The annual price for the Professional tier is **€66 per user per month, billed annually**.

### q02 (factual): What uptime SLA does the Enterprise tier guarantee?
- Expected: The Enterprise tier guarantees 99.95% uptime, which allows a maximum of about 21 minutes of downtime per month.
- Local: The Enterprise tier guarantees an uptime SLA of **99.95%**.
- Cloud: The Enterprise tier guarantees **99.95% uptime**, measured over a calendar month.

### q03 (factual): How long is the free trial, and what are its limits?
- Expected: The free trial lasts 14 days and includes full Professional-tier features. No credit card is required. Trial workspaces are limited to 10 users and 5 GB of storage.
- Local: The free trial lasts for **14 days** and includes full Professional-tier features. No credit card is required to start a trial. Trial workspaces are limited to: - **10 users** - **5 GB of storage**
- Cloud: The free trial lasts **14 days** and includes full **Professional-tier features**. No credit card is required. Trial workspaces are limited to: - **10 users** - **5 GB of storage**

### q04 (factual): What is the response time for critical issues on the Professional tier?
- Expected: The Professional tier has a 1 hour response time for critical (service down) issues.
- Local: The response time for critical issues on the Professional tier is **1 hour**. This information is found in the "Support Response Times" table under the 7.3 section of the product guide, which lists: * **Severity:** Critical (service down) * **Professional Tier:** 1 hour
- Cloud: The response time for critical issues on the Professional tier is **1 hour**.

### q05 (factual): How many days of paid time off do full-time employees receive per year?
- Expected: Full-time employees receive 25 days of paid time off per calendar year, in addition to public holidays observed at their office location. Part-time employees receive PTO pro rata.
- Local: Full-time employees receive **twenty-five (25) days** of paid time off (PTO) per calendar year, in addition to public holidays observed at their respective office location.
- Cloud: Full-time employees receive **25 days of paid time off (PTO) per calendar year**, in addition to public holidays.

### q06 (comparison): Compare the Professional and Enterprise support tiers.
- Expected: Professional has support during extended business hours (06:00-22:00 CET, Monday to Friday), email support, live chat during business hours, and a 1 hour response time for critical issues. Enterprise has 24/7 support including live chat and phone, a dedicated support manager, and a 15 minute response time for critical issues.
- Local: Based on the provided documents, here is a comparison between the **Professional** and **Enterprise** support tiers: ### 1. Response Times (Severity-Based) * **Critical (service down):** * Professional: 2 hours * Enterprise: 15 minutes * **High (major feature broken):** * Professional: 2 hours * Enterprise: 30 minutes * **Medium (minor feature iss…
- Cloud: | Aspect | Professional | Enterprise | |---|---|---| | **Critical response** | 1 hour | 15 minutes | | **High-severity response** | 2 hours | 30 minutes | | **Medium-severity response** | 8 hours | 2 hours | | **Low-severity response** | 24 hours | 8 hours | | **Support availability** | Extended business hours: 06:00–22:00 CET, Monday–Friday | 24/…

### q07 (comparison): How do the Enterprise and Professional tiers compare in number of accounts, revenue contribution and average contract value?
- Expected: Enterprise has 52 accounts (6.1%) contributing EUR 2.93M (61.0% of revenue), with an average contract value of EUR 56,346. Professional has 283 accounts (33.4%) contributing EUR 1.39M (29.0%), with an average contract value of EUR 4,912.
- Local: Based on the provided context, here is the comparison between the Enterprise and Professional tiers: * **Number of Accounts:** * **Enterprise:** 52 accounts (representing 6.1% of the total base). * **Professional:** 283 accounts (representing 33.4% of the total base). * *Comparison:* The Professional tier has significantly more accounts than the E…
- Cloud: | Tier | Accounts | Revenue contribution | Average contract value | |---|---:|---:|---:| | Enterprise | 52 (6.1% of accounts) | €2.93M (61.0%) | €56,346 | | Professional | 283 (33.4% of accounts) | €1.39M (29.0%) | €4,912 | Enterprise has far fewer accounts than Professional but contributes more than twice the revenue, with an average contract val…

### q08 (synthesis): What does the AI Task Prioritization Engine do, which tiers can use it, and how well has it been adopted?
- Expected: It uses machine learning models to analyze historical project data and recommend task prioritization. It is available to the Professional and Enterprise tiers. 34% of eligible accounts activated it within the first six weeks.
- Local: Based on the provided context: * **Function:** The AI Task Prioritization Engine uses machine learning models to analyze historical project data and recommend task prioritization. * **Available Tiers:** It is available to **Professional** and **Enterprise** tiers. * **Adoption:** Early adoption has been strong, with **34% of eligible accounts** ac…
- Cloud: The AI Task Prioritization Engine uses machine-learning models to analyze historical project data and recommend how tasks should be prioritized. It is available to **Professional and Enterprise** tiers. Adoption has been strong: **34% of eligible accounts activated it within the first six weeks**.

### q09 (multi_document): How many employees does NovaTech have?
- Expected: The documents give different figures for different dates. The employee handbook and the product guide say approximately 400. The January 15, 2026 leadership meeting notes say 396 as of January 1. The Q1 2026 report says 412 full-time employees at the end of Q1 (up from 374 at the end of Q4 2025, which does not match the 396 figure). The most recen…
- Local: Based on the provided documents, NovaTech Solutions ended **Q1 2026** with **412 full-time employees**. This information is found in the *quarterly_report_q1_2026.pdf* under section **6.1 Headcount Summary**, which states: "NovaTech Solutions ended Q1 2026 with 412 full-time employees, up from 374 at the end of Q4 2025." Additionally, the *company…
- Cloud: NovaTech Solutions had **412 full-time employees at the end of Q1 2026**.

### q10 (multi_document): What security awareness training must employees complete, and when?
- Expected: The security policy requires all employees to complete Information Security Awareness training within 30 days of joining and annually thereafter; employees with access to Confidential or Restricted data must also complete the Advanced Data Handling module, and access is suspended if training is not completed on time. The February 12, 2026 leadersh…
- Local: Based on the provided context, here are the requirements for security awareness training: **Mandatory Training:** * **Content:** All NovaTech employees must complete **Information Security Awareness training**. This covers data classification and handling, phishing recognition, password hygiene, incident reporting, and acceptable use. * **Timing:*…
- Cloud: All employees must complete Information Security Awareness training within 30 days of joining NovaTech and annually thereafter. It covers: - Data classification and handling - Phishing recognition - Password hygiene - Incident reporting - Acceptable use Employees who access Confidential or Restricted data must also complete the Advanced Data Handl…

### q11 (synthesis): What are the acknowledgment times for P1, P2, P3 and P4 security incidents?
- Expected: P1 (critical) incidents must be acknowledged within 15 minutes of detection, P2 (high) within 1 hour, P3 (medium) within 4 hours, and P4 (low) within 24 hours.
- Local: Based on the provided context, here are the acknowledgment times for each incident severity level: * **P1 (Critical):** 15 minutes of detection. * **P2 (High):** 1 hour of detection. * **P3:** 4 hours of detection. * **P4 (Low):** 24 hours.
- Cloud: - **P1 (Critical):** Within **15 minutes** of detection - **P2 (High):** Within **1 hour** of detection - **P3:** Within **4 hours** of detection - **P4 (Low):** Within **24 hours**

### q12 (conflict): How much does a dedicated support manager cost for an Enterprise customer?
- Expected: The product guide is inconsistent. Section 5.3 lists a dedicated support manager as a 2,000 EUR per month add-on for Enterprise only, while the support sections say Enterprise customers receive a dedicated support manager as part of their support.
- Local: Based on the provided context, a **dedicated support manager** costs **€2,000/month** for Enterprise customers. *Source: product_guide.pdf, page 11 (Section 5.3 Add-Ons)*
- Cloud: A dedicated support manager costs **€2,000 per month** for Enterprise customers.

### q13 (partially_answerable): How often does the Jira integration sync for Starter customers?
- Expected: The guide says the Jira integration is available on all tiers, but it gives sync frequencies only for Professional (every 10 minutes) and Enterprise (every 2 minutes). The Starter frequency is not stated.
- Local: Based on the provided context, the **Jira integration sync frequency is not specified for Starter customers**. The document states: * "Sync frequency: every 10 minutes (Professional), every 2 minutes (Enterprise)." * In the table on page 20, the Jira integration is listed as available on **"All tiers"**, but it does not list a specific sync interv…
- Cloud: The provided documents do not specify a Jira sync frequency for Starter customers. They state that syncing occurs every 10 minutes for Professional and every 2 minutes for Enterprise.

### q14 (table_reasoning): What service credit does a Professional customer receive if uptime for the month is 99.5%?
- Expected: A Professional customer receives a 10% service credit, because 99.5% falls in the 98.0%-99.89% band. Credits are applied to the next billing cycle and cannot exceed 30% of the monthly fee.
- Local: Based on the provided context, a Professional customer would receive **10%** service credits if the uptime for the month was 99.5%. This is found in the "SLA Credits" table under the row where Uptime Achieved is "99.9% - 99.94%" (which covers 99.5%) and the column for "Professional Credit".
- Cloud: I cannot find this information in the provided documents.

### q15 (conflict): When was ProjectHub v3.2 released?
- Expected: The documents conflict. The Q1 2026 report says v3.2 was released on February 12, 2026, while the leadership meeting notes (the meeting held on February 12) say it shipped on January 28, two weeks behind the original schedule.
- Local: ProjectHub v3.2 was released on **January 28, 2026**.
- Cloud: ProjectHub v3.2 was released on January 28, 2026.

### q16 (conflict): What is the maximum number of remote work days per week?
- Expected: The employee handbook (effective January 1, 2026) allows up to 3 remote days per week with manager approval (1 day during the six-month probation). At the March 5, 2026 leadership meeting the policy was updated to up to 4 remote days per week, effective Q3 2026, with Tuesday as the mandatory in-office day. So the limit is 3 days and becomes 4 from…
- Local: Based on the provided context, the **maximum** number of remote work days per week is **4 days**. This was established in the meeting notes (page 7) and proposed by Aisha Patel to be effective Q3 2026: * The policy will allow up to **4 days remote** per week. * **Tuesday** remains the mandatory in-office day company-wide. * Department heads may se…
- Cloud: The maximum is **4 remote work days per week**, effective Q3 2026. Tuesday is the mandatory in-office day, though department heads may require additional in-office days with HR approval.

### q17 (conflict): How often must employees change their passwords?
- Expected: The employee handbook says every 90 days (with a minimum of 14 characters). At the March 5, 2026 leadership meeting, rotation for employee user accounts was extended to 180 days, effective immediately, while infrastructure credentials stay on 90 days. The handbook does not reflect the change.
- Local: Based on the provided context, specifically the current **company_handbook.pdf** (page 14), employees are required to change their passwords every **90 days**. However, during the meeting, it was decided to extend this rotation period. As noted in the **meeting_notes.pdf** (page 7), the decision was made to extend password rotation from 90 days to…
- Cloud: Employees must change their passwords every **180 days** under the updated policy, effective immediately. Infrastructure credentials remain subject to **90-day** rotation.

### q18 (partially_answerable): Does NovaTech offer a native mobile app for iOS and Android?
- Expected: No mobile app is described as currently available. The Q1 2026 report's roadmap lists a ProjectHub Mobile App (iOS/Android) targeted for Q3 2026, currently in the design phase.
- Local: I cannot find this information in the provided documents.
- Cloud: I cannot find this information in the provided documents.

### q19 (unanswerable): What is the company's position on remote work for contractors?
- Expected: The documents do not contain information about contractor remote work policies. The remote work policy in the handbook refers to employees only.
- Local: I cannot find this information in the provided documents. The context discusses remote work policies primarily for employees, including eligibility based on probationary periods, cross-border restrictions, and allowances for regular remote workers. There is no specific mention of contractors or their remote work arrangements.
- Cloud: I cannot find this information in the provided documents.

### q20 (unanswerable): What is the company's dress code?
- Expected: The documents do not contain information about a dress code.
- Local: I cannot find this information in the provided documents.
- Cloud: I cannot find this information in the provided documents.

Read these pairs and answer, by id, where the cloud model fixed a local failure, where it did not, and where it was worse. The scores alone cannot tell you that.
