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
--icon=apps\execution_node_editor\assets\icons\app.ico ^
--name ExecutionNodeEditor ^
.\apps\execution_node_editor\main.py

xcopy .\apps\execution_node_editor\node_type_definitions .\dist\node_type_definitions\ /s /e
xcopy .\apps\execution_node_editor\assets .\dist\assets\ /s /e

"C:\Program Files (x86)\Inno Setup 6\ISCC.exe" .\apps\execution_node_editor\setup\setup-compile-script.iss

::cd dist
::ExecutionNodeEditor.exe
::cd ..