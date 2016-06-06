from authentication import *

profileId = userID
def filter():
    filter = KalturaMetadataFilter()
    filter.objectIdEqual = userID
    filter.metadataProfileIdEqual = profileId
    filter.metadataObjectTypeEqual = ks_type #KalturaMetadataObjectType
    results = client.metadata.list(filter).objects


filter = KalturaMediaEntryFilter()