import datetime
import calendar

DATE_FORMAT = '%d/%m/%Y'

def validate_date(sDate, dFallbackDate):
  """Return a valid formatted date from the input date or the fallback date"""
  try:
    valid_date = datetime.datetime.strptime(sDate, DATE_FORMAT).date()
  except (ValueError, TypeError), e:
    valid_date = dFallbackDate
  return valid_date
  return valid_date.strftime(DATE_FORMAT)

def first_day(year, month):
  """Return the first day of the month for the selected year"""
  return datetime.date(year, month, 1)

def last_day(year, month):
  """Return the last day of the month for the selected year"""
  return datetime.date(year, month, calendar.monthrange(year, month)[1])

def to_iseries(date):
  """Return a numeric date for the iseries"""
  return date.toordinal() - datetime.date(1899, 11, 29).toordinal()

def from_iseries(date):
  """Return a date from the iseries date"""
  return datetime.datetime.fromordinal(date + datetime.date(1899, 11, 29).toordinal())

def format(date, custom_format=DATE_FORMAT):
  """Return a formatted date"""
  return datetime.datetime.strftime(date, custom_format and custom_format or DATE_FORMAT)
