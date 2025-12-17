# demo.py
# Minimal demo runner: parses SQL -> logical plan (Planner Bridge) -> executes and prints rows + meta.

import sqlglot as sg
from optimizer.planner.planner import plan_logical_from_ast
from exec.operators.execute import execute_logical_with_meta

SQL1 = """
SELECT c.customer_id, COUNT(e.event_id) AS n
FROM customers c
JOIN events e ON c.customer_id = e.customer_id
WHERE e.event_type = 'page_view'
GROUP BY c.customer_id
ORDER BY n DESC, c.customer_id ASC
OFFSET 1000
LIMIT 10
"""

SQL = """
SELECT c.customer_id, COUNT(e.event_id) AS n
FROM customers c
JOIN events e ON c.customer_id = e.customer_id
WHERE e.event_type = 'purchase'
GROUP BY c.customer_id
ORDER BY n DESC, c.customer_id ASC
OFFSET 0
LIMIT 10
"""


def main():
    ast = sg.parse_one(SQL)
    lp = plan_logical_from_ast(ast)   # <-- Planner Bridge
    rows, meta = execute_logical_with_meta(lp)
    print("ROWS:", rows)
    print("META:", meta)

if __name__ == "__main__":
    main()
