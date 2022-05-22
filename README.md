# Random Songs
A python console application to fetch user-defined number of random words ranging between 5 to 20 from [random-words-api](https://random-words-api.vercel.app/word). These random words are unique and ordered alphabetically become the title of the song to be fetched from [MusicBrainz API](https://musicbrainz.org/doc/MusicBrainz_API). For each random word, the top recording in the MusicBrainz database is given the first priority and chosen. If one or more random words result in the same song on top of the response list then the next song is chosen, to maintain uniqueness in both random words and songs.
- pip version used - 21.2.4
- python version used - 3.10.2
- windows 10
## How to clone?
```
git clone https://github.com/RathishAadiraja/random-songs.git
```
## How to run it?
- Change the working directory to random-songs directory
```
cd random-songs
```
- Create a virtual environment, if unfamiliar check [documentation](https://docs.python.org/3/tutorial/venv.html)
```
python -m venv env
```
- Install the requirements by running  
 ```
 pip install -r requirements.txt
 ```
- Run python console application
```
python random_songs.py
```
## How to use it?
- After running the above commands the user will be asked to enter number of words to fetch
- The user must enter a value between 5 to 20, if not default value is used
- The result will be displayed on the console, it contains 
  - Whole list of pulled unique and ordered random words
  - For each random word, it displays
    - The word
    - Song title
    - Song artist
    - Song album
- If there are no recordings found for the random word, it displays only the word along with the message 'no recordings found'
