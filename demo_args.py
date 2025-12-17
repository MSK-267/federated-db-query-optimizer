# demo_args.py
# Run the federated query with CLI knobs: --offset, --limit, --event, --order.
# Prints rows and which path was used (fast/generic).

import argparse
import sqlglot as sg
from optimizer.planner.planner import plan_logical_from_ast
from exec.operators.execute import execute_logical_with_meta

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--offset", type=int, default=1000)
    ap.add_argument("--limit", type=int, default=10)
    ap.add_argument("--event", type=str, default="page_view")
    # order spec stays canonical for demo; allow override if needed
    ap.add_argument("--order", type=str, default="n DESC, c.customer_id ASC")
    args = ap.parse_args()

    SQL = f"""
    SELECT c.customer_id, COUNT(e.event_id) AS n
    FROM customers c
    JOIN events e ON c.customer_id = e.customer_id
    WHERE e.event_type = '{args.event}'
    GROUP BY c.customer_id
    ORDER BY {args.order}
    OFFSET {args.offset}
    LIMIT {args.limit}
    """

    ast = sg.parse_one(SQL)
    lp = plan_logical_from_ast(ast)
    rows, meta = execute_logical_with_meta(lp)

    print("SQL:", SQL.strip().replace("\n", " "))
    print("ROWS:", rows)
    print("META:", meta)

if __name__ == "__main__":
    main()
