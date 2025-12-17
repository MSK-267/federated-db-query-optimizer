from collections import Counter
from exec.connectors.postgres import PostgresConn
from exec.connectors.mongo import MongoConn

def active_buyers_by_region(order_date_cutoff="2024-01-01", event_type="add_to_cart"):
    pg = PostgresConn()
    mg = MongoConn()

    # Pushdowns to sources
    ids_from_orders = set(pg.distinct_customer_ids_after(order_date_cutoff))
    ids_from_events = mg.distinct_customer_ids_by_event(event_type)

    # Coordinator intersection
    active_ids = ids_from_orders & ids_from_events

    # Final group-by
    regions = pg.regions_for_customers(active_ids)
    return Counter(regions)

if __name__ == "__main__":
    res = active_buyers_by_region()
    print("Result:", dict(res))
