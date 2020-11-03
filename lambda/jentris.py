import calendar
import datetime


class Jentris:
    """Main class to deliver the Jentris functionality"""
    def __init__(self):
        # On initialisation, get the days and date.
        self.jentris_date = next_jentris_date()
        self.jentris_sleeps = self.sleeps_until_jentris()
        self.jentris_date_text = self.jentris_date_as_text()
        self.is_j_today = datetime.datetime.now().date() == self.jentris_date.date()
        self.error = False

    def sleeps_until_jentris(self):
        """Gets the number of days between the 'Day of J' and 'today'"""
        current_date = datetime.datetime.now()
        delta = self.jentris_date - current_date
        return delta.days

    def jentris_date_as_text(self):
        """Returns a "speech friendly" version of the J Day Date"""
        date_format = '%A, %B the {S}, %Y'
        return self.jentris_date.strftime(date_format).replace('{S}', str(self.jentris_date.day) +
                                                               date_suffix(self.jentris_date.day))


def date_suffix(day):
    """Returns a suffix for the day part of a date (1st, 3rd, 4th etc.)"""
    return 'th' if 11 <= day <= 13 else {1: 'st', 2: 'nd', 3: 'rd'}.get(day % 10, 'th')


def next_jentris_date():
    """Get the first Friday in November, as the 'Day of J'"""
    cal = calendar.Calendar(firstweekday=calendar.SUNDAY)
    current_date = datetime.datetime.now()
    current_year = current_date.year

    # November
    month = 11

    # Determine first Friday
    month_cal = cal.monthdatescalendar(current_year, month)
    j_day = [day for week in month_cal for day in week if
             day.weekday() == calendar.FRIDAY and
             day.month == month][0]

    # Convert to datetime, so that we can apply formatting
    j_day_dt = datetime.datetime.combine(j_day, datetime.datetime.min.time())
    return j_day_dt
