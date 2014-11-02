#!/usr/bin/env python
'''SelectX - easy eXtable text editor for developers writed on Python. Licensed by GPL3.'''

import sys
import os
from PyQt4 import QtGui, QtCore


from PyQt4.QtCore import QRegExp, QChar
from PyQt4.QtGui import QColor, QTextCharFormat, QFont, QSyntaxHighlighter


__version__ = '''0.3.3.5'''
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

TANGO_ICONS = {'edit-copy':
    """/* XPM */
static char *edit-copy_xpm[] = {
/* width height num_colors chars_per_pixel */
"    16    16      256            2",
/* colors */
"`` c #dbdcda",
"`. c #c3c4c2",
"`# c #dadbd8",
"`a c #ffffff",
"`b c #c5c6c3",
"`c c #f7f7f7",
"`d c #f7f7f6",
"`e c #e3e3e3",
"`f c #acadaa",
"`g c #888a85",
"`h c #b2b3b0",
"`i c #8a8c87",
"`j c #898b86",
"`k c #f0f0ef",
"`l c #c7c7c6",
"`m c #e2e2e2",
"`n c #f6f6f6",
"`o c #f6f6f5",
"`p c #fefefe",
"`q c #f5f5f5",
"`r c #e1e1e1",
"`s c #fafafa",
"`t c #f3f3f3",
"`u c #fcfcfc",
"`v c #f4f4f4",
"`w c #eeeeee",
"`x c #c3c4c3",
"`y c #f9f9f8",
"`z c #f9f9f9",
"`A c #f8f8f8",
"`B c #8c8e89",
"`C c #c4c5c2",
"`D c #fefefd",
"`E c #989a95",
"`F c #f8f8f7",
"`G c #e3e4e2",
"`H c #fafaf9",
"`I c #e3e3e2",
"`J c #9fa19d",
"`K c #fcfcfb",
"`L c #fbfbfb",
"`M c #d4d4d4",
"`N c #989a96",
"`O c #b5b6b3",
"`P c #a5a7a3",
"`Q c #000000",
"`R c #000000",
"`S c #000000",
"`T c #000000",
"`U c #000000",
"`V c #000000",
"`W c #000000",
"`X c #000000",
"`Y c #000000",
"`Z c #000000",
"`0 c #000000",
"`1 c #000000",
"`2 c #000000",
"`3 c #000000",
"`4 c #000000",
"`5 c #000000",
"`6 c #000000",
"`7 c #000000",
"`8 c #000000",
".` c #000000",
".. c #000000",
".# c #000000",
".a c #000000",
".b c #000000",
".c c #000000",
".d c #000000",
".e c #000000",
".f c #000000",
".g c #000000",
".h c #000000",
".i c #000000",
".j c #000000",
".k c #000000",
".l c #000000",
".m c #000000",
".n c #000000",
".o c #000000",
".p c #000000",
".q c #000000",
".r c #000000",
".s c #000000",
".t c #000000",
".u c #000000",
".v c #000000",
".w c #000000",
".x c #000000",
".y c #000000",
".z c #000000",
".A c #000000",
".B c #000000",
".C c #000000",
".D c #000000",
".E c #000000",
".F c #000000",
".G c #000000",
".H c #000000",
".I c #000000",
".J c #000000",
".K c #000000",
".L c #000000",
".M c #000000",
".N c #000000",
".O c #000000",
".P c #000000",
".Q c #000000",
".R c #000000",
".S c #000000",
".T c #000000",
".U c #000000",
".V c #000000",
".W c #000000",
".X c #000000",
".Y c #000000",
".Z c #000000",
".0 c #000000",
".1 c #000000",
".2 c #000000",
".3 c #000000",
".4 c #000000",
".5 c #000000",
".6 c #000000",
".7 c #000000",
".8 c #000000",
"#` c #000000",
"#. c #000000",
"## c #000000",
"#a c #000000",
"#b c #000000",
"#c c #000000",
"#d c #000000",
"#e c #000000",
"#f c #000000",
"#g c #000000",
"#h c #000000",
"#i c #000000",
"#j c #000000",
"#k c #000000",
"#l c #000000",
"#m c #000000",
"#n c #000000",
"#o c #000000",
"#p c #000000",
"#q c #000000",
"#r c #000000",
"#s c #000000",
"#t c #000000",
"#u c #000000",
"#v c #000000",
"#w c #000000",
"#x c #000000",
"#y c #000000",
"#z c #000000",
"#A c #000000",
"#B c #000000",
"#C c #000000",
"#D c #000000",
"#E c #000000",
"#F c #000000",
"#G c #000000",
"#H c #000000",
"#I c #000000",
"#J c #000000",
"#K c #000000",
"#L c #000000",
"#M c #000000",
"#N c #000000",
"#O c #000000",
"#P c #000000",
"#Q c #000000",
"#R c #000000",
"#S c #000000",
"#T c #000000",
"#U c #000000",
"#V c #000000",
"#W c #000000",
"#X c #000000",
"#Y c #000000",
"#Z c #000000",
"#0 c #000000",
"#1 c #000000",
"#2 c #000000",
"#3 c #000000",
"#4 c #000000",
"#5 c #000000",
"#6 c #000000",
"#7 c #000000",
"#8 c #000000",
"a` c #000000",
"a. c #000000",
"a# c #000000",
"aa c #000000",
"ab c #000000",
"ac c #000000",
"ad c #000000",
"ae c #000000",
"af c #000000",
"ag c #000000",
"ah c #000000",
"ai c #000000",
"aj c #000000",
"ak c #000000",
"al c #000000",
"am c #000000",
"an c #000000",
"ao c #000000",
"ap c #000000",
"aq c #000000",
"ar c #000000",
"as c #000000",
"at c #000000",
"au c #000000",
"av c #000000",
"aw c #000000",
"ax c #000000",
"ay c #000000",
"az c #000000",
"aA c #000000",
"aB c #000000",
"aC c #000000",
"aD c #000000",
"aE c #000000",
"aF c #000000",
"aG c #000000",
"aH c #000000",
"aI c #000000",
"aJ c #000000",
"aK c #000000",
"aL c #000000",
"aM c #000000",
"aN c #000000",
"aO c #000000",
"aP c #000000",
"aQ c #000000",
"aR c #000000",
"aS c #000000",
"aT c #000000",
"aU c #000000",
"aV c #000000",
"aW c #000000",
"aX c #000000",
"aY c #000000",
"aZ c #000000",
"a0 c #000000",
"a1 c #000000",
"a2 c #000000",
"a3 c #000000",
"a4 c #000000",
"a5 c #000000",
"a6 c #000000",
"a7 c #000000",
"a8 c #000000",
/* pixels */
"```.`.`.`.`.`.`.`.`.`.`#`a`a`a`a",
"`b`a`a`a`a`a`a`a`a`a`a`.`a`a`a`a",
"`b`a`c`d`d`d`d`d`c`c`a`.`a`a`a`a",
"`b`a`c`e`f`g`g`g`g`g`g`g`g`g`g`h",
"`b`a`c`c`i`a`a`a`a`a`a`a`a`a`a`g",
"`b`a`c`e`j`a`k`k`k`k`k`k`k`k`a`g",
"`b`a`c`d`i`a`k`l`l`l`l`l`l`k`a`g",
"`b`a`d`m`j`a`k`k`k`k`k`k`k`k`a`g",
"`b`a`n`o`i`a`k`l`l`l`l`l`k`k`a`g",
"`b`p`q`r`j`a`k`k`k`k`k`k`k`s`t`g",
"`b`u`q`v`i`a`k`l`l`l`l`l`w`d`x`g",
"`b`y`z`A`i`a`k`k`k`k`k`B`B`B`B`g",
"```C`C`C`j`D`k`k`k`k`s`E`s`F`G`g",
"`a`a`a`a`i`H`k`k`k`s`s`E`s`I`g`J",
"`a`a`a`a`i`v`d`o`K`L`M`N`G`g`.`a",
"`a`a`a`a`O`j`g`g`g`g`g`g`P`.`a`a"
};
""",
    }



