# -*- coding: utf-8 -*-
"""
Created on Fri Jan  8 13:21:40 2016

@author: root
"""

import sys
from PyQt4 import QtGui, QtCore
import numpy


from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure

class MyMplCanvas(FigureCanvas):
    
    def __init__(self, parent=None, width=5, height=4, dpi=100):
        fig = Figure(figsize=(width, height), dpi=dpi)
        self.axes = fig.add_subplot(111)

        self.axes.hold(False)

        self.compute_initial_figure()

        FigureCanvas.__init__(self, fig)
        self.setParent(parent)

        FigureCanvas.setSizePolicy(self,
                                   QtGui.QSizePolicy.Expanding,
                                   QtGui.QSizePolicy.Expanding)
        FigureCanvas.updateGeometry(self)

    def compute_initial_figure(self):
        pass

class MyStaticMplCanvas(MyMplCanvas):

    def compute_initial_figure(self):
        x = numpy.linspace(-15,15,100)
        y = 3*x+2
        self.axes.plot(x, y)

class MyDialog(QtGui.QDialog):
    def __init__(self, parent=None):
        super(MyDialog, self).__init__(parent)

        self.buttonBox = QtGui.QDialogButtonBox(self)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)

        self.buttonBox.accepted.connect(self.accept)
        self.buttonBox.rejected.connect(self.reject)
     
        self.textEdit = QtGui.QTextEdit(self)
        self.textEdit.setPlainText("Enter your slope and intercept here!")
        slope = self.textEdit.toPlainText()

        self.verticalLayout = QtGui.QVBoxLayout(self)
        self.verticalLayout.addWidget(self.textEdit)
        self.verticalLayout.addWidget(self.buttonBox)
        
class Example(QtGui.QWidget):
    
    def __init__(self):
        super(Example, self).__init__()
        
        self.initUI()
        
    def initUI(self):
        
        ##########################
        # Buttons to apply changes
        ##########################
        
        edit_inv = QtGui.QPushButton('Edit Invoiced', self)
        edit_inv.clicked.connect(self.editButtonClicked)
        edit_inv.resize(edit_inv.sizeHint())
        edit_inv.move(50, 160)   
        
        edit_book = QtGui.QPushButton('Edit Booked', self)
        edit_book.clicked.connect(self.editButtonClicked)
        edit_book.resize(edit_book.sizeHint())
        edit_book.move(50, 360)       
        
        edit_units = QtGui.QPushButton('Edit Units', self)
        edit_units.clicked.connect(self.editButtonClicked)
        edit_units.resize(edit_units.sizeHint())
        edit_units.move(50, 560)       
        
        btn = QtGui.QPushButton('Apply', self)
        btn.clicked.connect(self.applyaction)
        btn.resize(btn.sizeHint())
        btn.move(50, 190)   
        
        btn1 = QtGui.QPushButton('Apply', self)
        btn1.clicked.connect(self.applyaction)
        btn1.resize(btn.sizeHint())
        btn1.move(50, 390)       
        
        btn2 = QtGui.QPushButton('Apply', self)
        btn2.clicked.connect(self.applyaction)
        btn2.resize(btn.sizeHint())
        btn2.move(50, 590)       

        self.dialogTextBrowser = MyDialog(self)
            
        #######################################
        # Drop-down menu to select object level
        #######################################
        combo = QtGui.QComboBox(self)
        combo.addItem("Domain")
        combo.addItem("Kingdom")
        combo.addItem("Class")
        combo.addItem("Family")
        combo.addItem("Genus")
        combo.addItem("Species")
        combo.move(790, 10)
        
        #######################################
        # Drop-down menu to select object level
        #######################################
        combo = QtGui.QComboBox(self)
        combo.addItem("All")
        combo.addItem("Invoiced")
        combo.addItem("Booked")
        combo.addItem("Units")
        combo.move(790, 50)
        
        ###################################
        # Text boxes to submit date changes
        ###################################
        
        date = QtGui.QLineEdit(self)
        date.setPlaceholderText("mm/dd/yyyy")
        date.setEnabled(True)
        date.move(50, 130)

        date1 = QtGui.QLineEdit(self)
        date1.setPlaceholderText("mm/dd/yyyy")
        date1.setEnabled(True)
        date1.move(50, 330)
        
        date2 = QtGui.QLineEdit(self)
        date2.setPlaceholderText("mm/dd/yyyy")
        date2.setEnabled(True)
        date2.move(50, 530)

        #########################
        # Labels for change boxes
        #########################      
        
        lbl = QtGui.QLabel('Invoiced', self)
        lbl.move(50, 110)
        
        lbl1 = QtGui.QLabel('Booked', self)
        lbl1.move(50, 310)
        
        lbl2 = QtGui.QLabel('Units', self)
        lbl2.move(50, 510)
        
        ###############################
        # Embed plots for each forecast
        ###############################
        invoices = QtGui.QWidget(self)
        l = QtGui.QVBoxLayout(invoices)
        sc = MyStaticMplCanvas(invoices, width=5, height=4, dpi=100)
        l.addWidget(sc)
        invoices.resize(500,225)
        invoices.move(250, 10)
        
        booked = QtGui.QWidget(self)
        l = QtGui.QVBoxLayout(booked)
        sc = MyStaticMplCanvas(booked, width=5, height=4, dpi=100)
        l.addWidget(sc)
        booked.resize(500,225)
        booked.move(250, 240)
        
        units = QtGui.QWidget(self)
        l = QtGui.QVBoxLayout(units)
        sc = MyStaticMplCanvas(units, width=5, height=4, dpi=100)
        l.addWidget(sc)
        units.resize(500,225)
        units.move(250, 470)

        #########################################
        # Resize, center, title main window
        #########################################
        self.resize(900, 700)
        self.center()
        self.setWindowTitle('Graph Editor') 
                    

    def center(self):
        
        qr = self.frameGeometry()
        cp = QtGui.QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())
        
    @QtCore.pyqtSlot()
    def editButtonClicked(self):
        self.dialogTextBrowser.exec_()
    
    def applyaction(self, event):
    
        reply = QtGui.QMessageBox.question(self, 'Message',
            "Are you sure want to apply changes?", QtGui.QMessageBox.Yes | 
            QtGui.QMessageBox.No, QtGui.QMessageBox.No)
    
        if reply == QtGui.QMessageBox.Yes:
            event.accept()
        else:
            event.ignore() 
        
def main():
    app = QtGui.QApplication(sys.argv)
    ex = Example()
    ex.show() 
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()