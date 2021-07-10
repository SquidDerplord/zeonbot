import pytz
import datetime

def GetTimeZoneName(timezone, country_code):

    #see if it's already a valid time zone name
    if timezone in pytz.all_timezones:
        return timezone

    #if it's a number value, then use the Etc/GMT code
    try:
        offset = int(timezone)
        if offset > 0:
            offset = '+' + str(offset)
        else:
            offset = str(offset)
        return 'Etc/GMT' + offset
    except ValueError:
        pass

    #look up the abbreviation
    country_tzones = None
    try:
        country_tzones = pytz.country_timezones[country_code]
    except:
        pass

    set_zones = set()
    if country_tzones is not None and len(country_tzones) > 0:
        for name in country_tzones:
            tzone = pytz.timezone(name)
            for utcoffset, dstoffset, tzabbrev in getattr(tzone, '_transition_info', [[None, None, datetime.datetime.now(tzone).tzname()]]):
                if tzabbrev.upper() == timezone.upper():
                    set_zones.add(name)

        if len(set_zones) > 0:
            return min(set_zones, key=len)

        # none matched, at least pick one in the right country
        return min(country_tzones, key=len)


    #invalid country, just try to match the timezone abbreviation to any time zone
    for name in pytz.all_timezones:
        tzone = pytz.timezone(name)
        for utcoffset, dstoffset, tzabbrev in getattr(tzone, '_transition_info', [[None, None, datetime.datetime.now(tzone).tzname()]]):
            if tzabbrev.upper() == timezone.upper():
                set_zones.add(name)

    return min(set_zones, key=len)