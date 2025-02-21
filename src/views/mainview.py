# Form implementation generated from reading ui file 'src/views/mainwindow.ui'
#
# Created by: PyQt6 UI code generator 6.8.1
#
# WARNING: Any manual changes made to this file will be lost when pyuic6 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt6 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1321, 850)
        self.centralwidget = QtWidgets.QWidget(parent=MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.Iterations = QtWidgets.QPlainTextEdit(parent=self.centralwidget)
        self.Iterations.setGeometry(QtCore.QRect(9, 45, 300, 591))
        self.Iterations.setMinimumSize(QtCore.QSize(300, 0))
        self.Iterations.setMaximumSize(QtCore.QSize(300, 16777215))
        self.Iterations.setReadOnly(True)
        self.Iterations.setObjectName("Iterations")
        self.ExecuteButton = QtWidgets.QPushButton(parent=self.centralwidget)
        self.ExecuteButton.setGeometry(QtCore.QRect(9, 801, 121, 40))
        self.ExecuteButton.setMinimumSize(QtCore.QSize(0, 40))
        self.ExecuteButton.setMaximumSize(QtCore.QSize(150, 16777215))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.ExecuteButton.setFont(font)
        self.ExecuteButton.setStyleSheet("")
        self.ExecuteButton.setObjectName("ExecuteButton")
        self.SpecificMethod = QtWidgets.QComboBox(parent=self.centralwidget)
        self.SpecificMethod.setGeometry(QtCore.QRect(9, 9, 300, 30))
        self.SpecificMethod.setMinimumSize(QtCore.QSize(300, 0))
        self.SpecificMethod.setMaximumSize(QtCore.QSize(300, 16777215))
        font = QtGui.QFont()
        font.setPointSize(11)
        self.SpecificMethod.setFont(font)
        self.SpecificMethod.setObjectName("SpecificMethod")
        self.SpecificMethod.addItem("")
        self.verticalLayoutWidget = QtWidgets.QWidget(parent=self.centralwidget)
        self.verticalLayoutWidget.setGeometry(QtCore.QRect(330, 40, 521, 521))
        self.verticalLayoutWidget.setObjectName("verticalLayoutWidget")
        self.Plot = QtWidgets.QVBoxLayout(self.verticalLayoutWidget)
        self.Plot.setContentsMargins(0, 0, 0, 0)
        self.Plot.setObjectName("Plot")
        self.layoutWidget = QtWidgets.QWidget(parent=self.centralwidget)
        self.layoutWidget.setGeometry(QtCore.QRect(860, 40, 371, 571))
        self.layoutWidget.setObjectName("layoutWidget")
        self.Options = QtWidgets.QVBoxLayout(self.layoutWidget)
        self.Options.setContentsMargins(0, 0, 0, 0)
        self.Options.setObjectName("Options")
        self.widget = QtWidgets.QWidget(parent=self.centralwidget)
        self.widget.setGeometry(QtCore.QRect(10, 720, 301, 62))
        self.widget.setObjectName("widget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.widget)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.label = QtWidgets.QLabel(parent=self.widget)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.label.setFont(font)
        self.label.setObjectName("label")
        self.verticalLayout.addWidget(self.label)
        self.Function = QtWidgets.QLineEdit(parent=self.widget)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.Function.setFont(font)
        self.Function.setObjectName("Function")
        self.verticalLayout.addWidget(self.Function)
        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.ExecuteButton.setText(_translate("MainWindow", "Запустить"))
        self.SpecificMethod.setItemText(0, _translate("MainWindow", "Градиентный спуск"))
        self.label.setText(_translate("MainWindow", "Функция:"))
        self.Function.setText(_translate("MainWindow", "x**2 + x * y + y ** 2"))
