# baseline_join.py
import os, datetime
import psycopg2
import pymongo
from collections import Counter

PG = dict(host="localhost", port=5432, dbname="federated", user="admin", password="admin")
MONGO_URI = "mongodb://localhost:27017/"

# 1) Pushdown to Mongo: filter add_to_cart -> get distinct customer_ids (compact)
mongo = pymongo.MongoClient(MONGO_URI)
mdb = mongo["federated"]
cust_from_events = mdb.events.distinct("customer_id", {"event_type": "add_to_cart"})
cust_from_events = set(map(int, cust_from_events))

# 2) Pushdown to Postgres: orders after 2024-01-01 -> distinct customer_ids
pg = psycopg2.connect(**PG); cur = pg.cursor()
cur.execute("""
    SELECT DISTINCT customer_id
    FROM orders
    WHERE order_date >= DATE '2024-01-01'
""")
cust_from_orders = set(r[0] for r in cur.fetchall())

# 3) Intersection at coordinator
active_buyers = cust_from_events & cust_from_orders

# 4) Get regions for those customers (Postgres)
if active_buyers:
    cur.execute("""
        SELECT region
        FROM customers
        WHERE customer_id = ANY(%s)
    """, (list(active_buyers),))
    regions = [r[0] for r in cur.fetchall()]
else:
    regions = []

cur.close(); pg.close()

# 5) Final GROUP BY region
counts = Counter(regions)
print("active_buyers_by_region:", dict(counts))
