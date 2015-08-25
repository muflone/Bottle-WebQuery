from copy import copy
from optparse import Option, OptionValueError

def check_value(option, opt, value):
  if value.lower() not in ('yes', 'no', 'true', 'false', '1', '0'):
    raise OptionValueError(
        'option %s: invalid flag value: %r' % (opt, value))
  else:
    return value.lower() in ('yes', 'true', '1')

class OptParseTypeFlag (Option):
  TYPES = Option.TYPES + ('flag',)
  TYPE_CHECKER = copy(Option.TYPE_CHECKER)
  TYPE_CHECKER['flag'] = check_value
