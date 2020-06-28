# -*- coding:utf-8 -*-

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

import sqlite3
import os
import os.path
import shutil
import sys
import time
from libqnotero.config import getConfig
from libzotero.zotero_item import zoteroItem as zotero_item

term_index = {u"collection", u"tag", u"author", u"editor",
              u"date", u"year", u"publication", u"journal",
              u"title", u"doi", u'abs'}


def parse_query(query):

    """
    Parses a text search query into a list of tuples, which are acceptable
    for zotero_item.match().

    Argument:
    query		--	A search query.

    Returns:
    A list of tuples.
    """

    # To search in a specific field now the syntax is  author:doe
    # or author: doe

    # Make sure that spaces are handled correctly after
    # colon. E.g., author: doe
    while u": " in query:
        query = query.replace(u": ", u":")
    # Parse the terms into a suitable format
    items = []
    for item in query.strip().lower().split():
        s = item.split(u":")
        # Check if the criterium is type-specified
        if len(s) == 2 and s[0].lower() in term_index:
            # Check if the query is not empty
            if s[1] != "":
                # A query like "author:doe" or "author: doe
                items.append((s[0], s[1]))
            else:
                # An empty field search ("author: "), just ignore it
                continue
        else:
            # A query with a colon or a simple query.
            for subitem in s:
                if subitem != u"":
                    items.append((None, subitem.strip()))
    return items


def valid_location(path):
    """
	Checks if a given path is a valid Zotero folder, i.e., if it it contains
	zotero.sqlite.

	Arguments:
	path		--	The path to check.

	Returns:
	True if path is a valid Zotero folder, False otherwise.
	"""

    assert (isinstance(path, str))
    return os.path.exists(os.path.join(path, u"zotero.sqlite"))


