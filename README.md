# My Movie Hub

[![Build
Status](https://travis-ci.org/zhou-en/MovieUI.svg?branch=develop)](https://travis-ci.org/zhou-en/MovieUI)

Movie database interface built by scraping movie ratings and posters.

## Development Flow
1. Add ideas to the **To do** column in the project board
2. Flesh out each card/note in the project board
3. Convert cards/notes into issue when start working on it.
4. Create a branch with the card name off `develop` branch
5. Create a PR once the card is completed
6. Merge the PR to `develop` after review
7. Merge `develop` to `master` accordingly

## TODOs
The following ToDos need to be fleshed out and create cards on the [MovieUI board](https://github.com/users/zhou-en/projects/3)

### Backend (Django + SQL lite)

* [x] Define **movie** model
* [x] Create an API endpoint `/movie`
* [x] Update `/movie` endpoint to be able to query by:
  * year of release
  * title has
  * genres
* [x] Create a command to go through movies in the database and update imdb rating if it's changed.
* [x] Create command to scrap movie rating and data from [IMDb](https://www.imdb.com/) and [The Movie Database (TMDb)](https://www.themoviedb.org/)
  * [x] option: `-f` - search single movie by file name
  * [x] option: `-p` - search all movies in the given path
* [x] Add logging

### Frontend (React + Redux)

* [x] Movie list component
* [ ] Enable pagination for movie list component
* [ ] User profile component
* [ ] Search bar component
  * fields: title, year, rating
