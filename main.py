#!/usr/bin/env python
import json
from PyQt6.QtCore import QDir
from PyQt6.QtWidgets import (QApplication, QDialog, QGridLayout, QGroupBox, QHBoxLayout, QLineEdit,
                             QPushButton, QTableWidget, QFileDialog, QMessageBox, QTableWidgetItem)

class WidgetGallery(QDialog):
    def __init__(self, parent=None):
        super(WidgetGallery, self).__init__(parent)

        self.createTopLeftGroupBox()
        self.createBottomLeftWidget()

        def onClickHostBrowse():
            fileName, _ = QFileDialog.getOpenFileName(self, 'Single File', QDir.rootPath(), '*.json')
            self.textbox_host_json_path.setText(fileName)

        topLayout = QHBoxLayout()
        self.textbox_host_json_path = QLineEdit()
        self.textbox_host_json_path.setEnabled(0);
        topLayout.addWidget(self.textbox_host_json_path)
        hostPathButton = QPushButton("Browse host.json Path")
        hostPathButton.setDefault(True)
        hostPathButton.clicked.connect(onClickHostBrowse)
        topLayout.addWidget(hostPathButton)


        def onClickMapBrowse():
            fileName, _ = QFileDialog.getOpenFileName(self, 'Single File', QDir.rootPath(), '*.json')
            self.textbox_map_json_path.setText(fileName)

        topLayoutMap = QHBoxLayout()
        self.textbox_map_json_path = QLineEdit()
        self.textbox_map_json_path.setEnabled(0);
        topLayoutMap.addWidget(self.textbox_map_json_path)
        mapPathButton = QPushButton("Browse map.json Path")
        mapPathButton.setDefault(True)
        mapPathButton.clicked.connect(onClickMapBrowse)
        topLayoutMap.addWidget(mapPathButton)


        def onClickRunButton():
            if self.textbox_host_json_path.text() == "" or len(self.textbox_host_json_path.text()) < 5:
                QMessageBox.critical(None, "ERROR", "Host path is not null")
                return
            if self.textbox_map_json_path.text() == "" or len(self.textbox_map_json_path.text()) < 5:
                QMessageBox.critical(None, "ERROR", "Map path is not null")
                return

            hostList = list()
            hostFile = open(self.textbox_host_json_path.text())
            hostData = json.load(hostFile)
            hostFile.close()

            mapList = list()
            mapFile = open(self.textbox_map_json_path.text())
            mapData = json.load(mapFile)
            mapFile.close()
            if hostData is None or hostData["zabbix_export"] is None or mapData is None or mapData["zabbix_export"] is None:
                QMessageBox.critical(None, "ERROR", "Host or Map list is not null")
                return
            arrayHostZabbixExport = hostData["zabbix_export"]["hosts"]
            if arrayHostZabbixExport is not None:
                for hostZabbixExport in arrayHostZabbixExport:
                    hostList.append(hostZabbixExport.get("host"))

            arrayMapZabbixExport = mapData["zabbix_export"]["maps"]
            if arrayMapZabbixExport is not None:
                for arrayMapZabbixExport in arrayMapZabbixExport:
                    arraySelementsZabbixExport = arrayMapZabbixExport.get("selements")
                    if arraySelementsZabbixExport is not None:
                        for arraySelementZabbixExport in arraySelementsZabbixExport:
                            arrayElementsZabbixExport = arraySelementZabbixExport.get("elements")
                            if arrayElementsZabbixExport is not None:
                                for arrayElementZabbixExport in arrayElementsZabbixExport:
                                    mapList.append(arrayElementZabbixExport.get("host"))


            resultHost = list(set(hostList) - set(mapList))
            resultMap = list(set(mapList) - set(hostList))

            for idx, x in enumerate(resultHost):
                rowPosition = self.tableHostWidget.rowCount()
                self.tableHostWidget.insertRow(rowPosition)
                self.tableHostWidget.setItem(rowPosition, 0, QTableWidgetItem(x))

            for idx, x in enumerate(resultMap):
                rowPosition = self.tableMapWidget.rowCount()
                self.tableMapWidget.insertRow(rowPosition)
                self.tableMapWidget.setItem(rowPosition, 0, QTableWidgetItem(x))


        topLayoutRun = QHBoxLayout()
        runButton = QPushButton("Run")
        runButton.setDefault(True)
        runButton.clicked.connect(onClickRunButton)
        topLayoutRun.addWidget(runButton)

        mainLayout = QGridLayout()
        mainLayout.addLayout(topLayout, 0, 0, 1, 2)
        mainLayout.addLayout(topLayoutMap, 1, 0, 1, 2)
        mainLayout.addLayout(topLayoutRun, 2, 0, 1, 2)
        mainLayout.addWidget(self.topLeftGroupBox, 3, 0, 1, 2)
        mainLayout.addWidget(self.bottomLeftGroupBox, 4, 0, 1, 2)
        self.setLayout(mainLayout)

        self.setWindowTitle("Zabbix Json Parser")

    def createTopLeftGroupBox(self):
        self.topLeftGroupBox = QGroupBox("Host exist, Map not exist")

        self.tableHostWidget = QTableWidget(1,1)

        hosthbox = QHBoxLayout()
        hosthbox.setContentsMargins(5, 5, 5, 5)
        hosthbox.addWidget(self.tableHostWidget)
        self.topLeftGroupBox.setLayout(hosthbox)

    def createBottomLeftWidget(self):
        self.bottomLeftGroupBox = QGroupBox("Map exist, Host not exist")

        self.tableMapWidget = QTableWidget(1,1)

        maphbox = QHBoxLayout()
        maphbox.setContentsMargins(5, 5, 5, 5)
        maphbox.addWidget(self.tableMapWidget)
        self.bottomLeftGroupBox.setLayout(maphbox)


if __name__ == '__main__':

    import sys

    w = 600
    h = 600
    app = QApplication(sys.argv)
    gallery = WidgetGallery()
    gallery.resize(w, h)
    gallery.show()
    sys.exit(app.exec())
