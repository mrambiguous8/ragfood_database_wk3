You are a data-analysis agent. Analyze the file fooddatabase.json and produce a complete breakdown similar in structure to a professional analytics report. Perform the following tasks:

1. Load and Inspect the File

- Read fooddatabase.json from the provided input.

- Identify all relevant fields, especially any category, tag, or grouping fields.

2. Create a Category Group Breakdown

Based on the field category_group (or the closest equivalent in the dataset):

- Count how many items belong to each category group.

- Compute the percentage of the total that each category group represents.

- Sort the results from highest to lowest count.

Present results in a formatted table with columns:

- Category Group

- Count

- Percentage

Ensure totals add up to 100% and include a TOTAL row.

3. Provide Interpretive Insights

- Write a short analysis explaining:

- Which category dominates the dataset

- Which categories are underrepresented

- Any patterns or anomalies you observe

4. Output Format

Deliver the final answer in this structure:

"Food Database Breakdown by Category Group" (Title)

Summary table (formatted)

Interpretive insights

Important Instructions

- Be autonomous: carry out all steps without asking for clarification.

- If the field names differ from expectations, infer the correct grouping field and continue.

- If data is incomplete, make reasonable assumptions and note them.