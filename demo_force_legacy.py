"""
Run the page_view query using the legacy executor on purpose.
Use this when you want to show that the legacy path still works.
"""

import sqlglot as sg
from exec.operators.execute import execute_legacy

SQL = """
SELECT c.customer_id, COUNT(e.event_id) AS n
FROM customers c
JOIN events e ON c.customer_id = e.customer_id
WHERE e.event_type = 'page_view'
GROUP BY c.customer_id
ORDER BY n DESC, c.customer_id ASC
OFFSET 1000
LIMIT 10
"""

if __name__ == "__main__":
    ast = sg.parse_one(SQL)
    rows = execute_legacy(ast)
    print("ROWS:", rows)
