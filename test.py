# from KalturaClient import *
# from KalturaClient import Plugins
#
# #userID = "kamelia.zhelyazkova@ed.ac.uk"
# userID = "admin"
# ks_type = 2
# admin_secret = "1a7227978d8228dde2a574fac2c9b371"
# partnerID = 1817881
# #
# config = KalturaConfiguration(partnerID)
# config.serviceUrl = "http://www.kaltura.com/"
# client = KalturaClient(config)
#
#
# ks = client.generateSession(admin_secret, userID, ks_type, partnerID)
# client.setKs(ks)
#
# print "Retrieving..."
# entryId = "1_j5689kew";
#
# #try:
# #    mediaEntry = client.media.get(entryId)
# #    print mediaEntry.getName()
# #except Base.KalturaException, e:
# #    print "could not get entry from Kaltura. Reason: %s" % repr(e)
#
# #print "Done."
#
# filter = Plugins.Core.KalturaMediaEntryFilter()
#
#
# filterAdvancedSearch = Plugins.Metadata.KalturaMetadataSearchItem()
# filterAdvancedSearch.type = 2
# filterAdvancedSearch.metadataProfileId = 7409571
#
# filterAdvancedSearchItems = Plugins.Core.KalturaSearchCondition()
# filterAdvancedSearchItems.field = "/*[local-name()='metadata']/*[local-name()='CCLicenceType']"
# filterAdvancedSearchItems.value = "Creative Commons - Attribution No Derivatives"
#
# filterAdvancedSearchItems1 = Plugins.Core.KalturaSearchCondition()
# filterAdvancedSearchItems1.field = "/*[local-name()='metadata']/*[local-name()='CCLicenceType']"
# filterAdvancedSearchItems1.value = "Creative Commons - Attribution"
#
# pager = Plugins.Core.KalturaFilterPager()
# #print filterAdvancedSearch
# #print filterAdvancedSearchItems
#
#
# filterAdvancedSearch.items = [filterAdvancedSearchItems1]
# #print filterAdvancedSearch.items
# filter.advancedSearch = filterAdvancedSearch
#
# results = client.media.list(filter, pager)
# print "objs"
# for obj in results.getObjects():
#     print obj.getName()
#
# print results.getObjects()

# filter = Plugins.Core.KalturaMediaEntryFilter()
# filter.orderBy = "+ /*[local-name()='metadata']/*[local-name()='CCLicenceType']"
# filter.advancedSearch = Plugins.Metadata.KalturaMetadataSearchItem()
# filter.advancedSearch.type = 2
# filter.advancedSearch.items = []
# filter.advancedSearch.items.append(Plugins.Core.KalturaSearchCondition())
# filter.advancedSearch.items[0].field = "/*[local-name()='metadata']/*[local-name()='CCLicenceType']"
# filter.advancedSearch.items[0].value = "Creative Commons - Attribution"
# filter.advancedSearch.metadataProfileId = 7409571
# pager = Plugins.Core.KalturaFilterPager()
# result = client.media.list(filter, pager)
# print result.objects

from creationScript import *
file = open('settings.json')
settings = json.load(file)
file.close()
client = createSession(settings)