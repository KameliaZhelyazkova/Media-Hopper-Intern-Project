from KalturaClient import *
#from KalturaClient import Plugins

# SERVER SET UP
userID = "admin"
ks_type = 2
admin_secret = "1a7227978d8228dde2a574fac2c9b371"
partnerID = 1817881

config = KalturaConfiguration(partnerID)
config.serviceUrl = "http://www.kaltura.com/"
client = KalturaClient(config)

ks = client.generateSession(admin_secret, userID, ks_type, partnerID)
client.setKs(ks)



playlist = Plugins.Core.KalturaPlaylist()
playlist.name = "Test2"
playlist.description = "testing"
playlist.userId = "connie.crowe@ed.ac.uk"
playlist.licenseType = 3
playlist.playlistType = 10
playlist.totalResults = 10

update_stats = ""
print playlist.getPlaylistContent()
#results = client.playlist.add(
#    playlist,
#    update_stats)

#client.playlist.delete("1_k9kjuajm")