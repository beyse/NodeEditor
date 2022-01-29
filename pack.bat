::Write git commit hash into python file
git rev-parse --short HEAD > githash.txt
SET /p var= < githash.txt
echo GIT_HASH = '%var%' > .\apps\execution_node_editor\commit_info.py

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
--hidden-import randomname ^
--noconsole ^
--onefile ^
--icon=apps\execution_node_editor\assets\icons\app.ico ^
--name ExecutionNodeEditor ^
.\apps\execution_node_editor\main.py

xcopy ..\ExecutionSubsystems\CvSubsystem\_build\Release\CvSubsystem.exe .\dist\execution_subsystem\*
cd .\dist\execution_subsystem
ren CvSubsystem.exe run_graph.exe
:: Populate the subsystem folder with the node type definition json files
.\run_graph.exe
cd ..\..
xcopy .\apps\execution_node_editor\assets .\dist\assets\ /s /e

"C:\Program Files (x86)\Inno Setup 6\ISCC.exe" .\apps\execution_node_editor\setup\setup-compile-script.iss

::cd dist
::ExecutionNodeEditor.exe
::cd ..