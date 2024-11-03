from datetime import datetime
import pytz
from settings import HOUR_REGION

def convertir_timestamp(timestamp):
    dt_utc = datetime.fromisoformat(timestamp)

    timezone = pytz.timezone(HOUR_REGION)
    dt_with_timezone = dt_utc.astimezone(timezone)

    offset_seconds = dt_with_timezone.utcoffset().total_seconds()
    offset_hours = int(offset_seconds // 3600)
    utc_offset = f"UTC{'+' if offset_hours >= 0 else ''}{offset_hours}"
    print(utc_offset)

    return dt_with_timezone.strftime(f'**%H:%M:%S** %d/%m/%Y *{utc_offset}*')