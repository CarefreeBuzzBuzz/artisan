# -*- coding: utf-8 -*-
#
# ABOUT
# Artisan Template Background Dialog

# LICENSE
# This program or module is free software: you can redistribute it and/or
# modify it under the terms of the GNU General Public License as published
# by the Free Software Foundation, either version 2 of the License, or
# version 3 of the License, or (at your option) any later version. It is
# provided for educational purposes and is distributed in the hope that
# it will be useful, but WITHOUT ANY WARRANTY; without even the implied
# warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See
# the GNU General Public License for more details.

# AUTHOR
# Marko Luther, 2020

import platform

from artisanlib.util import deltaLabelUTF8, deltaLabelPrefix, stringfromseconds
from artisanlib.dialogs import ArtisanResizeablDialog

try:
    #pylint: disable = E, W, R, C
    from PyQt6.QtCore import (Qt, pyqtSlot, QSettings) # @UnusedImport @Reimport  @UnresolvedImport
    from PyQt6.QtGui import QColor, QKeySequence # @UnusedImport @Reimport  @UnresolvedImport
    from PyQt6.QtWidgets import (QApplication, QCheckBox, QGridLayout, QHBoxLayout, QVBoxLayout, # @UnusedImport @Reimport  @UnresolvedImport
                                 QLabel, QLineEdit,QPushButton, QComboBox, QDialogButtonBox, QHeaderView, # @UnusedImport @Reimport  @UnresolvedImport
                                 QSpinBox, QTableWidget, QTableWidgetItem, QTabWidget, QWidget) # @UnusedImport @Reimport  @UnresolvedImport
except Exception:
    #pylint: disable = E, W, R, C
    from PyQt5.QtCore import (Qt, pyqtSlot, QSettings) # @UnusedImport @Reimport  @UnresolvedImport
    from PyQt5.QtGui import QColor, QKeySequence # @UnusedImport @Reimport  @UnresolvedImport
    from PyQt5.QtWidgets import (QApplication, QCheckBox, QGridLayout, QHBoxLayout, QVBoxLayout, # @UnusedImport @Reimport  @UnresolvedImport
                                 QLabel, QLineEdit,QPushButton, QComboBox, QDialogButtonBox, QHeaderView, # @UnusedImport @Reimport  @UnresolvedImport
                                 QSpinBox, QTableWidget, QTableWidgetItem, QTabWidget, QWidget) # @UnusedImport @Reimport  @UnresolvedImport

