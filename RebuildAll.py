# -*- coding: utf-8 -*-
# See github page to report issues or to contribute:
# https://github.com/Arthaey/anki-rebuild-all
#
# Also available for Anki at https://ankiweb.net/shared/info/1639597619
#
# Contributors:
# - @Arthaey
# - @ankitest

import re
from anki.hooks import wrap
from aqt import mw
from aqt.deckbrowser import DeckBrowser
from aqt.utils import tooltip


def _updateFilteredDecks(actionFuncName):
    dynDeckIds = [ d["id"] for d in mw.col.decks.all() if d["dyn"] ]
    count = len(dynDeckIds)

    if not count:
        tooltip("No filtered decks found.")
        return

    # should be one of "rebuildDyn" or "emptyDyn"
    actionFunc = getattr(mw.col.sched, actionFuncName)

    mw.checkpoint("{0} {1} filtered decks".format(actionFuncName, count))
    mw.progress.start()
    [ actionFunc(did) for did in sorted(dynDeckIds) ]
    mw.progress.finish()
    tooltip("Updated {0} filtered decks.".format(count))

    mw.reset()


def _handleFilteredDeckButtons(self, url):
    if url in ["rebuildDyn", "emptyDyn"]:
        _updateFilteredDecks(url)


def _addButtons(self):
    # There's no clean way to add a button, so hack it in. :(
    newHtml = ""
    newButtons = [
        [_("Rebuild All"), "rebuildDyn"],
        [_("Empty All"),   "emptyDyn"],
    ]

    for newButton in newButtons:
        newHtml += "<button title='{0}' onclick='py.link(\"{1}\");'>{0}</button>".format(*newButton)

    html = self.bottom.web.page().mainFrame().toHtml()
    buttons = re.findall('<button.+</button>', html)
    self.bottom.draw(''.join(buttons) + newHtml)  


DeckBrowser._drawButtons = wrap(DeckBrowser._drawButtons, _addButtons, "after")
DeckBrowser._linkHandler = wrap(DeckBrowser._linkHandler, _handleFilteredDeckButtons, "after")
