from KalturaClient import *
import json


def main():
    file = open('/home/mediamigrator/django/channel_creation/settings.json')
    settings = json.load(file)
    file.close()

    # Channel Settings
    channel_name = settings["channel_settings"]["channel_name"]
    channel_description = settings["channel_settings"]["channel_description"]
    channel_privacy = settings["channel_settings"]["channel_privacy"]

    # Playlist Settings
    playlist_name = settings["playlist_settings"]["playlist_name"]
    playlist_desc = settings["playlist_settings"]["playlist_desc"]
    playlist_creation = settings["playlist_settings"]["playlist_creation"]

    client = create_session(settings)

    # Filter media based on filter settings
    filter_by = settings["filter_settings"]["filter_by"]
    if (filter_by == "CC"):
        filtered_media = filter_CC_content(client)
    elif (filter_by == "free_text"):
        filtered_media = filter_free_text(client, settings["filter_settings"]["free_text"])
    else:
        raise ValueError("Unexpected filter_by value. Got: " + filter_by + ". Expected: 'CC' or 'free_text'.")
    print filtered_media.getTotalCount()

    # Get Channel ID from existing channel, or create a new one
    try:
        channel = get_existing_channel(client, channel_name)
    except IndexError:
        channel = create_new_channel(client, channel_name, channel_description, channel_privacy)
    channel_id = channel.getId()
    channel_content = get_channel_content(client, channel_id)

    for media in filtered_media.getObjects():
        media_id = media.getId()
        print "Processing Media Entry " + str(media_id)
        if playlist_creation:
            try:
                playlist = get_existing_playlist(client, playlist_name, media.getUserId())
                print "Found old playlist, id: " + str(playlist.getId())
            except IndexError:
                playlist = create_new_playlist(client, playlist_name, media.getUserId(), playlist_desc)
                print "Created new playlist, id: " + str(playlist.getId())

            # add content if not already present
            current_pl_content = playlist.getPlaylistContent()
            if current_pl_content != "":
                content_to_add = current_pl_content + ", " + media_id
            else:
                content_to_add = media_id

            if media_id not in current_pl_content:
                playlist = update_playlist(client, content_to_add, playlist)
                print "Done, added " + str(media_id) + " to " + str(playlist.getId())

        if media_id not in channel_content:
            add_to_channel(client, channel_id, media_id)

    ids = [f.getId() for f in filtered_media.getObjects()]
    for media_ID in channel_content:
        if media_ID not in ids:
            client.categoryEntry.delete(media_ID, channel_id)
            print "rm" + str(media_ID)
            if playlist_creation:
                print "rm from playlist"
                delete_from_playlist(client, media_ID, playlist)




def create_session(settings):
    """ Connects to Kaltura Server and returns the authenticated client object"""
    user_id = settings["session_settings"]["user_id"]
    ks_type = settings["session_settings"]["ks_type"]
    admin_secret = settings["session_settings"]["admin_secret"]
    partner_id = settings["session_settings"]["partner_id"]
    service_url = settings["session_settings"]["service_url"]

    config = KalturaConfiguration(partner_id)
    config.serviceUrl = service_url
    client = KalturaClient(config)

    ks = client.generateSession(admin_secret, user_id, ks_type, partner_id)
    client.setKs(ks)
    return client


def filter_CC_content(client):
    """ Returns a <KalturaMediaListResponse> containing all media which has a CC License of any kind """
    filter = Plugins.Core.KalturaMediaEntryFilter()
    metadata_filter = Plugins.Metadata.KalturaMetadataSearchItem()

    # Type 2 = SEARCH_OR
    metadata_filter.setType(2)
    # Profile Id of "UoE Default" custom metadata field which we want to search through
    metadata_filter.setMetadataProfileId(7409571)

    # Setting all conditions, so all types of CC License are returned
    condition_attribution = Plugins.Core.KalturaSearchCondition()
    condition_attribution.setField("/*[local-name()='metadata']/*[local-name()='CCLicenceType']")
    condition_attribution.setValue("Creative Commons - Attribution")

    condition_att_no_deriv = Plugins.Core.KalturaSearchCondition()
    condition_att_no_deriv.setField("/*[local-name()='metadata']/*[local-name()='CCLicenceType']")
    condition_att_no_deriv.setValue("Creative Commons - Attribution No Derivatives")

    condition_att_non_like = Plugins.Core.KalturaSearchCondition()
    condition_att_non_like.setField("/*[local-name()='metadata']/*[local-name()='CCLicenceType']")
    condition_att_non_like.setValue("Creative Commons - Attribution Non Commercial  Share A Like")

    condition_like = Plugins.Core.KalturaSearchCondition()
    condition_like.setField("/*[local-name()='metadata']/*[local-name()='CCLicenceType']")
    condition_like.setValue("Creative Commons - Attribution Share A Like")

    condition_non_com = Plugins.Core.KalturaSearchCondition()
    condition_non_com.setField("/*[local-name()='metadata']/*[local-name()='CCLicenceType']")
    condition_non_com.setValue("Creative Commons - Attribution Non Commercial")

    condition_non_com_no_deriv = Plugins.Core.KalturaSearchCondition()
    condition_non_com_no_deriv.setField("/*[local-name()='metadata']/*[local-name()='CCLicenceType']")
    condition_non_com_no_deriv.setValue("Creative Commons - Attribution Non Commercial No Derivatives")

    # Set search conditions to filter
    metadata_filter.items = [condition_attribution, condition_att_no_deriv, condition_att_non_like,
                            condition_like, condition_non_com, condition_non_com_no_deriv]
    filter.advancedSearch = metadata_filter

    return client.media.list(filter)


