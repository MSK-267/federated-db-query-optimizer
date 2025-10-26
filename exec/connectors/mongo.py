import pymongo

class MongoConn:
    def __init__(self, uri="mongodb://localhost:27017/", db="federated"):
        self.client = pymongo.MongoClient(uri)
        self.db = self.client[db]

    def distinct_customer_ids_by_event(self, event_type):
        vals = self.db.events.distinct("customer_id", {"event_type": event_type})
        return set(int(v) for v in vals if v is not None)
