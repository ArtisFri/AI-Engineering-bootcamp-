# Judge vs your own ratings (local run)

## Rule A: generation metrics pass (Faithfulness and Answer Relevancy)

| Case | Count | Question ids |
|---|---|---|
| both pass | 11 | q02, q03, q05, q07, q08, q09, q10, q11, q13, q16, q17 |
| both fail | 2 | q14, q18 |
| judge pass, you fail | 1 | q06 |
| judge fail, you pass | 6 | q01, q04, q12, q15, q19, q20 |

### q06: judge pass, you fail
- Question: Compare the Professional and Enterprise support tiers.
- Your note: says the Professional critical response time is 2 hours, in both the list and the summary table. The guide says 1 hour.
- Answer: Based on the provided documents, here is a comparison between the **Professional** and **Enterprise** support tiers: ### 1. Response Times (Severity-Based) * **Critical (service down):** * Professional: 2 hours * Enterprise: 15 minutes * **High (maj…

### q01: judge fail, you pass
- Question: What is the annual price per user for the Professional tier?
- Your note: right number
- Answer: Based on the provided context, the **annual price per user** for the **Professional tier** is **€66**. This information can be found in the "Per-Product Pricing" table under section 5.1 of the product guide: * **Tier:** Professional * **Annual Price…
- Judge, Faithfulness = 0.6666666666666666: The score is 0.67 because the actual output goes beyond the context by claiming a "Per-Product Pricing" table, section 5.1, and a product guide that are not mentioned there, even though the context does confirm the Professional annual price and pricing tier.

### q04: judge fail, you pass
- Question: What is the response time for critical issues on the Professional tier?
- Your note: right number
- Answer: The response time for critical issues on the Professional tier is **1 hour**. This information is found in the "Support Response Times" table under the 7.3 section of the product guide, which lists: * **Severity:** Critical (service down) * **Profes…
- Judge, Faithfulness = 0.6666666666666666: The score is 0.67 because the actual output refers to a "7.3 section of the product guide," but the context only confirms the support response times and does not mention any such section.

### q12: judge fail, you pass
- Question: How much does a dedicated support manager cost for an Enterprise customer?
- Your note: it answers 2,000 EUR/month but never notes the conflict
- Answer: Based on the provided context, a **dedicated support manager** costs **€2,000/month** for Enterprise customers. *Source: product_guide.pdf, page 11 (Section 5.3 Add-Ons)*
- Judge, Faithfulness = 0.5: The score is 0.50 because the actual output cites product_guide.pdf, page 11, and Section 5.3 Add-Ons, but the retrieval context does not mention any of those details, so the source citation cannot be verified from the provided facts.

### q15: judge fail, you pass
- Question: When was ProjectHub v3.2 released?
- Your note: answers January 28 only.
- Answer: ProjectHub v3.2 was released on **January 28, 2026**.
- Judge, Faithfulness = 0.0: The score is 0.00 because the actual output treated ProjectHub v3.2 as shipping on January 28, 2026, but the context only says it shipped on January 28 and does not confirm the year.

### q19: judge fail, you pass
- Question: What is the company's position on remote work for contractors?
- Your note: correctly says the documents do not cover it
- Answer: I cannot find this information in the provided documents. The context discusses remote work policies primarily for employees, including eligibility based on probationary periods, cross-border restrictions, and allowances for regular remote workers. …
- Judge, Answer Relevancy = 0.5714285714285714: The score is 0.57 because the response appears to address remote work generally, but it includes unrelated discussion about probationary periods, cross-border restrictions, and allowances for regular remote workers that do not answer the specific question about contractors. It is not higher because these off-topic details dilute the relevance, but…

### q20: judge fail, you pass
- Question: What is the company's dress code?
- Your note: correctly says the documents do not cover it
- Answer: I cannot find this information in the provided documents.
- Judge, Faithfulness = 0.0: The score is 0.00 because the actual output claims it cannot find the requested information in the provided documents, but the retrieval context is only an employee handbook and does not support that claim at all.

