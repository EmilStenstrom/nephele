# What is Nephele?

Nephele is a Python script that lets you cross reference movie data from several sources. It currently supports **Torrentz**, **IMDB**, **Filmtipset** (Swedish rating site), **Kickass Torrentz**, and **YIFY Movies**. It's easy to add your own providers for new sources if you want (pull requests gladly accepted!).

## How do I run it?

```bash
python nephele.py get_popular
```
Get the most popular movies from Torrentz, cross-reference that data with data from Filmtipset and IMDB, and finally output the data to the terminal sorted by your Filmtipset grade.

```bash
python nephele.py get_grades "/path/to/your/directory"
```
Pass the path to a local directory with movie files, cross-reference that data with data from Filmtipset and IMDB, and finally output the data to the terminal sorted by your Filmtipset grade.

```bash
python nephele.py clear "Elephants Dream"
```
Remove a single movie from the movie db. This is useful when you have set a grade for a movie and want to update the local movie database.

## What does the result look like?

```
'71 (Filmtipset: 4, IMDB: 7.2)
  [Genre: Action, Drama, Thriller, Country: Storbritannien, Year: 2014]
  Plot: "A young and disoriented British soldier is accidentally abandoned by
  his unit following a riot on the deadly streets of Belfast in 1971."

Birdman (Filmtipset: 4, IMDB: 7.8)
  [Genre: Comedy, Drama, Country: USA, Year: 2014]
  Plot: "Illustrated upon the progress of his latest Broadway play, a former
  popular actor's struggle to cope with his current life as a wasted actor is
  shown."

Boyhood (Filmtipset: 4, IMDB: 8.0)
  [Genre: Drama, Country: USA, Year: 2014]
  Plot: "The life of Mason, from early childhood to his arrival at college."

Dallas Buyers Club (Filmtipset: 4, IMDB: 8.0)
  [Genre: Biography, Drama, Country: USA, Year: 2013]
  Plot: "In 1985 Dallas, electrician and hustler Ron Woodroof works around the
  system to help AIDS patients get the medication they need after he is
  diagnosed with the disease."

Dawn of the Planet of the Apes (Filmtipset: 4, IMDB: 7.7)
  [Genre: Action, Drama, Sci-Fi, Thriller, Country: USA, Year: 2014]
  Plot: "A growing nation of genetically evolved apes led by Caesar is
  threatened by a band of human survivors of the devastating virus unleashed a
  decade earlier."
```

## How do I install it?

Clone this repository to your computer and install dependencies (feel free to create your own virtualenv first).

```bash
git clone https://github.com/EmilStenstrom/nephele nephele
cd nephele
pip install -r requirements.txt
```

## How do I configure it?

You need two things: an `application.py` file and an `access_key.py` file.

### Set up a `application.py` file

All settings for your project are done in application.py. Create your application file by copying the application.py.sample file to application.py. Everything here should work out of the box, so skip to the next step if you are happy with the defaults.

If you want to change things, this is what the different settings do:

`DATABASE`: The filename of where the movie database will be stored. By default "db.json".

`POPULARITY_PROVIDER`: The service that will be used to fetch the currently popular movies. Default is Torrentz.

`MOVIEDATA_PROVIDERS`: A list of services where data about a particular movie will be found. Default is Filmtipset and IMDB.

`OUTPUT_PROVIDER`: How you want to output your data. By default it uses Filmtipset. It removes all movies you've seen, sorts it by the guessed grade and outputs it to the terminal.

### Set up an `access_key.py` file for Filmtipset

With those these changes, all requests are identified as your own (so I don't get the blame if you spam the API), and all grades will be based on your own accout.

- Rename `access_key.py.sample` to `access_key.py`
- Get your access key by following the instructions on [Filmtipset's API page](http://nyheter24.se/filmtipset/api.cgi)
- Get your user id by [searching for your username](http://nyheter24.se/filmtipset/search_member.cgi) and mouseover your nick, the member parameter is your user id
- Add those two settings to your `access_key.py`

## Contribute?

If you add more providers, please submit a pull request and I'll have a look!

## License (MIT)

Copyright (c) 2012 Emil Stenström

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
