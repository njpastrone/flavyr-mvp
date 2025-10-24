# 🍽️ Flavyr Code Challenge – Restaurant Sales Analyzer (Founders' Original Prompt)

This document contains the **original coding challenge** provided by the Founders of **Flavyr**, which serves as the baseline for building our MVP.  
It outlines the core analytical capabilities that the system must perform — these requirements will guide the structure and features of the MVP Restaurant Sales Analyzer.

---

## 📄 Challenge Overview

**Due Date:** November 2  
**Goal:** Build a **mini version of what Flavyr does** — a *Restaurant Sales Analyzer* written in **Python**.

---

## 📥 Input Format

A single CSV file containing daily POS data with the following columns:

| Column | Description |
|---------|-------------|
| `date` | Date of each transaction |
| `total` | Total sale amount for the transaction |
| `customer_id` | Unique identifier for each customer |
| `item_name` | Item purchased |
| `day_of_week` | Day of the week for each transaction |

---

## 🧮 What the Program Should Do

1. **Find the slowest day of the week**  
   - Determine the day with the fewest transactions.  
   - Determine the day with the lowest total revenue.

2. **Calculate customer loyalty rate**  
   - Compute the percentage of *repeat customers* (customers who made more than one purchase).

3. **Show average order value (AOV)**  
   - Calculate the overall average order value.  
   - Calculate the average order value by day of week.

4. **Identify best and worst selling items**  
   - List the **top 3** selling items (by revenue and quantity sold).  
   - List the **bottom 3** selling items.

5. **Print a clean, readable report**  
   - Include key metrics and **actionable recommendations** (e.g., “Consider running a midweek promotion on Wednesdays to increase traffic”).

---

## ⚙️ Requirements

- **Clean, readable code**
- **Graceful error handling** (e.g., missing file, invalid data, empty fields)
- **Include a README** explaining how to run the program
- **Bonus features:**
  - Use **pandas**
  - Add **visualizations** (e.g., bar charts, pie charts)
  - Make the code **modular and reusable**

---

## 🔍 Evaluation Criteria

The reviewers will assess your project on the following:

| Category | What They’re Looking For |
|-----------|--------------------------|
| **Code Quality** | Is the code clean, well-organized, and documented? |
| **Problem-Solving** | Did you think through edge cases and handle them gracefully? |
| **Practical Thinking** | Are the insights and recommendations useful to restaurant operators? |

---

## 📦 Deliverables

- Python script (or modular codebase) implementing all functionality  
- README with setup and execution instructions  
- Output examples or generated report (optional visualization)

---

### 🧠 Notes for MVP Planning

This challenge represents the **core analytical foundation** of the full Flavyr product.  
Future iterations will:
- Integrate automated data ingestion (POS, CRM, etc.)
- Compare results to industry benchmarks  
- Map identified issues to recommended deals from the Deal Bank  

---