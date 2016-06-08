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

if category.name != "Creative Commons license":
    results = client.category.add(category)


# Filter through media to find all Creative commons licence type content
filter = Plugins.Core.KalturaMediaEntryFilter()
filterAdvancedSearch = Plugins.Metadata.KalturaMetadataSearchItem()
filterAdvancedSearch.type = 2
filterAdvancedSearch.metadataProfileId = 7409571
# filter = Plugins.Core.KalturaMediaEntryFilter()
# filter.mediaTypeEqual = 5
# filter.mediaTypeEqual = 2
# filter.mediaTypeEqual = 5


filterAdvancedSearchItems = Plugins.Core.KalturaSearchCondition()

filterAdvancedSearchItemsCCType1 = Plugins.Core.KalturaSearchCondition()
filterAdvancedSearchItemsCCType1.field = "/*[local-name()='metadata']/*[local-name()='CCLicenceType']";
filterAdvancedSearchItemsCCType1.value = "Creative Commons - Attribution"

filterAdvancedSearchItemsCCType2 = Plugins.Core.KalturaSearchCondition()
filterAdvancedSearchItemsCCType2.field = "/*[local-name()='metadata']/*[local-name()='CCLicenceType']";
filterAdvancedSearchItemsCCType2.value = "Creative Commons - Attribution No Derivatives"

filterAdvancedSearchItemsCCType3 = Plugins.Core.KalturaSearchCondition()
filterAdvancedSearchItemsCCType3.field = "/*[local-name()='metadata']/*[local-name()='CCLicenceType']";
filterAdvancedSearchItemsCCType3.value = "Creative Commons - Attribution Non Commercial  Share A Like"

filterAdvancedSearchItemsCCType4 = Plugins.Core.KalturaSearchCondition()
filterAdvancedSearchItemsCCType4.field = "/*[local-name()='metadata']/*[local-name()='CCLicenceType']";
filterAdvancedSearchItemsCCType4.value = "Creative Commons - Attribution Share A Like"

filterAdvancedSearchItemsCCType5 = Plugins.Core.KalturaSearchCondition()
filterAdvancedSearchItemsCCType5.field = "/*[local-name()='metadata']/*[local-name()='CCLicenceType']";
filterAdvancedSearchItemsCCType5.value = "Creative Commons - Attribution Non Commercial"

filterAdvancedSearchItemsCCType6 = Plugins.Core.KalturaSearchCondition()
filterAdvancedSearchItemsCCType6.field = "/*[local-name()='metadata']/*[local-name()='CCLicenceType']";
filterAdvancedSearchItemsCCType6.value = "Creative Commons - Attribution Non Commercial No Derivatives"

pager = Plugins.Core.KalturaFilterPager()
# print filterAdvancedSearch
print filterAdvancedSearchItems
# print filterAdvancedSearch.items
filterAdvancedSearch.items = [filterAdvancedSearchItemsCCType1, filterAdvancedSearchItemsCCType2,
                              filterAdvancedSearchItemsCCType3, filterAdvancedSearchItemsCCType4,
                              filterAdvancedSearchItemsCCType5, filterAdvancedSearchItemsCCType6]

filter.advancedSearch = filterAdvancedSearch
results = client.media.list(filter, pager)
print filterAdvancedSearch
print filterAdvancedSearchItems
print results.getTotalCount()
print results.getObjects()

filterCategory = Plugins.Core.KalturaCategoryEntryFilter()
filterCategory.categoryIdEqual = 44792221

# Creating a list for all of the content of a channel
contentOfChannel = client.categoryEntry.list(filterCategory)
print contentOfChannel
channelContents = []
for c in contentOfChannel.getObjects():
    channelContents.append(c.entryId)
print channelContents


ccMedia = [client.media.get("1_9xxyjomm"), client.media.get("1_zmnvh38r"), client.media.get("1_j5689kew"), client.media.get("1_y1nhebhv"), client.media.get("1_x9s50hjz"), client.media.get("1_afs38koe")]
print contentOfChannel.getObjects()


# Delete changed type channel entries from actual channel
for mediaId in channelContents:
    # if media is not in result, delete it
    if client.media.get(mediaId) not in results.getObjects():
        # categoryEntry = Plugins.Core.KalturaCategoryEntry()
        # categoryEntry.setCategoryId(44792221)
        client.categoryEntry.delete(mediaId, 44792221)

# Add filtered media to the channel
for media in ccMedia:#results.getObjects():
    if media.getId() not in channelContents:
        categoryEntry = Plugins.Core.KalturaCategoryEntry()
        categoryEntry.setCategoryId(44792221)
        categoryEntry.entryId = media.getId()
        client.categoryEntry.add(categoryEntry)
        client.categoryEntry.add(categoryEntry)