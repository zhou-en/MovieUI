# My Movie Hub

[![Build
Status](https://travis-ci.org/zhou-en/MovieUI.svg?branch=develop)](https://travis-ci.org/zhou-en/MovieUI)

Movie database interface built by scraping movie ratings and posters.

## TODOs
The following ToDos need to be fleshed out and create cards on the [MovieUI board](https://github.com/zhou-en/MovieUI/projects/1)

### Backend (Django + SQL lite)

* [x] Define **movie** model
* [x] Create an API endpoint `/movie`
* [ ] Update `/movie` endpoint to be able to query by:
  * year of release
  * title has
  * genres
* [ ] Create a command to go through movies in the database and update imdb rating if it's changed.
* [ ] Create command to scrap movie rating and data from [IMDb](https://www.imdb.com/) and [The Movie Database (TMDb)](https://www.themoviedb.org/)
  * [x] option: `-f` - search single movie by file name
  * [ ] option: `-p` - search all movies in the given path
* [ ] Add logging

### Frontend (React + Redux)

* [ ] Movie list component
* [ ] User profile component
* [ ] Search bar componnet
  * fields: title, year, rating