class SelectX(QtGui.QMainWindow):

    def __init__(self):
        super(SelectX, self).__init__()
        #init class constants
        self.nonPrintFlag = False
        self.nonPrintSymbols = [' ', '\t']
        self.nonPrintMasks = [u'\u2022', u'\u2192']
        self.zoomRate = 0
        self.path = os.getenv('HOME')
        self.selectForCopyByWords = False
        self.startPath = os.getenv('HOME')
        
        
        
        self.initUI()
        #self.openInNewTab = True
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
        
        #self.initNonPrintCursor()
        
        self.mainTab.tabCloseRequested.connect(self.closeTab)
        self.setHighlighter()
        
        self.show()
    
    def initNonPrintCursor(self):
        # to see https://qt-project.org/doc/qt-4.7/richtext-textobject.html
        cursor = self.mainTab.currentWidget().textCursor()
        newsymbol=QTextCharFormat(u'\u21b5')
        newsymbol.setFont(self.qFont)
        cursor.insertText(QChar.ObjectReplacementCharacter, newsymbol)
        self.mainTab.currentWidget().setTextCursor(cursor)
        print 'ns'+str(ns)
    
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
        viewMenu.addSeparator()
        self.addActionParamX('Get formed non-printabale', 'Ctrl+G', 'Get formed non-printabale symbols', self.getFormedText, \
        viewMenu, 'list-add', self.toolbar, checkAble=True)
        
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
        newIcon = QtGui.QIcon.fromTheme(IconName)
        if newIcon.hasThemeIcon (IconName):
            print 'has '+IconName
        else:
            print 'has not '+IconName
            if IconName in TANGO_ICONS:
                newPixmap = QtGui.QPixmap()
                newPixmap.loadFromData(TANGO_ICONS[IconName])
                newIcon = QtGui.QIcon(newPixmap)
            
        MakeAction = QtGui.QAction(newIcon, ActText, self)
        if checkAble:
            MakeAction.setCheckable (True)
            MakeAction.setChecked (checkState)
            
        
        #MakeAction.setPriority (MakeAction.LowPriority)
        #MakeAction.setIconVisibleInMenu (False)
        MakeAction.setIconVisibleInMenu (True)
        MakeAction.setShortcut(ActSortcut)
        MakeAction.setStatusTip(ActTip)
        MakeAction.triggered.connect(ActConnect)
        TopActLevel.addAction(MakeAction)
        
        if toolBar:
            toolBar.addAction(MakeAction)
    
    def cursorPosition(self):
        currentWidget = self.mainTab.currentWidget()
        cursor = currentWidget.textCursor()
        line = cursor.blockNumber() + 1
        col = cursor.columnNumber()
        currentText = currentWidget.toPlainText()
        symb = len(currentText)
        allRows = currentText.split('\n') # ;)
        rows = len(allRows) 
        self.statusBar().showMessage("Rows: {} | Symbols: {} | Line: {} | Column: {}".format(symb,rows,line,col))
        
        #if self.nonPrintFlag:
            #if allRows[][]
            #self.nonPrintSymbols = 
        
    def setHighlighter(self):
        extention = str(getFileName(self.path, '.')).lower()
        if extention in ['c', 'cc','cpp', 'c++', 'cxx', 'h', 'hh', 'hpp', 'hxx']:
            self.highlighter = Highlighter(self.mainTab.currentWidget().document(), extention)
        elif extention in ['py', 'py3']:
            self.highlighter = PythonHighlighter(self.mainTab.currentWidget().document())
        #else:
            #self.highlighter = PythonHighlighter(self.mainTab.currentWidget().document())
        
    def newFile(self):
        self.mainTab.currentWidget().clear()
        self.path=None
        self.statusBar().showMessage('New Text')
        self.setWindowTitle('SelectX')
        
    def newTab(self):
        self.mainTab.addTab(self.initEdit(), "New text tab")
        self.mainTab.setCurrentWidget(self.textEdit)
        self.setHighlighter()
        
    def closeTab(self, tabIndex): 
        #print  'tabIndex-%s' % tabIndex
        self.mainTab.removeTab(tabIndex)
        #self.mainTab.setVisible(self.count() > 1)         
        
    def saveFile(self):
        if self.path:
            f = open(self.path, 'w')
            if self.nonPrintFlag:
                filedata = unMaskSpaces(self.mainTab.currentWidget().toPlainText())
            f.write(filedata)
            f.close()
            self.statusBar().showMessage('Save Text: %s' % self.path)
        else:
            self.saveFileAs()
        
    def saveFileAs(self):
        if self.startPath:
            filename = QtGui.QFileDialog.getSaveFileName(self, 'Save File', \
            self.startPath)
        else:
            #for windows
            self.startPath = './'
            filename = QtGui.QFileDialog.getSaveFileName(self, 'Save File', \
            self.startPath)
        if filename:
            f = open(filename, 'w')
            if self.nonPrintFlag:
                filedata = unMaskSpaces(self.mainTab.currentWidget().toPlainText())
            f.write(filedata)
            f.close()
            self.path = filename
            self.startPath = self.path[:-len(getFileName(self.path))]
            self.statusBar().showMessage('Save Text: %s' % filename)
            self.setWindowTitle('SelectX - %s' % filename)
            curtabind = self.mainTab.currentIndex()
            
            self.mainTab.setTabToolTip (curtabind, '%s' % self.path)
            newFileName =  getFileName(self.path)
            self.mainTab.setTabText(curtabind, '%s' % newFileName)
            self.setHighlighter()
        else:
            self.statusBar().showMessage('Stop Save Text')
        
    def setOpenInNewTab(self):
        self.openInNewTab = not(self.openInNewTab)
        print self.openInNewTab
        
    def openFile(self):
        ###to see http://www.rkblog.rk.edu.pl/w/p/simple-text-editor-pyqt4/
        if self.startPath:
            self.path = QtGui.QFileDialog.getOpenFileName(self, 'Open File', \
            self.startPath, \
             "All Files (*);;Text Files (*.txt *.log *.TXT *.LOG);;Python Files (*.py *.PY *.py3 *.PY3);;C/C++ Files (*.c *.cc *.cpp *.c++ *.cxx *.h *.hh *.hpp *.hxx *.CPP *.H *.c *.C)" \
            )
        else:
            #for windows
            self.startPath = './'
            self.path = QtGui.QFileDialog.getOpenFileName(self, 'Open File', \
            self.startPath, \
             "All Files (*);;Text Files (*.txt *.log *.TXT *.LOG);;Python Files (*.py *.PY *.py3 *.PY3);;C/C++ Files (*.c *.cc *.cpp *.c++ *.cxx *.h *.hh *.hpp *.hxx *.CPP *.H *.c *.C)" \
            )
        
        if self.path:
            self.startPath = self.path[:-len(getFileName(self.path))]
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
            inFile.close()
            try:
                # Python v3.
                text = str(text, encoding='ascii')
                #text = str(text, encoding='utf-8')
            except TypeError:
                # Python v2.
                text = str(text)
            self.mainTab.currentWidget().clear()
            self.setHighlighter()
            #self.highlighter = Highlighter(self.mainTab.currentWidget().document(), filePath.split('.')[-1])
            #self.highlight = PythonHighlighter(self.mainTab.currentWidget().document())
            #self.mainTab.currentWidget().insertPlainText(maskSpaces(text))
            if self.nonPrintFlag:
                text = maskSpaces(text)
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
        self.nonPrintFlag = not(self.nonPrintFlag)
        
    def getFormedText____old(self):
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

