# bench/data_gen.py
"""
Synthetic data loader for the federated DB project.

Generates:
- PostgreSQL: customers, orders
- MongoDB: events

Defaults: 50k customers, 300k orders, 1M events
You can override via CLI flags:  --customers 80000 --orders 500000 --events 1500000
"""

import argparse
import datetime as dt
import os
import random
import time
from typing import List, Tuple

import psycopg2
import pymongo


PG = dict(host="localhost", port=5432, dbname="federated", user="admin", password="admin")
MONGO_URI = "mongodb://localhost:27017/"
MONGO_DB = "federated"

REGIONS = ["Northeast", "Midwest", "South", "West"]
SEGMENTS = ["SMB", "ENT", "Prosumer"]
EVENT_TYPES = ["page_view", "add_to_cart", "checkout", "wishlist"]
# Tilt the distribution so add_to_cart isn’t too rare
EVENT_WEIGHTS = [60, 20, 10, 10]

ORDER_DATE_START = dt.date(2023, 1, 1)
ORDER_DATE_END = dt.date(2025, 9, 1)


def ts():
    return time.strftime("%H:%M:%S")


def rand_date(a: dt.date, b: dt.date) -> dt.date:
    t0 = int(time.mktime(a.timetuple()))
    t1 = int(time.mktime(b.timetuple()))
    return dt.date.fromtimestamp(random.randint(t0, t1))


def ensure_pg_schema(cur):
    cur.execute(
        """
        CREATE TABLE IF NOT EXISTS customers(
            customer_id INT PRIMARY KEY,
            region TEXT,
            segment TEXT
        );
        """
    )
    cur.execute(
        """
        CREATE TABLE IF NOT EXISTS orders(
            order_id INT PRIMARY KEY,
            customer_id INT,
            order_date DATE,
            total_amount NUMERIC,
            status TEXT
        );
        """
    )
    # Helpful indexes
    cur.execute("CREATE INDEX IF NOT EXISTS idx_orders_date ON orders(order_date);")
    cur.execute("CREATE INDEX IF NOT EXISTS idx_orders_customer ON orders(customer_id);")


def insert_customers(cur, n_customers: int, batch: int = 10_000):
    print(f"[{ts()}] Inserting {n_customers:,} customers …")
    rows: List[Tuple[int, str, str]] = []
    for cid in range(1, n_customers + 1):
        rows.append((cid, random.choice(REGIONS), random.choice(SEGMENTS)))
        if len(rows) >= batch:
            cur.executemany(
                "INSERT INTO customers(customer_id, region, segment) VALUES (%s,%s,%s) ON CONFLICT DO NOTHING;",
                rows,
            )
            rows.clear()
    if rows:
        cur.executemany(
            "INSERT INTO customers(customer_id, region, segment) VALUES (%s,%s,%s) ON CONFLICT DO NOTHING;",
            rows,
        )


def insert_orders(cur, n_orders: int, n_customers: int, batch: int = 20_000):
    print(f"[{ts()}] Inserting {n_orders:,} orders …")
    rows: List[Tuple[int, int, dt.date, float, str]] = []
    for oid in range(1, n_orders + 1):
        cid = random.randint(1, n_customers)
        od = rand_date(ORDER_DATE_START, ORDER_DATE_END)
        total = round(random.uniform(5, 500), 2)
        status = random.choice(["paid", "shipped", "cancelled"])
        rows.append((oid, cid, od, total, status))
        if len(rows) >= batch:
            cur.executemany(
                "INSERT INTO orders(order_id, customer_id, order_date, total_amount, status) "
                "VALUES (%s,%s,%s,%s,%s) ON CONFLICT DO NOTHING;",
                rows,
            )
            rows.clear()
    if rows:
        cur.executemany(
            "INSERT INTO orders(order_id, customer_id, order_date, total_amount, status) "
            "VALUES (%s,%s,%s,%s,%s) ON CONFLICT DO NOTHING;",
            rows,
        )


def ensure_mongo_indexes(mdb):
    mdb.events.create_index("customer_id")
    mdb.events.create_index("event_type")


def insert_events(mdb, n_events: int, n_customers: int, batch: int = 50_000):
    print(f"[{ts()}] Inserting {n_events:,} events (Mongo) …")
    docs = []
    for i in range(n_events):
        cid = random.randint(1, n_customers)
        et = random.choices(EVENT_TYPES, weights=EVENT_WEIGHTS, k=1)[0]
        docs.append({"customer_id": cid, "event_type": et, "ts": dt.datetime.utcnow()})
        if len(docs) >= batch:
            mdb.events.insert_many(docs, ordered=False)
            docs.clear()
    if docs:
        mdb.events.insert_many(docs, ordered=False)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--customers", type=int, default=50_000)
    parser.add_argument("--orders", type=int, default=300_000)
    parser.add_argument("--events", type=int, default=1_000_000)
    args = parser.parse_args()

    random.seed(42)

    print(f"[{ts()}] Connecting …")
    pg_conn = psycopg2.connect(**PG)
    pg_conn.autocommit = True
    cur = pg_conn.cursor()
    mongo = pymongo.MongoClient(MONGO_URI)
    mdb = mongo[MONGO_DB]

    ensure_pg_schema(cur)
    ensure_mongo_indexes(mdb)

    t0 = time.time()
    insert_customers(cur, args.customers)
    t1 = time.time()
    insert_orders(cur, args.orders, args.customers)
    t2 = time.time()
    insert_events(mdb, args.events, args.customers)
    t3 = time.time()

    cur.close()
    pg_conn.close()

    # Simple counts
    pg_conn2 = psycopg2.connect(**PG)
    c2 = pg_conn2.cursor()
    c2.execute("SELECT COUNT(*) FROM customers;")
    n_cust = c2.fetchone()[0]
    c2.execute("SELECT COUNT(*) FROM orders;")
    n_ord = c2.fetchone()[0]
    c2.close()
    pg_conn2.close()

    n_evt = mongo[MONGO_DB].events.count_documents({})

    print(f"[{ts()}] Done.")
    print(f"  customers: {n_cust:,}  (in {t1 - t0:0.1f}s)")
    print(f"  orders   : {n_ord:,}  (in {t2 - t1:0.1f}s)")
    print(f"  events   : {n_evt:,}  (in {t3 - t2:0.1f}s)")
    print("Indexes:")
    print("  Postgres: orders(order_date), orders(customer_id)")
    print("  Mongo   : events(customer_id), events(event_type)")


if __name__ == "__main__":
    main()
