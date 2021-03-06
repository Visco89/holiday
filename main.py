from datetime import datetime, date, timedelta

MAX_DAY_WORK_OFF = 4

dates = [
    "01/01",
    "06/01",
    "25/04",
    "01/05",
    "02/06",
    "15/08",
    "16/08",
    "01/11",
    "07/12",
    "08/12",
    "25/12",
    "26/12",
]


def easter_monday(y):
    a = year % 19
    b = year // 100
    c = year % 100
    d = (19 * a + b - b // 4 - ((b - (b + 8) // 25 + 1) // 3) + 15) % 30
    e = (32 + 2 * (b % 4) + 2 * (c // 4) - d - (c % 4)) % 7
    f = d + e - 7 * ((a + 11 * d + 22 * e) // 451) + 114
    month = f // 31
    day = f % 31 + 1
    return date(year, month, day + 1)


def party_time(d):
    if d.weekday() in set([5, 6]):
        return True
    if d in holidays:
        return True
    return False


def remove_work_day(dates):
    c = 0
    while dates and not party_time(dates[-1]):
        dates.pop(-1)
        c += 1
    return dates, c


def remove_contained(long_weekend):
    for i in long_weekend:
        for j in long_weekend:
            if set(i['list']) < set(j['list']):
                long_weekend.remove(i)
    return long_weekend

#####################################################################

global holidays
year = int(input("Year: "))
max_day = int(input("How many day you can take (Max: {0})? ".format(MAX_DAY_WORK_OFF)))
if max_day < 0 or max_day > MAX_DAY_WORK_OFF:
    exit(-1)


holidays = [datetime.strptime(date, "%d/%m").date().replace(year=year) for date in dates]
holidays.append(easter_monday(year))

delta = timedelta(days=1)
long_weekend = []

for i in holidays:
    d = i
    work_day = 0
    cached = []
    while work_day <= max_day:
        if not party_time(d):
            work_day += 1
        cached.append(d)
        d += delta
    cached, popped = remove_work_day(cached)
    struct = dict()
    struct['day_taken'] = work_day - popped
    struct['list'] = cached
    long_weekend.append(struct)

long_weekend = remove_contained(long_weekend)

for i in long_weekend:
    d = i['list'][0] - delta
    cached = []
    work_day = 0
    while work_day <= max_day - i['day_taken']:
        if not party_time(d):
            work_day += 1
        cached.append(d)
        d -= delta
    cached, popped = remove_work_day(cached)
    if len(i['list'] + cached) < 3:
        long_weekend.remove(i)
    else:
        i['list'].extend(cached)
        i['list'].sort()
        i['day_taken'] += work_day - popped

print(long_weekend)
