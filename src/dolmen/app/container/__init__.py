# -*- coding: utf-8 -*-

from zope.i18nmessageid import MessageFactory
MF = MessageFactory("dolmen.app.container")

from dolmen.app.container.addtofolder import AddMenuViewlet
from dolmen.app.container.listing import FolderListing, ListingPage
from dolmen.app.container.namechoosers import (
    UUIDNameChooser, NormalizingNameChooser)
