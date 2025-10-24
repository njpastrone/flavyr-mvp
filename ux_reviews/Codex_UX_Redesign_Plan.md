# Codex UX Redesign Plan

## 1. Project Objectives
- Deliver a Streamlit experience that guides restaurant operators from upload to action with minimal friction.
- Increase comprehension of benchmark gaps and confidence in the recommendations surfaced by FLAVYR.
- Present tactical transaction insights in a way that feels actionable and connected to the strategic dashboard.

## 2. Primary UX Pain Points
| Area | Current Issue | Evidence |
| --- | --- | --- |
| Navigation Flow | Horizontal tabs allow jumping ahead before data is processed, creating dead ends and context loss. | `app.py:758-801` |
| Upload Onboarding | Schema requirements surfaced only after upload; users lack sample data and inline validation cues. | `app.py:60-176` |
| KPI Interpretation | KPI cards flip colors for cost metrics, benchmark values are hidden, and trend context is missing. | `app.py:265-288`, `app.py:347-352` |
| Recommendations | Dense Markdown expanders overwhelm users, and there is no prioritization metadata. | `app.py:357-458` |
| Transaction Insights | Insights delivered as mixed Markdown with no sorting/filtering, decoupled from benchmark gaps. | `app.py:550-755` |

## 3. Redesign Initiatives
### 3.1 Guided Workflow Navigation
- Replace top tabs with a left-aligned progress stepper (Upload → Dashboard → Recommendations → Transaction Insights → Export).
- Disable downstream steps until prerequisite data is processed; display completion ticks and contextual tips per step.
- Add global status chip in the header that echoes last action (“POS data processed • Grade B”).

### 3.2 Frictionless Data Upload
- Introduce a “Download sample CSV” link adjacent to the uploader.
- Show a real-time schema checklist that turns green as each required column is detected; keep errors inline near the uploader.
- Embed a collapsible column glossary so operators can confirm definitions without leaving the page.
- After validation, auto-scroll to the preview and highlight anomalies (e.g., days missing values) before enabling “Process Data”.

### 3.3 Insight-Ready KPI Dashboard
- Fix delta color logic so red consistently signals underperformance while green signals strength across all KPIs.
- Surface benchmark values beside restaurant values (`value vs benchmark`) and add microtrend sparklines for last 3 months.
- Replace the bar chart with a segmented horizontal bar that includes thresholds (benchmark, goal, current) and explanatory captions.
- Add tooltips describing the business impact of being ±5% from benchmark to support quick decision-making.

### 3.4 Actionable Recommendation Playbooks
- Cluster recommendations into “Playbooks” grouped by business problem (e.g., “Drive Higher Average Ticket”).
- For each playbook, add impact tags (Effort, Expected Lift, Time to Value) and quick-action buttons (“Schedule Deal Review”, “Share with GM”).
- Default to expanded view for critical playbooks (gap >15%) with a concise summary sentence before deeper rationale.
- Provide a short “Why this matters” paragraph that ties the playbook back to specific KPI gaps.

### 3.5 Transaction Insights as Tactical Command Center
- Convert Markdown lists into interactive tables (sortable, filterable by daypart, cuisine, or campaign period).
- Visually integrate with strategic KPIs using banners like “Ties to: Average Ticket Gap (–18%)”.
- Add contextual recommendations per card (e.g., “Launch upsell on slowest day” with a CTA to the Playbooks section).
- Offer CSV download of insights and allow side-by-side comparison of two time ranges for A/B validation.

## 4. Implementation Roadmap
1. **Navigation Overhaul (Week 1)**  
   Build the stepper, gate tabs until prerequisites are met, and update the header status component.
2. **Upload Experience (Week 1-2)**  
   Add sample data links, checklist, and inline validation; QA with malformed CSVs.
3. **Dashboard Enhancements (Week 2-3)**  
   Refine metric cards, introduce benchmark display, and rebuild the gap visualization.
4. **Recommendations Redesign (Week 3-4)**  
   Create Playbook structure, impact tags, and CTA components; test comprehension with target users.
5. **Transaction Insights Revamp (Week 4-5)**  
   Develop interactive tables, filters, and cross-linking banners; ensure performance with large datasets.

## 5. Success Metrics
- Reduce upload-to-dashboard completion time by 30%.
- Increase user-reported clarity of KPI gaps (Likert score +1.0 in usability testing).
- Boost engagement with recommendations (≥50% of users interact with at least one playbook CTA).
- Achieve ≥75% positive feedback on transaction insights usefulness in pilot surveys.

## 6. Research & Validation Plan
- Conduct 3 moderated walkthroughs with restaurant operators to validate the guided workflow.
- Run A/B tests on KPI card variants to confirm comprehension gains.
- Shadow one pilot customer to capture qualitative reactions to Playbooks and tactical insights.
- Collect analytics on stepper progression and CTA usage to inform Phase 2 iterations.
