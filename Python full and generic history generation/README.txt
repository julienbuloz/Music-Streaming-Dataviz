All scripts to generate the full database that will be used by D3JS:

0) Full history definition:
['User','Date','Jour','Week_day', 'Heure', 'Artiste', 'Titre', 'Song', 'Genre']

1) DataViz-CDrandom-CreateTable.ipynb
Create an history for user "M" based on random weighted list of Albums and days
Input:
- CD2010.csv
- ProbDaysHours.csv
Output :
- history_CD.csv
- history_CD.json

2) DataViz-Deezer-CreateTable.ipynb
Create an history for user "Deez" based on écoutes.json file
Input :
- écoutes.json
Output :
- history_Deez.csv
- history_Deez.json

3) DataViz-Deezer-GenreTable.ipynb
Create the list of albums from écoutes.json in order to get Genre from Deezer database
Output format : ['album', 'album_id', 'album_title', 'album_link']
Input :
- écoutes.json
Output :
- Deez_albums.json

4) DataViz-history-Graph.ipynb
Compile the history from all our sources (Deezer and CD as a first step on 2021/12/19)
Generate various types of graph based on these sources according to various filtering criteria (purpose is to test compliancy, visualisation will be generated in the HTML/JS/D3 page at the end)
Input :
- history_CD.csv
- history_Deez.csv
Output:
- all_history.csv
- all_history.json



