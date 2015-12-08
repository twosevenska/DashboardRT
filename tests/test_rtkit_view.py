from rtkit.resource import RTResource
from rtkit.authenticators import CookieAuthenticator
from rtkit.errors import RTResourceError
from rtkit import set_logging
import logging

set_logging('debug')
logger = logging.getLogger('rtkit')

host = 'domo-kun.noip.me/rt/'
usr = 'twoskie@uc.pt'
pwd = 'shutup'
resource = RTResource('http://'+host+'/REST/1.0/', usr, pwd, CookieAuthenticator)
response = ''

try:
    response = resource.get(path='ticket/50')
    for r in response.parsed:
        for t in r:
            logger.info(t)
except RTResourceError as e:
    logger.error(e.response.status_int)
    logger.error(e.response.status)
    logger.error(e.response.parsed)

ticket_details = dict(response.parsed[0])
print 'Printing a dictionary with all the info'
print ticket_details

assert ticket_details['Requestors'] == 'twoskie@uc.pt'
