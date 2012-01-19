# -*- coding: utf-8 -*-

import dolmen.menu
from cromlech.browser import slot
from dolmen.app.layout import master, menus
from dolmen.app.container import listing, addtofolder
from dolmen.app.security import permissions
from grokcore.security import require, order


class AddMenu(addtofolder.AddMenuViewlet):
    order(20)
    slot(master.AboveBody)
    require(permissions.CanAddContent)


@dolmen.menu.menuentry(menus.ContextualMenu)
class Listing(listing.ListingPage):
    order(50)
    require(permissions.CanListContent)
