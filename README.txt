Media Hopper Intern Project

The aspiration of this project is to extend the capability of the University
of Edinburgh’s video platform Media Hopper.

== DESCRIPTION ==

The aim is to create a channel automatically populated with data
specified by a distinct license type, in this instance creative commons
license type. This would result that every time a user selects a creative
commons license and publishes content that content will be automatically
added to the channel.

Another instance of it's functionality is to further develop the concept by
creating a unique playlist inside the channel for each user who generates creative
commons licensed content. This will allow academics to embed a playlist of all
their creative commons content in any website they wish.


== DEPENDENCIES ==
Uses the Kaltura Python Client Library found here: http://www.kaltura.com/api_v3/testme/client-libs.php
This can be found in the "KalturaClient" directory.

== EXTERNAL DEPENDENCIES ==

The API library depends on the following python modules that are not included by
default with python:
 - setuptools - can be downloaded from https://pypi.python.org/pypi/setuptools
 - poster - can be downloaded from https://pypi.python.org/pypi/poster/
	installed by running: python setup.py install

== USAGE ==

After making sure you have the modules listed under the 'external dependencies' installed,
run the following command into the command prompt:
>> python creation_script.py

== CHANGE OF SETTINGS ==

You can change the Session, Channel, Playlist and Filter settings by opening settings.json
file in the KalturaClient. This is happening by entering for each key in the sub-dictionary - the
corresponding value to each of the corresponding fields into each dictionary.
For instance, channelName can be changed to new one by entering a proffered naming (content) after the colon within the
quotation marks.




