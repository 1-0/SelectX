from selectx import _ as _
from selectx import QtGui as QtGui

__plugin_name__ = _(u'SelectX Find Dialog')
__plugin_menu_caption__ = _(u'SelectX Find Dialog')
__plugin_menu_key__ = 'F7'
__plugin_menu_help__ = _(u'SelectX Find Dialog')
__plugin_menu_icon__ = """edit-find"""
__plugin_name__ = _(u'SelectX Find Dialog')
__plugin_version__ = '0.0.4'
__plugin_about__ = _(u'Enter text to find:')

def __plugin_init__(self, params_list=[]):
    nnn = __plugin_name__+' '+__plugin_version__
    print nnn
    self.statusBar().showMessage(nnn)

def __plugin_run_function__(self):
    findText(self)

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
    
