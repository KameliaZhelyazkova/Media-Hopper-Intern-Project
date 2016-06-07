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

#Filter through media to find all Creative commons licence type content
filter = Plugins.Core.KalturaMediaEntryFilter()
filterAdvancedSearch = Plugins.Metadata.KalturaMetadataSearchItem()
filterAdvancedSearch.type = 2
filterAdvancedSearch.metadataProfileId = 7409571
#filter = Plugins.Core.KalturaMediaEntryFilter()
#filter.mediaTypeEqual = 5
#filter.mediaTypeEqual = 2
#filter.mediaTypeEqual = 5

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

pager = Plugins.Core.KalturaFilterPager()
#print filterAdvancedSearch
print filterAdvancedSearchItems

#print filterAdvancedSearch.items
filterAdvancedSearch.items = [filterAdvancedSearchItemsCCType1, filterAdvancedSearchItemsCCType2,
                              filterAdvancedSearchItemsCCType3, filterAdvancedSearchItemsCCType4,
                              filterAdvancedSearchItemsCCType5, filterAdvancedSearchItemsCCType6]

filter.advancedSearch = filterAdvancedSearch
results = client.media.list(filter, pager)
print filterAdvancedSearch
print filterAdvancedSearchItems

#results = client.media.list(filter, pager)
#print "objs"
#for obj in results.getObjects():
#    print obj.getName()

#print results.getTotalCount()

#pager = Plugins.Core.KalturaFilterPager()
#results = client.media.list(filter, pager)
#for obj in results.getObjects():
 #   print obj.getName()
#print results.getObjects()
print results.getTotalCount()

# Insert filtered information into CC license channel

print results.getObjects()

categoryEntry = Plugins.Core.KalturaCategoryEntry()
categoryEntry.setCategoryId(44792221)



for media in results.getObjects():
    if media.getId() != entryId:





        #for media in category.getId():
    #if media.id != result