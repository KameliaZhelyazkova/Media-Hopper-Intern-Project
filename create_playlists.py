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


# Get all CC data
ccMedia = []

#for media in ccMedia:
try:
    filter = Plugins.Core.KalturaPlaylistFilter()
    filter.nameEqual = "seconds"#media.getName()
    filter.userIdEqual = "connie.crowe@ed.ac.uk"#media.getUserId()
    pager = Plugins.Core.KalturaFilterPager()
    filterResults = client.playlist.list(filter, pager)
    print filterResults.objects
    originalPlaylist = filterResults.objects[0]

except IndexError:
    newPlaylist = Plugins.Core.KalturaPlaylist()
    newPlaylist.setName("Connie's Creative Commons2")
    newPlaylist.setDescription("All my Media which is licensed with a Creative Commons License")
    newPlaylist.setUserId("connie.crowe@ed.ac.uk")#media.getUserId()"")
    newPlaylist.setPlaylistType(3)
    updateStats = ""
    client.playlist.add(newPlaylist, updateStats)
    originalPlaylist = newPlaylist


id = originalPlaylist.getId()
print "ID" + id


#playlist = Plugins.Core.KalturaPlaylist()
#playlist.name = "Connie Test"
#update_stats = ""
#playlist.setPlaylistContent("1_zmnvh38r")
#print playlist.getPlaylistContent()
#client.playlist.update("1_5lbnz26g", playlist, update_stats)
#results = client.playlist.add(
#    playlist,
#    update_stats)

#client.playlist.delete("1_k9kjuajm")