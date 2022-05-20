import asyncio
import aiohttp

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

    def get_session(self, session) -> list:
        session_list = []
        for i in range(self.number_of_songs):
            session_list.append(session.get(self.random_words_url, ssl=False))
        return session_list
    
    async def get_random_words(self) -> None:
        async with aiohttp.ClientSession() as session:
            url_list = self.get_session(session)
            responses = await asyncio.gather(*url_list)
            for res in responses:
                self.random_words.append(await res.json())
    
    def run_get_random_words(self) -> list:
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
        asyncio.run(self.get_random_words())
        return self.random_words




user1 = GetRandomSongs()
user1.get_number_of_songs()
print(user1.number_of_songs)
random_words = user1.run_get_random_words()
print(random_words)