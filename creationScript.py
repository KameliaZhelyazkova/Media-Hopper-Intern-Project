from KalturaClient import *
from KalturaClient import Plugins
import json



def main():

    # Load json file
    file = open('settings.json')
    settings = json.load(file)
    file.close()

    # Channel Settings
    channelName = settings["channelSettings"]["channelName"]
    channelDescription = settings["channelSettings"]["channelDescription"]
    channelPrivacy = settings["channelSettings"]["channelPrivacy"]

    # Playlist Settings
    playlistName = settings["playlistSettings"]["playlistName"]
    playlistDesc = settings["playlistSettings"]["playlistDesc"]
    playlistCreation = settings["playlistSettings"]["playlistCreation"]

    # Filter Settings
    filterBy = settings["filterSettings"]["filterBy"]

    client = createSession(settings)

    # Filter media based on filter settings
    if (filterBy == "CC"):
        filteredMedia = filterCCContent(client)
    elif (filterBy == "freeText"):
        filteredMedia = filterFreeText(client, settings["filterSettings"]["freeText"] )
    else:
        raise ValueError("Unexpected filterBy value. Expected values are 'CC' or 'freeText'.")

    #print filteredMedia.getTotalCount()
    # Get Channel ID from existing channel, or create a new one
    try:
        channel = getExistingChannel(client, channelName)
    except IndexError:
        channel = createNewChannel(client, channelName, channelDescription, channelPrivacy)
    channelID = channel.getId()
    channelContents = getChannelContents(client, channelID)

    for media in filteredMedia.getObjects():
        mediaID = media.getId()
        #print "Processing Media Entry " + str(mediaID)
        if playlistCreation:
            # Get playlist if it exists, or create a new one
            try:
                playlist = getExistingPlaylist(client, playlistName, media.getUserId())
                # print "Found old playlist, id: " + str(playlist.getId())
            except IndexError:
                playlist = createNewPlaylist(client, playlistName, media.getUserId(), playlistDesc)
                # print "Created new playlist, id: " + str(playlist.getId())

            # add content if not already present
            currentPlContent = playlist.getPlaylistContent()
            if currentPlContent != "":
                contentToAdd = currentPlContent + ", " + mediaID
            else:
                contentToAdd = mediaID

            if mediaID not in currentPlContent:
                playlist = updatePlaylist(client, contentToAdd, playlist)
                # print "Done, added " + str(mediaID) + " to " + str(playlist.getId())

        if mediaID not in channelContents:
            addToChannel(client, channelID, mediaID)

    ids = [f.getId() for f in filteredMedia.getObjects()]
    for mediaId in channelContents:
        if mediaId not in ids:
            client.categoryEntry.delete(mediaId, channelID)
            #print "rm" + str(mediaId)
            if playlistCreation:
                # print "rm from playlist"
                deleteFromPlaylist(client, mediaId, playlist)




def createSession(settings):
    """ Connects to Kaltura Server and returns the authenticated client object"""
    userID = settings["sessionSettings"]["userID"]
    ksType = settings["sessionSettings"]["ksType"]
    adminSecret = settings["sessionSettings"]["adminSecret"]
    partnerID = settings["sessionSettings"]["partnerID"]
    serviceUrl = settings["sessionSettings"]["serviceUrl"]

    config = KalturaConfiguration(partnerID)
    config.serviceUrl = serviceUrl
    client = KalturaClient(config)

    ks = client.generateSession(adminSecret, userID, ksType, partnerID)
    client.setKs(ks)
    return client


def filterCCContent(client):
    """ Returns a <KalturaMediaListResponse> containing all media which has a CC License of any kind """
    filter = Plugins.Core.KalturaMediaEntryFilter()
    metadataFilter = Plugins.Metadata.KalturaMetadataSearchItem()

    # Type 2 = SEARCH_OR
    metadataFilter.setType(2)
    # Profile Id of "UoE Default" custom metadata field which we want to search through
    metadataFilter.setMetadataProfileId(7409571)

    # Setting all conditions, so all types of CC License are returned
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


def filterFreeText(client, freeText):
    """ Returns <KalturaMediaListResponse> of the media which have the requested freeText in their metadata (tags/title) """
    filter = Plugins.Core.KalturaMediaEntryFilter()
    filter.setFreeText(freeText)
    filter.orderBy = "-weight"
    filter.advancedSearch = Plugins.Metadata.KalturaMetadataSearchItem()
    return client.media.list(filter)


def getExistingChannel(client, channelName):
    """ Returns requested channel, if it exists. Will throw an IndexError otherwise. """
    filter = Plugins.Core.KalturaCategoryFilter()
    filter.setFullNameEqual(channelName)
    results = client.category.list(filter)
    return results.getObjects()[0]


def createNewChannel(client, channelName, channelDescription, channelPrivacy):
    """ Creates and returns a new channel with the specified parameters """
    category = Plugins.Core.KalturaCategory()
    category.setName(channelName)
    category.setDescription(channelDescription)
    category.setPrivacy(channelPrivacy)
    return client.category.add(category)


def getChannelContents(client, channelID):
    """ Returns a list of the ids of the media in the channel, ie. the contents of hte channel """
    filterCategory = Plugins.Core.KalturaCategoryEntryFilter()
    filterCategory.setCategoryIdEqual(channelID)
    catCont = client.categoryEntry.list(filterCategory)
    channelContents = []
    for media in catCont.getObjects():
        channelContents.append(media.entryId)
    return channelContents


def getExistingPlaylist(client, playlistName, userId):
    """ Returns requested playlist, if it exists. Will throw an IndexError otherwise. """
    filter = Plugins.Core.KalturaPlaylistFilter()
    filter.setNameEqual(playlistName)
    filter.setUserIdEqual(userId)
    results = client.playlist.list(filter)
    return results.getObjects()[0]


def createNewPlaylist(client, playlistName, userId, playlistDesc):
    """ Creates and returns a new playlist with the specified parameters """
    playlist = Plugins.Core.KalturaPlaylist()
    playlist.setName(playlistName)
    playlist.setDescription(playlistDesc)
    playlist.setUserId(userId)
    playlist.setPlaylistType(3)
    return client.playlist.add(playlist, "")


def updatePlaylist(client, contentToAdd, originalPlaylist):
    """ Updates playlist content and returns updated playlist """
    newPlaylist = Plugins.Core.KalturaPlaylist()
    newPlaylist.setPlaylistContent(contentToAdd)
    client.playlist.update(originalPlaylist.getId(), newPlaylist, "")
    return getExistingPlaylist(client, originalPlaylist.getName(), originalPlaylist.getUserId())


def deleteFromPlaylist(client, contentToRemove, originalPlaylist):
    """ Deletes contentToRemove from the playlist originalPlaylist and returns the updated playlist"""
    elems = originalPlaylist.getPlaylistContent().split(", ")
    if contentToRemove in elems:
        elems.remove(contentToRemove)
    newContent = (", ".join(elems))
    return updatePlaylist(client, newContent, originalPlaylist)


def addToChannel(client, channelID, mediaID):
    """ Adds the media corresponding to mediaId to the channel """
    categoryEntry = Plugins.Core.KalturaCategoryEntry()
    categoryEntry.setCategoryId(channelID)
    categoryEntry.setEntryId(mediaID)
    client.categoryEntry.add(categoryEntry)



if __name__ == "__main__":
    main()

