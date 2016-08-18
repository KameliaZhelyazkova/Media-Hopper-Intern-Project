== MEDIA HOPPER INTERN PROJECT ==

The goal of this project is to extend the capability of the University of Edinburgh’s video platform Media Hopper.


== DESCRIPTION ==
The aim is to create a channel and automatically populate it with data specified either by keywords in its title/tags,
or by a distinct licence type, in this instance the Creative Commons licence.
As a result, every time a user selects a Creative Commons licence and publishes content, it will automatically be
added to the channel.

Another instance of its functionality is to create a unique playlist for each user containing their Creative Commons
licenced content. This allows the user to embed a playlist of all their Creative Commons content in
any website of their choice.


== DEPENDENCIES ==
The project uses the Kaltura Python Client Library: http://www.kaltura.com/api_v3/testme/client-libs.php
This library must first be installed (we recommend using a virtual environment), following the instructions contained in its README (see above link).
Please note that the library itself has certain external dependencies:
    - setuptools - can be downloaded from https://pypi.python.org/pypi/setuptools
    - poster - can be downloaded from https://pypi.python.org/pypi/poster/
Further information can be found in the Kaltura Client README.


== USAGE ==
The project runs every day at 5am and 7pm (the CRON job is set up on the site's CPanel).
To run it manually, you can either
    - ssh into MediaMigrator, or
    - download a copy of the project and run it locally

If you choose to run it locally, first ensure that you have all the external dependencies installed.
You will also have to check that in the "creation_script.py" file the path to the settings file is correct.
The first line of the "main" function should read:
    file = open('PATH/TO/settings.json')

If you ssh into MediaMigrator, first activate the virtual environment in "/home/mediamigrator/virtualenv/django/2.7/bin" 
by running:
    $ source activate

Navigate into the "channel_creation" folder, and you can then run the following from the command line:
    $ python creation_script.py 

You can change the run settings by following the instructions in the section below.



== CHANGING THE SETTINGS ==

"settings.json":
{
  "session_settings": {"user_id": "admin",
                      "ks_type": 2,
                      "admin_secret": "ADMIN_SECRET_KEY",
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
For instance, "channel_name" can be modified to a new one by entering your preferred naming after the colon.

Example code:
"channel_settings": {"channel_name": "Ada Lovelace Day",
                    "channel_description": "Ada Lovelace Day in 2016 will be on Tuesday 11 October...",
                    "channel_privacy": 1}.

2. "partner_id" and "admin_secret" can be found on http://kmc.kaltura.com/ --> Settings --> Integration Settings.
Ensure that you are using the correct values depending on whether you are running the project in development or production.

3. "ks_type" can take the values (though you'll only ever want ADMIN): 0 (USER) or 2 (ADMIN), "channel_privacy": 1 (ALL), 2 (AUTHENTICATED_USERS)
or 3 (MEMBERS_ONLY).
"playlist_creation" should be set to true if you wish to generate playlists as explained above, and to false otherwise.
"filter_by" takes the value "CC" if you want to filter by Creative Commons licence type,
and "free_text" if you want to filter by keywords. In the latter case, specify the keywords in "free_text".

4. Though this should not be required, if you choose to run change the environment in which the project is being run you will need 
to modify:
    - the "metadataProfileId" in the "filter_CC_content" function
    - the channel's "ParentId" in the "create_new_channel" function
Both development and production values for these can be found in the comments of the code itself. 

5. For any other values of an attribute, you can check Kaltura's API documentation
on: http://www.kaltura.com/api_v3/testmeDoc/.