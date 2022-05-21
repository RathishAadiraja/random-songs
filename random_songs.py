import asyncio
import aiohttp
import random 

ASCII_ALPHABET_LOWER_MIN = 97
ASCII_ALPHABET_LOWER_MAX = 122
MAX_WORD_FETCH_ITER = 5

class GetRandomSongs():
    def __init__(self) -> None:
        self.random_words_url = 'https://random-words-api.vercel.app/word'
        self.number_of_songs = 5
        self.random_words = []

    def get_number_of_songs(self) -> int:
        try:
            temp_num =  int(input("Wanna know some random song names?\nEnter a number between 5 to 20: "))
            if 5<= temp_num <= 20:
                self.number_of_songs = temp_num
        except:
            print("Input must be number. Considering 5 random songs :)")

    def get_session(self, session, num_songs) -> list:
        session_list = []
        for i in range(num_songs):
            session_list.append(session.get(self.random_words_url, ssl=False))
        return session_list
    
    async def get_random_words(self) -> None:
        max_iter = MAX_WORD_FETCH_ITER
        names_to_fetch = self.number_of_songs

        async with aiohttp.ClientSession() as session:
            for i in range(max_iter):
                temp_random_words = []
                url_list = self.get_session(session, names_to_fetch)
                responses = await asyncio.gather(*url_list)
                for res in responses:
                    temp_random_words.append(await res.json())
                temp_random_words = [i[0]['word'] for i in temp_random_words]
                temp_random_words = [i.lower() for i in temp_random_words]

                self.random_words += [i for i in list(set(temp_random_words)) if i not in self.random_words]
                duplicate_len = self.number_of_songs - len(self.random_words)

                if  duplicate_len > 0:
                    names_to_fetch = duplicate_len
                elif duplicate_len > 0 and i == max_iter-1:
                    alphabet_list = list(random.sample(range(ASCII_ALPHABET_LOWER_MIN, ASCII_ALPHABET_LOWER_MAX+1), duplicate_len))
                    self.random_words += [chr(i) for i in alphabet_list]
                else:
                    break
    
    def run_get_random_words(self) -> list:
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
        asyncio.run(self.get_random_words())
        return self.random_words


def main():
    user1 = GetRandomSongs()
    user1.get_number_of_songs()
    print(user1.number_of_songs)
    random_words = user1.run_get_random_words()
    print(random_words)

if __name__ == '__main__':
    main()