def filter_free_text(client, free_text):
    """ Returns <KalturaMediaListResponse> of the media which have the requested freeText in their metadata (tags/title) """
    filter = Plugins.Core.KalturaMediaEntryFilter()
    filter.setFreeText(free_text)
    filter.orderBy = "-weight"
    filter.advancedSearch = Plugins.Metadata.KalturaMetadataSearchItem()
    return client.media.list(filter)


def get_existing_channel(client, channel_name):
    """ Returns requested channel, if it exists. Will throw an IndexError otherwise. """
    filter = Plugins.Core.KalturaCategoryFilter()
    filter.setFullNameEqual("MediaSpace>site>channels>" + channel_name)
    results = client.category.list(filter)
    return results.getObjects()[0]


def create_new_channel(client, channel_name, channel_description, channel_privacy):
    """ Creates and returns a new channel with the specified parameters """
    category = Plugins.Core.KalturaCategory()
    category.setName(channel_name)
    category.setParentId(23880051)
    category.setDescription(channel_description)
    category.setPrivacy(channel_privacy)
    return client.category.add(category)


def get_channel_content(client, channel_id):
    """ Returns a list of the ids of the media in the channel, ie. the contents of the channel """
    filter_category = Plugins.Core.KalturaCategoryEntryFilter()
    filter_category.setCategoryIdEqual(channel_id)
    cat_cont = client.categoryEntry.list(filter_category)
    channel_contents = []
    for media in cat_cont.getObjects():
        channel_contents.append(media.entryId)
    return channel_contents


def get_existing_playlist(client, playlist_name, user_id):
    """ Returns requested playlist, if it exists. Will throw an IndexError otherwise. """
    filter = Plugins.Core.KalturaPlaylistFilter()
    filter.setNameEqual(playlist_name)
    filter.setUserIdEqual(user_id)
    results = client.playlist.list(filter)
    return results.getObjects()[0]


def create_new_playlist(client, playlist_name, user_id, playlist_desc):
    """ Creates and returns a new playlist with the specified parameters """
    playlist = Plugins.Core.KalturaPlaylist()
    playlist.setName(playlist_name)
    playlist.setDescription(playlist_desc)
    playlist.setUserId(user_id)
    playlist.setPlaylistType(3)
    return client.playlist.add(playlist, "")


def update_playlist(client, content_to_add, original_playlist):
    """ Updates playlist content and returns updated playlist """
    new_playlist = Plugins.Core.KalturaPlaylist()
    new_playlist.setPlaylistContent(content_to_add)
    client.playlist.update(original_playlist.getId(), new_playlist, "")
    return get_existing_playlist(client, original_playlist.getName(), original_playlist.getUserId())


def delete_from_playlist(client, content_to_remove, original_playlist):
    """ Deletes contentToRemove from the playlist originalPlaylist and returns the updated playlist"""
    elems = original_playlist.getPlaylistContent().split(", ")
    if content_to_remove in elems:
        elems.remove(content_to_remove)
    new_content = (", ".join(elems))
    return update_playlist(client, new_content, original_playlist)


def add_to_channel(client, channel_id, media_id):
    """ Adds the media corresponding to mediaId to the channel """
    category_entry = Plugins.Core.KalturaCategoryEntry()
    category_entry.setCategoryId(channel_id)
    category_entry.setEntryId(media_id)
    client.categoryEntry.add(category_entry)


if __name__ == "__main__":
    main()