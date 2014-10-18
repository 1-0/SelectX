#!/usr/bin/env python
'''SelectX - easy eXtable text editor for developers writed on Python. Licensed by GPL3.'''

import sys #, getopt
import os
from PyQt4 import QtGui, QtCore
#from PyQt4.QtCore import QString
from PyQt4.QtGui import QIcon


__version__ = '''0.2.6'''
KEYS_HELP = '''Keypresses:  Action:
Backspace  Deletes the character to the left of the cursor.
Delete     Deletes the character to the right of the cursor.
Ctrl+C     Copy the selected text to the clipboard.
Ctrl+Insert    Copy the selected text to the clipboard.
Ctrl+K     Deletes to the end of the line.
Ctrl+V     Pastes the clipboard text into text edit.
Shift+Insert   Pastes the clipboard text into text edit.
Ctrl+X     Deletes the selected text and copies it to the clipboard.
Shift+Delete   Deletes the selected text and copies it to the clipboard.
Ctrl+Z     Undoes the last operation.
Ctrl+Y     Redoes the last operation.
LeftArrow  Moves the cursor one character to the left.
Ctrl+LeftArrow     Moves the cursor one word to the left.
RightArrow     Moves the cursor one character to the right.
Ctrl+RightArrow    Moves the cursor one word to the right.
UpArrow    Moves the cursor one line up.
Ctrl+UpArrow   Moves the cursor one word up.
DownArrow  Moves the cursor one line down.
Ctrl+Down Arrow    Moves the cursor one word down.
PageUp     Moves the cursor one page up.
PageDown   Moves the cursor one page down.
Home   Moves the cursor to the beginning of the line.
Ctrl+Home  Moves the cursor to the beginning of the text.
End    Moves the cursor to the end of the line.
Ctrl+End   Moves the cursor to the end of the text.
Alt+Wheel  Scrolls the page horizontally (the Wheel is the mouse wheel).
Ctrl+Wheel     Zooms the text.'''

CONSOLE_USAGE = '''
[KEY]...[FILE]
Keys:
-h, --help                  Print this help message
--version                   Print version info
'''

VERSION_INFO = "SelectX. Text editor licenced by GPL3. Ver. %s"



