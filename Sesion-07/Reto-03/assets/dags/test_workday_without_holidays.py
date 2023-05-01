from datetime import datetime, timedelta, time
from pytz import UTC
from typing import List
from pprint import pprint
from airflow.timetables.base import TimeRestriction
from workday_without_holidays import AfterWorkdayWithoutHolidaysTimetable
from calendario_mexicano import AfterWorkdayWithoutMexicanHolidaysTimetable
from workday import AfterWorkdayTimetable
import pendulum

import pandas as pd
from pandas.tseries.holiday import (
    Holiday,
    DateOffset,
    MO,
    TH,
    FR,
    SA,
    EasterMonday,
    GoodFriday,
    AbstractHolidayCalendar,
    HolidayCalendarFactory,
)


def siguiente_ejecucion(timetable, start_date,end_date=None,catchup=False):
    

    #timetable = AfterWorkdayWithoutHolidaysTimetable()
    #timetable = AfterWorkdayWithoutMexicanHolidaysTimetable()

    tr = TimeRestriction(start_date, end_date, catchup)

    last_automated_data_interval=None
    for i in range(100):    
        next_dag_run = timetable.next_dagrun_info(
            last_automated_data_interval=last_automated_data_interval,
            restriction=tr)
        last_automated_data_interval=next_dag_run.data_interval
        pprint(next_dag_run.run_after.to_day_datetime_string())

def calendario_mexicano():
    class MexicanHolidays(AbstractHolidayCalendar):
        rules = [
            Holiday("New Year's Day", month=1, day=1, offset=pd.offsets.DateOffset(weekday=MO(1))),
            Holiday("Epiphany", month=1, day=6),
            Holiday("Constitution Day", month=2, day=6),
            Holiday("Benito Juarez Day", month=3, day=21),
            Holiday("Labour Day", month=5, day=1, offset=pd.offsets.DateOffset(weekday=MO(1))),
            Holiday("Battle of Puebla Day", month=5, day=5),
            Holiday("Independence Day", month=9, day=16),
            Holiday("Revolution Day", month=11, day=20, offset=pd.offsets.DateOffset(weekday=MO(3))),
            Holiday("Lady of Guadalupe Day", month=12, day=12),
            Holiday("Christmas Day", month=12, day=25),
        ]

    cal = MexicanHolidays()
    holidays = cal.holidays(pd.Timestamp("2022-01-01"), pd.Timestamp("2023-12-31"))
    print(holidays)

if __name__ == '__main__':
    start_date = pendulum.datetime(2023, 1, 1, tz="UTC")    
    siguiente_ejecucion(
        #AfterWorkdayWithoutMexicanHolidaysTimetable,
        AfterWorkdayWithoutHolidaysTimetable(),
        start_date,
        end_date=None,
        catchup=False
    )
#    calendario_mexicano()
