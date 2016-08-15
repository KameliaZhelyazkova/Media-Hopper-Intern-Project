== MEDIA HOPPER INTERN PROJECT ==

The goal of this project is to extend the capability of the University of Edinburgh’s video platform Media Hopper.


== DESCRIPTION ==
The aim is to create a channel and automatically populate it with data specified either by keywords in its title/tags,
or by a distinct licence type, in this instance the Creative Commons licence.
As a result, every time a user selects a Creative Commons licence and publishes content it will be automatically
added to the channel.

Another instance of its functionality is to create a unique playlist for each user containing their Creative Commons
licenced content. This allows the user to embed a playlist of all their Creative Commons content in
any website of their choice.


== DEPENDENCIES ==
The project uses the Kaltura Python Client Library: http://www.kaltura.com/api_v3/testme/client-libs.php
This library must first be installed, following the instructions contained in its README (see above link).
Please note that the library itself has certain external dependencies:
    - setuptools - can be downloaded from https://pypi.python.org/pypi/setuptools
    - poster - can be downloaded from https://pypi.python.org/pypi/poster/
Further information can be found in the Kaltura Client README.


== USAGE ==
The project runs every day at 5am and 7pm.
To run it manually, first download the project folder and ensure that you have all the external dependencies installed.
You can change the run settings by following the instructions in the section below.
In the "creation_script.py" file, please ensure that the first line of the main function has been provided with the
correct path to the "settings.json" file. It should read:
    file = open('PATH/TO/settings.json')

From the command line, you can then run:
    $ python creation_script.py


== CHANGING THE SETTINGS ==

{
  "session_settings": {"user_id": "admin",
                      "ks_type": 2,
                      "admin_secret": "Set to admin secret",
                      "partner_id": XXXXXXXX,
                      "service_url": "http://www.kaltura.com/"},

  "channel_settings": {"channel_name": "Test Channel",
                      "channel_description": "Enter channel description here.",
                      "channel_privacy": 1},

  "filter_settings": {"filter_by":"CC",
                     "free_text":"Enter free text to filter by here."},

  "playlist_settings": {"playlist_creation": true,
                       "playlist_name": "Test Playlist",
                       "playlist_desc": "Enter playlist description here."}
}


1. You can change the session, channel, playlist and filter settings by modifying "settings.json" file.
To do so, enter the desired value for the field you wish to change next to the corresponding key in the sub-dictionary.
For instance, "channel_name" can be modified to a new one by entering your preferred naming after the colons
within the quotation marks.

Example code:
"channel_settings": {"channel_name": "Ada Lovelace Day",
                    "channel_description": "Ada Lovelace Day in 2016 will be on Tuesday 11 October...",
                    "channel_privacy": 1}.

2. "partner_id" and "admin_secret" can be found on http://kmc.kaltura.com/ --> Settings --> Integration Settings.

3. "ks_type" can take the values: 0 (USER) or 2 (ADMIN), "channel_privacy": 1 (ALL), 2 (AUTHENTICATED_USERS)
or 3 (MEMBERS_ONLY).
"playlist_creation" should be set to true if you wish to generate playlists as explained above, and to false otherwise.
"filter_by" takes the value "CC" if you want to filter by Creative Commons licence type,
and "free_text" to filter by keywords. In the latter case, specify the keywords in "free_text".

4. To create a new channel into a particular place into the structure make sure that you set the category.setParentId(...) to the place you would like your new channel to be created. 

Example code:
def create_new_channel(client, channel_name, channel_description, channel_privacy):
    """ Create and return a new channel with the specified parameters. """
    category = Plugins.Core.KalturaCategory()
    category.setName(channel_name)
    category.setParentId(35401612)
    category.setDescription(channel_description)
    category.setPrivacy(channel_privacy)
    return client.category.add(category)

5. For any other values of an attribute, you can check Kaltura's API documentation
on: http://www.kaltura.com/api_v3/testmeDoc/.