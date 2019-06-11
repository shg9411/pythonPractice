from datetime import datetime, timedelta
from calendar import HTMLCalendar
from .models import Work


class Calendar(HTMLCalendar):
    def __init__(self, year=None, month=None):
        self.year = year
        self.month = month
        super(Calendar, self).__init__()

    def formatday(self, day, works):
        work_per_day = works.filter(start__day=day)
        d = ''
        for work in work_per_day:
            d += f'{work.name}<li>{work.start}~ {work.end} </li>'

        if day != 0:
            return f"<td><span class='date'>{day}</span><ul> {d} </ul></td>"
        return '<td></td>'

    # formats a week as a tr
    def formatweek(self, theweek, works):
        week = ''
        for d, weekday in theweek:
            week += self.formatday(d, works)
        return f'<tr> {week} </tr>'

    # formats a month as a table
    # filter events by year and month
    def formatmonth(self, withyear=True,work=None):
        works = work
        cal = f'<table border="0" cellpadding="0" cellspacing="0" class="calendar">\n'
        cal += f'{self.formatmonthname(self.year, self.month, withyear=withyear)}\n'
        cal += f'{self.formatweekheader()}\n'
        for week in self.monthdays2calendar(self.year, self.month):
            cal += f'{self.formatweek(week, works)}\n'
        return cal
