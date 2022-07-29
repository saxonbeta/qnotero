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

from libqnotero.qt.QtGui import QStyledItemDelegate, QStyle, QTextDocument
from libqnotero.qt.QtGui import QFont, QFontMetrics, QAbstractTextDocumentLayout
from libqnotero.qt.QtCore import Qt, QRect, QSize
from libzotero.zotero_item import cache as zoteroCache


class QnoteroItemDelegate(QStyledItemDelegate):

	"""Draws pretty result items"""

	def __init__(self, qnotero):

		"""
		Constructor

		Arguments:
		qnotero -- a Qnotero instance
		"""

		QStyledItemDelegate.__init__(self, qnotero)
		self.qnotero = qnotero
		self.boldFont = QFont()
		self.boldFont.setBold(True)
		self.regularFont = QFont()
		self.italicFont = QFont()
		self.italicFont.setItalic(True)
		self.tagFont = QFont()
		self.tagFont.setBold(True)
		self.tagFont.setPointSize(self.boldFont.pointSize() - 2)
		self.dy = int(QFontMetrics(self.boldFont) \
			.size(Qt.TextSingleLine, u"Dummy").height() \
			*self.qnotero.theme.lineHeight())
		self.margin = int(self.dy/2)
		self._margin = int(self.dy/10)
		self.height = int(5*self.dy+self._margin)
		self.noPdfPixmap = self.qnotero.theme.pixmap(u"nopdf")
		self.pdfPixmap = self.qnotero.theme.pixmap(u"pdf")
		self.aboutPixmap = self.qnotero.theme.pixmap(u"about")
		self.notePixmap = self.qnotero.theme.pixmap(u"note")
		self.pixmapSize = int(self.pdfPixmap.height()+self.dy/2)
		self.roundness = self.qnotero.theme.roundness()

	def sizeHint(self, option, index):

		"""
		Suggest a size for the widget

		Arguments:
		option -- a QStyleOptionView
		index -- a QModelIndex

		Returns:
		A QSize
		"""

		return QSize(0, self.height)

	def paint(self, painter, option, index):

		"""
		Draws the widget

		Arguments:
		painter -- a QPainter
		option -- a QStyleOptionView
		index -- a QModelIndex
		"""

		# Retrieve the data
		model = index.model()
		record = model.data(index)
		text = record
		zoteroItem = zoteroCache[text]

		if zoteroItem.fulltext is None:
			pixmap = self.noPdfPixmap
		else:
			pixmap = self.pdfPixmap

		# Choose the colors
		self.palette = self.qnotero.ui.listWidgetResults.palette()
		if option.state & QStyle.State_MouseOver:
			background = self.palette.Highlight
			foreground = self.palette.HighlightedText
			_note = zoteroItem.get_note()
			if _note is not None:
				self.qnotero.showNoteHint()
			else:
				self.qnotero.hideNoteHint()

		elif option.state & QStyle.State_Selected:
			background = self.palette.Dark
			foreground = self.palette.WindowText
		else:
			background = self.palette.Base
			foreground = self.palette.WindowText

		# Draw the frame
		_rect = option.rect.adjusted(self._margin, self._margin,
			- int(2*self._margin), -self._margin)
		pen = painter.pen()
		pen.setColor(self.palette.color(background))
		painter.setPen(pen)
		painter.setBrush(self.palette.brush(background))
		painter.drawRoundedRect(_rect, self.roundness, self.roundness)
		font = painter.font
		pen = painter.pen()
		pen.setColor(self.palette.color(foreground))
		painter.setPen(pen)

		# Draw icon
		_rect = QRect(option.rect)
		_rect.moveBottom(int(_rect.bottom() + self.dy/2))
		_rect.moveLeft(int(_rect.left() + self.dy/2))
		_rect.setHeight(self.pixmapSize)
		_rect.setWidth(self.pixmapSize)
		painter.drawPixmap(_rect, pixmap)

		# Draw the text
		painter.save()
		_rect = option.rect.adjusted(int(self.pixmapSize+self.dy/2), int(self.dy/2),
									 -self.dy, 0)

		f = [self.tagFont, self.italicFont, self.regularFont,
			 self.boldFont]
		itemText = zoteroItem.full_formatHTML()
		textRenderer = QTextDocument()
		context = QAbstractTextDocumentLayout.PaintContext()
		textRenderer.setHtml(itemText)
		painter.translate(_rect.topLeft())
		textRenderer.documentLayout().draw(painter, context)
		_rect = _rect.adjusted(0, self.dy, 0, 0)
		painter.restore()

