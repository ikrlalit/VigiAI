from django.db import connection

def execute(sql, params=None, fetchone=False, fetchall=False):
    with connection.cursor() as cursor:
        cursor.execute(sql, params or [])
        if fetchone:
            return cursor.fetchone()
        if fetchall:
            return cursor.fetchall()
