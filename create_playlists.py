from KalturaClient import *
from KalturaClient import Plugins

# SERVER SESSION PARAMETERS
USER_ID = "admin"
KS_TYPE = 2
ADMIN_SECRET = "1a7227978d8228dde2a574fac2c9b371"
PARTNER_ID = 1817881
SERVICE_URL = "http://www.kaltura.com/"
# OPTIONS
# Category Settings
CATEGORY_NAME = "Creative Commons license"
CAT_DESCRIPTION  = ""
# Privacy values: ALL = 1, AUTHENTICATED_USERS = 2, MEMBERS_ONLY = 3
PRIVACY  = 1


#  Create a playlist for each user and add their content? [True, False]
PLAYLIST_CREATION = True
PLAYLIST_NAME = "Test Thingy"
PLAY_DESC = "All my Media which is licensed with a Creative Commons License"

# FILTER_BY = "cc" or "freetext"
FILTER_BY = ""
FREE_TEXT = ""



# Initialise Session
config = KalturaConfiguration(PARTNER_ID)
config.serviceUrl = SERVICE_URL
client = KalturaClient(config)

ks = client.generateSession(ADMIN_SECRET, USER_ID, KS_TYPE, PARTNER_ID)
client.setKs(ks)




# Get all CC data
"""
1_afs38koe, user connie
1_kncytozs, user connie
1_xw612s64, user marc
1_0k19hsqi, marc
1_oj9khhra, stephen
1_opaqpg82, stephen
"""


ccMedia = [client.media.get("1_afs38koe"), client.media.get("1_kncytozs"), client.media.get("1_xw612s64"), client.media.get("1_0k19hsqi"), client.media.get("1_oj9khhra"), client.media.get("1_powzieyo")]

def main():
    #filtered = filterCCContent()

    # Get Category if it exists
        # get category id
    # create category if it doesn't
        # get cateogory id


    #for media in filtered:
    for media in ccMedia:
        mediaId = media.getId()
        print "Processing Media Entry " + str(mediaId)

        # retrieve the playlist if it exists
        # if PLAYLIST_CREATION = True:
        try:
            playlist = getExistingPlaylist(client, PLAYLIST_NAME, media.getUserId())
            print "Found old playlist, id: " + str(playlist.getId())

        # create playlist if it doesn't exist
        except IndexError:
            playlist = createNewPlaylist(client, PLAYLIST_NAME, media.getUserId())
            print "Created new playlist, id: " + str(playlist.getId())

        # add content if not already present
        currentPlContent = playlist.getPlaylistContent()
        if currentPlContent != "":
            contentToAdd = currentPlContent + ", " + mediaId
        else:
            contentToAdd = mediaId

        if mediaId not in currentPlContent:
            updatePlaylist(client, contentToAdd, playlist)
            print "Done, added " + str(mediaId) + " to " + str(playlist.getId())
        else:
            print "Media " + str(mediaId) + " already in playlist " + str(playlist.getId())


        # if mediaId in channel and media.get(mediaId) not in filtered
            # delete it from channel
            # if using playlists
                # delete it from appropriate playlist
        # if media in not in channel
            # add to channel


def getExistingPlaylist(client, playlistName, userId):
    """ Returns desired playlist, if it exists """
    filter = Plugins.Core.KalturaPlaylistFilter()
    filter.nameEqual = playlistName
    filter.userIdEqual = userId

    results = client.playlist.list(filter)
    return results.getObjects()[0]


def createNewPlaylist(client, playlistName, userId):
    """ Creates a new playlist with the specified parameters """
    playlist = Plugins.Core.KalturaPlaylist()
    playlist.setName(playlistName)
    playlist.setDescription(PLAY_DESC)
    playlist.setUserId(userId)
    playlist.setPlaylistType(3)

    return client.playlist.add(playlist, "")


def updatePlaylist(client, contentToAdd, originalPlaylist):
    """ Updates playlist content """
    newPlaylist = Plugins.Core.KalturaPlaylist()
    newPlaylist.setPlaylistContent(contentToAdd)
    client.playlist.update(originalPlaylist.getId(), newPlaylist, "")


def deleteFromPlaylist(client, contentToRemove, originalPlaylist):
    elems = originalPlaylist.getPlaylistContent().split(", ")
    elems.remove(contentToRemove)
    newContent = (", ".join(elems))
    updatePlaylist(client, newContent, originalPlaylist)


def filterCCContent():
    """ Returns all media which has a CC License of any kind """
    filter = Plugins.Core.KalturaMediaEntryFilter()
    metadataFilter = Plugins.Metadata.KalturaMetadataSearchItem()

    # Type 2 = SEARCH_OR
    metadataFilter.setType(2)
    # Profile Id of "UoE Default" custom metadata field which we want to search through
    metadataFilter.setMetadataProfileId(7409571)

    # Setting all conditions, so all types of CC License is returned
    conditionAttribution = Plugins.Core.KalturaSearchCondition()
    conditionAttribution.setField("/*[local-name()='metadata']/*[local-name()='CCLicenceType']")
    conditionAttribution.setValue("Creative Commons - Attribution")

    conditionAttNoDeriv = Plugins.Core.KalturaSearchCondition()
    conditionAttNoDeriv.setField("/*[local-name()='metadata']/*[local-name()='CCLicenceType']")
    conditionAttNoDeriv.setValue("Creative Commons - Attribution No Derivatives")

    conditionAttNonComLike = Plugins.Core.KalturaSearchCondition()
    conditionAttNonComLike.setField("/*[local-name()='metadata']/*[local-name()='CCLicenceType']")
    conditionAttNonComLike.setValue("Creative Commons - Attribution Non Commercial  Share A Like")

    conditionLike = Plugins.Core.KalturaSearchCondition()
    conditionLike.setField("/*[local-name()='metadata']/*[local-name()='CCLicenceType']")
    conditionLike.setValue("Creative Commons - Attribution Share A Like")

    conditionNonCom = Plugins.Core.KalturaSearchCondition()
    conditionNonCom.setField("/*[local-name()='metadata']/*[local-name()='CCLicenceType']")
    conditionNonCom.setValue("Creative Commons - Attribution Non Commercial")

    conditionNonComNoDeriv = Plugins.Core.KalturaSearchCondition()
    conditionNonComNoDeriv.setField("/*[local-name()='metadata']/*[local-name()='CCLicenceType']")
    conditionNonComNoDeriv.setValue("Creative Commons - Attribution Non Commercial No Derivatives")

    # Set search conditions to filter
    metadataFilter.items = [conditionAttribution, conditionAttNoDeriv, conditionAttNonComLike,
                            conditionLike, conditionNonCom, conditionNonComNoDeriv]
    filter.advancedSearch = metadataFilter

    return client.media.list(filter)


def filterFreeText():
    """ Returns media with the requested FREE_TEXT somewhere in its metadata (tags/title) """
    filter = Plugins.Core.KalturaMediaEntryFilter()
    filter.free_text = FREE_TEXT
    filter.order_by = "-weight"
    filter.advanced_search = Plugins.Core.KalturaMetadataSearchItem()
    return client.media.list(filter)



if __name__ == "__main__":
    main()

