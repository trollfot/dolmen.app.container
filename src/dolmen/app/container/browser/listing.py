# -*- coding: utf-8 -*-

import grok
import megrok.resourcelibrary

from ZODB.broken import PersistentBroken
from zope.component import queryMultiAdapter
from zope.i18nmessageid import MessageFactory
from zope.security.management import checkPermission

from dolmen.app import layout
from dolmen.content import IContainer, IOrderedContainer
from menhir.library.tablesorter import SimpleTableSorter, TableDnD
from megrok.z3ctable import NameColumn, LinkColumn, ModifiedColumn

_ = MessageFactory("dolmen")
grok.templatedir("templates")


class ContainerOrderingLibrary(megrok.resourcelibrary.ResourceLibrary):
    megrok.resourcelibrary.depend(TableDnD)
    megrok.resourcelibrary.directory('resources')
    megrok.resourcelibrary.include('container.reorder.js')
    

class ContainerOrderingJSON(grok.JSON):
    grok.context(IOrderedContainer)
    grok.require('dolmen.content.Edit')
          
    def updateContainerOrder(self):       
        newOrder = self.request.get("newOrder")
        if not newOrder or not isinstance(newOrder, list):
            return
        
        keys = self.context.keys()
        
        order = []
        for item in newOrder:
            if item.startswith("id_"):
                id = int(item[3:])
                order.append(keys[id])

        self.context.updateOrder(order)


class FolderListing(layout.TablePage, layout.ContextualMenuEntry):
    grok.name('base_view')
    grok.title(_(u"Content"))
    grok.context(IContainer)
    grok.require('dolmen.content.List')
    
    batchSize = 20
    startBatchingAt = 20
    cssClassEven = u'even'
    cssClassOdd = u'odd'
    sortOn = None
    
    @property
    def values(self):
        return self.context.values()

    def update(self):
        SimpleTableSorter.need()
        self.cssClasses = {'table': 'listing sortable'}
        layout.TablePage.update(self)
        self.table = self.renderTable()


class OrderedFolderListing(FolderListing):
    grok.name('base_view')
    grok.title(_(u"Content"))
    grok.context(IOrderedContainer)
    
    def update(self):
        if checkPermission("dolmen.content.Edit", self.context):
            ContainerOrderingLibrary.need()
            self.cssClasses = {'table': 'listing orderable'}
        else:
            SimpleTableSorter.need()
            self.cssClasses = {'table': 'listing sortable'}

        layout.TablePage.update(self)
        self.table = self.renderTable()


class Title(LinkColumn):
    """Display the name of the content item
    """
    grok.name('folderlisting.title')
    grok.adapts(None, None, FolderListing)
    header = _(u"Title")

    def renderCell(self, item):
        if isinstance(item, PersistentBroken):
            return "Broken item: " + item.__Broken_state__.get('__name__')
        
        title = LinkColumn.renderCell(self, item)
        iconview = queryMultiAdapter(
            (item, self.table.request),
            name = "contenttype_icon"
            )
        if iconview is not None:
            return "%s&nbsp;%s" % (iconview(), title)
        return title


class ModificationDate(ModifiedColumn):
    """Display the name of the content item
    """
    grok.name('folderlisting.modified')
    grok.adapts(None, None, FolderListing)
    weight = 1
    header = _(u"Modified")
