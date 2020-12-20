#!/usr/bin/python3
from collections import defaultdict
import logging

log = logging.getLogger(__name__)


def delete_keys_from_dict(dictionary, list_keys):
    """
    Helper to remove keys from a nested dictionary. Manipulates the original item.
    SO: https://stackoverflow.com/a/3405772

    Args:
        dictionary (Dict): Dictionary to manipulate
        list_keys (List(Str)): Keys to eliminate from dict

    Returns:
        dictionary (Dict): Resultant dict
    """
    for k in list_keys:
        try:
            del dictionary[k]
        except KeyError:
            pass
    for v in dictionary.values():
        if isinstance(v, dict):
            delete_keys_from_dict(v, list_keys)

    return dictionary


def get_all_saved_tracks(sp_client):
    """
    Helper to get all saved songs from a spotify user. Paginates on the max number of
    songs to request (50) and setting offsets.

    Args:
        sp_client (spotipy.Spotify): Spotify wrapper class to perform requests.

    Returns:
        all_songs (List(Dict)): List of user's complete saved songs
    """
    max_limit = 50
    offset = 0

    all_songs = []

    log.info("Requesting saved tracks: {} - {}".format(offset, max_limit))
    results = sp_client.current_user_saved_tracks(limit=max_limit, offset=offset)

    while results["next"]:
        all_songs.extend(results["items"])
        offset += max_limit
        log.info("Requesting saved tracks: {} - {}".format(offset, offset + max_limit))
        results = sp_client.current_user_saved_tracks(limit=max_limit, offset=offset)
        break

    for song in all_songs:
        delete_keys_from_dict(song, ["available_markets"])

    return all_songs
