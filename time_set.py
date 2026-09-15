import subprocess
import sys
from datetime import datetime, timezone, timedelta
from email.utils import parsedate_to_datetime
import requests

LOCAL_UTC_OFFSET_HOURS = 2

TIME_SOURCES = [
    "https://www.google.com",
    "https://www.cloudflare.com",
    "https://www.microsoft.com",
]

REQUEST_TIMEOUT = 5

def get_utc_time_from_server():
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 5.1; rv:52.0) Gecko/20100101 Firefox/52.0"
    }

    for url in TIME_SOURCES:
        try:
            response = requests.head(
                url, headers=headers, timeout=REQUEST_TIMEOUT, allow_redirects=True
            )
            date_str = response.headers.get("Date")
            if not date_str:
                continue

            server_time = parsedate_to_datetime(date_str)
            return server_time

        except requests.RequestException as e:
            continue
    return None

def convert_to_local(utc_dt, offset_hours):
    local_tz = timezone(timedelta(hours=offset_hours))
    return utc_dt.astimezone(local_tz)

def set_system_time_windows(dt):
    date_str = dt.strftime("%Y-%m-%d")
    time_str = dt.strftime("%H:%M:%S")

    subprocess.check_call("date %s" % date_str, shell=True)
    subprocess.check_call("time %s" % time_str, shell=True)

def main():
    utc_now = get_utc_time_from_server()

    if utc_now is None:
        sys.exit(1)

    local_now = convert_to_local(utc_now, LOCAL_UTC_OFFSET_HOURS)

    naive_local = local_now.replace(tzinfo=None)
    try:
        set_system_time_windows(naive_local)
    except subprocess.CalledProcessError as e:
        sys.exit(1)

if __name__ == "__main__":
    main()