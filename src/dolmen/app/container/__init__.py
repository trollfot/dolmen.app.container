# -*- coding: utf-8 -*-

from zope.i18nmessageid import MessageFactory
MF = MessageFactory("dolmen.app.container")

# base components that can be grokked via the components.zcml file loading.
from dolmen.app.container.addtofolder import AddMenuViewlet
from dolmen.app.container.namechoosers import NormalizingNameChooser
from dolmen.app.container.listing import FolderListing, ListingPage
