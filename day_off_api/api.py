import jdatetime
import requests
from hijri_converter import Gregorian

HOST = "https://farsicalendar.com/api/"
IS_THURSDAY_OFF = True


def is_off_api(date_type: str, month: int, day: int) -> bool:
    response = requests.get(f"{HOST}/{date_type}/{day}/{month}").json()
    if len(response["values"]):
        for value in response["values"]:
            if value["dayoff"]:
                return True
    return False


def is_day_off(month: int, day: int) -> bool:
    shamsi = jdatetime.datetime(
        year=jdatetime.datetime.now().year, month=month, day=day
    )
    if IS_THURSDAY_OFF and shamsi.weekday() == 5:
        return True
    if shamsi.weekday() == 6:
        return True
    # sh is for Shamsi
    if is_off_api("sh", month, day):
        return True
    gregorian = shamsi.togregorian()
    ghamari = Gregorian(gregorian.year, gregorian.month, gregorian.day).to_hijri()
    # ic is for Ghamari
    if is_off_api("ic", ghamari.month, ghamari.day):
        return True
    return False


def is_today_off() -> bool:
    today = jdatetime.datetime.now()
    return is_day_off(today.month, today.day)