#def maskSpaces(oldText, oldChars=[' ','\n', '\t'], newChars=[u'\u2022', u'\u21b5\n', u'\u2192']):
def maskSpaces(oldText, oldChars=[' ', '\t'], newChars=[u'\u2022', u'\u2192']):
    #print oldText
    import re
    nnn=0
    newText = oldText
    for ochar in oldChars:
        newText = re.sub(ochar, newChars[nnn], newText)
        nnn += 1
    return newText
    #nnn=0
    #for ochar in oldChars:
        #oldText.replace(ochar, newChars[nnn])
        #print ochar, newChars[nnn]
        #print oldText
        #nnn += 1
    
    #return oldText

#def unMaskSpaces(oldText, newChars=[' ','\n', '\t'], oldChars=[u'\u2022', u'\u21b5\n', u'\u2192']):
def unMaskSpaces(oldText, newChars=[' ', '\t'], oldChars=[u'\u2022', u'\u2192']):
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


def format(color, style=''):
    """Return a QTextCharFormat with the given attributes.
    """
    _color = QColor()
    _color.setNamedColor(color)

    _format = QTextCharFormat()
    _format.setForeground(_color)
    if 'bold' in style:
        _format.setFontWeight(QFont.Bold)
    if 'italic' in style:
        _format.setFontItalic(True)

    return _format