class SelectX(QtGui.QMainWindow):

    def __init__(self):
        super(SelectX, self).__init__()
        self.zoomRate = 0
        self.path=None
        self.initUI()
        
        try:
            if len(sys.argv)<3:
                print 'Try Open This File -> %s' % sys.argv[1]
                self.openExistFile(sys.argv[1])
            else:
                print 'Too many args'
                print CONSOLE_USAGE
        except IndexError:
            #print 'not open File'
            pass
    
    def initUI(self):
        
        self.MenuBar = self.makeMenu()
        
        
        self.statusBar()
        self.setGeometry(100, 100, 400, 400)
        self.setWindowIcon(QIcon.fromTheme("document-new"))
        #self.setWindowIcon(QIcon.fromTheme("document-new", QtCore,QIcon(":/new.png")))
        self.setMinimumSize(200,150)
        self.setWindowTitle('SelectX')
        
        self.mainTab = QtGui.QTabWidget(self)
        self.mainTab.setTabsClosable(True)
        self.mainTab.setMovable(True)
        self.setCentralWidget(self.mainTab)
        self.mainTab.addTab(self.initEdit(), "New Text")
        self.mainTab.tabCloseRequested.connect(self.removeTab)  
        self.show()
    
    def initEdit(self, fileName=None):
        
        self.qFont = QtGui.QFont()
        self.qFont.setFamily('Courier New')
        self.qFont.setFixedPitch(True)
        self.qFont.setPointSize(14)
        
        self.textEdit = QtGui.QTextEdit(self)
        self.textEdit.setFont(self.qFont)
        #self.textEdit.setStyleSheet("QTextEdit {font-family: Sans-serif;}")
        
        self.textEdit.cursorPositionChanged.connect(self.cursorPosition)
        return self.textEdit

    def makeMenu(self):
        menubar = self.menuBar()
        
        self.toolbar = self.addToolBar("File")
        self.toolbar.setMovable(True)
        
        fileMenu = menubar.addMenu('&File')
        self.addActionParamX('New', 'Ctrl+N', 'Create new file', self.newFile, \
        fileMenu, 'document-new', self.toolbar)
        self.addActionParamX('New Tab', 'Ctrl+T', 'Create new tab', self.newTab, \
        fileMenu, 'tab-new', self.toolbar)
        self.addActionParamX('Open', 'Ctrl+O', 'Open a file', self.openFile, \
        fileMenu, 'document-open', self.toolbar)
        self.addActionParamX('Save.', 'Ctrl+S', 'Save current file', \
        self.saveFile, fileMenu, 'document-save', self.toolbar)
        self.addActionParamX('Save As...', 'Ctrl+Shift+S', 'Save as new file', \
        self.saveFileAs, fileMenu, 'document-save-as', self.toolbar)
        fileMenu.addSeparator()
        self.addActionParamX('Preview', 'Ctrl+L', 'File Preview', \
        self.filePreview, fileMenu, 'document-print-preview', self.toolbar)
        self.addActionParamX('Print', 'Ctrl+P', 'File Print', \
        self.filePrint, fileMenu, 'document-print', self.toolbar)
        fileMenu.addSeparator()
        self.addActionParamX('Close Tab', 'Ctrl+Shift+Q', 'Close current tab', \
        self.removeTab, fileMenu, 'window-close', self.toolbar)
        self.addActionParamX('Exit', 'Ctrl+Q', 'Exit SelectX', \
        self.checkExitProgram, fileMenu, 'application-exit', self.toolbar)
        
        self.toolbar = self.addToolBar("Edit")
        self.toolbar.setMovable(True)
        editMenu = menubar.addMenu('&Edit')
        self.addActionParamX('Undo', 'Ctrl+Z', 'Undo last text edit', \
        self.undoText, editMenu, 'edit-undo', self.toolbar)
        self.addActionParamX('Redo', 'Ctrl+Y', 'Redo last text edit', \
        self.redoText, editMenu, 'edit-redo', self.toolbar)
        editMenu.addSeparator()
        self.addActionParamX('Copy', 'Ctrl+C', 'Copy selected text', \
        self.copyText, editMenu, 'edit-copy', self.toolbar)
        self.addActionParamX('Cut', 'Ctrl+X', 'Cut selected text', \
        self.cutText, editMenu, 'edit-cut', self.toolbar)
        self.addActionParamX('Paste', 'Ctrl+V', 'Paste text', self.pasteText, \
        editMenu, 'edit-paste', self.toolbar)
        editMenu.addSeparator()
        self.addActionParamX('Find', 'Ctrl+F', 'Find text', self.findText, \
        editMenu, 'edit-find')
        
        self.toolbar = self.addToolBar("Select")
        self.toolbar.setMovable(True)
        selectMenu = menubar.addMenu('&Select')
        self.addActionParamX('SelectAll', 'Ctrl+A', 'Select all text in editor', \
        self.selectSelectAll, selectMenu, 'edit-select-all', self.toolbar)
        
        self.toolbar = self.addToolBar("View")
        self.toolbar.setMovable(True)
        viewMenu = menubar.addMenu('&View')
        self.addActionParamX('Zoom In', 'Ctrl++', 'Zoom In text in editor', \
        self.viewZoomIn, viewMenu, 'zoom-in', self.toolbar)
        self.addActionParamX('Zoom Out', 'Ctrl+-', 'Zoom Out text in editor', \
        self.viewZoomOut, viewMenu, 'zoom-out', self.toolbar)
        self.addActionParamX('Zoom Original', 'Ctrl+0', 'Zoom original text in editor', \
        self.viewZoomOriginal, viewMenu, 'zoom-original', self.toolbar)
        viewMenu.addSeparator()
        self.addActionParamX('Font', 'F8', 'Font select dialog', \
        self.viewFont, viewMenu, 'preferences-desktop-font', self.toolbar)
        #self.addToolBarBreak()
        
        self.toolbar = self.addToolBar("Help")
        self.toolbar.setMovable(True)
        helpMenu = menubar.addMenu('&Help')
        self.addActionParamX('Help', 'F1', 'Keys Help', self.keyHelp, helpMenu, \
        'help-contents', self.toolbar)
        self.addActionParamX('About', 'F9', 'About editot', self.aboutHelp, \
        helpMenu, 'help-about')
        self.addActionParamX("About &Qt", 'Shift+F9', 'About current QT', QtGui.qApp.aboutQt, \
        helpMenu, 'help-about')
        #self.toolbar.addToolBarBreak()
        
    
      # Makes the next toolbar appear underneath this one
        #self.addToolBarBreak()
        
        return menubar
        
    def addActionParamX(self, ActText, ActSortcut, ActTip, ActConnect, \
    TopActLevel, IconName, toolBar=None):
        MakeAction = QtGui.QAction(QIcon.fromTheme(IconName), ActText, self)
        MakeAction.setIconVisibleInMenu (True)
        MakeAction.setShortcut(ActSortcut)
        MakeAction.setStatusTip(ActTip)
        MakeAction.triggered.connect(ActConnect)
        TopActLevel.addAction(MakeAction)
        
        if toolBar:
            toolBar.addAction(MakeAction)
    
    def cursorPosition(self):
        cursor = self.mainTab.currentWidget().textCursor()
        line = cursor.blockNumber() + 1
        col = cursor.columnNumber()
        self.statusBar().showMessage("Line: {} | Column: {}".format(line,col))
        
    def newFile(self):
        self.mainTab.currentWidget().clear()
        self.path=None
        self.statusBar().showMessage('New Text')
        self.setWindowTitle('SelectX')
        
    def newTab(self):
        self.mainTab.addTab(self.initEdit(), "New text tab")
        self.mainTab.setCurrentWidget(self.textEdit)
        
    def removeTab(self, tabIndex): 
        #print  'tabIndex-%s' % tabIndex
        self.mainTab.removeTab(tabIndex)
        #self.mainTab.setVisible(self.count() > 1)         
        
    def saveFile(self):
        if self.path:
            f = open(self.path, 'w')
            filedata = self.mainTab.currentWidget().toPlainText()
            f.write(filedata)
            f.close()
            self.statusBar().showMessage('Save Text: %s' % self.path)
        else:
            self.saveFileAs()
        
    def saveFileAs(self):
        filename = QtGui.QFileDialog.getSaveFileName(self, 'Save File', \
        os.getenv('HOME'))
        if filename:
            f = open(filename, 'w')
            filedata = self.mainTab.currentWidget().toPlainText()
            f.write(filedata)
            f.close()
            self.statusBar().showMessage('Save Text: %s' % filename)
            self.setWindowTitle('SelectX - %s' % filename)
        else:
            self.statusBar().showMessage('Stop Save Text')
        
    def openFile(self):
        ###to see http://www.rkblog.rk.edu.pl/w/p/simple-text-editor-pyqt4/
        self.path = QtGui.QFileDialog.getOpenFileName(self, 'Open File', \
        os.getenv('HOME'), \
         "All Files (*);;Text Files (*.txt *.log);;Python Files (*.py *.py3);;C++ Files (*.cpp *.h)" \
        )
        
        if self.path:
            self.openExistFile(self.path)
        else:
            self.statusBar().showMessage('Stop Open Text')
                
    def openExistFile(self, filePath):
        self.path = filePath
        inFile = QtCore.QFile(self.path)
        if inFile.open(QtCore.QFile.ReadOnly | QtCore.QFile.Text):
            text = inFile.readAll()
            try:
                # Python v3.
                text = str(text, encoding='ascii')
                #text = str(text, encoding='utf-8')
            except TypeError:
                # Python v2.
                text = str(text)
            self.mainTab.currentWidget().clear()
            self.highlighter = Highlighter(self.mainTab.currentWidget().document(), filePath.split('.')[-1])
            self.mainTab.currentWidget().insertPlainText(text)
            self.statusBar().showMessage('Open Text: %s' % self.path)
            self.setWindowTitle('SelectX - %s' % self.path)
        else:
            print 'Can Not Open This File -> %s' % self.path
            self.path = None
        
    def filePreview(self):
        '''Open preview dialog'''
        preview = QtGui.QPrintPreviewDialog()
        # If a print is requested, open print dialog
        preview.paintRequested.connect(lambda p: self.mainTab.currentWidget().print_(p))
        preview.exec_()

    def filePrint(self):
        '''Open printing dialog'''
        dialog = QtGui.QPrintDialog()
        if dialog.exec_() == QtGui.QDialog.Accepted:
            self.mainTab.currentWidget().document().print_(dialog.printer())

    def checkExitProgram(self):
        reply_exit = QtGui.QMessageBox.question(self, 'Confirm Exit SelectX', \
        "Are you sure to Exit?", QtGui.QMessageBox.Yes | QtGui.QMessageBox.No, \
        QtGui.QMessageBox.No)
        if reply_exit==QtGui.QMessageBox.Yes:
            self.close()
        self.statusBar().showMessage('Close Stoped')
        
    def undoText(self):
        self.mainTab.currentWidget().undo()
        self.statusBar().showMessage('Undo Text')
        
    def redoText(self):
        self.mainTab.currentWidget().redo()
        self.statusBar().showMessage('Redo Text')
        
    def copyText(self):
        self.mainTab.currentWidget().copy()
        self.statusBar().showMessage('Copy Text')
        
    def cutText(self):
        self.mainTab.currentWidget().cut()
        self.statusBar().showMessage('Cut Text')
        
    def pasteText(self):
        self.mainTab.currentWidget().paste()
        self.statusBar().showMessage('Paste Text')
        
    def findText(self):
        cursor = self.mainTab.currentWidget().textCursor()
        textSelected = cursor.selectedText()
        text_find, find_ok = QtGui.QInputDialog.getText(self, \
        'SelectX Find Dialog', 'Enter text to find:', QtGui.QLineEdit.Normal,  textSelected)
        if find_ok:
            if self.mainTab.currentWidget().find(str(text_find)):
                self.statusBar().showMessage('Finded: %s' % text_find)
                return
            else:
                self.statusBar().showMessage('Not finded: %s' % text_find)
                return
            return
        self.statusBar().showMessage('Find Canseled')
        
    def selectSelectAll(self):
        self.mainTab.currentWidget().selectAll()
        self.statusBar().showMessage('Select All Text')
        
    def viewZoomIn(self):
        self.mainTab.currentWidget().zoomIn(1)
        self.zoomRate += 1
        self.statusBar().showMessage('Zoom Rate: %s' % self.zoomRate)
        
    def viewZoomOut(self):
        self.mainTab.currentWidget().zoomOut(1)
        self.zoomRate -= 1
        self.statusBar().showMessage('Zoom Rate: %s' % self.zoomRate)
        
    def viewZoomOriginal(self):
        self.mainTab.currentWidget().zoomIn(-self.zoomRate)
        self.zoomRate = 0
        self.statusBar().showMessage('Zoom Rate: %s' % self.zoomRate)
        
    def viewFont(self):
        font, ok = QtGui.QFontDialog.getFont(self.qFont, self)
        if ok:
            self.qFont = font
            self.viewZoomOriginal()
            self.mainTab.currentWidget().setFont(self.qFont)
            self.statusBar().showMessage('Font set: %s' % self.qFont.toString())
        
    def aboutHelp(self):
        QtGui.QMessageBox.about(self, 'About SelectX', \
        "SelectX. Text editor licenced by GPL3. Ver. %s" % __version__)
        self.statusBar().showMessage(VERSION_INFO % \
        __version__)
        
    def keyHelp(self):
        QtGui.QMessageBox.information(self, 'Keys SelectX', KEYS_HELP, \
        QtGui.QMessageBox.Ok)


