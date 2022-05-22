# random-songs
A python console application to fetch user-defined number of random words between 5 to 20 from [random-words-api](https://random-words-api.vercel.app/word) and fetch information of songs with the titles of those names from [MusicBrainz API](https://musicbrainz.org/doc/MusicBrainz_API). The random words fetched are unique and ordered alphabetically. For each random word the top recoding in the MusicBrainz database is given the first priority and chosen. If one or more random words results in same song in top list the next top song is choosen to maintain uniqueness in both random words and songs.
- pip version used - 21.2.4
- python version used - 3.10.2
- windows 10
## How to clone?
```
git clone https://github.com/RathishAadiraja/random-songs.git
```
## How to run it?
- change the working directory to random-songs directory
```
cd random-songs
```
- create a virtual environment, if unfamiliar check [documentation](https://docs.python.org/3/tutorial/venv.html)
```
python -m venv env
```
- install the requirements by running  
 ```
 pip install -r requirements.txt
 ```
- run python console application
```
python random_songs.py
```
## How to use it?
- after running the above instructions the user will be asked to enter number of words to fetch
- the user must enter a value between 5 to 20, if not default value is used
- the result will be displayed on the console, it contains 
  - whole list of pulled unique and ordered random words
  - for each random word, it displays
    - the word
    - song title
    - song artist
    - song album
