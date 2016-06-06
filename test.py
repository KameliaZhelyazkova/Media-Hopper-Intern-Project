from KalturaClient import *
from KalturaClient import Plugins

#userID = "kamelia.zhelyazkova@ed.ac.uk"
userID = "admin"
ks_type = 2
admin_secret = "1a7227978d8228dde2a574fac2c9b371"
partnerID = 1817881
#
config = KalturaConfiguration(partnerID)
config.serviceUrl = "http://www.kaltura.com/"
client = KalturaClient(config)


ks = client.generateSession(admin_secret, userID, ks_type, partnerID)
client.setKs(ks)

print "Retrieving..."
entryId = "1_j5689kew";

#try:
#    mediaEntry = client.media.get(entryId)
#    print mediaEntry.getName()
#except Base.KalturaException, e:
#    print "could not get entry from Kaltura. Reason: %s" % repr(e)

#print "Done."
