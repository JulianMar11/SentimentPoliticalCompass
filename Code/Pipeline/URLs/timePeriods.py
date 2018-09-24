

import calendar  # documentation: https://docs.python.org/2/library/calendar.html
import datetime
from datetime import date, timedelta

# all date boundaries including # TODO not used?
observation_period_start = (2017, 1)
observation_period_end = (2018, 4)

# configurations for the observation periods
observation_period_start = date(2017, 1, 1)
observation_period_end = date(2018, 4, 30)


def monthly():
    """
    Generate monthly time range strings between start and end month

    :return: list of strings with time ranges spanning a month
    """

    time_periods = []

    year_month = []
    month = observation_period_start[1]
    for year in range(observation_period_start[0], observation_period_end[0] + 1):
        while month < 13:
            if year == observation_period_end[0] and month > observation_period_end[1]:
                break
            year_month.append((year, month))
            month += 1
        month = 1

    for year, month in year_month:
        _, num_days = calendar.monthrange(year, month)
        first_day = datetime.date(year, month, 1)
        last_day = datetime.date(year, month, num_days)

        first_day_str = first_day.strftime("%Y%m%d")
        last_day_str = last_day.strftime("%Y%m%d")
        time_periods.append(first_day_str + ":" + last_day_str)
    return time_periods






def in_days(range_in_days):
    """
    Generate time range strings between start and end date where each range is range_in_days days long

    :param range_in_days: number of days
    :return: list of strings with time ranges in the required format
    """


    delta = observation_period_end - observation_period_start  # timedelta
    period_starts = []
    for d in range(0, delta.days + 1, range_in_days):
        # print(observation_period_start + timedelta(days=d))
        period_starts.append(observation_period_start + timedelta(days=d))

    start_end = []
    for i, start in enumerate(period_starts[:-1]):
        start_end.append((start, period_starts[i+1] - timedelta(days=1)))


    time_periods = [start.strftime("%Y%m%d") + ":" + end.strftime("%Y%m%d") for start, end in start_end]
    return time_periods


def next_period(start_date, range_in_days):
    """
    Dynamically computing the next range and the start_date for next time.

    :param start_date: the date from which to start the range
    :param range_in_days: the range of the period in days
    :return:
    """
    end_date = start_date + timedelta(days=range_in_days - 1)  # 3 days including start and end date
    new_start_date = start_date + timedelta(days=range_in_days)
    # if the new start_date would be larger than the observation period end: new start date one day larger than obseration period end and end_date is observation period end
    if new_start_date > observation_period_end:
        end_date = observation_period_end
        new_start_date = observation_period_end + timedelta(days=1)

    time_period = start_date.strftime("%Y%m%d") + ":" + end_date.strftime("%Y%m%d")

    return time_period, new_start_date


if __name__ == "__main__":
    # print(monthly())
    # print(in_days(3))

    # format required
    # "date:r:20180520:20180526"

    time_period, new_start_date = next_period(date(2018, 4, 29), 5)
    print(time_period)
    print(new_start_date)