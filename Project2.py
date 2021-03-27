from bs4 import BeautifulSoup
import requests
import re
import os
import csv
import unittest


def get_titles_from_search_results(filename):
    """
    Write a function that creates a BeautifulSoup object on "search_results.htm". Parse
    through the object and return a list of tuples containing book titles (as printed on the Goodreads website) 
    and authors in the format given below. Make sure to strip() any newlines from the book titles and author names.

    [('Book title 1', 'Author 1'), ('Book title 2', 'Author 2')...]
    """

    filevar = open(filename, 'r')
    readvar = filevar.read()
    filevar.close()
    
    workingsoup = BeautifulSoup(readvar, 'html.parser')
    resultsvar1 = workingsoup.find_all('td', width = '100%')
    newitems = [(anyentry.find('a', class_ = "bookTitle").find('span').text, anyentry.find('a', class_ = "authorName").find('span').text) for anyentry in resultsvar1]
    return newitems


def get_search_links():
    """
    Write a function that creates a BeautifulSoup object after retrieving content from
    "https://www.goodreads.com/search?q=fantasy&qid=NwUsLiA2Nc". Parse through the object and return a list of
    URLs for each of the first ten books in the search using the following format:

    ['https://www.goodreads.com/book/show/84136.Fantasy_Lover?from_search=true&from_srp=true&qid=NwUsLiA2Nc&rank=1', ...]

    Notice that you should ONLY add URLs that start with "https://www.goodreads.com/book/show/" to 
    your list, and , and be sure to append the full path to the URL so that the url is in the format 
    “https://www.goodreads.com/book/show/kdkd".

    """

    textvar = requests.get("https://www.goodreads.com/search?q=fantasy&qid=NwUsLiA2Nc").text
    workingsoup = BeautifulSoup(textvar, 'html.parser')
    bookentries = workingsoup.find_all('tr', itemtype = "http://schema.org/Book")[:10]
    return_list = ["https://www.goodreads.com" + anyentry.find('a')['href'] for anyentry in bookentries]
    return return_list


def get_book_summary(book_url):
    """
    Write a function that creates a BeautifulSoup object that extracts book
    information from a book's webpage, given the URL of the book. Parse through
    the BeautifulSoup object, and capture the book title, book author, and number 
    of pages. This function should return a tuple in the following format:

    ('Some book title', 'the book's author', number of pages)

    HINT: Using BeautifulSoup's find() method may help you here.
    You can easily capture CSS selectors with your browser's inspector window.
    Make sure to strip() any newlines from the book title and number of pages.
    """

    textvar = requests.get(book_url).text
    workingsoup = BeautifulSoup(textvar, 'html.parser')
    bookdata = workingsoup.find('div', id = 'metacol', class_ = 'last col')
    (booktitle, bookauthor, numpages) = (
        bookdata.find('h1', id = 'bookTitle').text, 
        bookdata.find('div', id = 'bookAuthors').find('span', itemprop = 'name').text, 
        bookdata.find('div', id = 'details').find('span', itemprop = 'numberOfPages').text)
    return (booktitle.strip('\n').strip(), bookauthor.strip('\n').strip(), numpages.strip('\n').strip())


def summarize_best_books(filepath = None): # implement OS filepath stuff!
    """
    Write a function to get a list of categories, book title and URLs from the "BEST BOOKS OF 2020"
    page in "best_books_2020.htm". This function should create a BeautifulSoup object from a 
    filepath and return a list of (category, book title, URL) tuples.
    
    For example, if the best book in category "Fiction" is "The Testaments (The Handmaid's Tale, #2)", with URL
    https://www.goodreads.com/choiceawards/best-fiction-books-2020, then you should append 
    ("Fiction", "The Testaments (The Handmaid's Tale, #2)", "https://www.goodreads.com/choiceawards/best-fiction-books-2020") 
    to your list of tuples.
    """

    filevar = open('best_books_2020.htm', 'r')
    readvar = filevar.read()
    filevar.close()

    workingsoup = BeautifulSoup(readvar, 'html.parser')
    resultsholderlist = workingsoup.find_all('div', class_ = 'category clearFix')
    return_list = [(anyentry.find('h4', class_ = 'category__copy').text.strip('\n'),
        anyentry.find('img', class_ = 'category__winnerImage')['alt'].strip('\n'),
        anyentry.find('a')['href'].strip('\n'))
        for anyentry in resultsholderlist]
    return return_list


def write_csv(data, filename):
    """
    Write a function that takes in a list of tuples (called data, i.e. the
    one that is returned by get_titles_from_search_results()), writes the data to a 
    csv file, and saves it to the passed filename.

    The first row of the csv should contain "Book Title" and "Author Name", and
    respectively as column headers. For each tuple in data, write a new
    row to the csv, placing each element of the tuple in the correct column.

    When you are done your CSV file should look like this:

    Book title,Author Name
    Book1,Author1
    Book2,Author2
    Book3,Author3
    ......

    This function should not return anything.
    """

    filevar = open(filename, 'w')
    filevar.write("Book title,Author Name\n")
    for anyentry in data:
            filevar.write(anyentry[0].replace(",", "&#44") + ',' + anyentry[1].replace(",", "&#44") + "\n")
    filevar.close()
    return None


def extra_credit(filepath):
    """
    EXTRA CREDIT

    Please see the instructions document for more information on how to complete this function.
    You do not have to write test cases for this function.
    """
    pass

class TestCases(unittest.TestCase):

    def setUp(self):
    # call get_search_links() and save it to a static variable: search_urls
        self.search_urls = get_search_links()

    def test_get_titles_from_search_results(self):
        # call get_titles_from_search_results() on search_results.htm and save to a local variable
        workingtitles = get_titles_from_search_results('search_results.htm')
        # check that the number of titles extracted is correct (20 titles)
        self.assertEqual(len(workingtitles), 20)
        # check that the variable you saved after calling the function is a list
        self.assertEqual(type(workingtitles), list)
        # check that each item in the list is a tuple
        for anyentry in workingtitles:
            self.assertEqual(type(anyentry), tuple)
        # check that the first book and author tuple is correct (open search_results.htm and find it)
        self.assertEqual(workingtitles[0], ('Harry Potter and the Deathly Hallows (Harry Potter, #7)','J.K. Rowling'))
        # check that the last title is correct (open search_results.htm and find it)
        self.assertEqual(workingtitles[-1][0], 'Harry Potter: The Prequel (Harry Potter, #0.5)')

    def test_get_search_links(self):
        # check that TestCases.search_urls is a list
        self.assertEqual(type(self.search_urls), list)
        # check that the length of TestCases.search_urls is correct (10 URLs)
        self.assertEqual(len(self.search_urls), 10)
        for anyentry in self.search_urls:
            # check that each URL in the TestCases.search_urls is a string
            self.assertEqual(type(anyentry), str)
            # check that each URL contains the correct url for Goodreads.com followed by /book/show/
            self.assertTrue('www.goodreads.com/book/show/' in anyentry)

if __name__ == '__main__':
    print(extra_credit("extra_credit.htm"))
    unittest.main(verbosity=2)