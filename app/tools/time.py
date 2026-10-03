from datetime import datetime
from zoneinfo import ZoneInfo


def get_current_time():
    now = datetime.now(ZoneInfo("Asia/Tokyo"))
    return now.strftime("%Y-%m-%d %H:%M:%S")