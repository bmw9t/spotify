import spotipy
import sys
import random

# takes in the name of artist from the command line. defauls to weezer if no name is given.

if len(sys.argv) > 1:
    artist_name = sys.argv[1]
else:
    artist_name = 'weezer'

def genre_machine(artist_name, genres=[], counter=0, change='False'):
    """Generates a genre map for a given artist. To do so, it pulls in all genres for that artist as well as its related artists. Then it picks one of those related artists at random to follow the genealogy. If the aggregated genre list does not change after twenty new artists (the same number as listed on the related artist pages), the system assumes it has achieved a threshold genre mapping for this particular track and moves on."""

    # initializes the spotify object

    sp = spotipy.Spotify()

    try:
        # stores the search results for that artist, their name, and their uri
        result = sp.search(q='artist:' + artist_name, type='artist')
        name = result['artists']['items'][0]['name']
        uri = result['artists']['items'][0]['uri']
    
    except: 
        # in early stages the code was breaking frequently at this point because certain artists appear to have deleted from the system but still exist as traces in the related artist pages.

        print(result)
    
    print('Genres for', name)
    
    # pulls in all associated genres for that artist.
    for thing in result['artists']['items']:
        if thing['genres']:
            for genre in thing['genres']:
                if genre not in genres:
                    genres.append(genre)
                    change = 'True'

    # pulls in the related artists for the given artists
    related = sp.artist_related_artists(uri)
    
    # pulls in all of the genres for all of the related artists if they exist.
    for artist in related['artists']:
        if artist['genres']:
            for genre in thing['genres']:
                if genre not in genres:
                    genres.append(genre)
                    change = 'True' 
    
    # ends the recursion if 20 new artist traces don't produce any new genres            

    if counter == 19:
        print('Genre map completed:')
        print(genres)

    # if there are related artists, it picks one and runs again.
    elif len(related['artists']):

        # picks a new artist at random from the related genre list and uses it as the new artist.
        new_index = random.randint(0,(len(related['artists'])-1)) 
        new_artist = related['artists'][new_index]['name']
        print(genres)

        # if a new genre has added, the counter resets. otherwise, the counter increases towards the point at which it will assume a threshold genre map.
        if(change == 'True'):
            counter = 0
        else:
            counter += 1
        
        # if the new artist exists, go down that rabbit hole and run again.
        result = sp.search(q='artist:' + new_artist, type='artist')
        if result['artists']['items']:
            genre_machine(new_artist, genres, counter)
        else:
            # break if artists is deleted from spotify.
            print('Artist deleted from Spotify.')
    else:
        # break if the artist has no related artists.
        print('Musical Dead End - no connections for ', name, '.')
    
    return genres

def iterate_genres(artist_name, iterations=3):
    """Runs the genre machine function as many times as is wanted. Produces individual genre maps as well as an aggregate of them."""
    individual_genre_maps = []
    aggregate_genres = []

    # run the genre machine for as many times as suggested in the call to the function.
    for i in range(0, iterations):
        genres = genre_machine(artist_name, genres=[])

        # if genres were produced, add them to the aggregate as well as the collection of indiviudal genre maps.

        if genres:        
            for genre in genres:
                if genre not in aggregate_genres:
                    aggregate_genres.append(genre)
            individual_genre_maps.append(genres)
    # produce output
    print('===========================================')
    print('Individual genre Maps:')
    for genres in individual_genre_maps:
        print('Just one nerd\'s opinions on', artist_name)
        print(genres)
    print('===========================================')
    print('Aggregate genre map for', artist_name)
    print(aggregate_genres)

iterate_genres(artist_name, 5)
