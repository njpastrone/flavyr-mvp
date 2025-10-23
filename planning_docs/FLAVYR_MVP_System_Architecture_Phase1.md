# FLAVYR MVP System Architecture (Phase 1)

## 🧠 Overview
The FLAVYR MVP aims to help restaurants identify performance issues and recommend data-driven deals based on POS data and industry benchmarks.  
It focuses on diagnostic insights, deal recommendations, and performance tracking.

---

## 1. Data Inputs

| Source | Description | Example |
|--------|--------------|----------|
| **Restaurant POS Data** | Collected directly from restaurant POS exports (CSV, JSON, or API integration in later phases). | Sales, transactions, revenue by item, time, day. |
| **Industry Benchmark Data** | Preloaded dataset with average metrics by cuisine type, region, or restaurant model. | Avg revenue per seat, avg check size, labor %, etc. |

---

## 2. Data Layer

| Component | Description |
|------------|-------------|
| **Backend Database** | Centralized data repository combining POS data and benchmark metrics. Enables comparison, modeling, and reporting. |

---

## 3. Modeling Layer

| Component | Function |
|------------|-----------|
| **Simple Modeling (Identify Issues)** | Detects underperformance areas by comparing restaurant metrics against benchmarks. |
| **Deal Bank** | Structured list of deal templates (e.g., “Happy Hour,” “2-for-1 Appetizers,” “Off-Peak Lunch Discount”) that can be mapped to identified issues. |

---

## 4. Recommendation Engine

| Component | Description |
|------------|-------------|
| **Deal Recommendation Engine** | Matches identified issues to deal templates from the Deal Bank and ranks suggestions based on relevance. |

---

## 5. Outputs / Interfaces

| Output | Description |
|---------|-------------|
| **Deal Recommendations Report** | Auto-generated summary of identified issues and suggested promotions. |
| **Analytics Dashboard** | Visual interface for tracking performance, comparing KPIs, and evaluating deal effectiveness. |

---

## System Flow

1. Import POS data (initially manual upload or simple API call).  
2. Combine POS data with benchmark data in the backend database.  
3. Run simple modeling to identify problem areas.  
4. Match problems with relevant deal types from the deal bank.  
5. Output findings to:
   - Deal Recommendation Report (for management use)
   - Analytics Dashboard (for ongoing tracking)

---

## Mermaid System Diagram

```mermaid
flowchart TD

A[Restaurant POS Data<br/>(CSV or API Integration)] --> B[Backend Database]
B <-- C[Industry Benchmark Data]
B --> D[Simple Modeling<br/>(Identify Issues)]

D --> E[Deal Recommendations Report]
D --> F[Analytics Dashboard]

E <-- G[Deal Bank<br/>(Predefined Deals)]
```
