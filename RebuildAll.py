# -*- coding: utf-8 -*-
# See github page to report issues or to contribute:
# https://github.com/Arthaey/anki-rebuild-all
#
# Also available for Anki at https://ankiweb.net/shared/info/1639597619

import re
from anki.hooks import wrap
from aqt.deckbrowser import DeckBrowser

def _rebuildAll(self, url):
    if url == "rebuild":
        mw = self.mw
        dynDeckIds = [ d["id"] for d in mw.col.decks.all() if d["dyn"] ]
        mw.checkpoint("rebuild {0} decks".format(len(dynDeckIds)))
        mw.progress.start()
        [ mw.col.sched.rebuildDyn(did) for did in sorted(dynDeckIds) ]
        mw.progress.finish()
        mw.reset()

def _addButton(self):
    # There's no clean way to add a button, so hack it in. :(
    button = "<button title='Rebuild All' onclick='py.link(\"rebuild\");'>Rebuild All</button>"
    html = self.bottom.web.page().mainFrame().toHtml()
    html = re.sub("</button></td>", u"</button>{0}</td>".format(button), html)
    self.bottom.draw(html)

DeckBrowser._drawButtons = wrap(DeckBrowser._drawButtons, _addButton, "after")
DeckBrowser._linkHandler = wrap(DeckBrowser._linkHandler, _rebuildAll, "after")
