You are an autonomous evaluation agent. Perform the following tasks end-to-end and present the results in a clearly structured report.

1. Generate Comprehensive Test Queries

Create at least 15 diverse test queries that cover the following categories:

a. Semantic similarity queries
(e.g., “healthy Mediterranean options”)

b. Multi-criteria searches
(e.g., “spicy vegetarian Asian dishes”)

c. Nutritional queries
(e.g., “high-protein low-carb foods”)

d. Cultural exploration queries
(e.g., “traditional comfort foods”)

e. Cooking-method queries
(e.g., “dishes that can be grilled”)

For each query:

- State which category it belongs to.

- Explain what the system should understand about it.

2. Run Query Tests Against Both Systems

For each query you generated, run it against:

- System A: Original Architecture (Local Only)

- System B: Full Cloud (Upstash + Groq)

For each system and each query:

- Capture the response text

- Measure and record the response time (ms or seconds)

- Record any errors or anomalies

Present results in a comparison table.

3. Evaluate Answer Quality

For every query, evaluate the quality of each system’s response using these scoring criteria (0–5 scale):

- Accuracy: Does the answer correctly address the query?

- Relevance: Does the answer stay on topic?

- Completeness: Does it fully respond?

- Clarity: Is the response understandable and well-structured?

Provide both:

- Individual scores

- An overall average quality score for each system

4. Analyze Performance Differences

Provide a performance analysis including:

- Average response time per system

- Fastest and slowest queries

- Comparative performance summary

- Any patterns or bottlenecks observed

Include visual summaries if capable (tables, charts, etc.).

5. Provide a Final Recommendation

Based on your testing:

- Identify which system performs better overall

- Compare quality vs. speed trade-offs

- Recommend improvements for each system

- Highlight limitations of the test and propose next steps

Output Format

Produce the final report in this structure:

1. Test Query Set

2. System Responses + Timing Table

3. Quality Scoring Matrix

4. Performance Analysis

5. Key Findings

6. Recommendations

7. Appendix (raw logs if needed)

Important Instructions

- Execute the steps autonomously and sequentially.

- Do not skip any category or scoring task.

- Ensure all tables are well-formatted and labeled.

- If data is missing or ambiguous, make reasonable assumptions and note them.