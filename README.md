# Sentiment Political Compass

One answer to biased news and false information is transparancy and quantifiablity.
For this reason, we introduce the Sentiment Political Compass,
a data-driven framework to analyze newspapers with respect to their political conviction.


	@article{falcksentiment, 
		title={Sentiment Political Compass: A Data-driven Analysis
		       of Online Newspapers regarding Political Orientation}, 
		author={Falck, Fabian and Marstaller, Julian and Stoehr, Niklas and 
		       Maucher, S{\"o}ren and Ren, Jeana and Thalhammer, Andreas 
		       and Rettinger, Achim and Studer, Rudi}, 
		booktitle={The Internet, Policy & Politics Conference 2018}, 
		year={2018}, 
	}


# Overview

## Links and Downloads
+ [Homepage](http://politicalcompass.de/)
+ [Dataset](http://politicalcompass.de/)
+ [Paper](http://blogs.oii.ox.ac.uk/policy/wp-content/uploads/sites/77/2018/08/IPP2018_Falck.pdf)

## Data Exploration
In order to explore the data and the code for creating the plots, we provide you with a [jupyter notebook](https://github.com/JulianMar11/SentimentPoliticalCompass/blob/master/Code/analysis.ipynb). If you just want to see charts, please refer to folder [Charts](https://github.com/JulianMar11/SentimentPoliticalCompass/tree/master/Charts).

## Pipeline Exploration
If you want to replicate a Sentiment Polical Compass for different newspapers, times or countries, please clone this repository and refer to the section [Code](https://github.com/JulianMar11/SentimentPoliticalCompass/tree/master/Code). All code was written in Python Version 3.6.4

	git clone https://github.com/JulianMar11/SentimentPoliticalCompass
    cd SentimentPoliticalCompass/
    pip install -r requirements.txt

Further instructions of the pipeline steps are provided in the subfolders for the processing steps.

## Dataset structure

*URL information*

| Column  | Type |  Explanation | 
| ------------- | ------------- | ------------- | 
| startdate  | Date  | beginning of time range used in url-crawling | 
| enddate  | Date  | ending of time range used in url-crawling | 
| date  | Date  |  assumed date of article, also used as index | 
| datetimedelta  | Date  | search range | 
| newspaper  | Category  | name of newspaper  | 
| search_term  | Category | name of searched entity | 
| response_id  | Identifier | identifier of search result  | 
| url  | URL  | article url |

*Sentiment information* ([IBM NLU API](https://www.ibm.com/watson/developercloud/natural-language-understanding/api/v1/?python#post-analyze))

| Column  | Type |  Explanation | 
| ------------- | ------------- | ------------- | 
| entity_text  | String  | Article text of entity  | 
| entity_type  | Category  | Type of entity, ([doc](https://console.bluemix.net/docs/services/natural-language-understanding/entity-types-v2.html#entit-tstypen-und-untertypen-version-2-))  | 
| count  | Int  | Mentions in article  | 
| relevance  | Float  | Relevance of entity in text  | 
| sentiment  | Float  |  Sentiment of entity in range -1, 1  | 
| sentimentcategory  | Category  | negative, positive or neutral sentiment  | 
| sentiment_id  | Identifier  | identifier of sentiment | 

*Match information*

| Column  | Type |  Explanation | 
| ------------- | ------------- | ------------- | 
| levenshtein  | Int  | Levenshtein distance of matched politician | 
| match_type  | Category | 1 = full match and searched politician <br /> 2 = full match but not searched politician <br /> 3 = surname match and searched politician <br /> 4 = surname match but not searched politician  | 
| politician  | Category | Name of matched politician  | 
| party  | Category | Party of matched politician  | 
| role  | Category | Political role of matched politician  | 



# Contributors

[Fabian Falck](https://github.com/FabianFalck), [Julian Marstaller](https://www.linkedin.com/in/julian-marstaller-0a8959b6/), [Niklas Stoehr](https://github.com/niklasstoehr), [Soeren Maucher](https://github.com/soerenmaucher), [Jeana Ren](https://github.com/jtren), [Andreas Thalhammer](https://www.linkedin.com/in/andreas-thalhammer/), [Achim Rettinger](https://www.linkedin.com/in/achim-rettinger/), [Rudi Studer](https://www.linkedin.com/in/rudi-studer-a5aaa887/)


# License

The MIT License ([MIT](http://opensource.org/licenses/mit-license.php))

Copyright (c) 2018 Fabian Falck, Julian Marstaller, Niklas Stoehr, Soeren Maucher, Jeana Ren, Andreas Thalhammer, Achim Rettinger, Rudi Studer

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
