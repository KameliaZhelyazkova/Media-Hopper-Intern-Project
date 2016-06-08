from KalturaClient import *
from KalturaClient import Plugins
import json


# session credentials

file = open('test.json')
settings = json.load(file)

userID = settings['userID']
admin_secret = settings['adminSecret']
ks_type = settings['ks_type']
partnerID = settings['partnerID']

# config
config = KalturaConfiguration(partnerID)
config.serviceUrl = "http://www.kaltura.com/"
client = KalturaClient(config)
ks = client.generateSession(admin_secret, userID, ks_type, partnerID)
client.setKs(ks)

print "Retrieving..."
entryId = "1_j5689kew";

try:
    mediaEntry = client.media.get(entryId)
    print mediaEntry.getName()
except Base.KalturaException, e:
    print "could not get entry from Kaltura. Reason: %s" % repr(e)

print "Done."


filter = Plugins.Core.KalturaMediaEntryFilter()
filter.freeText = "1_j5689kew"
filter.orderBy = "-weight"
filter.advancedSearch = Plugins.Metadata.KalturaMetadataSearchItem()

pager = Plugins.Core.KalturaFilterPager()
results = client.media.list(filter, pager)
print results.getObjects()[0].getName()


print "Session Established."
file.close()