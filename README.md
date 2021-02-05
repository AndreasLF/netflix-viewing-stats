# Netflix Viewing Stats
This program is meant to take all the data from the Netflix viewing history csv (which can be retrieved from Netflix) and provide an estimate on how much time you have spent watching Netlfix.

It is only tested on the Danish Netflix and from a Danish IP address (Google searches are made to find things on Netflix).

Only a rough estimate can be provided since Netflix only provides a title and a date in their viewing history. 
The program makes searches on TMDB and retrieves the runtime from the first search result (it does not check if it is the correct movie/series) if no match is found it tries to do a Google search with option "site:netflix.com" and scrape the runtime from Netflix' website.