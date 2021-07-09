import psycopg2 

class Connection(object):
    _db=None

    def __init__(self, host, db, user, pws):
        self._db = psycopg2.connect(host=host, database=db, user=user, password=pws)


if __name__ == '__main__':
    