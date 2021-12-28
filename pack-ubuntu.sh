# create single binary from python source using PyInstaller
python -m PyInstaller --noconfirm \
--hidden-import PyQt5.QtWidgets \
--hidden-import pyqode \
--hidden-import pyqode.qt \
--hidden-import pyqode.qt.QtCore \
--hidden-import nodeeditor \
--hidden-import nodeeditor.node_socket \
--hidden-import SocketDefinition \
--hidden-import nodeeditor.node_socket.SocketDefinition \
--noconsole \
--onefile \
--icon=./apps/execution_node_editor/assets/icons/app.ico \
--name ExecutionNodeEditor \
./apps/execution_node_editor/main.py

# make the file executable
chmod 777 ./dist/ExecutionNodeEditor

# copy assets and subsystem
cp -a ./apps/execution_node_editor/execution_subsystem ./dist/execution_subsystem
cp -a ./apps/execution_node_editor/assets ./dist/assets

# zip the package
cd dist && zip -r ExecutionNodeEditor_linux_x64.zip . && cd ..
