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


PLAYLISTNAME = "Creative Commons Stuff Proper Test Thing"



# Get all CC data
"""
1_9xxyjomm, user admin
1_zmnvh38r, user connie
1_j5689kew, user marc
1_y1nhebhv, marc
1_x9s50hjz, marc
1_afs38koe, connie
"""


ccMedia = [client.media.get("1_9xxyjomm"), client.media.get("1_zmnvh38r"), client.media.get("1_j5689kew"), client.media.get("1_y1nhebhv"), client.media.get("1_x9s50hjz"), client.media.get("1_afs38koe")]

def main():

    for media in ccMedia:
        mediaId = media.getId()
        print "Processing Media Entry " + str(mediaId)

        # retrieve the playlist if it exists
        try:
            playlist = getExistingPlaylist(client, PLAYLISTNAME, media.getUserId())
            print "Found old playlist, id: " + str(playlist.getId())

        # the playlist does not yet exist
        except IndexError:
            playlist = createNewPlaylist(client, PLAYLISTNAME, media.getUserId())
            print "Created new playlist, id: " + str(playlist.getId())

        # add content if not already present
        currentPlContent = playlist.getPlaylistContent()
        if currentPlContent != "":
            contentToAdd = currentPlContent + ", " + mediaId
        else:
            contentToAdd = mediaId
        if mediaId not in currentPlContent:
            addToPlaylist(client, playlist, contentToAdd)
            print "Done, added " + str(mediaId) + "to " + str(playlist.getId())



def getExistingPlaylist(client, playlistName, userId):
    """ Checks whether the desired playlist already exists and returns it """
    filter = Plugins.Core.KalturaPlaylistFilter()
    filter.nameEqual = playlistName
    filter.userIdEqual = userId

    results = client.playlist.list(filter)
    return results.getObjects()[0]


def createNewPlaylist(client, playlistName, userId):
    """ Creates a new playlist with the specified parameters """
    playlist = Plugins.Core.KalturaPlaylist()
    playlist.setName(playlistName)
    playlist.setDescription("All my Media which is licensed with a Creative Commons License")
    playlist.setUserId(userId)
    playlist.setPlaylistType(3)

    return client.playlist.add(playlist, "")


def addToPlaylist(client, originalPlaylist, contentToAdd):
    """ Updates playlist content """
    newPlaylist = Plugins.Core.KalturaPlaylist()
    newPlaylist.setPlaylistContent(contentToAdd)
    client.playlist.update(originalPlaylist.getId(), newPlaylist, "")



if __name__ == "__main__":
    main()

