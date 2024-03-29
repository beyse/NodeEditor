from apps.execution_node_editor.execution_node_base import GraphicsExecutionNode
from apps.execution_node_editor.json_editor import JsonEditor
from PyQt5 import QtCore, QtGui
from PyQt5.QtWidgets import QToolBar
from apps.execution_node_editor.conf import register_node_types
import os, sys
from sys import platform
from qtpy.QtGui import QIcon, QKeySequence
from qtpy.QtWidgets import QMdiArea, QWidget, QDockWidget, QAction, QMessageBox, QFileDialog
from qtpy.QtCore import Qt, QSignalMapper
import subprocess
from apps.execution_node_editor.version_info import VERSION_MAJOR, VERSION_MINOR, VERSION_PATCH
from version_info import VERSION_MAJOR, VERSION_MINOR, VERSION_PATCH
from commit_info import GIT_HASH

import requests
import shutil
import tempfile
from PyQt5.QtCore import QObject, pyqtSlot as pyQtSlot


from nodeeditor.utils import loadStylesheets
from nodeeditor.node_editor_window import NodeEditorWindow
from sub_window import SubWindow
from drag_listbox import QDMDragListbox
from nodeeditor.utils import dumpException, pp
from apps.execution_node_editor.node_type_definition import NodeTypeDefinition, PortDefinition, read_node_type_definitions_from_dirs
# Enabling edge validators
from nodeeditor.node_edge import Edge
from nodeeditor.node_edge_validators import (
    edge_validator_debug,
    edge_cannot_connect_two_outputs_or_two_inputs,
    edge_cannot_connect_input_and_output_of_same_node
)
Edge.registerEdgeValidator(edge_validator_debug)
Edge.registerEdgeValidator(edge_cannot_connect_two_outputs_or_two_inputs)
Edge.registerEdgeValidator(edge_cannot_connect_input_and_output_of_same_node)


# images for the dark skin


DEBUG = False

node_type_definitions = []

class DownloaderSignals(QObject):
    signalSuccess = QtCore.pyqtSignal()
    installerPath = QtCore.pyqtSignal(object)
class Downloader(QtCore.QRunnable):

    def __init__(self):
        super(Downloader, self).__init__()
        self.signals = DownloaderSignals()


    def download_file(self, url, folder_name, local_filename):
        path = os.path.join(folder_name, local_filename)
        with requests.get(url, stream=True) as r:
            with open(path, 'wb') as f:
                shutil.copyfileobj(r.raw, f)
        
        return path

    @pyQtSlot()
    def run(self):
        response = requests.get("https://api.github.com/repos/beyse/NodeEditor/releases/latest")
        release_info = response.json()
        assets = release_info["assets"]
        tag_name = release_info["tag_name"]
        url = None
        for asset in assets:
            content_type = asset["content_type"]
            name = asset["name"]
            if content_type == "application/x-msdownload" and (name.startswith('Setup') or name.startswith('Install')): 
                url = asset["browser_download_url"]
        
        if url is not None:
            local_filename = 'install_{}.exe'.format(tag_name)
            tmpdir = tempfile.gettempdir()
            app_tmpdir = os.path.join(tmpdir, 'ExecutionNodeEditor')
            if not os.path.exists(app_tmpdir):
                os.mkdir(app_tmpdir)
            
            path = self.download_file(url, app_tmpdir, local_filename)
            print('Successfully Downloaded {}'.format(path))
            self.signals.installerPath.emit(path)
            self.signals.signalSuccess.emit()


