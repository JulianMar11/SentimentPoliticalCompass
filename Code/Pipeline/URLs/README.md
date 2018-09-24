


Data pipeline
-------------

The data pipeline steps correspond to the file structure stated below.

1. Crawl all article URLs with the Google custom search API
2. Crawl all pages of the articles
3. Verify date of all pages crawled and compare with the range crawled
4. Extract the textual content, check the date

New structure
-------------

1. Crawl all article URLs with the Google custom search API
2. Crawl all pages of the articles, at the same time extracting the date and the text information.
3. Verify the date
4. Eliminate duplicates


File structure:
---------------

The file structure coresponds to the steps of the data pipeline explained above.

1. urls -> urls.xlsx
    * databases
    * timePeriods
2. all_urls -> all_urls.xlsx
    * all_pages
    * verif_url
3. verify_date
4. text
    * article_content


TODO
----

* remove duplicates in the final URL list
* insert graphic of data pipeline into this README file


Lessons learned
---------------

* If you have an Import error, it is likely that you have circular dependencies (see https://stackoverflow.com/questions/9252543/importerror-cannot-import-name-x)


