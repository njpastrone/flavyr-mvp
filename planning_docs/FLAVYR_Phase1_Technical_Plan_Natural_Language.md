# FLAVYR — Phase 1 Technical Plan (MVP)

## Goal
Build a working MVP that helps restaurants compare their performance to industry benchmarks and get useful insights about where they’re underperforming. The MVP doesn’t need complex modeling yet — it just needs to process data, find gaps, and present them clearly through a dashboard and a report.

---

## 1. What Phase 1 Will Do

- Let a restaurant upload a simple CSV export of their POS data.  
- Combine that data with benchmark data we already have for similar restaurants (by cuisine and dining model).  
- Identify key performance gaps — e.g., low sales per seat, high labor cost, or slow table turnover.  
- Suggest relevant deals from the existing **Deal Bank** that could help fix those issues.  
- Present all of this through a clean dashboard and downloadable report.

---

## 2. Main Components

1. **Data Upload + Validation**
   - Restaurants upload a CSV file in a fixed format (we’ll provide a template).
   - The app checks that all required columns are there and the numbers make sense.
   - Once validated, the data is stored locally.

2. **Benchmarks**
   - We’ll load benchmark data from static CSVs or a small database — averages by cuisine and restaurant type.
   - These are used to compare each restaurant’s KPIs.

3. **KPI + Gap Analysis**
   - The app calculates basic metrics (e.g., average ticket size, labor %, sales per seat).
   - It compares these to benchmarks and shows where the restaurant is doing better or worse.
   - Each gap gets a score (e.g., “10% below average”).

4. **Recommendations**
   - Based on which metrics are weak, the app links to relevant deal types in the existing Deal Bank.
   - Example: if table turnover is low → suggest “Happy Hour or Off-Peak Discount.”

5. **Outputs**
   - **Dashboard:** a simple Streamlit interface showing KPIs, gaps, and recommended deals.
   - **Report:** downloadable summary (PDF or HTML) that a restaurant can share with their team.

---

## 3. How It Will Be Built

- **Frontend:** Streamlit (fast to prototype, easy for non-technical users).  
- **Backend:** Python scripts inside the app — no separate API layer needed yet.  
- **Database:** SQLite (local file) to store uploads, metrics, and results.  
- **Data Format:** CSV for both POS uploads and benchmark tables.  
- **Language:** Python 3.10+ with Pandas for data handling.

---

## 4. Development Steps

1. **Week 1–2 — Setup & Data Flow**
   - Build the upload page and validation logic.  
   - Load benchmark data and link it to each restaurant upload.  
   - Make sure we can compute the key KPIs.

2. **Week 3 — Gap Analysis**
   - Compare restaurant metrics to benchmarks.  
   - Display results clearly (green = above average, red = below).  

3. **Week 4 — Recommendations + Report**
   - Connect the Deal Bank to the gap results.  
   - Create a short written summary for each recommended deal.  
   - Add a button to download the PDF or HTML report.

4. **Week 5 — Testing & Pilot**
   - Test the tool with 2–3 sample restaurants.  
   - Adjust benchmark matching and recommendation rules based on feedback.

---

## 5. Outputs at the End of Phase 1

- A fully working Streamlit MVP where a restaurant can:
  - Upload data,
  - See how they compare to industry averages,
  - View and download their performance report,
  - And receive deal recommendations from the Deal Bank.  

This version establishes the foundation for later phases (e.g., clustering and causal impact modeling), but it keeps Phase 1 lightweight, fast to build, and ready for pilot testing.
