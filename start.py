import sys
from app_constants import PATH_ROOT, FILE_CONFIGURATION, SECTION_SETTINGS, DIR_MODULES, DIR_VAR, DIR_LOGS
import configuration
import os
import optparse
import datetime
import logging

from optparse_type_flag import OptParseTypeFlag

os.chdir(PATH_ROOT)
sys.path.insert(1, DIR_MODULES)

import bottle
import logging

if __name__ == '__main__':
  # Prepare logging
  if not os.path.isdir(DIR_VAR):
    os.mkdir(DIR_VAR)
  if not os.path.isdir(DIR_LOGS):
    os.mkdir(DIR_LOGS)
  logging.basicConfig(
    filename=os.path.join(DIR_LOGS, 
      datetime.datetime.today().strftime('%Y-%m-%d %H.%M.%S.log')),
    format='%(asctime)s '
      '%(levelname)-8s '
      '%(filename)-25s '
      'line: %(lineno)-5d '
      '%(funcName)-30s '
      'pid: %(process)-8d '
      '%(message)s',
    datefmt='%Y-%m-%d %H:%M:%S',
    level=logging.DEBUG)
  
  logging.debug('Loading application app_webquery')
  root_app = bottle.load_app('app_webquery.app:setup()')
  logging.debug('Loaded application app_webquery')

  logging.debug('Loading configuration')
  general_configuration = configuration.get_config_obj(FILE_CONFIGURATION)
  startup_options = {
    'host': general_configuration.get(SECTION_SETTINGS, 'LISTEN'),
    'port': general_configuration.getint(SECTION_SETTINGS, 'PORT_NUMBER'),
    'debug': general_configuration.getboolean(SECTION_SETTINGS, 'DEBUG'),
    'reloader': general_configuration.getboolean(SECTION_SETTINGS, 'RELOADER'),
    'server': general_configuration.get(SECTION_SETTINGS, 'SERVER_TYPE')
  }
  # Parse command line arguments to override configuration settings
  cmd_parser = optparse.OptionParser(option_class=OptParseTypeFlag)
  cmd_parser.add_option('-s', '--server',
    action='store', choices=bottle.server_names.keys(),
    default=startup_options['server'],
    help='use SERVER as backend.')
  cmd_parser.add_option('-a', '--address',
    action='store', type=str, dest='host',
    default=startup_options['host'],
    help='bind socket to ADDRESS.')
  cmd_parser.add_option('-p', '--port',
    action='store', type=int,
    default=startup_options['port'],
    help='bind socket to PORT number.')
  cmd_parser.add_option('-d', '--debug',
    action='store', type='flag',
    default=startup_options['debug'],
    help='start server in debug mode.')
  cmd_parser.add_option('-r', '--reloader',
    action='store', type='flag',
    default=startup_options['reloader'],
    help='auto-reload on file changes.')
  startup_options = vars(cmd_parser.parse_args()[0])
  logging.info('Startup options: %s' % startup_options)
  logging.debug('Starting main loop')
  while True:
    logging.info('Launching bottle application')
    bottle.run(app=root_app, **startup_options)
    logging.critical('Bottle application has exited unexpectedly')
