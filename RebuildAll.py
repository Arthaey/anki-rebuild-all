# -*- coding: utf-8 -*-
# See github page to report issues or to contribute:
# https://github.com/Arthaey/anki-rebuild-all
#
# Also available for Anki at https://ankiweb.net/shared/info/1639597619
from __future__ import unicode_literals

import anki
import aqt
from aqt.qt import *
from aqt import mw


def _rebuildAllDecks():
    dynDeckIds = [d["id"] for d in mw.col.decks.all() if d["dyn"]]
    if not len(dynDeckIds):
        aqt.utils.tooltip('Filtered decks are not found')
        return
    mw.checkpoint("rebuild {0} decks".format(len(dynDeckIds)))
    mw.progress.start()
    [mw.col.sched.rebuildDyn(did) for did in dynDeckIds]
    mw.progress.finish()
    aqt.utils.tooltip('Rebuild All Filtered Decks <b>done.</b>')
    mw.reset()


def _emptyAllDecks():
    dynDeckIds = [d["id"] for d in mw.col.decks.all() if d["dyn"]]
    if not len(dynDeckIds):
        aqt.utils.tooltip('Filtered decks were not found')
        return
    mw.checkpoint("empty {0} decks".format(len(dynDeckIds)))
    mw.progress.start()
    [mw.col.sched.emptyDyn(did) for did in dynDeckIds]
    mw.progress.finish()
    aqt.utils.tooltip('Empty All Filtered Decks <b>done.</b>')
    mw.reset()


def _rebuildAll(self, url):
    if url == "rebuildAll":
        _rebuildAllDecks()
    if url == "emptyAll":
        _emptyAllDecks()

aqt.deckbrowser.DeckBrowser._linkHandler = anki.hooks.wrap(
    aqt.deckbrowser.DeckBrowser._linkHandler, _rebuildAll, "after")


def _drawButtons(self):
    links = [
        ["", "shared", _("Get Shared")],
        ["", "create", _("Create Deck")],
        ["", "import", _("Import File")],  # Ctrl+I works from menu
        ['', "rebuildAll", _("Rebuild") + ' ' + _("All")],
        ['', "emptyAll", _("Empty") + ' ' + _("All")],
    ]
    buf = ""
    for b in links:
        buf += """
<button title='%s' onclick='py.link(\"%s\");'>%s</button>""" % tuple(b)
    self.bottom.draw(buf)
    if anki.utils.isMac:
        size = 28
    else:
        size = 36 + self.mw.fontHeightDelta*3
    self.bottom.web.setFixedHeight(size)
    self.bottom.web.setLinkHandler(self._linkHandler)

aqt.deckbrowser.DeckBrowser._drawButtons = _drawButtons  # NB! Monkey Patch

#
