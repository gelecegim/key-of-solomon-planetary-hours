import datetime
import sys
from astral import LocationInfo
from astral.sun import sun
from zoneinfo import ZoneInfo
import calendar
import json
import pylunar

from LatLongToDMSConverter import LatLongToDMSConverter

with open("defaults.json") as defaults_data_file:
    default_data = json.load(defaults_data_file)
    chaldean_week_dict = default_data["ChaldeanWeek"]
    chaldean_day_dict = default_data["ChaldeanDay"]
    angel_day_dict = default_data["AngelDay"]
    chaldean_night_dic = default_data["ChaldeanNight"]
    angel_night_dic = default_data["AngelNight"]
    magical_day_name_array = default_data["MagicalDayNames"]
    magical_night_name_array = default_data["MagicalNightNames"]


with open("config.json") as config_data_file:
    config_data = json.load(config_data_file)
    cityname = config_data["Location"]["City"]
    timezone = config_data["Location"]["Timezone"]
    region = config_data["Location"]["Region"]
    latitude = config_data["Location"]["latitude"]
    longitude = config_data["Location"]["longitude"]
    day = config_data["Date"]["Day"]
    month = config_data["Date"]["Month"]
    year = config_data["Date"]["Year"]

try:
    zone_info = ZoneInfo(timezone)
    city = LocationInfo(cityname, region=region, timezone = zone_info.tzname, latitude=latitude, longitude=longitude)
except KeyError:
    print("The location could not be identified.")   
    sys.exit()    


current_date = datetime.date(year, month, day) if year > 0 and month > 0 and day > 0 else datetime.date.today()

weekday_int = current_date.weekday()
weekday_str = str(weekday_int)

chaldean_day_array = chaldean_week_dict.get(weekday_str, ["Err", "Err", "Err", "Err", "Err"])
attribute_array = ["Archangel", "Angel", "Planet", "Metal", "Color"]

print("Day of the week:" + calendar.day_name[weekday_int])
for i in range(len(chaldean_day_array)):
    print(attribute_array[i] + ": " + chaldean_day_array[i])

dms_converter = LatLongToDMSConverter()
latitude_dms, longitude_dms = dms_converter.convert_to_dms(latitude, longitude)

mi = pylunar.MoonInfo(latitude=latitude_dms, longitude=longitude_dms)

print("Moon phase: " + mi.phase_name())

day_start = datetime.datetime.combine(current_date, datetime.time.min).replace(tzinfo=zone_info)

s = sun(city.observer, date=current_date, tzinfo=zone_info)

sunrise_time = s['sunrise']
sunset_time = s['sunset']

sunrise_delta = (sunrise_time - day_start)
sunset_delta = (sunset_time - day_start)

sunrise_total_seconds = sunrise_delta.total_seconds()
sunset_total_seconds = sunset_delta.total_seconds()
day_difference = sunset_total_seconds - sunrise_total_seconds

# Planetary hours calculation
length_of_hour = day_difference/12
hour_array = [sunrise_total_seconds + i * length_of_hour for i in range(13)]

error_array = ["Err", "Err", "Err", "Err", "Err", "Err", "Err"]

chaldean_day_hour_array = chaldean_day_dict.get(weekday_str, error_array)
chaldean_day_hour_array = chaldean_day_hour_array * 2
chaldean_day_hour_array = chaldean_day_hour_array[:12] + ["End"]

angel_day_hour_array = angel_day_dict.get(weekday_str, error_array)
angel_day_hour_array = angel_day_hour_array * 2
angel_day_hour_array = angel_day_hour_array[:12] + [""]

print("Planetary day hours:")
for hour, magical_name, chaldean_hour, angel_hour in zip(hour_array, magical_day_name_array, chaldean_day_hour_array, angel_day_hour_array):
    hh = int(hour // 3600)
    mm = int((hour % 3600) // 60)
    hhmm = f"{hh:02}:{mm:02}"
    print(f"{hhmm} {magical_name} {chaldean_hour} {angel_hour}")

current_seconds = (datetime.datetime.now(tz=zone_info) - day_start).total_seconds()
for i in range(len(hour_array) - 1):
    if current_seconds >= hour_array[i] and current_seconds < hour_array[i+1]:
        print("You are now in '" + magical_day_name_array[i] + "'")
        break

next_date = current_date + datetime.timedelta(days=1)

s = sun(city.observer, date=next_date, tzinfo=zone_info)

next_sunrise_time = s['sunrise']
next_sunrise_delta = (next_sunrise_time - day_start)

next_sunrise_seconds = next_sunrise_delta.total_seconds()
night_difference = next_sunrise_seconds - sunset_total_seconds

length_of_hour = night_difference/12
hour_array = [sunset_total_seconds + i * length_of_hour for i in range(13)]

chaldean_night_hour_array = chaldean_night_dic.get(weekday_str, error_array)
chaldean_night_hour_array = chaldean_night_hour_array * 2
chaldean_night_hour_array = chaldean_night_hour_array[:12] + ["End"]

angel_night_hour_array = angel_night_dic.get(weekday_str, error_array)
angel_night_hour_array = angel_night_hour_array * 2
angel_night_hour_array = angel_night_hour_array[:12] + [""]

print("Planetary night hours:")
for hour, magical_name, chaldean_hour, angel_hour in zip(hour_array, magical_night_name_array, chaldean_night_hour_array, angel_night_hour_array):
    hh, mm = divmod(hour % 86400, 3600)
    hhmm = f"{int(hh):02}:{int(mm) // 60:02}"
    print(f"{hhmm} {magical_name} {chaldean_hour} {angel_hour}")

for i in range(len(hour_array) - 1):
    if current_seconds >= hour_array[i] and current_seconds < hour_array[i+1]:
        print("You are now in '" + magical_day_name_array[i] + "'")
        break
