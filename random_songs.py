import asyncio
import aiohttp
import random 
import time

ASCII_ALPHABET_LOWER_MIN = 97
ASCII_ALPHABET_LOWER_MAX = 122
MAX_FETCH_LIMIT = 5
MIN_RANDOM_WORDS_NUM = 5
MAX_RANDOM_WORDS_NUM = 20
RANDOM_WORDS_URL = 'https://random-words-api.vercel.app/word'
MUSICBRAINZ_URL =  'http://musicbrainz.org/ws/2/recording/?query={}&limit={}&fmt=json'

class GetRandomSongs():
    def __init__(self) -> None:
        self.random_words_url = RANDOM_WORDS_URL
        self.musicbrainz_url = MUSICBRAINZ_URL
        self.number_of_words = MIN_RANDOM_WORDS_NUM
        self.random_words = []
        self.random_songs = []

    def get_number_of_words_from_user(self) -> int:
        try:
            temp_num =  int(input("Wanna know some random song names?\nEnter a number between 5 to 20: "))
            if MIN_RANDOM_WORDS_NUM <= temp_num <= MAX_RANDOM_WORDS_NUM:
                self.number_of_words = temp_num
            return self.number_of_words
        except:
            print("Input must be number. Considering 5 random songs :)")
            return 0

    def get_words_sessions(self, session, fetch_nums) -> list:
        session_list = []
        for i in range(fetch_nums):
            session_list.append(session.get(RANDOM_WORDS_URL, ssl=False))
        return session_list
        
    
    async def get_random_words(self) -> None:
        max_iter = MAX_FETCH_LIMIT
        names_to_fetch = self.get_number_of_words_from_user()

        async with aiohttp.ClientSession() as session:
            for i in range(max_iter):
                temp_random_words = []
                url_list = self.get_words_sessions(session, names_to_fetch)
                responses = await asyncio.gather(*url_list)
                for res in responses:
                    temp_random_words.append(await res.json())

                temp_random_words = [i[0]['word'] for i in temp_random_words]
                temp_random_words = [i.lower() for i in temp_random_words]

                self.random_words += [i for i in list(set(temp_random_words)) if i not in self.random_words]
                duplicate_len = self.number_of_words - len(self.random_words)

                if  duplicate_len > 0:
                    names_to_fetch = duplicate_len
                elif duplicate_len > 0 and i == max_iter-1:
                    alphabet_list = list(random.sample(range(ASCII_ALPHABET_LOWER_MIN, ASCII_ALPHABET_LOWER_MAX+1), duplicate_len))
                    self.random_words += [chr(i) for i in alphabet_list]
                else:
                    break
            
        print(self.random_words)

    def get_songs_sessions(self, session, words_to_fetch) -> list:
        session_list = []
        for word in words_to_fetch:
            session_list.append(session.get(MUSICBRAINZ_URL.format(word, MAX_FETCH_LIMIT), ssl=False))
        return session_list
    
    def duplicate_songs_exists(self, current_title, current_artist, current_album) -> bool:
            for song in self.random_songs:
                if song['title'] == current_title and song['artist'] == current_artist and song['album'] == current_album:
                    return True
            return False
    
    async def get_random_songs(self) -> None:
        max_iter = MAX_FETCH_LIMIT

        async with aiohttp.ClientSession() as session:      
            url_list = self.get_songs_sessions(session, self.random_words)
            responses = await asyncio.gather(*url_list)
            for res in responses: 
                temp_json = await res.json()
                if 'error' in temp_json.keys():
                    break
                
                temp_dict = {}

                total_recordings = len(temp_json['recordings'])

                if(total_recordings > 0):
                    top_song = top_artist = top_release = 0
                    max_recordings_iter = total_recordings if total_recordings < MAX_FETCH_LIMIT else MAX_FETCH_LIMIT

                    for i in range(max_recordings_iter):
                        temp_dict['title'] = temp_json['recordings'][top_song]['title']
                        temp_dict['artist'] =  temp_json['recordings'][top_song]['artist-credit'][top_artist]['name']
                        temp_dict['album'] = temp_json['recordings'][top_song]['releases'][top_release]['title']

                        if self.duplicate_songs_exists(temp_dict['title'], temp_dict['artist'] , temp_dict['album']):
                            top_song += 1
                        else:
                            break
                else:
                    temp_dict['title'] = temp_dict['artist'] = temp_dict['album']  = None

                self.random_songs.append(temp_dict)
                

    def print_words_and_songs(self) -> None:
        if len(self.random_words) != len(self.random_songs):
            print('Could not fetch enough songs[API fetch limit reached] :( \nShowing only the fetched songs...')
            self.random_words = self.random_words[:len(self.random_songs)]
        
        for word, song in zip(self.random_words, self.random_songs):
            print("___________________________________________________")
            print(f"\nRandom word - {word}\n")
            if (song['title']):
                print(f"Song associated with this word: ")
                print(f"Title - {song['title']}")
                print(f"Artist - {song['artist']}")
                print(f"Album - {song['album']}")
            else:
                print("No recording found for this word :(")
            print("___________________________________________________")
        


    def run_get_words_and_songs(self) -> tuple:
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
        asyncio.run(self.get_random_words())
        asyncio.run(self.get_random_songs())
        self.print_words_and_songs()
        return zip(self.random_words, self.random_songs)

        


def main():
    user1 = GetRandomSongs()
    words_and_songs = user1.run_get_words_and_songs()

if __name__ == '__main__':
    main()