class LibZotero(object):
    """
	Libzotero provides access to the zotero database.
	This is an object oriented reimplementation of the
	original zoterotools.
	"""

    attachment_query = u"""
		select items.itemID, itemAttachments.path, itemAttachments.itemID
		from items, itemAttachments
		where items.itemID = itemAttachments.parentItemID
		"""

    info_query = u"""
    		select items.itemID, items.itemTypeID, fields.fieldName, itemDataValues.value, items.key
    		from items, itemData, fields, itemDataValues
    		where
    			items.itemID = itemData.itemID
    			and itemData.fieldID = fields.fieldID
    			and itemData.valueID = itemDataValues.valueID
    			and (fields.fieldName = "date"
    			    or fields.fieldName = "title"
    				or fields.fieldName = "publicationTitle"
    				or fields.fieldName = "programTitle"
    				or fields.fieldName = "websiteTitle"
    				or fields.fieldName = "proceedingsTitle"
    				or fields.fieldName = "forumTitle"
    				or fields.fieldName = "encyclopediaTitle"
    				or fields.fieldName = "dictionaryTitle"
    				or fields.fieldName = "bookTitle"
    				or fields.fieldName = "blogTitle"
    				or fields.fieldName = "subject"
    				or fields.fieldName = "url"
    				or fields.fieldName = "abstractNote"
    				or fields.fieldName = "DOI"
    				or fields.fieldName = "volume"
    				or fields.fieldName = "issue")
    		"""

    author_query = u"""
		select items.itemID, creators.lastName
		from items, itemCreators, creators, creatorTypes
		where
			items.itemID = itemCreators.itemID
			and itemCreators.creatorID = creators.creatorID
			and itemCreators.creatorTypeID = creatorTypes.creatorTypeID
			and creatorTypes.creatorType = "author"
		order by itemCreators.orderIndex
		"""

    editor_query = u"""
    		select items.itemID, creators.lastName
    		from items, itemCreators, creators, creatorTypes
    		where
    			items.itemID = itemCreators.itemID
    			and itemCreators.creatorID = creators.creatorID
    			and itemCreators.creatorTypeID = creatorTypes.creatorTypeID
    			and creatorTypes.creatorType = "editor"
    		order by itemCreators.orderIndex
    		"""

    collection_query = u"""
		select items.itemID, collections.collectionName
		from items, collections, collectionItems
		where
			items.itemID = collectionItems.itemID
			and collections.collectionID = collectionItems.collectionID
		order by collections.collectionName != "To Read",
			collections.collectionName
		"""

    tag_query = u"""
		select items.itemID, tags.name
		from items, tags, itemTags
		where
			items.itemID = itemTags.itemID
			and tags.tagID = itemTags.tagID
		"""

    deleted_query = u"select itemID from deletedItems"

    retracted_query = u"select itemID from retractedItems"

    attachmentid_query = u"""select itemTypes.itemTypeID from itemTypes 
                             where itemTypes.typeName = "attachment"
                             """

    def __init__(self, zotero_path, noteProvider=None):

        """
		Intialize libzotero.

		Arguments:
		zotero_path		--	A string to the Zotero folder.

		Keyword arguments:
		noteProvider	--	A noteProvider object. (default=None)
		"""

        assert (isinstance(zotero_path, str))
        print(u"libzotero.__init__(): zotero_path = %s" % bytes(zotero_path,
                                                                'utf-8'))
        # Set paths
        self.zotero_path = zotero_path
        self.storage_path = os.path.join(self.zotero_path, u"storage")
        self.zotero_database = os.path.join(self.zotero_path, u"zotero.sqlite")
        self.noteProvider = noteProvider
        if os.name == u"nt":
            home_folder = os.environ[u"USERPROFILE"]
        elif os.name == u"posix":
            home_folder = os.environ[u"HOME"]
        else:
            print(u"libzotero.__init__(): you appear to be running an unsupported OS")

        self.gnotero_database = os.path.join(home_folder, u".gnotero.sqlite")
        # Remember search results so results speed up over time
        self.search_cache = {}
        # Check whether verbosity is turned on
        self.verbose = "-v" in sys.argv
        # These dates are treated as special and are not parsed into a year
        # representation
        self.special_dates = u"in press", u"submitted", u"in preparation", \
                             u"unpublished"
        # These extensions are recognized as fulltext attachments
        self.attachment_ext = u".pdf", u"epub", u'djvu', u'html'

        self.index = {}
        self.collection_index = []
        self.tag_index = []
        self.last_update = None

        # The notry parameter can be used to show errors which would
        # otherwise be obscured by the try clause
        if "--notry" in sys.argv:
            self.search(u"dummy")

        # Start by updating the database
        try:
            self.search(u"dummy")
            self.error = False
        except Exception as e:
            print(e)
            self.error = True

    def update(self, force=False):

        """
		Checks if the local copy of the zotero database is up to date. If not,
		the data is also indexed.

		Arguments:
		force		--	Indicates that the data should also be indexed, even
						if the local copy is up to date. (default=False)
		"""

        try:
            stats = os.stat(self.zotero_database)
        except Exception as e:
            print(u"libzotero.update(): %s" % e)
            return False

        # Only update if necessary
        if force or self.last_update is None or stats[8] > self.last_update:
            t = time.time()
            self.last_update = stats[8]
            self.index = {}
            self.collection_index = []
            self.search_cache = {}
            # Copy the zotero database to the gnotero copy
            shutil.copyfile(self.zotero_database, self.gnotero_database)
            self.conn = sqlite3.connect(self.gnotero_database)
            self.cur = self.conn.cursor()
            # First create a list of deleted items, so we can ignore those later
            deleted = []
            self.cur.execute(self.deleted_query)
            for item in self.cur.fetchall():
                deleted.append(item[0])
            # Then create a list of retracted item to ignore them too
            retracted = []
            self.cur.execute(self.retracted_query)
            for item in self.cur.fetchall():
                retracted.append(item[0])
            # Retrieve the attachment ID
            self.cur.execute(self.attachmentid_query)
            item = self.cur.fetchone()
            attachmentid = item[0]
            # Retrieve information about date, publication, volume, issue, DOI,
            # title, and abstract.
            self.cur.execute(self.info_query)
            for item in self.cur.fetchall():
                # If the item is marked as attachment just continue to the next one
                if item[1] == attachmentid:
                    continue
                item_id = item[0]
                key = item[4]
                if item_id not in deleted and item_id not in retracted:
                    item_name = item[2]
                    # Parse date fields, because we only want a year or a
                    # 'special' date
                    if item_name == u"date":
                        item_value = None
                        for sd in self.special_dates:
                            if sd in item[3].lower():
                                item_value = sd
                                break
                        item_value = item[3][0:4]
                    else:
                        item_value = item[3]
                    if item_id not in self.index:
                        self.index[item_id] = zotero_item(item_id,
                                                          noteProvider=self.noteProvider)
                        self.index[item_id].key = key
                    # Not all items have the publicationTitle field
                    if item_name == u"publicationTitle" or item_name == u"bookTitle"\
                            or item_name == u"blogTitle" or item_name == u"encyclopediaTitle"\
                            or item_name == u"proceedingsTitle" or item_name == u"programTitle"\
                            or item_name == u"dictionaryTitle":
                        self.index[item_id].publication = str(item_value)
                    elif item_name == u"date":
                        self.index[item_id].date = item_value
                    elif item_name == u"volume":
                        self.index[item_id].volume = item_value
                    elif item_name == u"issue":
                        self.index[item_id].issue = item_value
                    elif item_name == u"DOI":
                        self.index[item_id].doi = item_value
                        # subject corresponds to the email title
                    elif item_name == u"title" or item_name == u"subject":
                        self.index[item_id].title = str(item_value)
                    elif item_name == u'url':
                        self.index[item_id].url = item_value
                    elif item_name == u'abstractNote':
                        self.index[item_id].abstract = item_value
            # Retrieve author information
            self.cur.execute(self.author_query)
            for item in self.cur.fetchall():
                item_id = item[0]
                if item_id not in deleted and item_id not in retracted:
                    item_author = item[1].title()
                    if item_id not in self.index:
                        self.index[item_id] = zotero_item(item_id)
                    self.index[item_id].authors.append(item_author)
            # Retrieve editor information
            self.cur.execute(self.editor_query)
            for item in self.cur.fetchall():
                item_id = item[0]
                if item_id not in deleted and item_id not in retracted:
                    item_editor = item[1].title()
                    if item_id not in self.index:
                        self.index[item_id] = zotero_item(item_id)
                    self.index[item_id].editors.append(item_editor)
            # Retrieve collection information
            self.cur.execute(self.collection_query)
            for item in self.cur.fetchall():
                item_id = item[0]
                if item_id not in deleted and item_id not in retracted:
                    item_collection = item[1]
                    if item_id not in self.index:
                        self.index[item_id] = zotero_item(item_id)
                    self.index[item_id].collections.append(item_collection)
                    if item_collection not in self.collection_index:
                        self.collection_index.append(item_collection)
            # Retrieve tag information
            self.cur.execute(self.tag_query)
            for item in self.cur.fetchall():
                item_id = item[0]
                # Only add tags for existing entries in the index
                if item_id in self.index:
                    item_tag = item[1]
                    self.index[item_id].tags.append(item_tag)
                    if item_tag not in self.tag_index:
                        self.tag_index.append(item_tag)
            # Retrieve attachments
            self.cur.execute(self.attachment_query)
            for item in self.cur.fetchall():
                item_id = item[0]
                if item_id not in deleted and item_id not in retracted:
                    if item[1] is not None:
                        att = item[1]
                        # If the attachment is stored in the Zotero folder, it is preceded
                        # by "storage:"
                        if att[:8] == u"storage:":
                            item_attachment = att[8:]
                            attachment_id = item[2]
                            if item_attachment[-4:].lower() in \
                                    self.attachment_ext:
                                if item_id not in self.index:
                                    self.index[item_id] = zotero_item(item_id)
                                self.cur.execute(
                                    u"select items.key from items where itemID = %d"
                                    % attachment_id)
                                key = self.cur.fetchone()[0]
                                self.index[item_id].fulltext.append(os.path.join(
                                    self.storage_path, key, item_attachment))
                        # If the attachment is linked, it is simply the full
                        # path to the attachment
                        else:
                            self.index[item_id].fulltext.append(att)
            self.cur.close()
            print(u"libzotero.update(): indexing completed in %.3fs"
                  % (time.time() - t))
            print(u"%s entries processed" % len(self.index))
        return True

    def search(self, query):

        """
		Searches the zotero database.

		Argument:
		query		--	A search query.

		Returns:
		A list of zotero_items.
		"""

        if not self.update():
            return []
        if query in self.search_cache:
            print(u"libzotero.search(): retrieving results for '%s' from cache"
                  % query)
            return self.search_cache[query]
        t = time.time()
        terms = parse_query(query)
        if len(terms) == 0:
            return []
        results = []
        for item_id, item in self.index.items():
            if item.match(terms):
                results.append(item)
        self.search_cache[query] = results
        print(u"libzotero.search(): search for '%s' completed in %.3fs" %
              (query, time.time() - t))
        return results

