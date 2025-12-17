# demo_timing.py
# Time the same query on both engines: legacy vs logical (fast/generic)

import time
import sqlglot as sg
from optimizer.planner.planner import plan_logical_from_ast
from exec.operators.execute import execute_logical_with_meta, execute_legacy

SQL_TPL = """
SELECT c.customer_id, COUNT(e.event_id) AS n
FROM customers c
JOIN events e ON c.customer_id = e.customer_id
WHERE e.event_type = '{event}'
GROUP BY c.customer_id
ORDER BY n DESC, c.customer_id ASC
OFFSET {offset}
LIMIT {limit}
"""

def time_ms(fn, *args, **kwargs):
    t0 = time.perf_counter()
    out = fn(*args, **kwargs)
    t1 = time.perf_counter()
    return out, (t1 - t0) * 1000.0

def run(event="page_view", offset=0, limit=10):
    sql = SQL_TPL.format(event=event, offset=offset, limit=limit)
    ast = sg.parse_one(sql)

    # --- legacy timing ---
    (legacy_rows), legacy_ms = time_ms(execute_legacy, ast)

    # --- logical timing ---
    lp = plan_logical_from_ast(ast)
    (logical_rows, meta), logical_ms = time_ms(execute_logical_with_meta, lp)

    # --- sanity: same rows? ---
    equal = legacy_rows == logical_rows

    print(f"offset={offset:>5} limit={limit:>4} | legacy {legacy_ms:7.2f} ms | logical {logical_ms:7.2f} ms | equal={equal} | path={meta.get('path')}")
    # Optional: print first row for confidence
    if logical_rows:
        print("sample_row:", logical_rows[0])

if __name__ == "__main__":
    # Feel free to change or add calls here during the demo
    run(event="page_view", offset=0, limit=10)
    run(event="page_view", offset=1000, limit=10)
    run(event="page_view", offset=5000, limit=10)
