import spotipy
import sys
import pprint
import random

# takes in two artists and looks to see if they are connected as related artists. If not, it pulls a randomly selected artist from that related list and tries again to find a connection. Goes until it finds a link, a dead end, or Python screams for it to stop.


def kevin_bacon(artist_name, counter=0):
    sp = spotipy.Spotify()
    result = sp.search(q='artist:' + artist_name, type='artist')
    try:
        name = result['artists']['items'][0]['name']
        uri = result['artists']['items'][0]['uri']

        related = sp.artist_related_artists(uri)
        print('Related artists for', name)
        for artist in related['artists']:
            print('  ', artist['name'])
    except:
        print("usage show_related.py [artist-name]")

    if sys.argv[2] in (artist['name'] for artist in related['artists']):
        print('success!')

    elif related['artists']:
        new_index = random.randint(0,19)    
        new_artist = related['artists'][new_index]['name']
        print('New artist: ', new_artist)
        counter += 1
        print(counter, ' degrees of separation from', sys.argv[1])
        kevin_bacon(new_artist, counter)
        
    else:
        print('Name is a musical dead end.')
if len(sys.argv) > 1:
    artist_name = sys.argv[1]
else:
    artist_name = 'weezer'

kevin_bacon(artist_name)