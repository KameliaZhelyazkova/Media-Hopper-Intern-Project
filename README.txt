== MEDIA HOPPER INTERN PROJECT ==

The aspiration of this project is to extend the capability of the University of Edinburgh’s
video platform Media Hopper.


== DESCRIPTION ==
The aim is to create a channel automatically populated with data specified either by keywords in the title/tags of the
data, or by a distinct license type, in this instance Creative Commons license type.
This would result that every time a user selects a Creative Commons license and publishes content,
it will be automatically added to the channel.

Another instance of its functionality is to create a unique playlist inside the channel for each user
who generates Creative Commons licensed content.
This allows embedding a playlist of all of a user's Creative Commons content in any website of their choice.


== DEPENDENCIES ==
Uses the Kaltura Python Client Library: http://www.kaltura.com/api_v3/testme/client-libs.php
This can be found in the "KalturaClient" directory.


== EXTERNAL DEPENDENCIES ==
The API library depends on the following python modules that are not included by default with python:
 - setuptools - can be downloaded from https://pypi.python.org/pypi/setuptools
 - poster - can be downloaded from https://pypi.python.org/pypi/poster/
	installed by running: python setup.py install


== USAGE ==
After making sure you have the modules listed under the 'external dependencies' installed,
run the following in the command prompt:
>> python creation_script.py


== CHANGE OF SETTINGS ==
{
  "sessionSettings": {"userID": "admin",
                      "ksType": 2,
                      "adminSecret": "1a7227978d8228dde2a574fac2c9b371",
                      "partnerID": 1817881,
                      "serviceUrl": "http://www.kaltura.com/"},

  "channelSettings": {"channelName": "Ada Lovelace Day",
                      "channelDescription": "Woo",
                      "channelPrivacy": 1},

  "filterSettings": {"filterBy":"CC",
                     "freeText":"media"}

  "playlistSettings": {"playlistCreation": true,
                       "playlistName": "Ada Lovelace Day in 2016 will be on Tuesday 11 October...",
                       "playlistDesc": "No"},
}

You can change the Session, Channel, Playlist and Filter settings by modifying "settings.json" file.
This is happening by entering for each key in the sub-dictionary the desired value for the corresponding
fields you would wish to change. For instance, "channelName" can be modified to a new one by entering
content (preferred naming) after the colons within the quotation marks.

Example code:
"channelSettings": {"channelName": "Ada Lovelace Day",
                    "channelDescription": "Ada Lovelace Day in 2016 will be on Tuesday 11 October...",
                    "channelPrivacy": 1}.



In addition "ksType" can hold values: 0 (USER) or 2 (ADMIN), "channelPrivacy": 1 (ALL), 2 (AUTHENTICATED_USERS) or
3 (MEMBERS_ONLY). "playlistCreation" should be set to true if you wish to generate playlists as explained above,
and to false otherwise. "filterBy" takes the value "CC" if you want to filter by Creative Commons license type,
and "freeText" to filter by keywords. In the later case, specify the keywords in "freeText".

Analogically, for any other values of an attribute, you can check the Kaltura's API documentation
on: http://www.kaltura.com/api_v3/testmeDoc/.





