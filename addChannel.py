from KalturaClient import *
from KalturaClient import Plugins

# User credentials
userID = "admin"
profileID = 7409571
ks_type = 2
admin_secret = "1a7227978d8228dde2a574fac2c9b371"
partnerID = 1817881

# Client configuration
config = KalturaConfiguration(partnerID)
config.serviceUrl = "http://www.kaltura.com/"
client = KalturaClient(config)
ks = client.generateSession(admin_secret, userID, ks_type, partnerID)
client.setKs(ks)

# Create/ add a CC licence category
category = Plugins.Core.KalturaCategory()
category.name = "Creative Commons license"
category.description = ""
category.tags = "Creative Commons license"
category.privacy = 1
results = client.category.add(category)


# 1. Filter through All media
# 2. Find the custom metadata field = "CC license type"