## Rule B: all five metrics pass

| Case | Count | Question ids |
|---|---|---|
| both pass | 0 | - |
| both fail | 3 | q06, q14, q18 |
| judge pass, you fail | 0 | - |
| judge fail, you pass | 17 | q01, q02, q03, q04, q05, q07, q08, q09, q10, q11, q12, q13, q15, q16, q17, q19, q20 |

### q01: judge fail, you pass
- Question: What is the annual price per user for the Professional tier?
- Your note: right number
- Answer: Based on the provided context, the **annual price per user** for the **Professional tier** is **€66**. This information can be found in the "Per-Product Pricing" table under section 5.1 of the product guide: * **Tier:** Professional * **Annual Price…
- Judge, Faithfulness = 0.6666666666666666: The score is 0.67 because the actual output goes beyond the context by claiming a "Per-Product Pricing" table, section 5.1, and a product guide that are not mentioned there, even though the context does confirm the Professional annual price and pricing tier.
- Judge, Contextual Relevancy = 0.1896551724137931: The score is 0.19 because most of the retrieved context is off-topic, e.g. it says the question is not answered by items about "Starter", "Enterprise", add-ons, churn, or "customer concentration and ARR." However, a few lines are relevant and do mention Professional pricing, such as "Per-Product Pricing lists the Professional tier with a monthly p…

### q02: judge fail, you pass
- Question: What uptime SLA does the Enterprise tier guarantee?
- Your note: right number
- Answer: The Enterprise tier guarantees an uptime SLA of **99.95%**.
- Judge, Contextual Relevancy = 0.12: The score is 0.12 because most of the retrieved text is about unrelated topics like "service credits," "Support Response Times," and "custom data residency," which do not answer the Enterprise uptime SLA question. Only a small portion is relevant, especially "Enterprise 99.95% ~21 minutes Calendar month" and "NovaTech provides uptime guarantees ba…

### q03: judge fail, you pass
- Question: How long is the free trial, and what are its limits?
- Your note: right numbers
- Answer: The free trial lasts for **14 days** and includes full Professional-tier features. No credit card is required to start a trial. Trial workspaces are limited to: - **10 users** - **5 GB of storage**
- Judge, Contextual Relevancy = 0.18: The score is 0.18 because most of the retrieval context is unrelated to the free trial question, such as "Feature Comparison by Tier," "PTO carryover limits," and "OAuth parameters." However, it does include a directly relevant answer: "All tiers include a 14-day free trial with full Professional-tier features" and "Trial workspaces are limited to…

### q04: judge fail, you pass
- Question: What is the response time for critical issues on the Professional tier?
- Your note: right number
- Answer: The response time for critical issues on the Professional tier is **1 hour**. This information is found in the "Support Response Times" table under the 7.3 section of the product guide, which lists: * **Severity:** Critical (service down) * **Profes…
- Judge, Faithfulness = 0.6666666666666666: The score is 0.67 because the actual output refers to a "7.3 section of the product guide," but the context only confirms the support response times and does not mention any such section.
- Judge, Contextual Relevancy = 0.1111111111111111: The score is 0.11 because most of the context is off-topic, e.g. it says things like "The question is about critical issues, so the part 'High (major feature broken) 8 hours 2 hours 30 minutes' is not relevant" and "This is a general incident response overview and does not state the response time for critical issues on the Professional tier." Only…

### q05: judge fail, you pass
- Question: How many days of paid time off do full-time employees receive per year?
- Your note: right number
- Answer: Full-time employees receive **twenty-five (25) days** of paid time off (PTO) per calendar year, in addition to public holidays observed at their respective office location.
- Judge, Contextual Relevancy = 0.09375: The score is 0.09 because most of the retrieved text is unrelated, such as “mandatory in-office day per week,” “remote work policy,” and “professional development budget,” which do not answer the PTO question. Only one statement is directly relevant: “Full-time employees receive twenty-five days of paid time off per calendar year,” so the context …

