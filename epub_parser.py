# This reads the table of contents built into all epubs to get the text organised into chapters.
# The function epub_to_chapters() returns a dictionary:
# {title: "Title of Book", words: [first_word, second_word, ...], chapters: [(chapter_title, starting index), ...] }
# (Eventually want to build this into a book dataclass instead.)
#
# How it works
# (1) We read the table of contents and see where entries point.
# (2) Use the book's spine to go through in reading order, collecting words (which have <p> tags).
# (3) Whenever we reach somewhere the TOC pointed at, note the number of words collected to get an index.

# Imports #
import ebooklib
from ebooklib import epub
from bs4 import BeautifulSoup
from pathlib import Path

# Config #
IGNORED_CLASSES = ["caption", "figcenter"]  # These deprecated HTML classes are used in Project Gutenberg epubs

# Functions #

# Returns a list of tuples (title, href) for every table of contents entry, taking account of nesting.
def get_toc_entries(toc_list):
    entries = []
    for entry in toc_list:
        if isinstance(entry, tuple):
            # Suppose the book is divided into parts with chapters: (part, [chapters])
            part, chapters = entry
            if part.href:
                 entries.append((part.title, part.href))
            entries.extend(get_toc_entries(chapters))  # The function calls itself on the chapters
        else:
            entries.append((entry.title, entry.href))
    return entries

# This ensures TOC and spine filenames are in the same format for comparison purposes, as they're written differently.
def just_the_filename(path):
    return path.split("/")[-1]

# This turns an epub into a dictionary containing the title, list of words, and list of chapters and chapter starts.
def epub_to_chapters(path_to_book):
    book = epub.read_epub(str(path_to_book))

    title_data = book.get_metadata("DC", "title")
    if title_data:
        title = title_data[0][0]
    else:
        title = Path(path_to_book).stem

    # Step 1: build a lookup of where each chapter starts.
    # Key: (filename, anchor). The anchor is "" when the chapter starts at the top of the file.
    chapter_starts = {}
    for chapter_title, href in get_toc_entries(book.toc):
        if "#" in href:
            file_part, anchor = href.split("#", 1)
        else:
            file_part, anchor = href, ""
        if not chapter_title:
            chapter_title = "Untitled"
        chapter_starts[(just_the_filename(file_part), anchor)] = chapter_title.strip()

    if not chapter_starts:
        print("  ! no table of contents found")

    # Step 2: walk the book in reading order, collecting words and noting chapter starts.
    words = []
    chapters = []
    for idref, linear in book.spine:
        item = book.get_item_with_id(idref)
        if item is None:
            print(f"  ! spine entry {idref} has no matching file, skipped")
            continue
        filename = just_the_filename(item.get_name())

        # Does a chapter start right at the top of this file?
        if (filename, "") in chapter_starts:
            chapters.append((chapter_starts[(filename, "")], len(words)))

        soup = BeautifulSoup(item.get_body_content(), "html.parser")
        for tag in soup.find_all(class_=IGNORED_CLASSES):
            tag.decompose()

        # find_all(True) gives every tag in the file, in the order they appear.
        for tag in soup.find_all(True):
            anchor = tag.get("id")
            if anchor and (filename, anchor) in chapter_starts:
                chapters.append((chapter_starts[(filename, anchor)], len(words)))
            if tag.name == "p":
                words.extend(tag.get_text().split())

    # Step 3: report anything the TOC pointed at that we never found.
    if len(chapters) < len(chapter_starts):
        print(f"  ! found {len(chapters)} of {len(chapter_starts)} TOC entries in the text")

    # Words before the first chapter (title page, licence, preface...) get a chapter of their
    # own so nothing is lost. If no chapters were found at all, this covers the whole book.
    if len(chapters) == 0 or chapters[0][1] > 0:
        chapters.insert(0, ("Front matter", 0))

    return {"title": title, "words": words, "chapters": chapters}

# Testing code which for each book prints a summary, plus the number, title and length of each chapter.
def describe(book_data):
    words = book_data["words"]
    chapters = book_data["chapters"]
    print(f"{book_data['title']}  |  {len(words)} words  |  {len(chapters)} chapters")

    for i in range(len(chapters)):
        chapter_title, start = chapters[i]
        if i + 1 < len(chapters):
            end = chapters[i + 1][1]  # this chapter ends where the next one starts
        else:
            end = len(words)  # the last chapter runs to the end of the book
        length = end - start
        first_words = " ".join(words[start:start + 8])
        note = "   <-- EMPTY" if length == 0 else ""
        print(f"  {i + 1:>3}. {chapter_title[:40]:<40} {length:>7} words | {first_words}{note}")

# Testing
if __name__ == "__main__":
    for path in sorted(Path("books").glob("*.epub")):
        print(f"\n=== {path.name} ===")
        try:
            describe(epub_to_chapters(path))
        except Exception as error:  # keep going: one broken book shouldn't stop the survey
            print(f"  ! failed: {type(error).__name__}: {error}")