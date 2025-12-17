# adhoc_probe.py
import sys
import sqlglot as sg
from exec.operators import execute, execute_logical, execute_legacy
from optimizer.planner.planner import plan as legacy_plan
from optimizer.planner.logical import plan_pageview_counts_per_customer

def run(offset: int = 0, limit: int = 15, event_type: str = "page_view"):
    ast = sg.parse_one(
        "SELECT c.customer_id, COUNT(e.event_id) AS n "
        "FROM customers c JOIN events e ON c.customer_id = e.customer_id "
        f"WHERE e.event_type = '{event_type}' "
        "GROUP BY c.customer_id "
        "ORDER BY n DESC, c.customer_id ASC "
        f"OFFSET {offset} "
        f"LIMIT {limit}"
    )
    legacy_out = execute_legacy(ast)
    lp = plan_pageview_counts_per_customer([("n","DESC"), ("customer_id","ASC")], offset, limit)
    logical_out = execute_logical(lp)
    print("LEGACY:", legacy_out)
    print("LOGICAL:", logical_out)
    print("EQUAL?:", legacy_out == logical_out)

if __name__ == "__main__":
    try:
        off = int(sys.argv[1]) if len(sys.argv) > 1 else 0
        lim = int(sys.argv[2]) if len(sys.argv) > 2 else 15
    except ValueError:
        print("Args must be integers: python adhoc_probe.py <OFFSET:int> <LIMIT:int>")
        raise SystemExit(1)
    run(off, lim)
