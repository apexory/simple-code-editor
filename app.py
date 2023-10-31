from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from tabs import TabWidget
import sys

class CodeEditor(QWidget):
    def __init__(self):
        super().__init__()

        layout = QVBoxLayout(spacing=0, margin=0)

        open = QWidgetAction(self)
        open.setDefaultWidget(QLabel("    Open ...    "));
        open.triggered.connect(self.Open)

        save = QWidgetAction(self)
        save.setDefaultWidget(QLabel("    Save    "));

        newtab = QWidgetAction(self)
        newtab.setDefaultWidget(QLabel("    New File    "));
        newtab.triggered.connect(self.NewTab)

        self.menuBar = QMenuBar(self)
        self.menuBar.setStyleSheet("* { border: none; }")
        file = self.menuBar.addMenu("File")

        file.addAction(open)
        file.addAction(save)
        file.addAction(newtab)

        self.tab = QTextEdit(self)
        self.tabWidget = TabWidget()
        self.tabWidget.addTab(self.tab, 'New File')
        self.tab = textHighlight(self.tab.document())

        layout.addWidget(self.menuBar)
        layout.addWidget(self.tabWidget)

        self.setLayout(layout)

    def NewTab(self, widget):
        self._tab = QTextEdit(self)
        self.tabWidget.addTab(self._tab, 'New File')
        self._tab = textHighlight(self._tab.document())

    def closeEvent(self, event):

        def closed():
            self.reply.close()

        self.reply = QDialog()
        vbox = QVBoxLayout()
        label_dialog = QLabel()
        label_dialog.setText('Do you want to save the file?')
        button_yes = QPushButton(self.reply)
        button_yes.setText("Yes")
        button_yes.clicked.connect(self.SaveAndExit)
        button_no = QPushButton(self.reply)
        button_no.setText('No')
        button_no.clicked.connect(closed)

        layout = QHBoxLayout()
        layout.addWidget(button_yes)
        layout.addWidget(button_no)

        vbox.addWidget(label_dialog)
        vbox.addLayout(layout)
        self.reply.setLayout(vbox)
        self.reply.exec()

    def Open(self):
        filename = QtWidgets.QFileDialog.getOpenFileName(self, 'Open File', ".", "(*.*)All Files")[0]
        if filename == '':
            return
        else:
            f = open(filename, 'r', encoding='utf-8')
            file = f.read()
            self.tabWidget.currentWidget().setText(file)
            f.close()

    def Save(self):
        filename = QtWidgets.QFileDialog.getSaveFileName(self, 'Save File', ".", "(*.*)All Files")[0]
        if filename == '':
            FramelessWindow()
        else:
            f = open(filename, 'w')
            file = self.tabWidget.currentWidget().toPlainText()
            f.write(file)
            f.close()

    def SaveAndExit(self):
    	filename = QtWidgets.QFileDialog.getSaveFileName(self, 'Save File', ".", "(*.*)All Files")[0]
    	if filename == '':
            self.reply.close()
    	else:
            f = open(filename, 'w')
            file = self.tabWidget.currentWidget().toPlainText()
            f.write(file)
            f.close()
            self.reply.close()

class textHighlight(QSyntaxHighlighter):
    def highlightBlock(self, text):
        sym_await = QTextCharFormat()
        sym_await.setForeground(QColor("#ff2b2b"))

        it = QRegularExpression(r"\b(await|new|for|of|return|if|!|>)\b").globalMatch(text)
        while it.hasNext():
            match = it.next()
            self.setFormat(match.capturedStart(), match.capturedLength(), sym_await)

        sym_const = QTextCharFormat()
        sym_const.setForeground(QColor("#00bfff"))

        it = QRegularExpression(r"\b(const|require|save|Discord|parseInt|fetch|then|setDescription|let|var|global|push|set|get|console.log|once|async|fetch)\b").globalMatch(text)
        while it.hasNext():
            match = it.next()
            self.setFormat(match.capturedStart(), match.capturedLength(), sym_const)

        sym_boolean = QTextCharFormat()
        sym_boolean.setForeground(QColor("#8a2be2"))

        it = QRegularExpression(r"\b(true|false)\b").globalMatch(text)
        while it.hasNext():
            match = it.next()
            self.setFormat(match.capturedStart(), match.capturedLength(), sym_boolean)

        sym_arg = QTextCharFormat()
        sym_arg.setForeground(QColor("#ff9900"))

        it = QRegularExpression(r"\b(client|message)\b").globalMatch(text)
        while it.hasNext():
            match = it.next()
            self.setFormat(match.capturedStart(), match.capturedLength(), sym_arg)

if __name__ == '__main__':
    app = QApplication(sys.argv)

    w = CodeEditor()
    w.setGeometry(100, 150, 600, 500)
    w.setWindowTitle('Code Editor v1.0 by kolami')

    with open("style.css", "r") as style:
        app.setStyleSheet(style.read())

    w.show()
    sys.exit(app.exec_())