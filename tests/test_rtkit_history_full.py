from rtkit.resource import RTResource
from rtkit.authenticators import CookieAuthenticator

from rtkit.errors import RTResourceError
from rtkit import set_logging
import logging

set_logging('debug')
logger = logging.getLogger('rtkit')
response = ''

host = 'domo-kun.noip.me/rt/'
usr = 'twoskie@uc.pt'
pwd = 'shutup'
resource = RTResource('http://'+host+'/REST/1.0/', usr, pwd, CookieAuthenticator)

try:
    response = resource.get(path='ticket/50/history?format=l')
    logger.info(response.parsed)
except RTResourceError as e:
    logger.error(e.response.status_int)
    logger.error(e.response.status)
    logger.error(e.response.parsed)

# 404 Ticket does not exist
# 400 Wrong action/Invalid request
# 200 Success

assert response.status_int == 200