HILIGHTER_SETUP_CPP = {'keywordPatternsRules' : ["\\bchar\\b", "\\bclass\\b", "\\bconst\\b",
                "\\bdouble\\b", "\\benum\\b", "\\bexplicit\\b", "\\bfriend\\b",
                "\\binline\\b", "\\bint\\b", "\\blong\\b", "\\bnamespace\\b",
                "\\boperator\\b", "\\bprivate\\b", "\\bprotected\\b",
                "\\bpublic\\b", "\\bshort\\b", "\\bsignals\\b", "\\bsigned\\b",
                "\\bslots\\b", "\\bstatic\\b", "\\bstruct\\b",
                "\\btemplate\\b", "\\btypedef\\b", "\\btypename\\b",
                "\\bunion\\b", "\\bunsigned\\b", "\\bvirtual\\b", "\\bvoid\\b",
                "\\bvolatile\\b"],
                'classFormatRules' : "\\bQ[A-Za-z]+\\b",
                'quotationFormatRules':"\".*\"",
                'functionFormatRules':"\\b[A-Za-z0-9_]+(?=\\()",
                'multiLineCommentFormat' : ["/\\*", "\\*/"],
                }


class Highlighter(QtGui.QSyntaxHighlighter):
    def __init__(self, parent=None, fileExt=''):
        if fileExt:
            super(Highlighter, self).__init__(parent)
    
            keywordFormat = QtGui.QTextCharFormat()
            keywordFormat.setForeground(QtCore.Qt.darkBlue)
            keywordFormat.setFontWeight(QtGui.QFont.Bold)
    
            keywordPatterns = ["\\bchar\\b", "\\bclass\\b", "\\bconst\\b",
                    "\\bdouble\\b", "\\benum\\b", "\\bexplicit\\b", "\\bfriend\\b",
                    "\\binline\\b", "\\bint\\b", "\\blong\\b", "\\bnamespace\\b",
                    "\\boperator\\b", "\\bprivate\\b", "\\bprotected\\b",
                    "\\bpublic\\b", "\\bshort\\b", "\\bsignals\\b", "\\bsigned\\b",
                    "\\bslots\\b", "\\bstatic\\b", "\\bstruct\\b",
                    "\\btemplate\\b", "\\btypedef\\b", "\\btypename\\b",
                    "\\bunion\\b", "\\bunsigned\\b", "\\bvirtual\\b", "\\bvoid\\b",
                    "\\bvolatile\\b"]
    
            self.highlightingRules = [(QtCore.QRegExp(pattern), keywordFormat)
                    for pattern in keywordPatterns]
    
            classFormat = QtGui.QTextCharFormat()
            classFormat.setFontWeight(QtGui.QFont.Bold)
            classFormat.setForeground(QtCore.Qt.darkMagenta)
            self.highlightingRules.append((QtCore.QRegExp("\\bQ[A-Za-z]+\\b"),
                    classFormat))
    
            singleLineCommentFormat = QtGui.QTextCharFormat()
            singleLineCommentFormat.setForeground(QtCore.Qt.red)
            self.highlightingRules.append((QtCore.QRegExp("//[^\n]*"),
                    singleLineCommentFormat))
    
            self.multiLineCommentFormat = QtGui.QTextCharFormat()
            self.multiLineCommentFormat.setForeground(QtCore.Qt.red)
    
            quotationFormat = QtGui.QTextCharFormat()
            quotationFormat.setForeground(QtCore.Qt.darkGreen)
            self.highlightingRules.append((QtCore.QRegExp("\".*\""),
                    quotationFormat))
    
            functionFormat = QtGui.QTextCharFormat()
            functionFormat.setFontItalic(True)
            functionFormat.setForeground(QtCore.Qt.blue)
            self.highlightingRules.append((QtCore.QRegExp("\\b[A-Za-z0-9_]+(?=\\()"),
                    functionFormat))
    
            self.commentStartExpression = QtCore.QRegExp("/\\*")
            self.commentEndExpression = QtCore.QRegExp("\\*/")

    def highlightBlock(self, text):
        for pattern, format in self.highlightingRules:
            expression = QtCore.QRegExp(pattern)
            index = expression.indexIn(text)
            while index >= 0:
                length = expression.matchedLength()
                self.setFormat(index, length, format)
                index = expression.indexIn(text, index + length)

        self.setCurrentBlockState(0)

        startIndex = 0
        if self.previousBlockState() != 1:
            startIndex = self.commentStartExpression.indexIn(text)

        while startIndex >= 0:
            endIndex = self.commentEndExpression.indexIn(text, startIndex)

            if endIndex == -1:
                self.setCurrentBlockState(1)
                commentLength = len(text) - startIndex
            else:
                commentLength = endIndex - startIndex + self.commentEndExpression.matchedLength()

            self.setFormat(startIndex, commentLength,
                    self.multiLineCommentFormat)
            startIndex = self.commentStartExpression.indexIn(text,
                    startIndex + commentLength);


