# -*- coding: utf-8 -*-

import grokcore.view as grok
from zope.component import queryMultiAdapter
from zope.i18nmessageid import MessageFactory

from dolmen.content import IContainer
from dolmen.app.layout import models, ISortable
from menhir.library.tablesorter import SimpleTableSorter
from megrok.z3ctable import NameColumn, LinkColumn, ModifiedColumn

_ = MessageFactory("dolmen")


class FolderListing(models.TablePage, models.TabView):
    grok.name('base_view')
    grok.title(_(u"Content"))
    grok.context(IContainer)
    grok.implements(ISortable)
    grok.require('dolmen.content.List')
    
    batchSize = 20
    startBatchingAt = 20
    cssClasses = {'table': 'listing sortable'}
    cssClassEven = u'even'
    cssClassOdd = u'odd'
    sortOn = None
    
    @property
    def values(self):
        return self.context.values()

    def render(self):
        SimpleTableSorter.need()
        return self.renderTable()


class Title(LinkColumn):
    """Display the name of the content item
    """
    grok.name('folderlisting.title')
    grok.adapts(None, None, FolderListing)
    header = _(u"Title")

    def renderCell(self, item):
        title = LinkColumn.renderCell(self, item)
        iconview = queryMultiAdapter(
            (item, self.table.request),
            name = "contenttype_icon"
            )
        if icon is not None:
            return "%s&nbsp;%s" % (icon(), title)
        return title


class ModificationDate(ModifiedColumn):
    """Display the name of the content item
    """
    grok.name('folderlisting.modified')
    grok.adapts(None, None, FolderListing)
    weight = 1
    header = _(u"Modified")