# Syntax styles that can be shared by all languages
STYLES = {
    'keyword': format('blue'),
    'operator': format('red'),
    'brace': format('darkGray'),
    'defclass': format('black', 'bold'),
    'string': format('magenta'),
    'string2': format('darkMagenta'),
    'comment': format('darkGreen', 'italic'),
    'self': format('black', 'italic'),
    'numbers': format('brown'),
}


class PythonHighlighter (QSyntaxHighlighter):
    """Syntax highlighter for the Python language.
    """
    # Python keywords
    keywords = [
        'and', 'assert', 'break', 'class', 'continue', 'def',
        'del', 'elif', 'else', 'except', 'exec', 'finally',
        'for', 'from', 'global', 'if', 'import', 'in',
        'is', 'lambda', 'not', 'or', 'pass', 'print',
        'raise', 'return', 'try', 'while', 'yield',
        'None', 'True', 'False',
    ]

    # Python operators
    operators = [
        '=',
        # Comparison
        '==', '!=', '<', '<=', '>', '>=',
        # Arithmetic
        '\+', '-', '\*', '/', '//', '\%', '\*\*',
        # In-place
        '\+=', '-=', '\*=', '/=', '\%=',
        # Bitwise
        '\^', '\|', '\&', '\~', '>>', '<<',
    ]

    # Python braces
    braces = [
        '\{', '\}', '\(', '\)', '\[', '\]',
    ]
    def __init__(self, document):
        QSyntaxHighlighter.__init__(self, document)

        # Multi-line strings (expression, flag, style)
        # FIXME: The triple-quotes in these two lines will mess up the
        # syntax highlighting from this point onward
        #self.tri_single = (QRegExp("'''[^'''\\]*(\\.[^'''\\]*)*'''"), 1, STYLES['string2'])
        #self.tri_double = (QRegExp('"""[^"""\\]*(\\.[^"""\\]*)*"""'), 2, STYLES['string2'])
        self.tri_single = (QRegExp("'''"), 1, STYLES['string2'])
        self.tri_double = (QRegExp('"""'), 2, STYLES['string2'])

        rules = []

        # Keyword, operator, and brace rules
        rules += [(r'\b%s\b' % w, 0, STYLES['keyword'])
            for w in PythonHighlighter.keywords]
        rules += [(r'%s' % o, 0, STYLES['operator'])
            for o in PythonHighlighter.operators]
        rules += [(r'%s' % b, 0, STYLES['brace'])
            for b in PythonHighlighter.braces]

        # All other rules
        rules += [
            # 'self'
            (r'\bself\b', 0, STYLES['self']),

            # Double-quoted string, possibly containing escape sequences
            (r'"[^"\\]*(\\.[^"\\]*)*"', 0, STYLES['string']),
            # Single-quoted string, possibly containing escape sequences
            (r"'[^'\\]*(\\.[^'\\]*)*'", 0, STYLES['string']),

            # 'def' followed by an identifier
            (r'\bdef\b\s*(\w+)', 1, STYLES['defclass']),
            # 'class' followed by an identifier
            (r'\bclass\b\s*(\w+)', 1, STYLES['defclass']),

            # From '#' until a newline
            (r'#[^\n]*', 0, STYLES['comment']),

            # Numeric literals
            (r'\b[+-]?[0-9]+[lL]?\b', 0, STYLES['numbers']),
            (r'\b[+-]?0[xX][0-9A-Fa-f]+[lL]?\b', 0, STYLES['numbers']),
            (r'\b[+-]?[0-9]+(?:\.[0-9]+)?(?:[eE][+-]?[0-9]+)?\b', 0, STYLES['numbers']),
        ]

        # Build a QRegExp for each pattern
        self.rules = [(QRegExp(pat), index, fmt)
            for (pat, index, fmt) in rules]


    def highlightBlock(self, text):
        """Apply syntax highlighting to the given block of text.
        """
        # Do other syntax formatting
        for expression, nth, format in self.rules:
            index = expression.indexIn(text, 0)

            while index >= 0:
                # We actually want the index of the nth match
                index = expression.pos(nth)
                length = expression.cap(nth).length()
                self.setFormat(index, length, format)
                index = expression.indexIn(text, index + length)

        self.setCurrentBlockState(0)

        # Do multi-line strings
        in_multiline = self.match_multiline(text, *self.tri_single)
        if not in_multiline:
            in_multiline = self.match_multiline(text, *self.tri_double)


    def match_multiline(self, text, delimiter, in_state, style):
        """Do highlighting of multi-line strings. ``delimiter`` should be a
        ``QRegExp`` for triple-single-quotes or triple-double-quotes, and
        ``in_state`` should be a unique integer to represent the corresponding
        state changes when inside those strings. Returns True if we're still
        inside a multi-line string when this function is finished.
        """
        # If inside triple-single quotes, start at 0
        if self.previousBlockState() == in_state:
            start = 0
            add = 0
        # Otherwise, look for the delimiter on this line
        else:
            start = delimiter.indexIn(text)
            # Move past this match
            add = delimiter.matchedLength()

        # As long as there's a delimiter match on this line...
        while start >= 0:
            # Look for the ending delimiter
            end = delimiter.indexIn(text, start + add)
            # Ending delimiter on this line?
            if end >= add:
                length = end - start + add + delimiter.matchedLength()
                self.setCurrentBlockState(0)
            # No; multi-line string
            else:
                self.setCurrentBlockState(in_state)
                length = text.length() - start + add
            # Apply formatting
            self.setFormat(start, length, style)
            # Look for the next match
            start = delimiter.indexIn(text, start + length)

        # Return True if still inside a multi-line string, False otherwise
        if self.currentBlockState() == in_state:
            return True
        else:
            return False



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

def getFileName(pathName, separatorSymbol=None):
    #print pathName
    if separatorSymbol:
        try:
            return pathName.split(separatorSymbol)[-1]
        except AttributeError:
            return None
    elif ( '\\' in pathName ) :
        return pathName.split('\\')[-1]
    else:
        return pathName.split('/')[-1]


def usage():
    print sys.argv[0] + '\n' + VERSION_INFO % __version__ + CONSOLE_USAGE


def runWindow():
    app = QtGui.QApplication(sys.argv)
    selxnotepad = SelectX()
    sys.exit(app.exec_())


if __name__ == "__main__":
   main()

