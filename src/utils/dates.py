from datetime import datetime, timedelta
import random

def random_past_date(days_back=180):
    """Return a random datetime within the last `days_back` days."""
    now = datetime.now()
    delta_days = random.randint(0, days_back)
    return now - timedelta(days=delta_days)

def random_workday_date(days_back=180):
    """Avoid weekends most of the time."""
    while True:
        dt = random_past_date(days_back)
        if dt.weekday() < 5:  # Mon–Fri
            return dt
