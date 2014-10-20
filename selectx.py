#!/usr/bin/env python
'''SelectX - easy eXtable text editor for developers writed on Python. Licensed by GPL3.'''

import sys
import os
from PyQt4 import QtGui, QtCore


__version__ = '''0.2.12'''
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
        #self.openInNewTab = True
        self.selectForCopyByWords = False
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
        self.setWindowIcon(QtGui.QIcon.fromTheme("edit-select-all"))
        #self.setWindowIcon(QtGui.QIcon.fromTheme("document-new", QtCore.QIcon(":/new.png")))
        self.setMinimumSize(200,150)
        self.setWindowTitle('SelectX')
        
        self.mainTab = QtGui.QTabWidget(self)
        self.mainTab.setTabsClosable(True)
        self.mainTab.setMovable(True)
        self.setCentralWidget(self.mainTab)
        self.mainTab.addTab(self.initEdit(), "New Text")
        self.mainTab.tabCloseRequested.connect(self.closeTab)
        
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
        #self.addActionParamX('New', 'Ctrl+N', 'Create new file', self.newFile, \
        #fileMenu, 'document-new', self.toolbar)
        self.addActionParamX('New Tab', 'Ctrl+T', 'Create new tab', self.newTab, \
        fileMenu, 'tab-new', self.toolbar)
        #self.addActionParamX('Open in new tab', 'Ctrl+Shift+O', 'Set open a file in new tab', self.setOpenInNewTab, \
        #fileMenu, 'document-open', checkAble=True)
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
        self.closeTab, fileMenu, 'window-close', self.toolbar)
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
        editMenu, 'edit-find', self.toolbar)
        #self.addActionParamX('Get formed', 'Ctrl+G', 'Get formed text', self.getFormedText, \
        #editMenu, 'edit-find', self.toolbar)
        
        self.toolbar = self.addToolBar("Select")
        self.toolbar.setMovable(True)
        selectMenu = menubar.addMenu('&Select')
        self.addActionParamX('SelectAll', 'Ctrl+A', 'Select all text in editor', \
        self.selectSelectAll, selectMenu, 'edit-select-all', self.toolbar)
        #self.addActionParamX('Select For Copy By Words', 'Ctrl+Shift+A', 'Set Select For Copy By Words', \
        #self.setSelectByWords, selectMenu, 'edit-select', self.toolbar, checkAble=True)
        
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
        
        self.toolbar = self.addToolBar("Help")
        self.toolbar.setMovable(True)
        helpMenu = menubar.addMenu('&Help')
        self.addActionParamX('Help', 'F1', 'Keys Help', self.keyHelp, helpMenu, \
        'help-contents', self.toolbar)
        self.addActionParamX('About', 'F9', 'About editot', self.aboutHelp, \
        helpMenu, 'help-about')
        self.addActionParamX("About &Qt", 'Shift+F9', 'About current QT', QtGui.qApp.aboutQt, \
        helpMenu, 'help-about')
        
        
        return menubar
        
    def addActionParamX(self, ActText, ActSortcut, ActTip, ActConnect, \
    TopActLevel, IconName, toolBar=None, checkAble=False, checkState=False):
        MakeAction = QtGui.QAction(QtGui.QIcon.fromTheme(IconName), ActText, self)
        if checkAble:
            MakeAction.setCheckable (True)
            MakeAction.setChecked (checkState)
            
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
        symb = len(self.mainTab.currentWidget().toPlainText())
        rows = len(self.mainTab.currentWidget().toPlainText().split('\n')) # ;)
        self.statusBar().showMessage("Rows: {} | Symbols: {} | Line: {} | Column: {}".format(symb,rows,line,col))
        
    def newFile(self):
        self.mainTab.currentWidget().clear()
        self.path=None
        self.statusBar().showMessage('New Text')
        self.setWindowTitle('SelectX')
        
    def newTab(self):
        self.mainTab.addTab(self.initEdit(), "New text tab")
        self.mainTab.setCurrentWidget(self.textEdit)
        
    def closeTab(self, tabIndex): 
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
            self.path = filename
            self.statusBar().showMessage('Save Text: %s' % filename)
            self.setWindowTitle('SelectX - %s' % filename)
            curtabind = self.mainTab.currentIndex()
            self.mainTab.setTabToolTip (curtabind, '%s' % self.path)
            self.mainTab.setTabText(curtabind, '%s' % getFileName(self.path))
        else:
            self.statusBar().showMessage('Stop Save Text')
        
    def setOpenInNewTab(self):
        self.openInNewTab = not(self.openInNewTab)
        print self.openInNewTab
        
    def openFile(self):
        ###to see http://www.rkblog.rk.edu.pl/w/p/simple-text-editor-pyqt4/
        self.path = QtGui.QFileDialog.getOpenFileName(self, 'Open File', \
        os.getenv('HOME'), \
         "All Files (*);;Text Files (*.txt *.log *.TXT *.LOG);;Python Files (*.py *.PY *.py3 *.PY3);;C++ Files (*.cpp *.h *.CPP *.H *.c *.C)" \
        )
        
        if self.path:
            if len(self.mainTab.currentWidget().toPlainText()) > 0:
                self.newTab()
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
            #self.mainTab.currentWidget().insertPlainText(maskSpaces(text))
            self.mainTab.currentWidget().insertPlainText(text)
            self.statusBar().showMessage('Open Text: %s' % self.path)
            curtabind = self.mainTab.currentIndex()
            
            self.mainTab.setTabToolTip (curtabind, '%s' % self.path)
            self.mainTab.setTabText(curtabind, '%s' % getFileName(self.path))
            #elf.currentIndex()
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
        if self.selectForCopyByWords:
        
            self.cursorMain = self.mainTab.currentWidget().cursorRect()
            print self.cursorMain
            print 'self.cursorMain.height(), self.cursorMain.width(), self.cursorMain.top(), self.cursorMain.bottom(), self.cursorMain.left(), self.cursorMain.right(), self.cursorMain.x(), self.cursorMain.y()'
            print self.cursorMain.height(), self.cursorMain.width(), self.cursorMain.top(), self.cursorMain.bottom(), self.cursorMain.left(), self.cursorMain.right(), self.cursorMain.x(), self.cursorMain.y()
        self.mainTab.currentWidget().copy()
        self.statusBar().showMessage('Copy Text')
        
    def cutText(self):
        self.mainTab.currentWidget().cut()
        self.statusBar().showMessage('Cut Text')
        
    def pasteText(self):
        self.mainTab.currentWidget().paste()
        self.statusBar().showMessage('Paste Text')
        
    def getFormedText(self):
        text_get, get_ok = QtGui.QInputDialog.getText(self, \
        'Get Formed Text', 'Enter form start_row,start_word_number,number_of_words,end_row')
        if get_ok:
            try:
                params_get = text_get.split(',')
                print params_get
                filedata = self.mainTab.currentWidget().toPlainText()
                filelist = filedata.split('\n')
                newdata='************************************\n'
                for row in filelist[int(params_get[0]):int(params_get[-1])]:
                    for word in row[int(params_get[1]):int(params_get[1])+int(params_get[2])+1]:
                        newdata=newdata+str(word)+' '
                    newdata=newdata+'\n'
                self.mainTab.currentWidget().insertPlainText(filedata+newdata)
                self.statusBar().showMessage('adde get from') 
            except IndexError, ValueError:
                self.statusBar().showMessage('wrong get from')
       
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
        
    def setSelectByWords(self):
        self.selectForCopyByWords = not(self.selectForCopyByWords)
        
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