class backgroundDlg(ArtisanResizeablDialog):
    def __init__(self, parent = None, aw = None, activeTab = 0):
        super().__init__(parent, aw)
        self.setWindowTitle(QApplication.translate("Form Caption","Profile Background"))
        self.setModal(True)
        
        settings = QSettings()
        if settings.contains("BackgroundGeometry"):
            self.restoreGeometry(settings.value("BackgroundGeometry"))
        
        #TAB 1
        self.pathedit = QLineEdit(self.aw.qmc.backgroundpath)
        self.pathedit.setStyleSheet("background-color:'lightgrey';")
        self.pathedit.setReadOnly(True)
        self.pathedit.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        self.filename = ""
        self.backgroundCheck = QCheckBox(QApplication.translate("CheckBox","Show"))
        self.backgroundDetails = QCheckBox(QApplication.translate("CheckBox","Annotations"))
        self.backgroundeventsflag = QCheckBox(QApplication.translate("CheckBox","Events"))
        self.backgroundDeltaETflag = QCheckBox()
        backgroundDeltaETflagLabel = QLabel(deltaLabelPrefix + QApplication.translate("Label","ET"))
        self.backgroundDeltaBTflag = QCheckBox()
        backgroundDeltaBTflagLabel = QLabel(deltaLabelPrefix + QApplication.translate("Label","BT"))
        self.backgroundETflag = QCheckBox(QApplication.translate("CheckBox","ET"))
        self.backgroundBTflag = QCheckBox(QApplication.translate("CheckBox","BT"))
        self.backgroundFullflag = QCheckBox(QApplication.translate("CheckBox","Show Full"))
        self.backgroundCheck.setChecked(self.aw.qmc.background)
        self.backgroundDetails.setChecked(self.aw.qmc.backgroundDetails)
        self.backgroundeventsflag.setChecked(self.aw.qmc.backgroundeventsflag)
        self.backgroundDeltaETflag.setChecked(self.aw.qmc.DeltaETBflag)
        self.backgroundDeltaBTflag.setChecked(self.aw.qmc.DeltaBTBflag)
        self.backgroundETflag.setChecked(self.aw.qmc.backgroundETcurve)
        self.backgroundBTflag.setChecked(self.aw.qmc.backgroundBTcurve)
        self.backgroundFullflag.setChecked(self.aw.qmc.backgroundShowFullflag)
        loadButton = QPushButton(QApplication.translate("Button","Load"))
        loadButton.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        delButton = QPushButton(QApplication.translate("Button","Delete"))
        delButton.setFocusPolicy(Qt.FocusPolicy.NoFocus)

        # connect the ArtisanDialog standard OK/Cancel buttons
        self.dialogbuttons.accepted.connect(self.accept)
        self.dialogbuttons.removeButton(self.dialogbuttons.button(QDialogButtonBox.StandardButton.Cancel))
        
        alignButton = QPushButton(QApplication.translate("Button","Align"))
        alignButton.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        self.alignComboBox = QComboBox()
        alignnames = [
            QApplication.translate("Label","CHARGE"),
            QApplication.translate("Label","DRY"),
            QApplication.translate("Label","FCs"),
            QApplication.translate("Label","FCe"),
            QApplication.translate("Label","SCs"),
            QApplication.translate("Label","SCe"),
            QApplication.translate("Label","DROP"),
            QApplication.translate("Label","ALL"),
            ]
        self.alignComboBox.addItems(alignnames)
        self.alignComboBox.setCurrentIndex(self.aw.qmc.alignEvent)
        self.alignComboBox.currentIndexChanged.connect(self.changeAlignEventidx)
        loadButton.clicked.connect(self.load)
        alignButton.clicked.connect(self.timealign)
        
        self.speedSpinBox = QSpinBox()
        self.speedSpinBox.setAlignment(Qt.AlignmentFlag.AlignRight)
        self.speedSpinBox.setRange(1,90)
        self.speedSpinBox.setSingleStep(5)
        self.speedSpinBox.setValue(self.aw.qmc.backgroundmovespeed)
        
        curvenames = [""] # first entry is the empty one, no extra curve displayed
        for i in range(min(len(self.aw.qmc.extraname1B),len(self.aw.qmc.extraname2B),len(self.aw.qmc.extratimexB))):
            curvenames.append("B" + str(2*i+3) + ": " + self.aw.qmc.extraname1B[i])
            curvenames.append("B" + str(2*i+4) + ": " + self.aw.qmc.extraname2B[i])

        self.xtcurvelabel = QLabel(QApplication.translate("Label", "Extra 1"))
        self.xtcurveComboBox = QComboBox()
        self.xtcurveComboBox.setToolTip(QApplication.translate("Tooltip","For loaded backgrounds with extra devices only"))
        self.xtcurveComboBox.setMinimumWidth(120)
        self.xtcurveComboBox.addItems(curvenames)
        if self.aw.qmc.xtcurveidx < len(curvenames):
            self.xtcurveComboBox.setCurrentIndex(self.aw.qmc.xtcurveidx)
        self.xtcurveComboBox.currentIndexChanged.connect(self.changeXTcurveidx)

        self.ytcurvelabel = QLabel(QApplication.translate("Label", "Extra 2"))
        self.ytcurveComboBox = QComboBox()
        self.ytcurveComboBox.setToolTip(QApplication.translate("Tooltip","For loaded backgrounds with extra devices only"))
        self.ytcurveComboBox.setMinimumWidth(120)
        self.ytcurveComboBox.addItems(curvenames)
        if self.aw.qmc.ytcurveidx < len(curvenames):
            self.ytcurveComboBox.setCurrentIndex(self.aw.qmc.ytcurveidx)
        self.ytcurveComboBox.currentIndexChanged.connect(self.changeYTcurveidx)
        
        self.upButton = QPushButton(QApplication.translate("Button","Up"))
        self.upButton.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        self.downButton = QPushButton(QApplication.translate("Button","Down"))
        self.downButton.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        self.leftButton = QPushButton(QApplication.translate("Button","Left"))
        self.leftButton.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        self.rightButton = QPushButton(QApplication.translate("Button","Right"))
        self.rightButton.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        self.backgroundCheck.clicked.connect(self.readChecks)
        self.backgroundDetails.clicked.connect(self.readChecks)
        self.backgroundeventsflag.clicked.connect(self.readChecks)
        self.backgroundDeltaETflag.clicked.connect(self.readChecks)
        self.backgroundDeltaBTflag.clicked.connect(self.readChecks)
        self.backgroundETflag.clicked.connect(self.readChecks)
        self.backgroundBTflag.clicked.connect(self.readChecks)
        self.backgroundFullflag.clicked.connect(self.readChecks)
        delButton.clicked.connect(self.delete)
        self.upButton.clicked.connect(self.moveUp)
        self.downButton.clicked.connect(self.moveDown)
        self.leftButton.clicked.connect(self.moveLeft)
        self.rightButton.clicked.connect(self.moveRight)
        #TAB 2 EVENTS
        #table for showing events
        self.eventtable = QTableWidget()
        self.eventtable.setTabKeyNavigation(True)
        self.createEventTable()
        self.copyeventTableButton = QPushButton(QApplication.translate("Button", "Copy Table"))
        self.copyeventTableButton.setToolTip(QApplication.translate("Tooltip","Copy table to clipboard, OPTION or ALT click for tabular text"))
        self.copyeventTableButton.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        self.copyeventTableButton.setMaximumSize(self.copyeventTableButton.sizeHint())
        self.copyeventTableButton.setMinimumSize(self.copyeventTableButton.minimumSizeHint())
        self.copyeventTableButton.clicked.connect(self.copyEventTabletoClipboard)
        #TAB 3 DATA
        #table for showing data
        self.datatable = QTableWidget()
        self.datatable.setTabKeyNavigation(True)
        self.createDataTable()
        self.copydataTableButton = QPushButton(QApplication.translate("Button", "Copy Table"))
        self.copydataTableButton.setToolTip(QApplication.translate("Tooltip","Copy table to clipboard, OPTION or ALT click for tabular text"))
        self.copydataTableButton.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        self.copydataTableButton.setMaximumSize(self.copydataTableButton.sizeHint())
        self.copydataTableButton.setMinimumSize(self.copydataTableButton.minimumSizeHint())
        self.copydataTableButton.clicked.connect(self.copyDataTabletoClipboard)
        #TAB 4
        self.replayComboBox = QComboBox()
        replayVariants = [
            QApplication.translate("Label","by time"),
            QApplication.translate("Label","by BT"),
            QApplication.translate("Label","by ET"),
            ]
        self.replayComboBox.addItems(replayVariants)
        self.replayComboBox.setCurrentIndex(self.aw.qmc.replayType)
        self.replayComboBox.currentIndexChanged.connect(self.changeReplayTypeidx)
                
        self.backgroundReproduce = QCheckBox(QApplication.translate("CheckBox","Playback Aid"))
        self.backgroundReproduce.setChecked(self.aw.qmc.backgroundReproduce)
        self.backgroundReproduce.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        self.backgroundReproduce.stateChanged.connect(self.setreproduce)
        self.backgroundReproduceBeep = QCheckBox(QApplication.translate("CheckBox","Beep"))
        self.backgroundReproduceBeep.setChecked(self.aw.qmc.backgroundReproduceBeep)
        self.backgroundReproduceBeep.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        self.backgroundReproduceBeep.stateChanged.connect(self.setreproduceBeep)
        self.backgroundPlaybackEvents = QCheckBox(QApplication.translate("CheckBox","Playback Events"))
        self.backgroundPlaybackEvents.setChecked(self.aw.qmc.backgroundPlaybackEvents)
        self.backgroundPlaybackEvents.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        self.backgroundPlaybackEvents.stateChanged.connect(self.setplaybackevent)
        self.backgroundPlaybackDROP = QCheckBox(QApplication.translate("CheckBox","Playback DROP"))
        self.backgroundPlaybackDROP.setChecked(self.aw.qmc.backgroundPlaybackDROP)
        self.backgroundPlaybackDROP.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        self.backgroundPlaybackDROP.stateChanged.connect(self.setplaybackdrop)
        etimelabel =QLabel(QApplication.translate("Label", "Text Warning"))
        etimeunit =QLabel(QApplication.translate("Label", "sec"))
        self.etimeSpinBox = QSpinBox()
        self.etimeSpinBox.setRange(1,60)
        self.etimeSpinBox.setValue(self.aw.qmc.detectBackgroundEventTime)
        self.etimeSpinBox.valueChanged.connect(self.setreproduce)
        self.clearBgbeforeprofileload = QCheckBox(QApplication.translate("CheckBox","Clear the background before loading a new profile"))
        self.clearBgbeforeprofileload.setChecked(self.aw.qmc.clearBgbeforeprofileload)
        self.clearBgbeforeprofileload.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        self.clearBgbeforeprofileload.stateChanged.connect(self.optclearbgbeforeprofileload)
        self.hideBgafterprofileload = QCheckBox(QApplication.translate("CheckBox","Always hide background when loading a profile"))
        self.hideBgafterprofileload.setChecked(self.aw.qmc.hideBgafterprofileload)
        self.hideBgafterprofileload.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        self.hideBgafterprofileload.stateChanged.connect(self.opthideBgafterprofileload)
        
        #LAYOUT MANAGERS
        movelayout = QGridLayout()
        movelayout.addWidget(self.upButton,0,1)
        movelayout.addWidget(self.leftButton,1,0)
        movelayout.addWidget(self.speedSpinBox,1,1)
        movelayout.addWidget(self.rightButton,1,2)
        movelayout.addWidget(self.downButton,2,1)
        movelayout.setSpacing(20)
        checkslayout1 = QHBoxLayout()
        checkslayout1.addStretch()
        checkslayout1.addWidget(self.backgroundCheck)
        checkslayout1.addSpacing(5)
        checkslayout1.addWidget(self.backgroundDetails)
        checkslayout1.addSpacing(5)
        checkslayout1.addWidget(self.backgroundeventsflag)
        checkslayout1.addSpacing(5)
        checkslayout1.addWidget(self.backgroundETflag)
        checkslayout1.addSpacing(5)
        checkslayout1.addWidget(self.backgroundBTflag)
        checkslayout1.addSpacing(5)
        checkslayout1.addWidget(self.backgroundDeltaETflag)
        checkslayout1.addSpacing(3)
        checkslayout1.addWidget(backgroundDeltaETflagLabel)
        checkslayout1.addSpacing(5)
        checkslayout1.addWidget(self.backgroundDeltaBTflag)
        checkslayout1.addSpacing(3)
        checkslayout1.addWidget(backgroundDeltaBTflagLabel)
        checkslayout1.addSpacing(5)
        checkslayout1.addWidget(self.backgroundFullflag)
        checkslayout1.addStretch()
        layout = QGridLayout()
        layoutBoxedH = QHBoxLayout()
        layoutBoxedH.addStretch()
        layoutBoxedH.addLayout(movelayout)
        layoutBoxedH.addLayout(layout)
        layoutBoxedH.addStretch()
        layoutBoxed = QVBoxLayout()
        layoutBoxed.addStretch()
        layoutBoxed.addLayout(checkslayout1)
        layoutBoxed.addStretch()
        layoutBoxed.addLayout(layoutBoxedH)
        layoutBoxed.addStretch()
        alignButtonBoxed = QHBoxLayout()
        alignButtonBoxed.addWidget(self.xtcurvelabel)
        alignButtonBoxed.addWidget(self.xtcurveComboBox)
        alignButtonBoxed.addSpacing(10)
        alignButtonBoxed.addWidget(self.ytcurvelabel)
        alignButtonBoxed.addWidget(self.ytcurveComboBox)
        alignButtonBoxed.addStretch()
        alignButtonBoxed.addWidget(alignButton)
        alignButtonBoxed.addWidget(self.alignComboBox)
        tab4content = QHBoxLayout()
        tab4content.addWidget(self.backgroundReproduce)
        tab4content.addSpacing(10)
        tab4content.addWidget(self.backgroundReproduceBeep)
        tab4content.addSpacing(10)
        tab4content.addWidget(etimelabel)
        tab4content.addWidget(self.etimeSpinBox)
        tab4content.addWidget(etimeunit)
        tab4content.addSpacing(20)
        tab4content.addStretch()
        tab4content.addWidget(self.backgroundPlaybackEvents)
        tab4content.addSpacing(10)
        tab4content.addWidget(self.backgroundPlaybackDROP)
        tab4content.addSpacing(10)
        tab4content.addWidget(self.replayComboBox)
        optcontent = QHBoxLayout()
        optcontent.addWidget(self.clearBgbeforeprofileload)
        optcontent.addStretch()
        optcontent.addWidget(self.hideBgafterprofileload)
        tab1layout = QVBoxLayout()
        tab1layout.addLayout(layoutBoxed)
