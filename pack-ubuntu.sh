#!/bin/bash

git rev-parse --short HEAD > githash.txt
value=$(<githash.txt)
echo "GIT_HASH = '$value'" > ./apps/execution_node_editor/commit_info.py

rm -r ./build
rm -r ./dist

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

mkdir ./dist/execution_subsystem
cp ../ExecutionSubsystems/CvSubsystem/_build/CvSubsystem ./dist/execution_subsystem/run_graph
cd ./dist/execution_subsystem/
./run_graph
cd ../..

cp -a ./apps/execution_node_editor/assets ./dist/assets

# zip the package
cd dist && zip -r ExecutionNodeEditor_linux_x64.zip . && cd ..
