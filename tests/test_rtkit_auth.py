from rtkit.resource import RTResource
from rtkit.authenticators import CookieAuthenticator
from rtkit.errors import RTResourceError
from rtkit import set_logging
import logging

set_logging('debug')
logger = logging.getLogger('rtkit')
statusCode = {}

host = 'domo-kun.noip.me/rt/'
usr = 'twoskie@uc.pt'
pwd = 'shutup'
resource = RTResource('http://'+host+'/REST/1.0/', usr, pwd, CookieAuthenticator)

print 'Real and valid login'

try:
    response = resource.get(path='ticket/1')
    statusCode['Real'] = response.status_int
    for r in response.parsed:
        for t in r:
            logger.info(t)
except RTResourceError as e:
    logger.error(e.response.status_int)
    logger.error(e.response.status)
    logger.error(e.response.parsed)

print 'Real and valid login but ticket does not exist'

try:
    response = resource.get(path='ticket/1324231423543253245235432')
    statusCode['Missing'] = response.status_int
    for r in response.parsed:
        for t in r:
            logger.info(t)
except RTResourceError as e:
    logger.error(e.response.status_int)
    logger.error(e.response.status)
    logger.error(e.response.parsed)

wrongUserResource = RTResource('http://'+host+'/REST/1.0/', 'INVALID', 'dsafdsf', CookieAuthenticator)

print 'Fake user login'

try:
    wrongUserResponse = wrongUserResource.get(path='ticket/1')
    statusCode['Fake User'] = wrongUserResponse.status_int
    for r in wrongUserResponse.parsed:
        for t in r:
            logger.info(t)
except RTResourceError as e:
    logger.error(e.response.status_int)
    logger.error(e.response.status)
    logger.error(e.response.parsed)

wrongPassResource = RTResource('http://'+host+'/REST/1.0/', usr, 'dsafdsf', CookieAuthenticator)

print 'Wrong Pass login'

try:
    wrongPassResponse = wrongPassResource.get(path='ticket/1')
    statusCode['Wrong Pass'] = wrongPassResponse.status_int
    for r in wrongPassResponse.parsed:
        for t in r:
            logger.info(t)
except RTResourceError as e:
    logger.error(e.response.status_int)
    logger.error(e.response.status)
    logger.error(e.response.parsed)

print 'Login status code for each situation:'
print statusCode

# 200 means everything is ok
# 401 means that login went wrong
# 404 means that the ticket does not exist

assert statusCode['Real'] == 200
assert statusCode['Missing'] == 404
assert statusCode['Fake User'] == 401
assert statusCode['Wrong Pass'] == 401
