import os.path

PATH_ROOT = os.path.abspath(os.path.dirname(__file__))
DIR_CONF = 'conf'
DIR_SQL = 'sql'
DIR_VIEWS = 'views'
DIR_STATIC = 'static'
DIR_VAR = 'var'
DIR_MODULES = '../Bottle Modules'
DIR_BEAKER_CACHE = os.path.join(DIR_VAR, 'beaker_cache')
DIR_BEAKER_LOCKS = os.path.join(DIR_VAR, 'beaker_locks')
DIR_LOGS = os.path.join(DIR_VAR, 'logs')

FILE_CONFIGURATION = os.path.isfile(os.path.join(DIR_CONF, 'custom.ini')) \
  and 'custom.ini' or 'general.ini'

SECTION_SETTINGS = 'APPLICATION'
SESSION_TIMEOUT = 2 * 60 * 60
