# .ONESHELL: # Applies to every targets in the file!
all: init generate

ROOTENV = .\.env\Scripts
ENV = ${ROOTENV}\activate.bat
PYINSTALLER = ${ROOTENV}\pyinstaller.exe
PYTEST = ${ROOTENV}\pytest.exe
BIN = .\bin
DIST = ${BIN}\dist
BUILD = ${BIN}\build
SPEC = ${BIN}\spec


install:
	@echo Install Env.
	@python -m virtualenv -p python3 .env 
	@${ENV}&pip install -r requirements.txt
	
build:
	@echo Compile File Sequences tool.
	@${ENV}&${PYINSTALLER} --noconfirm --onefile --console ".\cli.py" --specpath ${SPEC} --distpath ${BIN} --workpath ${BUILD} 

tests:
	@echo Run tests of File Sequences tool.
	@${ENV}&${PYTEST} -s -v