#        tab1layout.addStretch()
        tab1layout.addLayout(alignButtonBoxed)
        tab1layout.addLayout(tab4content)
        tab1layout.addLayout(optcontent)
        tab1layout.setContentsMargins(5, 0, 5, 0) # left, top, right, bottom
        eventbuttonLayout = QHBoxLayout()
        eventbuttonLayout.addWidget(self.copyeventTableButton)
        eventbuttonLayout.addStretch()
        tab2layout = QVBoxLayout()
        tab2layout.addWidget(self.eventtable)
        tab2layout.addLayout(eventbuttonLayout)
        tab2layout.setContentsMargins(5, 0, 5, 0) # left, top, right, bottom
        databuttonLayout = QHBoxLayout()
        databuttonLayout.addWidget(self.copydataTableButton)
        databuttonLayout.addStretch()
        tab3layout = QVBoxLayout()
        tab3layout.addWidget(self.datatable)
        tab3layout.addLayout(databuttonLayout)
        tab3layout.setContentsMargins(5, 0, 5, 0) # left, top, right, bottom
        #tab layout
        tab1layout.setSpacing(5)
        self.TabWidget = QTabWidget()
        C1Widget = QWidget()
        C1Widget.setLayout(tab1layout)
        self.TabWidget.addTab(C1Widget,QApplication.translate("Tab","Config"))
        C2Widget = QWidget()
        C2Widget.setLayout(tab2layout)
        self.TabWidget.addTab(C2Widget,QApplication.translate("Tab","Events"))
        C3Widget = QWidget()
        C3Widget.setLayout(tab3layout)
        self.TabWidget.addTab(C3Widget,QApplication.translate("Tab","Data"))
        buttonLayout = QHBoxLayout()
        buttonLayout.addWidget(loadButton)
        buttonLayout.addWidget(delButton)
        buttonLayout.addStretch()
        buttonLayout.addWidget(self.dialogbuttons)
        mainLayout = QVBoxLayout()
        mainLayout.addWidget(self.TabWidget) 
        mainLayout.addWidget(self.pathedit)
        mainLayout.addLayout(buttonLayout)
        mainLayout.setContentsMargins(5, 10, 5, 5) # left, top, right, bottom 
        self.setLayout(mainLayout)
        if platform.system() == 'Windows':
            self.dialogbuttons.button(QDialogButtonBox.StandardButton.Ok)
        else:
            self.dialogbuttons.button(QDialogButtonBox.StandardButton.Ok).setFocus()
        self.TabWidget.setCurrentIndex(activeTab)
    
    @pyqtSlot(bool)
    def timealign(self,_):
        self.aw.qmc.timealign()
    
    #keyboard presses. There must not be widgets (pushbuttons, comboboxes, etc) in focus in order to work 
    def keyPressEvent(self,event):
        if event.matches(QKeySequence.StandardKey.Copy):
            if self.TabWidget.currentIndex() == 2: # datatable
                self.aw.copy_cells_to_clipboard(self.datatable)
                self.aw.sendmessage(QApplication.translate("Message","Data table copied to clipboard"))
        else:
            super().keyPressEvent(event)

    @pyqtSlot()
    def accept(self):
        self.aw.qmc.backgroundmovespeed = self.speedSpinBox.value()
        self.close()
        
    def closeEvent(self,_):
        settings = QSettings()
        #save window geometry
        settings.setValue("BackgroundGeometry",self.saveGeometry())
        self.aw.backgroundDlg_activeTab = self.TabWidget.currentIndex()