def main():
    if len(sys.argv) < 2:
        runWindow()
    elif sys.argv[1]=='-h' or sys.argv[1]=='--help':
        usage()
        sys.exit()
    elif sys.argv[1]=='--version':
        print VERSION_INFO % __version__
        sys.exit()
    runWindow()


def usage():
    print sys.argv[0] + '''
''' + VERSION_INFO % __version__ + CONSOLE_USAGE


def runWindow():
    app = QtGui.QApplication(sys.argv)
    selxnotepad = SelectX()
    sys.exit(app.exec_())


#def main():
    #try:
        #opts, args = getopt.getopt(sys.argv[1:], "h:v", ["help",])
    #except getopt.GetoptError as err:
        ## print help information and exit:
        #print(err) # will print something like "option -a not recognized"
        #usage()
        #sys.exit(2)
    #output = None
    #verbose = False
    #for o, a in opts:
        #if o == "-v":
            #verbose = True
            #print 'vvv'
        #elif o in ("-h", "--help"):
            #usage()
            #print 'hhhh'
            #sys.exit()
        #else:
            #assert False, "unhandled option"
            
    #app = QtGui.QApplication(sys.argv)
    #selxnotepad = SelectX()
    #sys.exit(app.exec_())
    ## ...

if __name__ == "__main__":
   main()

