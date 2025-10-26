import psycopg2

class PostgresConn:
    def __init__(self, host="localhost", port=5432, dbname="federated", user="admin", password="admin"):
        self.kw = dict(host=host, port=port, dbname=dbname, user=user, password=password)

    def query(self, sql, params=None):
        con = psycopg2.connect(**self.kw)
        cur = con.cursor()
        cur.execute(sql, params or ())
        rows = cur.fetchall()
        cur.close(); con.close()
        return rows

    def distinct_customer_ids_after(self, date_str):
        sql = """SELECT DISTINCT customer_id FROM orders WHERE order_date >= %s"""
        return [r[0] for r in self.query(sql, (date_str,))]

    def regions_for_customers(self, ids):
        if not ids: return []
        sql = "SELECT region FROM customers WHERE customer_id = ANY(%s)"
        return [r[0] for r in self.query(sql, (list(ids),))]