class ExecutionNodeEditorWindow(NodeEditorWindow):

    def initUI(self):
        #self.setWindowFlags(QtCore.Qt.FramelessWindowHint)
        self.name_company = 'Sebastian Beyer'
        self.name_product = 'ExecutionNodeEditor'
        self.process = None
        self.stylesheet_filename = os.path.join("./assets/qss/nodeeditor-light.qss")
        loadStylesheets(
            "./assets/qss/nodeeditor.qss",
            self.stylesheet_filename
        )

        app_icon = QtGui.QIcon()
        app_icon.addFile('assets/icons/16x16.png', QtCore.QSize(16, 16))
        app_icon.addFile('assets/icons/24x24.png', QtCore.QSize(24, 24))
        app_icon.addFile('assets/icons/32x32.png', QtCore.QSize(32, 32))
        app_icon.addFile('assets/icons/48x48.png', QtCore.QSize(48, 48))
        app_icon.addFile('assets/icons/64x64.png', QtCore.QSize(64, 64))
        app_icon.addFile('assets/icons/128x128.png', QtCore.QSize(128, 128))
        app_icon.addFile('assets/icons/256x256.png', QtCore.QSize(256, 256))
        self.setWindowIcon(app_icon)

        self.empty_icon = QIcon(".")

        if DEBUG:
            print("Registered nodes:")
            # pp(CALC_NODES)

        exe_path = os.path.dirname(os.path.realpath(sys.argv[0]))
        node_definitions_dir = os.path.join(exe_path, 'execution_subsystem' , 'node_type_definitions')
        
        if platform == "linux" or platform == "linux2":
            # linux
            self.execution_subsystem_path = os.path.join(exe_path, 'execution_subsystem' , 'run_graph')
        elif platform == "darwin":
            # OS X
            pass
        elif platform == "win32":
            # Windows...
            self.execution_subsystem_path = os.path.join(exe_path, 'execution_subsystem' , 'run_graph.exe')
        categorizes_node_type_definitions = read_node_type_definitions_from_dirs(node_definitions_dir)

        for category, node_types in categorizes_node_type_definitions.items():
            register_node_types(node_types, category)

        self.mdiArea = QMdiArea()
        self.mdiArea.setHorizontalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        self.mdiArea.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        self.mdiArea.setViewMode(QMdiArea.TabbedView)
        self.mdiArea.setDocumentMode(True)
        self.mdiArea.setTabsClosable(True)
        self.mdiArea.setTabsMovable(True)
        self.setCentralWidget(self.mdiArea)

        self.mdiArea.subWindowActivated.connect(self.updateMenus)
        self.windowMapper = QSignalMapper(self)
        self.windowMapper.mapped[QWidget].connect(self.setActiveSubWindow)

        self.createNodesDock()
        self.createSettingsDock()

        self.createActions()
        self.createMenus()
        self.createToolBars()
        self.createStatusBar()
        self.updateMenus()

        self.readSettings()

        self.setWindowTitle("Execution Nodes Editor")

    def closeEvent(self, event):
        self.mdiArea.closeAllSubWindows()
        if self.mdiArea.currentSubWindow():
            event.ignore()
        else:
            self.writeSettings()
            event.accept()
            # hacky fix for PyQt 5.14.x
            import sys
            sys.exit(0)

    def createActions(self):
        super().createActions()

        self.actClose = QAction("Cl&ose", self, statusTip="Close the active window",
                                triggered=self.mdiArea.closeActiveSubWindow)
        self.actCloseAll = QAction(
            "Close &All", self, statusTip="Close all the windows", triggered=self.mdiArea.closeAllSubWindows)
        self.actTile = QAction(
            "&Tile", self, statusTip="Tile the windows", triggered=self.mdiArea.tileSubWindows)
        self.actCascade = QAction(
            "&Cascade", self, statusTip="Cascade the windows", triggered=self.mdiArea.cascadeSubWindows)
        self.actNext = QAction("Ne&xt", self, shortcut=QKeySequence.NextChild,
                               statusTip="Move the focus to the next window", triggered=self.mdiArea.activateNextSubWindow)
        self.actPrevious = QAction("Pre&vious", self, shortcut=QKeySequence.PreviousChild,
                                   statusTip="Move the focus to the previous window", triggered=self.mdiArea.activatePreviousSubWindow)

        self.actSeparator = QAction(self)
        self.actSeparator.setSeparator(True)

        self.actAbout = QAction(
            "&About", self, statusTip="Show the application's About box", triggered=self.about)

        is_update_available = self.check_for_update()

        if is_update_available:
            self.actUpdate = QAction("&Get Latest Version!", self, statusTip="A newer version is available. Click here to download and install it.", triggered=self.update)
            self.update = self.menuBar().addAction(self.actUpdate)

    def getCurrentNodeEditorWidget(self):
        """ we're returning NodeEditorWidget here... """
        activeSubWindow = self.mdiArea.activeSubWindow()
        if activeSubWindow:
            return activeSubWindow.widget()
        return None

    def openFile(self, filename):
        self.getCurrentNodeEditorWidget().fileLoad(filename)
        self.setTitle()

    def onFileNew(self):
        try:
            subwnd = self.createMdiChild()
            subwnd.widget().fileNew()
            subwnd.show()
        except Exception as e:
            dumpException(e)

    def onFileOpen(self):
        fnames, filter = QFileDialog.getOpenFileNames(
            self, 'Open graph from file', self.getFileDialogDirectory(), self.getFileDialogFilter())

        try:
            for fname in fnames:
                if fname:
                    existing = self.findMdiChild(fname)
                    if existing:
                        self.mdiArea.setActiveSubWindow(existing)
                    else:
                        # we need to create new subWindow and open the file
                        nodeeditor = SubWindow()
                        if nodeeditor.fileLoad(fname):
                            self.statusBar().showMessage("File %s loaded" % fname, 5000)
                            nodeeditor.setTitle()
                            subwnd = self.createMdiChild(nodeeditor)
                            subwnd.show()
                        else:
                            nodeeditor.close()
        except Exception as e:
            dumpException(e)

    def check_for_update(self):
        try:
            #check for updated version
            response = requests.get("https://api.github.com/repos/beyse/NodeEditor/releases/latest")
            release_info = response.json()
            tag_name = release_info["tag_name"]
            tag_name = tag_name.replace('v', '')
            tokens = tag_name.split('.')
            r_major = int(tokens[0])
            r_minor = int(tokens[1])
            r_patch = int(tokens[2])

            if r_major > VERSION_MAJOR or r_minor > VERSION_MINOR or r_patch > VERSION_PATCH:
                return True
            else:
                return False
        except Exception:
            print('Unable to check for update')
            return False


    def update_ready(self, installer_path):
        self.downloader=None
        print('path = ', installer_path)
        if installer_path is not None:
            res = QMessageBox.information(self, "Update ready", "Download finished.\nThe application will be closed.\n\nUnsaved changes can be saved.")
            if res is not None:
                args = [installer_path]
                self.process = subprocess.Popen(args)
                self.actExit.trigger()

    def update(self):
        #download newer version
        self.threadpool = QtCore.QThreadPool()
        self.downloader = Downloader()
        self.downloader.signals.installerPath.connect(self.update_ready)
        self.threadpool.start(self.downloader)
        self.statusBar().showMessage("Downloading...", 10000)
        self.menuBar().removeAction(self.actUpdate)
        

    def about(self):

        #Version 0.1.0-eb42a6f
        version_info_text = "{} v{}.{}.{}-{}".format(self.name_product, VERSION_MAJOR, VERSION_MINOR, VERSION_PATCH, GIT_HASH)
        QMessageBox.about(self, "About",
                          version_info_text + "\n\n"
                          "Created by Sebastian Beyer (sebastian.beyer@live.com)\n\n"

                          "View it on GitHub: https://github.com/beyse/NodeEditor.\n\n"

                          "It is a fork of pyqt-node-editor, created by Pavel Křupala.\n"
                          "Check it out as well at: https://gitlab.com/pavel.krupala/pyqt-node-editor.\n\n"

                          "The project is licensed under the MIT License.\n"
                          "Learn more about it here: https://choosealicense.com/licenses/mit/.")

    def createMenus(self):
        super().createMenus()

        self.windowMenu = self.menuBar().addMenu("&Window")
        self.updateWindowMenu()
        self.windowMenu.aboutToShow.connect(self.updateWindowMenu)

        self.menuBar().addSeparator()

        self.helpMenu = self.menuBar().addMenu("&Help")
        self.helpMenu.addAction(self.actAbout)
        self.editMenu.aboutToShow.connect(self.updateEditMenu)

    def updateMenus(self):
        # print("update Menus")
        active = self.getCurrentNodeEditorWidget()
        hasMdiChild = (active is not None)

        self.actSave.setEnabled(hasMdiChild)
        self.actSaveAs.setEnabled(hasMdiChild)
        self.actClose.setEnabled(hasMdiChild)
        self.actCloseAll.setEnabled(hasMdiChild)
        self.actTile.setEnabled(hasMdiChild)
        self.actCascade.setEnabled(hasMdiChild)
        self.actNext.setEnabled(hasMdiChild)
        self.actPrevious.setEnabled(hasMdiChild)
        self.actSeparator.setVisible(hasMdiChild)

        self.updateEditMenu()
        self.updateSettingsDock()

    def updateEditMenu(self):
        try:
            # print("update Edit Menu")
            active = self.getCurrentNodeEditorWidget()
            hasMdiChild = (active is not None)

            self.actPaste.setEnabled(hasMdiChild)

            self.actCut.setEnabled(hasMdiChild and active.hasSelectedItems())
            self.actCopy.setEnabled(hasMdiChild and active.hasSelectedItems())
            self.actDelete.setEnabled(
                hasMdiChild and active.hasSelectedItems())

            self.actUndo.setEnabled(hasMdiChild and active.canUndo())
            self.actRedo.setEnabled(hasMdiChild and active.canRedo())
        except Exception as e:
            dumpException(e)

    def updateSettingsDock(self):
        try:
            # print("update Settings Dock")
            active = self.getCurrentNodeEditorWidget()
            hasMdiChild = (active is not None)

            self.settingsDock.update({}, None, False)
            if hasMdiChild:
                print(type(active))
                selected_items = active.getSelectedItems()
                if len(selected_items) == 1:
                    selected_item = selected_items[0]
                    if isinstance(selected_item, GraphicsExecutionNode):
                        node = selected_item.node
                        self.settingsDock.update(node.settings, node.setSettings, True)
        except Exception as e:
            dumpException(e)

    def updateWindowMenu(self):
        self.windowMenu.clear()

        toolbar_nodes = self.windowMenu.addAction("Nodes Toolbar")
        toolbar_nodes.setCheckable(True)
        toolbar_nodes.triggered.connect(self.onWindowNodesToolbar)
        toolbar_nodes.setChecked(self.nodesDock.isVisible())

        self.windowMenu.addSeparator()

        self.windowMenu.addAction(self.actClose)
        self.windowMenu.addAction(self.actCloseAll)
        self.windowMenu.addSeparator()
        self.windowMenu.addAction(self.actTile)
        self.windowMenu.addAction(self.actCascade)
        self.windowMenu.addSeparator()
        self.windowMenu.addAction(self.actNext)
        self.windowMenu.addAction(self.actPrevious)
        self.windowMenu.addAction(self.actSeparator)

        windows = self.mdiArea.subWindowList()
        self.actSeparator.setVisible(len(windows) != 0)

        for i, window in enumerate(windows):
            child = window.widget()

            text = "%d %s" % (i + 1, child.getUserFriendlyFilename())
            if i < 9:
                text = '&' + text

            action = self.windowMenu.addAction(text)
            action.setCheckable(True)
            action.setChecked(child is self.getCurrentNodeEditorWidget())
            action.triggered.connect(self.windowMapper.map)
            self.windowMapper.setMapping(action, window)

    def onWindowNodesToolbar(self):
        if self.nodesDock.isVisible():
            self.nodesDock.hide()
        else:
            self.nodesDock.show()

    def createToolBars(self):
        toolbar = QToolBar("Main Toolbar")
        toolbar.setFloatable(False)
        toolbar.setMovable(False)
        self.run_graph_action = QAction(
            QIcon("assets/icons/play.png"), "Run Graph (F5)", self)
        self.run_graph_action.setShortcut('F5')
        self.run_graph_action.triggered.connect(self.run_graph)
        toolbar.addAction(self.run_graph_action)

        self.addToolBar(toolbar)

    def execute_process(self, graph_file):
        if self.process is not None:
            print('A process already exists')
            if self.process.poll() is None:
                print('Process is still running')
                # process is still running
                print('I will terminate the process')
                self.process.terminate()
                try:
                    print('Waiting for a maximum of 1 seconds')
                    self.process.wait(1)
                    print('Process terminated')
                except:
                    print('Waiting timed out and process still running')
                    print('I will kill the process')
                    self.process.kill()
            else:
                print('This process terminated')

        #flags = subprocess.CREATE_NEW_CONSOLE
        args = [self.execution_subsystem_path, graph_file] 
        print(args)

        if platform == "win32":
            flags = subprocess.CREATE_NO_WINDOW
            self.process = subprocess.Popen(args, creationflags=flags)
        else:
            self.process = subprocess.Popen(args)

    def run_graph(self):
        print('run graph')
        # first save the graph
        ok, graph_file = self.onFileAutosave()
        # get the file name of the graph
        #current_nodeeditor = self.getCurrentNodeEditorWidget()
        # print(current_nodeeditor)
        if ok:
            self.execute_process(graph_file)
            #print('Run now {}'.format(graph_file))

    def createNodesDock(self):
        self.nodesListWidget = QDMDragListbox()

        self.nodesDock = QDockWidget("NODES")
        self.nodesDock.setFont(QtGui.QFont('Roboto', 10))
        self.nodesDock.setFeatures(QDockWidget.DockWidgetMovable)
        self.nodesDock.setWidget(self.nodesListWidget)
        self.nodesDock.setFloating(False)

        self.addDockWidget(Qt.RightDockWidgetArea, self.nodesDock)

    def createSettingsDock(self):
        self.settingsDock = JsonEditor()
        self.addDockWidget(Qt.RightDockWidgetArea, self.settingsDock)

    def createStatusBar(self):
        self.statusBar().showMessage("Ready")

    def createMdiChild(self, child_widget=None):
        nodeeditor = child_widget if child_widget is not None else SubWindow()
        subwnd = self.mdiArea.addSubWindow(nodeeditor)
        subwnd.setWindowIcon(self.empty_icon)
        # nodeeditor.scene.addItemSelectedListener(self.updateEditMenu)
        # nodeeditor.scene.addItemsDeselectedListener(self.updateEditMenu)
        nodeeditor.scene.history.addHistoryModifiedListener(
            self.updateEditMenu)
        nodeeditor.scene.history.addHistoryModifiedListener(
            self.updateSettingsDock)
        nodeeditor.addCloseEventListener(self.onSubWndClose)
        return subwnd

    def onSubWndClose(self, widget, event):
        existing = self.findMdiChild(widget.filename)
        self.mdiArea.setActiveSubWindow(existing)

        if self.maybeSave():
            event.accept()
        else:
            event.ignore()

    def findMdiChild(self, filename):
        for window in self.mdiArea.subWindowList():
            if window.widget().filename == filename:
                return window
        return None

    def setActiveSubWindow(self, window):
        if window:
            self.mdiArea.setActiveSubWindow(window)
