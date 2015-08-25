# -*- coding: UTF-8 -*-
import os.path

import configuration
from app_constants import DIR_CONF

MODULE_NAME = os.path.basename(os.path.dirname(__file__))
SETTINGS_FILENAME = '%s%s.ini' % (MODULE_NAME, os.path.isfile(
  configuration.get_path(DIR_CONF, '%s_custom.ini' % MODULE_NAME)) \
  and '_custom' or '')
SETTINGS_DB = configuration.get_config_string(
  SETTINGS_FILENAME, 'GENERAL', 'SETTINGS')
