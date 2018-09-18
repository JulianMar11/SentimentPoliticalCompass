Entity Sentiment Analysis of News Paper Articles
========

General notes
-------------

* This work heaviliy uses the Polyglot library: http://polyglot.readthedocs.io/en/latest/index.html as well as research conducted by Chen, Yanqing and Skiena, Steven (Building sentiment lexicons for all major languages)and by Al-Rfou, Rami and Kulkarni, Vivek and Perozzi, Bryan and Skiena, Steven (Massive Multilingual Named Entity Recognition)



Installation
----------------

Code is written in python 3

`sudo pip3 polyglot`, `sudo pip3 pyicu`


Folder structure
----------------

* (folder) entity_sentiment_analysis
   * (folder) articles (1)
        * 0.txt
        * 1.txt
        * ...
   * (folder) keywords (2)
        * CDU.txt
        * SPD.txt
        * ...
   * (script) entity_sentiment_analysis.py (3)
   * (script) readme.md (4)

Data Format
----------------

* (1) articles: article files named and numbered: 0.txt, 1.txt and so on

    * articles are structured with tags:
    
       * `<t_*>` title and subtitles (0 <= * <= n) 
       * `<b_*>` body paragraph (0 <= * <= n) 
     
    if tags are too complicated, code will also work, just using `<>` as a deliminitor. Please refer to the following examplatory article:
    
    `<>Eine Idee gegen Merkel, wird Deutschland künftig Asylbewerber an der Grenze zurückweisen? Das fordert die CSU, die Idee soll Teil des Masterplans von Innenminister Seehofer sein.<>Seinen großen Aufschlag als Bundesinnenminister will Horst Seehofer nächste Woche zunächst den eigenen Leuten präsentieren: In der CSU-Landesgruppe am Montagabend wird Seehofer dem Vernehmen nach seinen sogenannten Masterplan Migration vorstellen.<>`
    
* (2) keywords: keywords belonging to one theme, topic, political party or organization are stored in separate .txt files.
  In every file, the keywords are simply listed row after row. There may be more keywords in one row if there are synonyms or associated terms:
  `entity_name, entity_name synonyms...` The keywords should be separated with a comma and a space as shown in the example. For instance, a keyword 
  file for the political party SPD may look like displayed below:
  
   `Nahles, Andrea, Andrea Nahles
    SPD, Sozialdemokratische Partei, Sozialdemokraten
    Lange, Simone Lange
    Gabriel, Sigmar Gabriel
    JuSos, Juso,
    Sozen, Sozis
    Kühnert, Kevin Kühnert, Juso-Chef`

* (3) entity_sentiment_analysis.py: Please configure the path to the articles and the keywords in the main method: 
   
    `articles_paths = "/Users/macbookpro/compass/articles/"`
    `keywords_path = "/Users/macbookpro/compass/keywords/"`


Code Working Principles
-------------

We provide different metrics for entity sentiment weighting.

* Weighting within Paragraph

    * `average`: if keyword occurs multiple times in paragraph, take the average sentiment

* Weighting within Article

    * `linear`: weight of sentiment decreases linearly from beginning to end of the article
    * `uniform`: all sentiments weight the same
    * `headline`: title weights 80% more than body



