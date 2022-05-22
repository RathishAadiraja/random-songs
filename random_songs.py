import asyncio
import aiohttp
import random 

# default values
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
        self.random_words_and_songs_dict = {         
            'data': []
        }                                            

    def get_number_of_words_from_user(self) -> int:

        # if the number is invalid or not an integer, the minimum number of words to fetch (5) is considered as default value
        try:
            print("Wanna know some random words and the songs associated with those words?")
            temp_num =  int(input("Enter the number of random words you wanna know and the number must be between 5 to 20: "))
            if MIN_RANDOM_WORDS_NUM <= temp_num <= MAX_RANDOM_WORDS_NUM:
                self.number_of_words = temp_num
            else:
                print("Input must be between the limit. Considering 5 random words :)")
            return self.number_of_words
        except:
            print("Input must be a number. Considering 5 random words :)")
            return self.number_of_words

    def get_words_sessions(self, session, fetch_nums) -> list:

        # type of session - <class 'aiohttp.client.ClientSession'>
        # fetch_nums - number of words to fetch

        session_list = []

        for i in range(fetch_nums):
            session_list.append(session.get(RANDOM_WORDS_URL, ssl=False))
        return session_list
        
    
    async def fetch_random_words(self) -> None:
        # using asynchronous fetching 
        number_of_words_to_fetch = self.get_number_of_words_from_user()

        async with aiohttp.ClientSession() as session:
            
            for i in range(MAX_FETCH_LIMIT):
                temp_random_words = []
                url_list = self.get_words_sessions(session, number_of_words_to_fetch)
                responses = await asyncio.gather(*url_list)

                for res in responses:
                    temp_random_words.append(await res.json())

                # the default response is a json format of list/array containing a single dictionary/object  
                # if the response is not in a valid format(error response)
                # example resultant string from the get request: 'Something Went Wrong - Enter the Correct API URL'
                # the response is skipped by checking the length of the response(default length = 1)
                
                temp_random_words = [i[0]['word'].lower() for i in temp_random_words if len(i)==1]

                # only unique words are added to self.random_words
                # the variable 'duplicate_len' represents number of unique words more to be fetched

                self.random_words += [i for i in list(set(temp_random_words)) if i not in self.random_words]
                duplicate_len = self.number_of_words - len(self.random_words)

                if  duplicate_len > 0:
                    number_of_words_to_fetch = duplicate_len
                else:
                    break

        self.random_words = sorted(self.random_words)   

    def get_songs_sessions(self, session, words_to_fetch) -> list:

        # type of session - <class 'aiohttp.client.ClientSession'>
        # words_to_fetch - list of random words to fetch

        session_list = []

        for word in words_to_fetch:

            # the MAX_FETCH_LIMIT is the limit value to misicbranz API
            # limits the number of recordings fetched for an unique word

            session_list.append(session.get(MUSICBRAINZ_URL.format(word, MAX_FETCH_LIMIT), ssl=False))
        return session_list
    
    async def fetch_random_songs(self) -> None:

        async with aiohttp.ClientSession() as session:      
            url_list = self.get_songs_sessions(session, self.random_words)
            responses = await asyncio.gather(*url_list)

            for res in responses: 
                temp_json = await res.json()

                # if the maximum fetch limit reached for musicbrainz API it returns a dictionary/object with key 'error'
                # {'error': 'Your requests are exceeding the allowable rate limit. Please see http://wiki.musicbrainz.org/XMLWebService for more information.'}
                # then for the subsequent random words the values of title, artist and album are set to None 

                if 'error' in temp_json.keys():
                    total_recordings = 0
                else:
                    total_recordings = len(temp_json['recordings'])  

                temp_dict = {}
                if(total_recordings > 0):
                    top_song = 0
                    max_recordings_iter = total_recordings if total_recordings < MAX_FETCH_LIMIT else MAX_FETCH_LIMIT

                    for i in range(max_recordings_iter):
                        temp_dict['title'] = temp_json['recordings'][top_song]['title']
                        temp_dict['artist'] =  temp_json['recordings'][top_song]['artist-credit'][0]['name']
                        temp_dict['album'] = temp_json['recordings'][top_song]['releases'][0]['title']

                        if temp_dict in self.random_songs:
                            top_song += 1
                        else:
                            break
                else:
                    temp_dict['title'] = temp_dict['artist'] = temp_dict['album']  = None

                self.random_songs.append(temp_dict)
     
    def make_words_and_songs_dict(self):
        
        self.random_words_and_songs_dict['data'] = []
        if len(self.random_words) != len(self.random_songs):
            self.random_words = self.random_words[:len(self.random_songs)]
        
        for word, song in zip(self.random_words, self.random_songs):
            temp = {}
            temp['word'] = word
            temp['title'] = song['title']
            temp['artist'] = song['artist']
            temp['album'] = song['album']
            self.random_words_and_songs_dict['data'].append(temp) 

    def print_words_and_songs(self) -> None:
        
        for item in self.random_words_and_songs_dict['data']:
            print("___________________________________________________")
            print(f"\nRandom word - {item['word']}\n")
            if (item['title']):
                print(f"Song associated with this word: ")
                print(f"Title - {item['title']}")
                print(f"Artist - {item['artist']}")
                print(f"Album - {item['album']}")
            else:
                print("No recording found for this word :(")
            print("___________________________________________________")
        


    def run_get_words_and_songs(self) -> dict:

        # using WindowsSelectorEventLoopPolicy() to override the 'RuntimeError: Event loop is closed' on windows
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

        asyncio.run(self.fetch_random_words())
        asyncio.run(self.fetch_random_songs())
        self.make_words_and_songs_dict()
        self.print_words_and_songs()
        return self.random_words_and_songs_dict

        


def main():
    user1 = GetRandomSongs()
    words_and_songs = user1.run_get_words_and_songs()

if __name__ == '__main__':
    main()


