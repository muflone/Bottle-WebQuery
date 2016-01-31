import time
import logging

from app_constants import SESSION_TIMEOUT_SINCE_CREATION

class ExpiringSession():
  """A session which expires after some seconds from the creation date"""
  def __init__(self, session):
    """Class initialization"""
    self.session = session
    # Check if the session was already expired
    now = time.time()
    if now - session.created > SESSION_TIMEOUT_SINCE_CREATION:
      # Session expired, it will be invalidated
      logging.warning('Session %s expired after %d seconds from creation' % (
        session.id, SESSION_TIMEOUT_SINCE_CREATION))
      # Delete the session
      session.delete()
      # Invalidate the expired session
      session.invalidate()

  def __getattr__(self, attr):
    """Return any member from the original Session instance"""
    return self.session.__getattr__(attr)
