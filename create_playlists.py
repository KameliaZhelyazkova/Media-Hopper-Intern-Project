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

"""
loop through all media in cc licence
try to check if in playlist
    save id of it
except there is no newPlaylist
    create a newPlaylist
    save id of it

add media to newPlaylist
"""
ccMedia = [client.media.get("1_aswwijmi"), client.media.get("1_9xxyjomm")]

def __main__(self):

    for media in ccMedia:
        mediaId = media.getId()
        # retrieve the playlist if it exists
        try:
            playlist = self.getExistingPlaylist(client, "CCTest", "connie.crowe@ed.ac.uk")
            print "Found old playlist, id: " + str(playlist.getId())

        # the playlist does not yet exist
        except IndexError:
            playlist = createNewPlaylist(client, "CCTest", "connie.crowe@ed.ac.uk")
            print "Created new playlist, id: " + str(playlist.getId())

        # add content if not already present
        currentPlContent = playlist.getPlaylistContents()
        if mediaId not in currentPlContent:



        #
        # newPlaylist = Plugins.Core.KalturaPlaylist()
        # print originalPlaylist.getPlaylistContent()
        # newPlaylist.setPlaylistContent(originalPlaylist.getPlaylistContent().append(media.getId()))
        # print originalPlaylist.getId()
        # client.playlist.update(originalPlaylist.getId(), newPlaylist, updateStats)
        # print "Done, added" + str(media.getId())
        # print originalPlaylist.getId()
        # print originalPlaylist.getPlaylistContent()



def getExistingPlaylist(self, client, playlistName, userId):
    """ Checks whether the desired playlist already exists and returns it"""
    filter = Plugins.Core.KalturaPlaylistFilter()
    filter.nameEqual = playlistName
    filter.userIdEqual = userId

    results = client.playlist.list(filter)
    return results.getObjects()[0]


def createNewPlaylist(self, client, playlistName, userId):
    """ Creates a new playlist with the specified parameters"""

    playlist = Plugins.Core.KalturaPlaylist()
    playlist.setName(playlistName)
    playlist.setDescription("All my Media which is licensed with a Creative Commons License")
    playlist.setUserId(userId)
    playlist.setPlaylistType(3)

    return client.playlist.add(playlist, "")

def addToPlaylist(self, client, contentToAdd,  )
    newPlaylist = Plugins.Core.KalturaPlaylist()
    print originalPlaylist.getPlaylistContent()
    newPlaylist.setPlaylistContent(originalPlaylist.getPlaylistContent().append(media.getId()))
    print originalPlaylist.getId()
    client.playlist.update(originalPlaylist.getId(), newPlaylist, updateStats)
    print "Done, added" + str(media.getId())
    print originalPlaylist.getId()
    print originalPlaylist.getPlaylistContent()




