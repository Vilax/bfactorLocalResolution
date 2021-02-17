from PyQt5 import QtWidgets, QtGui, QtCore, uic
from PyQt5.QtWidgets import QFileDialog
import sys
import os
import icons
from subprocess import Popen
from libraries.analyzeResults import Ui_AnalyzeResults
from libraries.scriptFunctions import launchXmippScript, launchChimeraSCript, addcolonmrc
import configparser
from libraries import icons


class Ui(QtWidgets.QMainWindow):
    # TODO: fix the help
    def __init__(self):
        super(Ui, self).__init__()
        uic.loadUi('GUI/mainwindow_bfactor.ui', self)

        configFile = configparser.ConfigParser()
        configFile.read('config.ini')

        self.xmippPath = configFile['EXTERNAL_PROGRAMS']['XMIPP_PATH']
        self.chimeraPath = None

        self.pathApp = os.getcwd()
        self.resultsPath = self.pathApp + "/results/"

        # Path line and path button
        self.linePathDir = self.findChild(QtWidgets.QLineEdit, 'linePath')
        self.linePathDir.setText(self.pathApp)
        self.pathButton = self.findChild(QtWidgets.QPushButton, 'buttonPath')
        self.pathButton.clicked.connect(self.browsePath)

        # Lab website button
        self.xmippButton = self.findChild(QtWidgets.QPushButton, 'buttonXmipp')
        self.xmippButton.clicked.connect(self.labwebsite)

        # Help button
        self.helpButton = self.findChild(QtWidgets.QPushButton, 'buttonHelp')
        self.helpButton.clicked.connect(self.helpApp)

        # Cite button
        self.citeButton = self.findChild(QtWidgets.QPushButton, 'buttonCite')
        self.citeButton.clicked.connect(self.cite)

        # Local Resolution Map
        self.browseLocRes = self.findChild(QtWidgets.QPushButton, 'ButtonLocRes')
        self.viewLocRes = self.findChild(QtWidgets.QPushButton, 'ButtonViewLocRes')
        self.viewLocRes.clicked.connect(lambda: self.showSlices(self.lineLocRes.text()))
        self.browseLocRes.clicked.connect(self.setLocRes)
        self.lineResMap = self.findChild(QtWidgets.QLineEdit, 'lineLocRes')

        # Atomic Model
        self.browsePDB = self.findChild(QtWidgets.QPushButton, 'ButtonAtModel')
        self.browsePDB.clicked.connect(self.setPDB)
        self.lineAtModel = self.findChild(QtWidgets.QLineEdit, 'linePDB')



        # Sampling rate
        self.lineSampling.setText("1")

        ## ACTIONS
        # Execute Button and Analyze
        self.execute = self.findChild(QtWidgets.QPushButton, 'executeButton')
        self.execute.clicked.connect(self.runButton)
        self.analyze = self.findChild(QtWidgets.QPushButton, 'resultsButton')
        self.analyze.clicked.connect(self.analyzeButton)

        # Compute the normalized resolution
        self.checkNormalizeYes = self.findChild(QtWidgets.QCheckBox, 'checkNormalize')
        self.checkNormalizeYes.toggled.connect(self.passToggledNormalize)

        self.checkNormalizeYes.setChecked(True)

        self.labelFSCNormalize.show()
        self.lineFSC.show()

        ## ADVANCE PARAMETERS
        # Checkbox Use median
        self.checkMedian_Yes = self.findChild(QtWidgets.QRadioButton, 'checkMedianYes')
        self.checkMedian_No = self.findChild(QtWidgets.QRadioButton, 'checkMedianNo')
        self.checkMedian_Yes.toggled.connect(self.passToggledMedian)
        self.checkMedian_No.toggled.connect(self.passToggledMedian)

        self.show()

    def passToggledNormalize(self):
        if self.checkNormalizeYes.isChecked():
            self.labelFSCNormalize.show()
            self.lineFSC.show()
        else:
            self.labelFSCNormalize.hide()
            self.lineFSC.hide()

    
    def passToggledMedian(self):
        if self.checkMedian_Yes.isChecked():
            self.labelFSCNormalize.show()
            self.lineFSC.show()
        else:
            self.labelFSCNormalize.hide()
            self.lineFSC.hide()
    

    def browsePath(self):
        self.pathApp = QFileDialog.getExistingDirectory(self, "Set working directory",
                                                        QtCore.QCoreApplication.applicationDirPath())
        self.linePathDir.setText(self.pathApp)
        self.resultsPath = self.pathApp + "/results/"

    def labwebsite(self):
        QtGui.QDesktopServices.openUrl(QtCore.QUrl("http://wwwuser.cnb.csic.es/~jrcaston/Caston-lab/Home.html"))

    def helpApp(self):
        QtWidgets.QMessageBox.about(self, "About bfactor-local resolution",
                                    "<b>B factor</b><br>"
                                    "<small>This program may be used t.</small><br>"
                                    "<br>"
                                    "<b> Local Resolution </b><br>"
                                    "<small> Local Resolution. </small><br>"
                                    "<br>");

    def cite(self):
        QtWidgets.QMessageBox.about(self, "Reference of the algorithm",
                                    "Reference: Authors, et. at, , Journal, XX, X, XX-XX (2021)")

    def setLocRes(self):
        pathlineMap1 = QFileDialog.getOpenFileName(self, "Select Local Resolution Map", self.pathApp)
        self.lineLocRes.setText(pathlineMap1[0])

    def setPDB(self):
        pathlineMap2 = QFileDialog.getOpenFileName(self, "Select a pdb file", self.pathApp)
        self.linePDB.setText(pathlineMap2[0])

    def showSlices(self, fn):
        pass

    def runButton(self):
        xmippCmdline, params = self.createXmippScript()

        if not os.path.exists(self.resultsPath):
            os.makedirs(self.resultsPath)

        xmippCmdline = xmippCmdline + " " + params

        os.environ['XMIPP_HOME'] = self.xmippPath
        os.environ['PATH'] = self.xmippPath + '/bin' + ':' + os.environ['PATH']
        os.environ['LD_LIBRARY_PATH'] = self.xmippPath + '/lib' + ':' + os.environ['LD_LIBRARY_PATH']
        print(xmippCmdline)
        os.system(xmippCmdline)

        self.analyze.setEnabled(True)

    def analyzeButton(self):
        self.window = QtWidgets.QMainWindow()
        self.ui = Ui_AnalyzeResults(self.chimeraPath, self.resultsPath)

    def createXmippScript(self):
        program = "xmipp_resolution_pdb_bfactor" \
                  " "

        ## Normal Parameters
        params = " --atmodel %s" % addcolonmrc(self.lineAtModel.text())
        params += " --vol %s" % addcolonmrc(self.lineResMap.text())
        params += " --sampling %s" % self.lineSampling.text()

        ## Advanced Parameters
        if self.checkMedian_Yes.isChecked():
            params += " --median "

        if self.checkNormalizeYes.isChecked():
            params += " --fscResolution %s" % self.lineFSC.text()

        ## output
        params += ' -o %s' % self.resultsPath

        return program, params

app = QtWidgets.QApplication(sys.argv)
window = Ui()
app.exec_()
