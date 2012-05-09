# -*- coding: utf-8 -*-

from cromlech.browser import IRenderable
from dolmen.app.container import MF as _
from dolmen.forms.base import Fields
from dolmen.forms.table import BaseTable
from grokcore.component import title
from zope.i18n import translate
from zope.interface import implements
from zope.location.interfaces import ILocation


class FolderListing(BaseTable):
    title(u"Content")

    css_class = "listing sortable"

    fields = Fields(ILocation).omit('__parent__')
    fields['__name__'].mode = 'link'

    @property
    def title(self):
        return u"<h1>%s</h1>" % translate(
            _(u'Folder contents'), context=self.request)


class ListingRenderer(object):
    implements(IRenderable)

    def __init__(self, context, request):
        self.context = context
        self.request = request

    def update(self):
        self.table = FolderListing(self.context, self.request)
        self.table.update()

    def render(self):
        return self.table.render()