HILIGHTER_SETUP = {'cpp c h' : {'keywordPatternsRules' : ["\\bchar\\b", "\\bclass\\b", "\\bconst\\b",
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
                'multiLineCommentFormat' : ["/\\*", "\\*/"]},
                'py py3':{'keywordPatternsRules' : ["\\bchar\\b", "\\bclass\\b", "\\bconst\\b",
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
                'multiLineCommentFormat' : ["/\\*", "\\*/"]}
                }

def maskSpaces(oldText, oldChars=[' ','\n', '\t'], newChars=[u'\u2022', u'\u21b5\n', u'\u2192']):
    import re
    nnn=0
    newText = oldText
    for ochar in oldChars:
        newText = re.sub(ochar, newChars[nnn], newText)
        nnn += 1
    return newText

def unMaskSpaces(oldText, newChars=[' ','\n', '\t'], oldChars=[u'\u2022', u'\u21b5\n', u'\u2192']):
    maskSpaces(oldText, newChars, oldChars)

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

def getFileName(pathName):
    if ( '\\' in pathName ) :
        return pathName.split('\\')[-1]
    else:
        return pathName.split('/')[-1]


def usage():
    print sys.argv[0] + '''
''' + VERSION_INFO % __version__ + CONSOLE_USAGE


def runWindow():
    app = QtGui.QApplication(sys.argv)
    selxnotepad = SelectX()
    sys.exit(app.exec_())


if __name__ == "__main__":
   main()

