from django.db import connection

def AddEvent_q(data):
    with connection.cursor() as cursor:
        cursor.execute("""
            INSERT INTO events (source_name, event_type, severity, description)
            VALUES (%s, %s, %s, %s)
        """, (data['source_name'], data['event_type'], data['severity'], data['description']))

        event_id = cursor.lastrowid

        if data["severity"] in ("High", "Critical"):
            cursor.execute("""
                INSERT INTO alerts (event_id, status)
                VALUES (%s, 'Open')
            """, (event_id,))
    return event_id

def AddNewUser_q(data):
    with connection.cursor() as cursor:
        cursor.execute("""
            INSERT INTO users (username, password_hash, role)
            VALUES (%s, %s, %s)
        """, (data['username'], data['password'], data['role']))

    event_id = cursor.lastrowid
    return event_id

def CheckUser_q(username):
    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT id, username, password_hash, role, created_at FROM users WHERE username = %s
        """, (username,))
        row = cursor.fetchone()

        if row:
            user = {
                'id': row[0],
                'username': row[1],
                'password_hash': row[2],
                'role': row[3],
                'created_at': row[4],
            }
            return type('User', (object,), user)  # Create a simple User object
        else:
            return None



def AlertsListByEventSeverityAndAlertStatus_q(event_severity, alert_status):
    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT a.id,a.status,a.created_at,a.event_id,e.source_name,
                       e.event_type,e.severity,e.description FROM alerts a left join events e on a.event_id=e.id
            WHERE e.severity = %s AND a.status = %s  ORDER BY a.id DESC""",(event_severity, alert_status,))
        rows = cursor.fetchall()

        columns = [col[0] for col in cursor.description]
        alerts = [dict(zip(columns, row)) for row in rows]
    return alerts

def AlertsListByEventSeverity_q(event_severity):
    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT a.id,a.status,a.created_at,a.event_id,e.source_name,
                       e.event_type,e.severity,e.description FROM alerts a left join events e on a.event_id=e.id
            WHERE e.severity = %s ORDER BY a.id DESC""",(event_severity,))
        rows = cursor.fetchall()

        columns = [col[0] for col in cursor.description]
        alerts = [dict(zip(columns, row)) for row in rows]
    return alerts

def AlertsListByAlertStatus_q(alert_status):
    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT a.id,a.status,a.created_at,a.event_id,e.source_name,
                       e.event_type,e.severity,e.description FROM alerts a left join events e on a.event_id=e.id
            WHERE a.status = %s ORDER BY a.id DESC""",(alert_status,))
        rows = cursor.fetchall()

        columns = [col[0] for col in cursor.description]
        alerts = [dict(zip(columns, row)) for row in rows]
    return alerts

def AlertsList_q():
    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT a.id,a.status,a.created_at,a.event_id,e.source_name,
                       e.event_type,e.severity,e.description FROM alerts a left join events e on a.event_id=e.id ORDER BY a.id DESC""")
        rows = cursor.fetchall()

        columns = [col[0] for col in cursor.description]
        alerts = [dict(zip(columns, row)) for row in rows]
    return alerts

def AlertStatusUpdate_q(alert_id, alert_status):
    try:
        with connection.cursor() as cursor:
            cursor.execute("""
                UPDATE alerts
                SET status = %s
                WHERE id = %s
            """, (alert_status, alert_id))
            affected_rows = cursor.rowcount
        return affected_rows
    except Exception as e:
        print(f"Error updating alert status: {e}")
        return 0