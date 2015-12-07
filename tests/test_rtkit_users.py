from rtkit.resource import RTResource
from rtkit.authenticators import CookieAuthenticator

from rtkit.errors import RTResourceError
from rtkit import set_logging
import logging


host = 'domo-kun.noip.me/rt/'
usr = 'twoskie@uc.pt'
pwd = 'shutup'
resource = RTResource('http://'+host+'/REST/1.0/', usr, pwd, CookieAuthenticator)
users = []

query = "Queue='general'"

response = resource.get(path='search/ticket?query='+query)

for ticket in response.parsed[0]:
    ticketNumber = ticket[0]
    ticketInfo = resource.get(path='ticket/'+ticketNumber)
    owner = [item for item in ticketInfo.parsed[0] if item[0] == 'Owner']
    user = owner[0][1]
    if user not in users and user != 'Nobody':
        users.append(user)

print users