# adhoc_orderby_preview.py
import sqlglot as sg
from exec.operators import execute
from optimizer.planner.planner import plan

q = sg.parse_one(
    "SELECT c.customer_id, COUNT(e.event_id) AS n "
    "FROM customers c JOIN events e ON c.customer_id = e.customer_id "
    "WHERE e.event_type = 'page_view' "
    "GROUP BY c.customer_id "
    "ORDER BY n DESC, c.customer_id ASC "
    "LIMIT 15"
)
res = execute(plan(q))
print(res)