#        self.aw.closeEventSettings() # save all app settings
        
    def getColorIdx(self,c):
        try:
            return self.defaultcolorsmapped.index(c)
        except Exception: # pylint: disable=broad-except
            try:
                return self.colors.index(c) + 5
            except Exception:  # pylint: disable=broad-except
                return 0

    @pyqtSlot(int)
    def setplaybackevent(self,_):
        s = None
        if self.backgroundPlaybackEvents.isChecked():
            self.aw.qmc.backgroundPlaybackEvents = True
            msg = QApplication.translate("Message","Playback Events set ON")
        else:
            self.aw.qmc.backgroundPlaybackEvents = False
            msg = QApplication.translate("StatusBar","Playback Events set OFF")
            s = "background-color:'transparent';"
        self.aw.sendmessage(msg, style=s)

    @pyqtSlot(int)
    def setplaybackdrop(self,_):
        s = None
        if self.backgroundPlaybackDROP.isChecked():
            self.aw.qmc.backgroundPlaybackDROP = True
            msg = QApplication.translate("Message","Playback DROP set ON")
        else:
            self.aw.qmc.backgroundPlaybackDROP = False
            msg = QApplication.translate("StatusBar","Playback DROP set OFF")
            s = "background-color:'transparent';"
        self.aw.sendmessage(msg, style=s)
                
    @pyqtSlot(int)
    def setreproduceBeep(self,_):
        if self.backgroundReproduceBeep.isChecked():
            self.aw.qmc.backgroundReproduceBeep = True
        else:
            self.aw.qmc.backgroundReproduceBeep = False

    @pyqtSlot(int)
    def setreproduce(self,_):
        self.aw.qmc.detectBackgroundEventTime = self.etimeSpinBox.value()
        s = None
        if self.backgroundReproduce.isChecked():
            self.aw.qmc.backgroundReproduce = True
            msg = QApplication.translate("Message","Playback Aid set ON at {0} secs").format(str(self.aw.qmc.detectBackgroundEventTime))
        else:
            self.aw.qmc.backgroundReproduce = False
            msg = QApplication.translate("StatusBar","Playback Aid set OFF")
            s = "background-color:'transparent';"
        self.aw.sendmessage(msg, style=s)

    @pyqtSlot(int)
    def optclearbgbeforeprofileload(self,_):
        if self.clearBgbeforeprofileload.isChecked():
            self.aw.qmc.clearBgbeforeprofileload = True
        else:
            self.aw.qmc.clearBgbeforeprofileload = False

    @pyqtSlot(int)
    def opthideBgafterprofileload(self,_):
        if self.hideBgafterprofileload.isChecked():
            self.aw.qmc.hideBgafterprofileload = True
        else:
            self.aw.qmc.hideBgafterprofileload = False

    def adjustcolor(self,curve):
        
        curve = str(curve).lower()

        etcolor = str(self.metcolorComboBox.currentText()).lower()
        btcolor = str(self.btcolorComboBox.currentText()).lower()
        deltabtcolor = str(self.deltabtcolorComboBox.currentText()).lower()
        deltaetcolor = str(self.deltaetcolorComboBox.currentText()).lower()
        xtcolor = str(self.xtcolorComboBox.currentText()).lower()

        defaults =  ["et","bt","deltaet","deltabt"]
        
        if curve == "et":
            if etcolor in defaults:
                self.aw.qmc.backgroundmetcolor = self.aw.qmc.palette[etcolor]
            else:
                self.aw.qmc.backgroundmetcolor = etcolor
                
        elif curve == "bt":
            if btcolor in defaults:
                self.aw.qmc.backgroundbtcolor = self.aw.qmc.palette[btcolor]
            else:
                self.aw.qmc.backgroundbtcolor = btcolor

        elif curve == "deltaet":
            if deltaetcolor in defaults:
                self.aw.qmc.backgrounddeltaetcolor = self.aw.qmc.palette[deltaetcolor]
            else:
                self.aw.qmc.backgrounddeltaetcolor = deltaetcolor
            
        elif curve == "deltabt":
            if deltabtcolor in defaults:
                self.aw.qmc.backgrounddeltabtcolor = self.aw.qmc.palette[deltabtcolor]
            else:
                self.aw.qmc.backgrounddeltabtcolor = deltabtcolor

        elif curve == "xt":
            if xtcolor in defaults:
                self.aw.qmc.backgroundxtcolor = self.aw.qmc.palette[xtcolor]
            else:
                self.aw.qmc.backgroundxtcolor = xtcolor 

        self.aw.qmc.redraw(recomputeAllDeltas=False)

    @pyqtSlot(bool)
    def delete(self,_):
        self.pathedit.setText("")
