# upload_to_neon.py — execute FRUITFUL_REVIEW_DB.sql against the Neon project
# Usage: python3 upload_to_neon.py   (network must be available)
import psycopg2, sys

SQL_FILE = "FRUITFUL_REVIEW_DB.sql"

def connect():
    return psycopg2.connect(
        host="ep-floral-cloud-ax0sva9p-pooler.c-4.us-east-2.aws.neon.tech",
        port=5432,
        dbname="neondb",
        user="neondb_owner",
        password="npg_o40IQPjwXiTJ",  # ROTATE AFTER DEEP DIVE (per Heyns)
        sslmode="require",
        connect_timeout=30,
    )

def main():
    try:
        conn = connect()
    except Exception as e:
        print("CONNECT FAIL:", type(e).__name__, str(e)[:150])
        sys.exit(1)
    cur = conn.cursor()
    with open(SQL_FILE, encoding="utf-8") as f:
        sql = f.read()
    cur.execute(sql)
    conn.commit()
    # verify
    cur.execute("""
        SELECT 'portals', count(*) FROM fruitful.portals
        UNION ALL SELECT 'menu_lines', count(*) FROM fruitful.menu_lines
        UNION ALL SELECT 'menu_translations', count(*) FROM fruitful.menu_translations
        UNION ALL SELECT 'boq_items', count(*) FROM fruitful.boq_items
        UNION ALL SELECT 'malls', count(*) FROM fruitful.malls
        UNION ALL SELECT 'deployment_economics', count(*) FROM fruitful.deployment_economics
        UNION ALL SELECT 'container_fill', count(*) FROM fruitful.container_fill
        UNION ALL SELECT 'history_log', count(*) FROM fruitful.history_log
        UNION ALL SELECT 'financial_snapshot', count(*) FROM fruitful.financial_snapshot
        UNION ALL SELECT 'suppliers', count(*) FROM fruitful.suppliers;
    """)
    print("UPLOAD OK — row counts:")
    for name, cnt in cur.fetchall():
        print(f"  {name}: {cnt}")
    conn.close()

if __name__ == "__main__":
    main()
