from django.db import connection

def AddEvent_q(data):
    with connection.cursor() as cursor:
        cursor.execute("""
            INSERT INTO events (source_name, event_type, severity, description)
            VALUES (%s, %s, %s, %s)
        """, (data['source_name'], data['event_type'], data['severity'], data['description']))

    event_id = cursor.lastrowid
    return event_id
