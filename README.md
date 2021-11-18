# Nanori: A tool to make reading Japanese name easier
#### Video Demo:
#### Description:
Japanese names are written using kanji or chinese characters. Reading Japanese names was always a difficult thing to do, 
even for Japanese people. a kanji can have multiple readings and there is thousands of kanjis, not to mention that names
often use old kanjis that is no longer used in daily life often. There has been a lot of good online dictionaries for kanji
in the internet like jisho.org, but unfortunately often their readings are not complete (e.g not showing nanori/name reading).
Even after finding the kanji entries in dictionary it kinda inconvenient to try all the combinations of readings in our own head
and see what seems fit best. This web app will help you find the appropriate reading of a name by showing you the combinations
of kunyomi, onyomi, or even nanori readings of a combination of kanjis.  


#### Features
#### Search kanji
Pretty self explanatory, you can enter the kanjis in the search bar and see each of their meanings, and readings
#### Combine kanji readings
After searching the kanjis, you can combine their readings based on your choice, (either kunyomi, onyomi, or nanori) 
and show the list of the combinations. Note that this app will only combine the two first letters. Its also by no means accurate as japanaese name readings is
more complex and can consist of a combination of different readings (e.g kunyomi-onyomi), so this tool will just help you visualize the combination, not
necessarily telling you how the name is read
#### How
This flask app is build based on KANJIDIC2, an open source japanese english kanji dictionary made by Jim Breen, link 
to their website here http://www.edrdg.org/wiki/index.php/KANJIDIC_Project. When you entered the kanji to searchbar the back-end will iterate over the letters
and sending queries to sql. And then it give back the complete information about the letter (readings, meanings), and render it on the web page
#### Research
In making this project I learn a lot about how javascript and flask interact, new python modules such as sqlite3 and xml, python data structures, making a sqlite3 
database, CSS and HTML formatting and positioning, setting up virtual environment and git. I also take a look on variations of Japanese names readings and its conventions 

#### Files/program structure
`app.py` This is the back end flask application that will handle all requests from the web browser. You can run this app locally by running `flask run` on the repo
folder.  
  
`template/main.html` This is the first web page you will see, which only include the searchbar. When you entered text into the searchbar and submit, it will send get
request with parameter to `app.py`  
  
`template/search.html` This is a web page that will display your search result in the webpage and contain the javascript application to combine kanji readings by sending
AJAX call to `app.py` and display the results based on mode you selected
`Kanji Database/kanji.db` This the sqlite database file that is based on KANJIDIC2 and contain 5 tables for kanjis, meanings, and all three different readings 


#### Things that should be Improved
Unfortunately because it is using sqlite as a database, it can only be used and hosted on local machine. Deploying this app to Heroku requires PostgresSQL
with limited size if using free account. However migrating from sqlite to PostgresSQL requires pgloader which is only available in Linux and WSL, and I still
dont know how to use it as I am using windows. The database itself unfortunately is not very efficient in memory as its using 4 tables for all the different
readings, meanings and their respective kanji primary key
The usefulness of this application is also very limited because it just generate combinations instead of just using name dictionary, which contains hundreds
of thousands of japanese names
