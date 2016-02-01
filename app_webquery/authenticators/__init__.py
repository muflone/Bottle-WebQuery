import logging

from .dummy import AuthenticatorDummy
from .disabled import AuthenticatorDisabled
from .plain import AuthenticatorPlain
from .hash_md5 import AuthenticatorMD5
from .hash_sha1 import AuthenticatorSHA1
from .hash_sha256 import AuthenticatorSHA256
from .hash_sha512 import AuthenticatorSHA512

ALGORITHMS_CLASSES = {
  AuthenticatorDummy.ALGORITHM: AuthenticatorDummy,
  AuthenticatorDisabled.ALGORITHM: AuthenticatorDisabled,
  AuthenticatorPlain.ALGORITHM: AuthenticatorPlain,
  AuthenticatorMD5.ALGORITHM: AuthenticatorMD5,
  AuthenticatorSHA1.ALGORITHM: AuthenticatorSHA1,
  AuthenticatorSHA256.ALGORITHM: AuthenticatorSHA256,
  AuthenticatorSHA512.ALGORITHM: AuthenticatorSHA512,
}
KEY_USERNAME = 'username'
KEY_FULLNAME = 'fullname'
KEY_ROLES = 'roles'

def check_login(db_settings, username, password):
  result = db_settings.get_data(
    'SELECT description, algorithm, roles '
    'FROM users '
    'WHERE name=?',
    None,
    (username, ))[1]
  if result:
    description, algorithm, roles = result[0]
    if algorithm in ALGORITHMS_CLASSES:
      authenticator = ALGORITHMS_CLASSES[algorithm](db_settings)
      if authenticator.check_login(username, password):
        return {
          KEY_USERNAME: username,
          KEY_FULLNAME: description,
          KEY_ROLES: roles.split(',')
        }
    else:
      logging.error('unexpected algorithm "%s"' % algorithm)
  return None