### q07: judge fail, you pass
- Question: How do the Enterprise and Professional tiers compare in number of accounts, revenue contribution and average contract value?
- Your note: right numbers
- Answer: Based on the provided context, here is the comparison between the Enterprise and Professional tiers: * **Number of Accounts:** * **Enterprise:** 52 accounts (representing 6.1% of the total base). * **Professional:** 283 accounts (representing 33.4% …
- Judge, Contextual Relevancy = 0.29545454545454547: The score is 0.30 because the context contains the needed tier data, such as "Enterprise has 52 accounts (6.1%), EUR 2.93M revenue contribution (61.0%), and EUR 56,346 average contract value" and "Professional has 283 accounts (33.4%), EUR 1.39M revenue contribution (29.0%), and EUR 4,912 average contract value," but much of the retrieval is off-t…

### q08: judge fail, you pass
- Question: What does the AI Task Prioritization Engine do, which tiers can use it, and how well has it been adopted?
- Your note: right explanation
- Answer: Based on the provided context: * **Function:** The AI Task Prioritization Engine uses machine learning models to analyze historical project data and recommend task prioritization. * **Available Tiers:** It is available to **Professional** and **Ente…
- Judge, Contextual Relevancy = 0.10638297872340426: The score is 0.11 because most retrieved items are unrelated—e.g., "Smart Dependency Mapping" and "Enhanced Gantt View"—and many others "do not answer what the AI Task Prioritization Engine does, which tiers can use it, or how well it has been adopted." Only a small portion is on target, stating the engine "uses machine learning models to analyze …

### q09: judge fail, you pass
- Question: How many employees does NovaTech have?
- Your note: it gives 412 and about 400, the right figures. It doesn’t mention the 396 from the January meeting notes.
- Answer: Based on the provided documents, NovaTech Solutions ended **Q1 2026** with **412 full-time employees**. This information is found in the *quarterly_report_q1_2026.pdf* under section **6.1 Headcount Summary**, which states: "NovaTech Solutions ended …
- Judge, Contextual Relevancy = 0.3103448275862069: The score is 0.31 because most of the retrieval context is off-topic, such as "founded in 2017 in Munich, Germany" and "annual recurring revenue of approximately €17 million," which do not answer the employee-count question. However, a few lines are directly relevant, including "NovaTech Solutions ended Q1 2026 with 412 full-time employees" and "E…
- Judge, Contextual Precision = 0.56875: The score is 0.57 because the retrieval contexts mix several relevant headcount nodes with many irrelevant nodes ranked above and between them. For example, the 1st node in the retrieval contexts is relevant because it quotes "approximately 400 employees across three offices," and the 4th node is also relevant because it says "NovaTech Solutions e…

### q10: judge fail, you pass
- Question: What security awareness training must employees complete, and when?
- Your note: correct response and even extended
- Answer: Based on the provided context, here are the requirements for security awareness training: **Mandatory Training:** * **Content:** All NovaTech employees must complete **Information Security Awareness training**. This covers data classification and ha…
- Judge, Contextual Relevancy = 0.2619047619047619: The score is 0.26 because the context does include the direct answer that "All NovaTech employees must complete the Information Security Awareness training within 30 days of joining the Company and annually thereafter" and that "New hires must complete the training within 30 days of onboarding," but much of the rest is off-topic, like "Completion …

### q11: judge fail, you pass
- Question: What are the acknowledgment times for P1, P2, P3 and P4 security incidents?
- Your note: correct numbers
- Answer: Based on the provided context, here are the acknowledgment times for each incident severity level: * **P1 (Critical):** 15 minutes of detection. * **P2 (High):** 1 hour of detection. * **P3:** 4 hours of detection. * **P4 (Low):** 24 hours.
- Judge, Contextual Relevancy = 0.2702702702702703: The score is 0.27 because most of the retrieved material is off-topic, e.g. it is “about investigation and escalation timing, not the acknowledgment times” and includes unrelated details like “encryption standards” and “training and compliance measures.” However, the context does contain the needed facts: “P1 incidents require acknowledgment withi…

### q12: judge fail, you pass
- Question: How much does a dedicated support manager cost for an Enterprise customer?
- Your note: it answers 2,000 EUR/month but never notes the conflict
- Answer: Based on the provided context, a **dedicated support manager** costs **€2,000/month** for Enterprise customers. *Source: product_guide.pdf, page 11 (Section 5.3 Add-Ons)*
- Judge, Faithfulness = 0.5: The score is 0.50 because the actual output cites product_guide.pdf, page 11, and Section 5.3 Add-Ons, but the retrieval context does not mention any of those details, so the source citation cannot be verified from the provided facts.
- Judge, Contextual Relevancy = 0.09090909090909091: The score is 0.09 because most of the retrieval context is about unrelated support timings, feature limits, and CRM/pricing details, e.g. "The statement \"7.3 Support Response Times\" is about support timing, not the cost of a dedicated support manager" and "The statement about \"Custom data residency\" costing \"€3,000/month\" is unrelated." Only…

### q13: judge fail, you pass
- Question: How often does the Jira integration sync for Starter customers?
- Your note: correct response and even extended
- Answer: Based on the provided context, the **Jira integration sync frequency is not specified for Starter customers**. The document states: * "Sync frequency: every 10 minutes (Professional), every 2 minutes (Enterprise)." * In the table on page 20, the Jir…
- Judge, Contextual Relevancy = 0.038461538461538464: The score is 0.04 because most of the context is unrelated to Starter Jira sync, and the only relevant Jira details say “Sync frequency: every 10 minutes (Professional), every 2 minutes (Enterprise)” and “Jira (Cloud and Server) sync is bidirectional and available on all tiers,” which still do not answer how often it syncs for Starter customers.
- Judge, Contextual Precision = 0.6666666666666666: The score is 0.67 because the relevant retrieval context nodes are placed high but not perfectly: the 1st node directly mentions Jira sync timing with "Sync frequency: every 10 minutes (Professional), every 2 minutes (Enterprise)," which is useful for the question, and the 6th node also stays on-topic with "Jira (Cloud and Server) Bidirectional sy…

### q15: judge fail, you pass
- Question: When was ProjectHub v3.2 released?
- Your note: answers January 28 only.
- Answer: ProjectHub v3.2 was released on **January 28, 2026**.
- Judge, Faithfulness = 0.0: The score is 0.00 because the actual output treated ProjectHub v3.2 as shipping on January 28, 2026, but the context only says it shipped on January 28 and does not confirm the year.
- Judge, Contextual Relevancy = 0.10909090909090909: The score is 0.11 because most of the retrieval context is unrelated to the release date question, like "The statement focuses on metrics such as '89% of existing customers upgraded'" and "The context is about API endpoints, not a release date". However, it does contain a directly relevant clue: "ProjectHub v3.2 launched and was shipped January 28…
- Judge, Contextual Recall = 0.0: The score is 0.00 because sentence 1 of the expected output claims a document conflict, but node(s) in retrieval context do not explicitly state any conflict. Node 1 and node 8 only indicate v3.2 shipped on Jan 28 / launch results, and node 9 says the launch was in February, while nothing in the retrieval context supports the Q1 2026 report saying…
- Judge, Contextual Precision = 0.5396825396825397: The score is 0.54 because the most relevant node in the retrieval contexts appears first, with node 1 saying v3.2 was "shipped January 28, two weeks behind original schedule," which strongly supports the release date. The score is not higher because several irrelevant nodes in the retrieval contexts are ranked above other relevant ones, such as no…

### q16: judge fail, you pass
- Question: What is the maximum number of remote work days per week?
- Your note: right number
- Answer: Based on the provided context, the **maximum** number of remote work days per week is **4 days**. This was established in the meeting notes (page 7) and proposed by Aisha Patel to be effective Q3 2026: * The policy will allow up to **4 days remote**…
- Judge, Contextual Relevancy = 0.40816326530612246: The score is 0.41 because the context contains some direct policy details like "Remote work policy updated to allow up to 4 days remote per week" and "Current policy allows up to 3 days remote per week," but much of it is off-topic, including "Password Rotation Policy Review" and "the maximum number of remote work days per week" being unrelated to…

### q17: judge fail, you pass
- Question: How often must employees change their passwords?
- Your note: right explanation and numbers
- Answer: Based on the provided context, specifically the current **company_handbook.pdf** (page 14), employees are required to change their passwords every **90 days**. However, during the meeting, it was decided to extend this rotation period. As noted in t…
- Judge, Contextual Relevancy = 0.3181818181818182: The score is 0.32 because most of the retrieved text is unrelated to password policy, such as references to "remote work policy changes," "access approval and background verification," and "incident response timeline," while only a smaller portion directly answers the question, including "The current IT security policy mandates password changes ev…
- Judge, Contextual Recall = 0.6666666666666666: The score is 0.67 because sentence 1 is supported by node 1 and node 5 in retrieval context, which mention the 14-character minimum and 90-day password rule; sentence 2 is also supported by node 2 and node 3, which mention the 180-day employee account rotation and 90-day infrastructure credentials; but sentence 3 is not fully attributable because …

### q19: judge fail, you pass
- Question: What is the company's position on remote work for contractors?
- Your note: correctly says the documents do not cover it
- Answer: I cannot find this information in the provided documents. The context discusses remote work policies primarily for employees, including eligibility based on probationary periods, cross-border restrictions, and allowances for regular remote workers. …
- Judge, Answer Relevancy = 0.5714285714285714: The score is 0.57 because the response appears to address remote work generally, but it includes unrelated discussion about probationary periods, cross-border restrictions, and allowances for regular remote workers that do not answer the specific question about contractors. It is not higher because these off-topic details dilute the relevance, but…
- Judge, Contextual Relevancy = 0.35: The score is 0.35 because much of the context is off-target: it talks about "Employees" and "employee survey" details, and even "password changes every 90 days for all systems," which do not answer the contractor question. However, a few lines are somewhat related, such as "Remote work policy updated to allow up to 4 days remote per week" and the …
- Judge, Contextual Recall = 0.5: The score is 0.50 because sentence 2 is supported by node(s) in retrieval retrieval context 2 and 5, which mention employees and updating the employee handbook, so the policy refers to employees only, but sentence 1 is not supported since none of node(s) in retrieval context 1–9 mention contractors or any lack of contractor remote work policies.

### q20: judge fail, you pass
- Question: What is the company's dress code?
- Your note: correctly says the documents do not cover it
- Answer: I cannot find this information in the provided documents.
- Judge, Faithfulness = 0.0: The score is 0.00 because the actual output claims it cannot find the requested information in the provided documents, but the retrieval context is only an employee handbook and does not support that claim at all.
- Judge, Contextual Relevancy = 0.0: The score is 0.00 because the retrieval context contains no dress code information at all; it only covers unrelated topics like "office locations and working hours," "code of conduct," and "4 days remote / 1 day in-office," none of which answer "What is the company's dress code?"
- Judge, Contextual Recall = 0.0: The score is 0.00 because sentence 1 says the documents do not contain information about a dress code, but node(s) in retrieval context (all nodes) never mention a dress code or support any claim that the documents lack one.

For each disagreement above, decide who was right and say why in the report. Rows where a correct refusal was marked unfaithful are a judge finding.
