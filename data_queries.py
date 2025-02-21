import datetime
from database import get_connection

# Returns two lists: days and hours.
# days is a list of date strings ('YYYY-MM-DD') beginning from last Sunday.
# hours is the corresponding list of total hours spent on each day.
def get_weekly_data():
    last_sunday = get_last_sunday()

    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute('''
            SELECT substr(start_time, 1, 10) as date, SUM(duration)/3600.0 as hours
            FROM screen_time_log
            WHERE substr(start_time, 1, 10) >= ?
            GROUP BY date
            ORDER BY date;
        ''', (last_sunday.isoformat(),))
        data = dict(cursor.fetchall())

    days = []
    hours = []
    for i in range(7):
        date = (last_sunday + datetime.timedelta(days=i)).isoformat()
        days.append(date)
        hours.append(data.get(date, 0))

    return days, hours


# Returns two lists: hours and minutes.
# hours is a list of integers from 0 to 23.
# minutes is the corresponding list of total minutes spent on each hour.
def get_daily_data(selected_date):
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute('''
            SELECT substr(start_time, 12, 2) as hour, SUM(duration)/60.0 as minutes
            FROM screen_time_log
            WHERE substr(start_time, 1, 10) = ?
            GROUP BY hour
            ORDER BY hour;
        ''', (selected_date,))
        data = dict(cursor.fetchall())

    hours = []
    minutes = []
    for i in range(24):
        hours.append(i)
        minutes.append(data.get(f"{i:02d}", 0))

    return hours, minutes


# Returns a list of (app_name, total_minutes) tuples for the selected date.
def get_daily_app_usage(selected_date):
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute('''
            SELECT process_name, SUM(duration)/60.0 as minutes
            FROM screen_time_log
            WHERE substr(start_time, 1, 10) = ?
            GROUP BY process_name
            ORDER BY minutes DESC;
        ''', (selected_date,))
        data = cursor.fetchall()
    return data


# Returns a list of (app_name, total_minutes) tuples for the current week starting from Sunday.
def get_weekly_app_usage():
    last_sunday = get_last_sunday()

    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute('''
            SELECT process_name, SUM(duration)/60.0 as minutes
            FROM screen_time_log
            WHERE substr(start_time, 1, 10) >= ?
            GROUP BY process_name
            ORDER BY minutes DESC;
        ''', (last_sunday.isoformat(),))
        data = cursor.fetchall()
    return data


def get_last_sunday():
    today = datetime.date.today()
    if today.weekday() == 6:
        return today
    else:
        return today - datetime.timedelta(days=today.weekday() + 1)