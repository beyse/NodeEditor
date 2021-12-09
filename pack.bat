rmdir /S /Q .\build 
rmdir /S /Q .\dist 

python -m PyInstaller --noconfirm ^
--hidden-import PyQt5.QtWidgets ^
--hidden-import pyqode ^
--hidden-import pyqode.qt ^
--hidden-import pyqode.qt.QtCore ^
--hidden-import nodeeditor ^
--hidden-import nodeeditor.node_socket ^
--hidden-import SocketDefinition ^
--hidden-import nodeeditor.node_socket.SocketDefinition ^
--noconsole ^
--onefile ^
--name ExecutionNodeEditor ^
.\apps\execution_node_editor\main.py

xcopy .\apps\execution_node_editor\node_type_definitions .\dist\node_type_definitions\ /s /e
xcopy .\apps\execution_node_editor\gui .\dist\gui\ /s /e

