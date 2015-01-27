#def _(s): return s
from gettext import gettext as _
#global _
#from .. import _

def __plugin_init__(self, gt, params_list=[]):
    global _
    _ = gt
    nnn = __plugin_name__+' '+__plugin_version__
    print nnn
    self.statusBar().showMessage(nnn)
__plugin_name__ = _(u'SelectX Find Dialog')
__plugin_version__ = '0.0.1'
__plugin_about__ = _(u'Enter text to find:')



def __plugin_run_function__(self):
    return findText

def findText(self):
    cursor = self.cWidget.edit.textCursor()
    textSelected = cursor.selectedText()
    text_find, find_ok = QtGui.QInputDialog.getText(self, \
    _(u'SelectX Find Dialog'), _(u'Enter text to find:'), QtGui.QLineEdit.Normal,  textSelected)
    if find_ok:
        if self.cWidget.edit.find(str(text_find)):
            self.statusBar().showMessage(_(u'Found: %s') % text_find)
            return
        else:
            self.statusBar().showMessage(_(u'Not found: %s') % text_find)
            return
        return
    self.statusBar().showMessage(_(u'Find Canceled'))
    
