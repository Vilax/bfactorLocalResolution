#!../env/bin/python3
# -*- coding: utf-8 -*-
"""
Created on Thu Apr 30 15:46:30 2020

@author: vilas
"""

from PyQt5 import QtWidgets, uic
# from PyQt5.QtWidgets import QFileDialog
from libraries.plotWindow import PlotLocalResolution_Bfactor

# import os
import icons
# from confPaths import confPaths

class Ui_AnalyzeResults(QtWidgets.QDialog):
    def __init__(self, chimeraPath, resultsPath, limlow, limup):
        super(Ui_AnalyzeResults, self).__init__()
        #uic.loadUi('GUI/analyzewindow_v0.ui', self)
        self.chimeraPath = chimeraPath
        self.resultsPath = resultsPath
        self.limlower = limlow
        self.limupper = limup
        
        #self.show()

        self.window = QtWidgets.QMainWindow()
        pathFile = self.resultsPath + 'bfactor_resolution.xmd'
        labelX_Residue = "Residue"
        labelY_bfactor = "bfactor (A)"
        labelY_locres  = "Local Resolution (1/A)"
        residue = '_residue'
        BFactor = '_bFactor'
        localResolution = '_localresolutionResidue'

        title = 'Local Resolution - bfactor'
        self.ui = PlotLocalResolution_Bfactor(pathFile,  residue, BFactor, localResolution, labelX_Residue, labelY_bfactor, labelY_locres, title, self.limlower, self.limupper)
