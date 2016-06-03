from KalturaClient import *

# session credentials
userID = "kamelia.zhelyazkova@ed.ac.uk"
ks_type = 2
admin_secret = "1a7227978d8228dde2a574fac2c9b371"
partnerID = 1817881


# config
config = KalturaConfiguration(partnerID)
config.serviceUrl = "http://www.kaltura.com/"
client = KalturaClient(config)
ks = client.generateSession(admin_secret, userID, ks_type, partnerID)
client.setKs(ks)


print "Session Established."