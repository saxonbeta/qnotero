#-*- coding:utf-8 -*-

#  This file is part of Qnotero.
#
#      Qnotero is free software: you can redistribute it and/or modify
#      it under the terms of the GNU General Public License as published by
#      the Free Software Foundation, either version 3 of the License, or
#      (at your option) any later version.
#
#      Qnotero is distributed in the hope that it will be useful,
#      but WITHOUT ANY WARRANTY; without even the implied warranty of
#      MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#      GNU General Public License for more details.
#
#      You should have received a copy of the GNU General Public License
#      along with Qnotero.  If not, see <https://www.gnu.org/licenses/>.
#      Copyright (c) 2019 E. Albiter

#

term_collection = None, u"collection"
term_tag = None, u"tag"
term_author = None, u"author"
term_editor = None, u"editor"
term_date = None, u"date", u"year"
term_publication = None, u"publication", u"journal"
term_title = None, u"title"
term_doi = None, u"doi"
term_abstract = None, u'abs'

cache = {}


class zoteroItem(object):

    """Represents a single zotero item."""

    def __init__(self, item=None, noteProvider=None):

        """
        Constructor.

        Keyword arguments:
        item			--	A `dict` with item information, or an `int` with the
                            item id	. (default=None)
        noteProvider	--	A noteProvider object. (default=None)
        """

        self.gnotero_format_str = None
        self.html_format_str = None
        self.simple_format_str = None
        self.filename_format_str = None
        self.collection_color = u"#000000"
        self.noteProvider = noteProvider
        self.note = -1
        if isinstance(item, dict):
            # TODO: Add the information like bookTitle, programTitle, etc. It seems that this code is not used
            # anywhere
            if u"item_id" in item:
                self.id = item[u"item_id"]
            else:
                self.id = None
            if u"publicationTitle" in item:
                self.publication = item[u"publicationTitle"]
            else:
                self.publication = None
            if u"title" in item:
                self.title = item[u"title"]
            else:
                self.title = None
            if u"author" in item:
                self.authors = item[u"author"]
            else:
                self.authors = []
            if u"editor" in item:
                self.editors = item[u"editor"]
            else:
                self.editors = None
            if u"date" in item:
                self.date = item[u"date"]
            else:
                self.date = None
            if u"issue" in item:
                self.issue = item[u"issue"]
            else:
                self.issue = None
            if u"volume" in item:
                self.volume = item[u"volume"]
            else:
                self.volume = None
            if u"fulltext" in item:
                self.fulltext = item[u"fulltext"]
            else:
                self.fulltext = []
            if u"collections" in item:
                self.collections = item[u"collections"]
            else:
                self.collections = []
            if u"tags" in item:
                self.tags = item[u"tags"]
            else:
                self.tags = []
            if u"key" in item:
                self.key = item[u"key"]
            else:
                self.key = None
            if u'DOI' in item:
                self.doi = item[u'DOI']
            else:
                self.doi = None
            if u'url' in item:
                self.url = item[u'url']
            else:
                self.url = None
            if u'abstractNote' in item[u'abstractNote']:
                self.abstract = item[u'abstractNote']
            else:
                self.abstract = item[u'abstractNote']
        else:
            self.title = None
            self.collections = []
            self.publication = None
            self.authors = []
            self.editors = []
            self.tags = []
            self.issue = None
            self.volume = None
            self.fulltext = []
            self.date = None
            self.key = None
            self.doi = None
            self.abstract = None
            self.url = None
            if isinstance(item, int):
                self.id = item
            else:
                self.id = None

    def match(self, terms):

        """
        Matches the current item against a term.

        Arguments:
        terms	--	A list of (term_type, term) tuples.

        Returns:
        True if the current item matches the terms, False otherwise.
        """

        global term_collection, term_author, term_title, term_date, \
            term_publication, term_tag
        # Nothing to search
        if len(terms) == 0:
            return False
        # Walk through all search terms
        for term_type, term in terms:
            match = False
            # Do at least one criteria match?
            if term_type in term_tag:
                for tag in self.tags:
                    if term in tag.lower():
                        match = True
            if term_type in term_collection:
                for collection in self.collections:
                    if term in collection.lower():
                        match = True
            if not match and term_type in term_author:
                for author in self.authors:
                    if term in author.lower():
                        match = True
            if not match and term_type in term_editor:
                for editor in self.editors:
                    if term in editor.lower():
                        match = True
            if not match and self.date is not None and term_type in term_date:
                if term in self.date:
                    match = True
            if not match and self.title is not None and term_type in \
                    term_title and term in self.title.lower():
                match = True
            if not match and self.publication is not None and term_type in \
                    term_publication and term in self.publication.lower():
                match = True
            if not match and self.doi is not None and term_type in \
                    term_doi and term in self.doi.lower():
                match = True
            if not match and self.abstract is not None and term_type in \
                    term_abstract and term in self.abstract.lower():
                match = True
            # If not return false, otherwise continue
            if not match:
                return False
        # If we reach this code, all the criteria matched
        return True

    def get_note(self):

        """
        Retrieves a note.

        Returns:
        A note for the current item.
        """

        if self.note != -1:
            return self.note
        # Return None if noteProvider is not defined
        if self.noteProvider is not None:
            self.note = self.noteProvider.search(self)
            return self.note
        else:
            return None

    def format_author(self):

        """
        Returns:
        A pretty representation of the author.
        """

        if not self.authors:
            return u"Unknown author"
        elif len(self.authors) >= 3:
            return u"%s et al." % self.authors[0]
        elif len(self.authors) == 2:
            return self.authors[0] + u" & " + self.authors[1]
        else:
            return self.authors[0]

    def format_date(self):

        """
        Returns:
        A pretty representation of the date.
        """

        if self.date is None:
            return u"(Date unknown)"

        return u"(%s)" % self.date

    def format_title(self):

        """
        Returns:
        A pretty representation of the title.
        """

        if self.title is None:
            return u"Unknown title"
        return self.title

    def format_publication(self):

        """
        Returns:
        A pretty representation of the publication (journal).
        """

        if self.publication is None:
            return u"Unknown journal"
        return self.publication

    def format_tags(self):

        """
        Returns:
        A pretty representation of the tags.
        """

        return u", ".join(self.tags)

    def gnotero_format(self):

        """
        Returns:
        A pretty apa-like representation of the item, which can be used as a
        label in Qnotero.
        """

        if self.gnotero_format_str is None:
            s =  u"<b>" + self.format_author() + u" " + self.format_date() + \
                u"</b>"
            if self.title is not None:
                s += u"\n<small>" + self.title
            if self.publication is not None:
                s += u"\n<i>" + self.publication
                if self.volume is not None:
                    s += u", %s" % self.volume
                s += u"</i>"
                if self.issue is not None:
                    s += u"(%s)" % self.issue
            s += u"</small>"
            self.gnotero_format_str = s.replace(u"&", u"&amp;")
        return self.gnotero_format_str

    def author_date_format(self):
        """

        :return: String containing the author(s) and publication date
        """
        return self.format_author() + u" " + self.format_date()

    def full_format(self):

        """
        Returns:
        A pretty, extensive representation of the current item.
        """

        if self.gnotero_format_str is None:
            s = self.author_date_format()
            if self.title is not None:
                s += u"\n" + self.title
            if self.publication is not None:
                s += u"\n" + self.publication
                if self.volume is not None:
                    s += u", %s" % self.volume
                if self.issue is not None:
                    s += u"(%s)" % self.issue
            else:
                s += u"\n"
            if self.tags is not None:
                s += u"\n" + self.format_tags()
            self.gnotero_format_str = s
        return self.gnotero_format_str

    def full_formatHTML(self):

        """
        Returns:
        A pretty, extensive representation of the current item in HTML format
        """
        if self.html_format_str is None:
            s = u"<b>"
            s += self.author_date_format() + u"</b>"
            if self.title is not None:
                s += u"<br/>" + self.title
            if self.publication is not None:
                s += u"<br/><i>" + self.publication + u"</i>"
                if self.volume is not None:
                    s += u", %s" % self.volume
                    if self.issue is not None:
                        s += u"(%s)" % self.issue
            else:
                s += u"<br/>"
            if self.tags is not None:
                s += u"<br/><b><small>" + self.format_tags() + u"</small></b>"
            self.html_format_str = s
        return self.html_format_str

    def simple_format(self):

        """
        Returns:
        A pretty, simple representation of the current item.
        """

        if self.simple_format_str is None:
            self.simple_format_str = self.format_author() + u" " + \
                self.format_date()
        return self.simple_format_str

    def filename_format(self):

        """
        Returns:
        A pretty filename format representation of the current item.
        """

        if self.filename_format_str is None:
            self.filename_format_str = self.format_author() + u" " + \
                self.format_date().replace(u"\\", u"")
        return self.filename_format_str

    def hashKey(self):

        """
        Returns:
        A hash representation of the current object.
        """

        global cache
        hashKey = str(self)
        cache[hashKey] = self
        return hashKey
