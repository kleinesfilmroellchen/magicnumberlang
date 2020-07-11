# Magic Number Language generator

Script that generates a language lexicon where all the words are NHentai sauce numbers of Doujinshis on that site. These numbers are also known as "six-digit numbers", "magic numbers" etc. and are a common occurrance in ~degenerate weeb~ anime culture. After a joke by reddit user [u/Anjeez929](https://www.reddit.com/user/Anjeez929/) on [r/conlangscirclejerk](https://www.reddit.com/r/conlangscirclejerk/comments/holp4l/prompt_a_numerical_language_made_out_of_sauce/), I was inspired to create a bot that takes care of the lexicon part for them. Just to clarify, nobody asked me for this. ~I am a fucking hardcore degenerate weeb that uses Computer Science to create a porn cipher language instead of curing cancer.~

To use this stuff, download and run with Python 3.8+, may also work with earlier Python3's. Run with `-h` option to get information on all the available parameters (I strongly recommend this before just randomly running it). Also note that due to the nature of the script, it cannot be cancelled with ^C. Close the terminal window instead.

Because NHentai has a very strong request restriction of about five requests per second per IP, this script will inherently run slow, there's no way around that. If you don't care about running this on a virtualized super-computer system of some sort to examine every Doujinshi in existance, you can just use the `mnl_dictionary.csv` file that I generated with the options `python magiclexigen.py -n 3000 -s 100`, i.e. 3000 doujinshis and only processing every 100th doujinshi. This resulted, with half an hour of (system-independent) runtime, in about 18 000 raw words which include a bunch of Japanese terms and names.

The format of these output files is normal CSV (can be opened in most spreadsheet programs) with the first column containing the English word, the second column containing the source number that is now the translation of that word, and the final column containing the rating value. This is a value where each occurance of the specific word in the doujin's title and tags are counted, while title occurrances count as 4 each. Higher scores generally mean that the doujin better represents the word. You will commonly encounter 4 and 1 scores, where 4 means a single occurrance in the title, and 1 means a single occurance in the tags.

This project requires BeautifulSoup4, the lxml parser and requests. Install all of these and their dependencies with `pip install bs4 lxml requests`.

This script uses a ported version of the nhentai.py library that can be found on PyPy, but its GitHub page seems to have gone missing. I assume it was licensed under Apache 2.0, as is usually all Python code, which makes this use legal. My modification includes porting to the newest NHentai page structure and handling 429 request errors as well as commented test code. (The latter statement is just for legalese's sake)

This thing I apparently made is licensed under MIT, go do with it whatever you please.

NHentai content is not appropriate for minors and may be subject to copyright. I take no responsiblity nor provide liability for any content found on nhentai.net or indirectly through this script.
