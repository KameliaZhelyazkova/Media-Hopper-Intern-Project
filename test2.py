from KalturaClient import *
from KalturaClient import Plugins

# SERVER SESSION PARAMETERS
USER_ID = "admin"
KS_TYPE = 2
ADMIN_SECRET = "1a7227978d8228dde2a574fac2c9b371"
PARTNER_ID = 1817881


# Initialise Session
config = KalturaConfiguration(PARTNER_ID)
config.serviceUrl = "http://www.kaltura.com/"
client = KalturaClient(config)

ks = client.generateSession(ADMIN_SECRET, USER_ID, KS_TYPE, PARTNER_ID)
client.setKs(ks)


media1 = client.media.get("1_aswwijmi")
media2 = client.media.get("1_9xxyjomm")


""" Update existing Playlist"""
# playlist1 = Plugins.Core.KalturaPlaylist()
# update_stats = ""
# playlist1.setPlaylistContent(media1.getId() +", " + media2.getId())
# client.playlist.update("1_ei36v2yw", playlist1, update_stats)


"""" New Playlist """

# newPlaylist = Plugins.Core.KalturaPlaylist()
# newPlaylist.setName("CC Test")
# newPlaylist.setDescription("All my Media which is licensed with a Creative Commons License")
# newPlaylist.setUserId("connie.crowe@ed.ac.uk") # media.getUserId())
# newPlaylist.setPlaylistType(3)
# updateStats = ""
# originalPlaylist = client.playlist.add(newPlaylist, updateStats)
# print originalPlaylist
# print originalPlaylist.getId()
# print "Created new playlist" + str(originalPlaylist.getId())




""" Finding correct playlists """
filter = Plugins.Core.KalturaPlaylistFilter()
filter.nameEqual = "Connie Test2"
filter.userIdEqual = "connie.crowe@ed.ac.uk" # media.getUserId()
#pager = Plugins.Core.KalturaFilterPager()
filterResults = client.playlist.list(filter) #, #pager)
# print filterResults.getObjects()
originalPlaylist = filterResults.getObjects()[0]
updateStats = ""
print "Found old playlist" + str(originalPlaylist.getId())


"""" Adding Content """

# playlist1 = Plugins.Core.KalturaPlaylist()
# playlist1.name = "Connie Test3"
# playlist1.setPlaylistType(3)
# update_stats = ""
# playlist1.setPlaylistContent(media1.getId() +", " + media2.getId())
# addedPlay = client.playlist.add(playlist1,update_stats)
# print "addedPlay"
# print addedPlay.getPlaylistContent()
# print type(addedPlay.getPlaylistContent())
# print  addedPlay.getId()
#
#
# playlist2 = Plugins.Core.KalturaPlaylist()
# playlist2.name = "Connie Test4"
# playlist2.setPlaylistType(3)
# update_stats = ""
# playlist2.setPlaylistContent(addedPlay.getPlaylistContent() + ", " + media2.getId())
# print type(addedPlay.getPlaylistContent())
#
#
# results = client.playlist.add(
#     playlist2,
#     update_stats)

#client.playlist.delete("1_k9kjuajm")