# we should not overwrite the users app settings here, right:
# but we have to deactivate the show flag
        self.backgroundCheck.setChecked(False)
        self.aw.qmc.background = False
        self.aw.qmc.backgroundprofile = None
        self.xtcurveComboBox.blockSignals(True)
        self.xtcurveComboBox.clear()
        self.aw.deleteBackground()
        self.eventtable.clear()
        self.createEventTable()
        self.createDataTable()
        self.aw.qmc.resetlinecountcaches()
        self.xtcurveComboBox.blockSignals(False)
        self.aw.qmc.redraw(recomputeAllDeltas=False)

    @pyqtSlot(bool)
    def moveUp(self,_):
        self.upButton.setDisabled(True)
        self.move("up")
        self.upButton.setDisabled(False)
    @pyqtSlot(bool)
    def moveDown(self,_):
        self.downButton.setDisabled(True)
        self.move("down")
        self.downButton.setDisabled(False)
    @pyqtSlot(bool)
    def moveLeft(self,_):
        self.leftButton.setDisabled(True)
        self.move("left")
        self.leftButton.setDisabled(False)
    @pyqtSlot(bool)
    def moveRight(self,_):
        self.rightButton.setDisabled(True)
        self.move("right")
        self.rightButton.setDisabled(False)
    
    def move(self,m):
        step = self.speedSpinBox.value()
        self.aw.qmc.movebackground(m,step)
        self.createEventTable()
        self.createDataTable()
        self.aw.qmc.redraw(recomputeAllDeltas=False)

    def readChecks(self):
        self.aw.qmc.background = bool(self.backgroundCheck.isChecked())
        self.aw.qmc.backgroundDetails = bool(self.backgroundDetails.isChecked())
        self.aw.qmc.backgroundeventsflag = bool(self.backgroundeventsflag.isChecked())
        self.aw.qmc.DeltaETBflag = bool(self.backgroundDeltaETflag.isChecked())
        self.aw.qmc.DeltaBTBflag = bool(self.backgroundDeltaBTflag.isChecked())
        self.aw.qmc.backgroundETcurve = bool(self.backgroundETflag.isChecked())
        self.aw.qmc.backgroundBTcurve = bool(self.backgroundBTflag.isChecked())
        self.aw.qmc.backgroundShowFullflag = bool(self.backgroundFullflag.isChecked())
        self.aw.qmc.redraw(recomputeAllDeltas=True)
    
    @pyqtSlot(int)
    def changeAlignEventidx(self,i):
        self.aw.qmc.alignEvent = i
        
    @pyqtSlot(int)
    def changeReplayTypeidx(self,i):
        self.aw.qmc.replayType = i

    @pyqtSlot(int)
    def changeXTcurveidx(self,i):
        self.aw.qmc.xtcurveidx = i
        self.createDataTable()
        self.aw.qmc.redraw(recomputeAllDeltas=False,smooth=True)

    @pyqtSlot(int)
    def changeYTcurveidx(self,i):
        self.aw.qmc.ytcurveidx = i
        self.createDataTable()
        self.aw.qmc.redraw(recomputeAllDeltas=False,smooth=True)

    @pyqtSlot(bool)
    def load(self,_):
        self.filename = self.aw.ArtisanOpenFileDialog(msg=QApplication.translate("Message","Load Background"),ext_alt=".alog")
        if len(self.filename) == 0:
            return
        self.aw.sendmessage(QApplication.translate("Message","Reading background profile..."))
        self.aw.qmc.resetlinecountcaches()
        self.aw.loadbackground(self.filename)
        
        # reset XT curve popup
        curvenames = [""] # first entry is the empty one (no extra curve displayed)
        for i in range(min(len(self.aw.qmc.extraname1B),len(self.aw.qmc.extraname2B),len(self.aw.qmc.extratimexB))):
            curvenames.append("B" + str(2*i+3) + ": " + self.aw.qmc.extraname1B[i])
            curvenames.append("B" + str(2*i+4) + ": " + self.aw.qmc.extraname2B[i])
            
        self.xtcurveComboBox.blockSignals(True)
        self.xtcurveComboBox.clear()
        self.xtcurveComboBox.addItems(curvenames)
        if self.aw.qmc.xtcurveidx < len(curvenames):
            self.xtcurveComboBox.setCurrentIndex(self.aw.qmc.xtcurveidx)
        self.xtcurveComboBox.blockSignals(False)

        self.ytcurveComboBox.blockSignals(True)
        self.ytcurveComboBox.clear()
        self.ytcurveComboBox.addItems(curvenames)
        if self.aw.qmc.ytcurveidx < len(curvenames):
            self.ytcurveComboBox.setCurrentIndex(self.aw.qmc.ytcurveidx)
        self.ytcurveComboBox.blockSignals(False)

        self.pathedit.setText(self.filename)
        self.backgroundCheck.setChecked(True)
        self.aw.qmc.timealign(redraw=False)
        self.readChecks()
        self.createEventTable()
        self.createDataTable()

    def createEventTable(self):
        ndata = len(self.aw.qmc.backgroundEvents)
        
        # self.eventtable.clear() # this crashes Ubuntu 16.04
