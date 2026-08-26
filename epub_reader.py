# This will eventually feed to get_word() in reader.py.
# Right now I am focussing on just getting the text out of Pride and Prejudice in the form of a list of words.
# This needs some extra chapter navigation to be really usable as currently the first several hundred "words" will be
# the introduction and possibly bits of the table of contents.
# Interestingly it's not even capturing all of the introduction which is somewhat perplexing and concerning.

# Imports #
import ebooklib
from ebooklib import epub
from bs4 import BeautifulSoup

# Functions #
# This function takes html data items and uses BeautifulSoup to grab text from them.
def xhtml_to_paragraphs(item):
    soup = BeautifulSoup(item.get_body_content(), "html.parser")
    for tag in soup.find_all(class_="caption"):
        tag.decompose()
    text = [para.get_text() for para in soup.find_all("p")]
    return text

# This turns an epub into a single list of words, which I am going to have to tear down and rebuild with
# -> chapter navigation.
def epub_to_words(path_to_book):
    book = epub.read_epub(path_to_book)
    words = []
    for item in book.get_items_of_type(ebooklib.ITEM_DOCUMENT):
        for para in xhtml_to_paragraphs(item):
            words.extend(para.split())
    return words

print(epub_to_words("books/test-pride-and-prejudice.epub"))