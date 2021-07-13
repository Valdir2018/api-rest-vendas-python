import psycopg2 


def Connection(pghost, port, dbname, usr, pws):
    conn = psycopg2.connect(host=pghost, port=port, database=dbname, user=usr, password=pws )
    return conn
   