#        if ndata != 0:
#            self.eventtable.clearContents() # this crashes Ubuntu 16.04 if device table is empty and also sometimes else
        self.eventtable.clearSelection() # this seems to work also for Ubuntu 16.04
        
        self.eventtable.setRowCount(ndata)
        self.eventtable.setColumnCount(6)
        self.eventtable.setHorizontalHeaderLabels([QApplication.translate("Table","Time"),
                                                   QApplication.translate("Table", "ET"),
                                                   QApplication.translate("Table", "BT"),
                                                   QApplication.translate("Table","Description"),
                                                   QApplication.translate("Table","Type"),
                                                   QApplication.translate("Table","Value")])
        self.eventtable.setAlternatingRowColors(True)
        self.eventtable.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        self.eventtable.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        self.eventtable.setSelectionMode(QTableWidget.SelectionMode.ExtendedSelection)
        self.eventtable.setShowGrid(True)
        self.eventtable.verticalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Fixed)
        if self.aw.qmc.timeindex[0] != -1:
            start = self.aw.qmc.timex[self.aw.qmc.timeindex[0]]
        else:
            start = 0
        for i in range(ndata):
            timez = QTableWidgetItem(stringfromseconds(self.aw.qmc.timeB[self.aw.qmc.backgroundEvents[i]]-start))
            timez.setTextAlignment(Qt.AlignmentFlag.AlignRight + Qt.AlignmentFlag.AlignVCenter)
    
            if self.aw.qmc.LCDdecimalplaces:
                fmtstr = "%.1f"
            else:
                fmtstr = "%.0f"
            
            etline = QTableWidgetItem(fmtstr%(self.aw.qmc.temp1B[self.aw.qmc.backgroundEvents[i]]) + self.aw.qmc.mode)
            etline.setTextAlignment(Qt.AlignmentFlag.AlignRight + Qt.AlignmentFlag.AlignVCenter)
            
            btline = QTableWidgetItem(fmtstr%(self.aw.qmc.temp2B[self.aw.qmc.backgroundEvents[i]]) + self.aw.qmc.mode)
            btline.setTextAlignment(Qt.AlignmentFlag.AlignRight + Qt.AlignmentFlag.AlignVCenter)
            
            description = QTableWidgetItem(self.aw.qmc.backgroundEStrings[i])
            etype = QTableWidgetItem(self.aw.qmc.Betypesf(self.aw.qmc.backgroundEtypes[i]))
            evalue = QTableWidgetItem(self.aw.qmc.eventsvalues(self.aw.qmc.backgroundEvalues[i]))
            evalue.setTextAlignment(Qt.AlignmentFlag.AlignRight + Qt.AlignmentFlag.AlignVCenter)
            #add widgets to the table
            self.eventtable.setItem(i,0,timez)
            self.eventtable.setItem(i,1,etline)
            self.eventtable.setItem(i,2,btline)
            self.eventtable.setItem(i,3,description)
            self.eventtable.setItem(i,4,etype)
            self.eventtable.setItem(i,5,evalue)
        # improve width of Time column
        self.eventtable.setColumnWidth(1,175)
        header = self.eventtable.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.ResizeMode.Fixed)
        header.setSectionResizeMode(1, QHeaderView.ResizeMode.Fixed)
        header.setSectionResizeMode(2, QHeaderView.ResizeMode.Fixed)
        header.setSectionResizeMode(3, QHeaderView.ResizeMode.Stretch)
        header.setSectionResizeMode(4, QHeaderView.ResizeMode.Fixed)
        header.setSectionResizeMode(5, QHeaderView.ResizeMode.Fixed)
        self.eventtable.resizeColumnsToContents()
        self.eventtable.setColumnWidth(1,65)
        self.eventtable.setColumnWidth(2,65)

    def createDataTable(self):
        try:
            #### lock shared resources #####
            self.aw.qmc.profileDataSemaphore.acquire(1)
            
            ndata = len(self.aw.qmc.timeB)
            
            self.datatable.clear() # this crashes Ubuntu 16.04
    #        if ndata != 0:
    #            self.datatable.clearContents() # this crashes Ubuntu 16.04 if device table is empty and also sometimes else
            self.datatable.clearSelection() # this seems to work also for Ubuntu 16.04
    
            if self.aw.qmc.timeindexB[0] != -1 and len(self.aw.qmc.timeB) > self.aw.qmc.timeindexB[0]:
                start = self.aw.qmc.timeB[self.aw.qmc.timeindexB[0]]
            else:
                start = 0
            self.datatable.setRowCount(ndata)
            headers = [QApplication.translate("Table","Time"),
                                                      QApplication.translate("Table","ET"),
                                                      QApplication.translate("Table","BT"),
                                                      deltaLabelUTF8 + QApplication.translate("Table","ET"),
                                                      deltaLabelUTF8 + QApplication.translate("Table","BT")]
            xtcurve = False # no XT curve
            if self.aw.qmc.xtcurveidx > 0: # 3rd background curve set?
                idx3 = self.aw.qmc.xtcurveidx - 1
                n3 = idx3 // 2
                if len(self.aw.qmc.temp1BX) > n3 and len(self.aw.qmc.extratimexB) > n3:
                    xtcurve = True
                    if self.aw.qmc.xtcurveidx % 2:
                        headers.append(self.aw.qmc.extraname1B[n3])
                    else:
                        headers.append(self.aw.qmc.extraname2B[n3])

            ytcurve = False # no YT curve
            if self.aw.qmc.ytcurveidx > 0: # 4th background curve set?
                idx4 = self.aw.qmc.ytcurveidx - 1
                n4 = idx4 // 2
                if len(self.aw.qmc.temp1BX) > n4 and len(self.aw.qmc.extratimexB) > n4:
                    ytcurve = True
                    if self.aw.qmc.ytcurveidx % 2:
                        headers.append(self.aw.qmc.extraname1B[n4])
                    else:
                        headers.append(self.aw.qmc.extraname2B[n4])
            
            headers.append("") # dummy column that stretches
            self.datatable.setColumnCount(len(headers))
            self.datatable.setHorizontalHeaderLabels(headers)
            self.datatable.setAlternatingRowColors(True)
            self.datatable.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
            self.datatable.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
            self.datatable.setSelectionMode(QTableWidget.SelectionMode.ExtendedSelection) # QTableWidget.SelectionMode.SingleSelection, ContiguousSelection, MultiSelection
            self.datatable.setShowGrid(True)
            self.datatable.verticalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Fixed)
            for i in range(ndata):
                Rtime = QTableWidgetItem(stringfromseconds(self.aw.qmc.timeB[i]-start))
                Rtime.setTextAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignVCenter)
                if self.aw.qmc.LCDdecimalplaces:
                    fmtstr = "%.1f"
                else:
                    fmtstr = "%.0f"
                ET = QTableWidgetItem(fmtstr%self.aw.qmc.temp1B[i])
                BT = QTableWidgetItem(fmtstr%self.aw.qmc.temp2B[i])
                ET.setTextAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignVCenter)
                BT.setTextAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignVCenter)
                if i:
                    d = (self.aw.qmc.timeB[i]-self.aw.qmc.timeB[i-1])
                    if d == 0:
                        dET = 0.
                        dBT = 0.
                    else:
                        dET = (60*(self.aw.qmc.temp1B[i]-self.aw.qmc.temp1B[i-1])/d)
                        dBT = (60*(self.aw.qmc.temp2B[i]-self.aw.qmc.temp2B[i-1])/d)
                    deltaET = QTableWidgetItem("%.1f"%dET)
                    deltaBT = QTableWidgetItem("%.1f"%dBT)
                else:
                    deltaET = QTableWidgetItem("--")
                    deltaBT = QTableWidgetItem("--")
                deltaET.setTextAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignVCenter)
                deltaBT.setTextAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignVCenter)
                self.datatable.setItem(i,0,Rtime)
                        
                if i:
                    #identify by color and add notation
                    if i == self.aw.qmc.timeindexB[0] != -1:
                        self.datatable.item(i,0).setBackground(QColor('#f07800'))
                        text = QApplication.translate("Table", "CHARGE")
                    elif i == self.aw.qmc.timeindexB[1]:
                        self.datatable.item(i,0).setBackground(QColor('orange'))
                        text = QApplication.translate("Table", "DRY END")
                    elif i == self.aw.qmc.timeindexB[2]:
                        self.datatable.item(i,0).setBackground(QColor('orange'))
                        text = QApplication.translate("Table", "FC START")
                    elif i == self.aw.qmc.timeindexB[3]:
                        self.datatable.item(i,0).setBackground(QColor('orange'))
                        text = QApplication.translate("Table", "FC END")
                    elif i == self.aw.qmc.timeindexB[4]:
                        self.datatable.item(i,0).setBackground(QColor('orange'))
                        text = QApplication.translate("Table", "SC START")
                    elif i == self.aw.qmc.timeindexB[5]:
                        self.datatable.item(i,0).setBackground(QColor('orange'))
                        text = QApplication.translate("Table", "SC END")
                    elif i == self.aw.qmc.timeindexB[6]:
                        self.datatable.item(i,0).setBackground(QColor('#f07800'))
                        text = QApplication.translate("Table", "DROP")
                    elif i == self.aw.qmc.timeindexB[7]:
                        self.datatable.item(i,0).setBackground(QColor('orange'))
                        text = QApplication.translate("Table", "COOL")
                    elif i in self.aw.qmc.backgroundEvents:
                        self.datatable.item(i,0).setBackground(QColor('yellow'))
                        index = self.aw.qmc.backgroundEvents.index(i)
                        text = QApplication.translate("Table", "#{0} {1}{2}").format(str(index+1),self.aw.qmc.Betypesf(self.aw.qmc.backgroundEtypes[index])[0],self.aw.qmc.eventsvalues(self.aw.qmc.backgroundEvalues[index]))
                    else:
                        text = ""
                    Rtime.setText(text + " " + Rtime.text())
                self.datatable.setItem(i,1,ET)
                self.datatable.setItem(i,2,BT)
                self.datatable.setItem(i,3,deltaET)
                self.datatable.setItem(i,4,deltaBT)
                
                if xtcurve and len(self.aw.qmc.temp1BX[n3]) > i: # an XT column is availble, fill it with data
                    if self.aw.qmc.xtcurveidx % 2:
                        XT = QTableWidgetItem("%.0f"%self.aw.qmc.temp1BX[n3][i])
                    else:
                        XT = QTableWidgetItem("%.0f"%self.aw.qmc.temp2BX[n3][i])
                    XT.setTextAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignVCenter)
                    self.datatable.setItem(i,5,XT)
                
                if ytcurve and len(self.aw.qmc.temp1BX[n4]) > i: # an YT column is availble, fill it with data
                    if self.aw.qmc.ytcurveidx % 2:
                        YT = QTableWidgetItem("%.0f"%self.aw.qmc.temp1BX[n4][i])
                    else:
                        YT = QTableWidgetItem("%.0f"%self.aw.qmc.temp2BX[n4][i])
                    YT.setTextAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignVCenter)
                    if xtcurve:
                        self.datatable.setItem(i,6,YT)
                    else:
                        self.datatable.setItem(i,5,YT)
                    
            header = self.datatable.horizontalHeader()
            header.setSectionResizeMode(0, QHeaderView.ResizeMode.Fixed)
            header.setSectionResizeMode(1, QHeaderView.ResizeMode.Fixed)
            header.setSectionResizeMode(2, QHeaderView.ResizeMode.Fixed)
            header.setSectionResizeMode(3, QHeaderView.ResizeMode.Fixed)
            header.setSectionResizeMode(4, QHeaderView.ResizeMode.Fixed)
            if (xtcurve and not ytcurve) or (ytcurve and not xtcurve):
                header.setSectionResizeMode(5, QHeaderView.ResizeMode.Fixed)
                header.setSectionResizeMode(6, QHeaderView.ResizeMode.Stretch)
            elif xtcurve and ytcurve:
                header.setSectionResizeMode(5, QHeaderView.ResizeMode.Fixed)
                header.setSectionResizeMode(6, QHeaderView.ResizeMode.Fixed)
                header.setSectionResizeMode(7, QHeaderView.ResizeMode.Stretch)
            else:
                header.setSectionResizeMode(5, QHeaderView.ResizeMode.Stretch)
            self.datatable.resizeColumnsToContents()
        finally:
            if self.aw.qmc.profileDataSemaphore.available() < 1:
                self.aw.qmc.profileDataSemaphore.release(1)

    @pyqtSlot(bool)
    def copyDataTabletoClipboard(self,_=False):
        self.datatable.selectAll()
        self.aw.copy_cells_to_clipboard(self.datatable,adjustment=7)
        self.datatable.clearSelection()
        self.aw.sendmessage(QApplication.translate("Message","Data table copied to clipboard"))

    @pyqtSlot(bool)
    def copyEventTabletoClipboard(self,_=False):
        self.aw.copy_cells_to_clipboard(self.eventtable,adjustment=0)
        self.aw.sendmessage(QApplication.translate("Message","Event table copied to clipboard"))