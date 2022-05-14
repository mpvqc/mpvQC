MAKE_FILE:= $(lastword $(MAKEFILE_LIST))
SHELL:=/bin/bash


#######################################
# Tools
#######################################
PYTHON:=$(shell type -p python3 || echo python)

TOOL_LUPDATE=pyside6-lupdate
TOOL_LRELEASE=pyside6-lrelease
TOOL_RCC=pyside6-rcc
# TOOL_TEST_QML_RUNNER=qmltestrunner-qt6

EXECUTABLES=${PYTHON} ${TOOL_LUPDATE} ${TOOL_LRELEASE} ${TOOL_RCC} ${TOOL_TEST_QML_RUNNER}
K := $(foreach exec,$(EXECUTABLES),\
		$(if $(shell which $(exec)),some string,$(error "No $(exec) in PATH")))


#######################################
# Available directories
#######################################
DIR_ROOT:=$(shell dirname $(realpath $(firstword $(MAKEFILE_LIST))))
DIR_BUILD_SCRIPTS=${DIR_ROOT}/build-aux
DIR_DATA=${DIR_ROOT}/data
DIR_DOCS=${DIR_ROOT}/docs
DIR_I18N=${DIR_ROOT}/i18n
DIR_PY=${DIR_ROOT}/mpvqc
DIR_QML=${DIR_ROOT}/qml
DIR_TESTS_PY=${DIR_ROOT}/test
DIR_TESTS_QML=${DIR_ROOT}/qml


#######################################
# Generated directories
#######################################
DIR_BUILD=${DIR_ROOT}/build
DIR_BUILD_QRC_QML=${DIR_BUILD}/qrc-qml
DIR_BUILD_QRC_DATA=${DIR_BUILD}/qrc-data
DIR_BUILD_QRC_I18N=${DIR_BUILD}/qrc-i18n
DIR_BUILD_TRANSLATIONS=${DIR_BUILD}/translations
DIR_BUILD_RESOURCES=${DIR_BUILD}/resources
DIR_BUILD_PYTHON=${DIR_BUILD}/mpvqc


#######################################
# Generated files
#######################################
FILE_APP_ENTRY=main.py
FILE_QRC_QML=${DIR_BUILD_QRC_QML}/qml.qrc
FILE_QRC_DATA=${DIR_BUILD_QRC_DATA}/data.qrc
FILE_QRC_I18N=${DIR_BUILD_QRC_I18N}/i18n.qrc
FILE_QRC_I18N_JSON=${DIR_BUILD_QRC_I18N}/mpvQC.json
FILE_TRANSLATIONS=${DIR_BUILD_TRANSLATIONS}/mpvQC.json
FILE_RESOURCES=${DIR_BUILD_RESOURCES}/generated_resources.py
FILE_RESOURCES_DEVELOP=${DIR_PY}/generated_resources.py
FILE_RESOURCES_TEST=${DIR_TESTS_PY}/generated_resources.py


#######################################
# High Level Tasks
#######################################

build: \
	build-clean \
	develop-clean \
	compile-resources \

	@# Builds the project into build/mpvqc

	@rm -rf ${DIR_BUILD_PYTHON}
	@mkdir -p ${DIR_BUILD_PYTHON}
	@cp -r ${DIR_PY}/. ${DIR_BUILD_PYTHON}
	@cp ${FILE_RESOURCES} ${DIR_BUILD_PYTHON}
	@cp ${FILE_APP_ENTRY} ${DIR_BUILD}

	@rm -rf ${DIR_BUILD_QRC_DATA} ${DIR_BUILD_QRC_I18N} ${DIR_BUILD_QRC_QML} ${DIR_BUILD_RESOURCES} ${DIR_BUILD_TRANSLATIONS}
	@echo ''; echo 'Please find the finished project in ${DIR_BUILD_PYTHON}'


build-clean:
	@# Cleans up the build directory

	@rm -rf ${DIR_BUILD}


test: \
	test-clean \
	compile-resources

	@# Runs all tests

	@cp ${FILE_RESOURCES} ${FILE_RESOURCES_TEST}

	@${PYTHON} -m pytest test
	@${TOOL_TEST_QML_RUNNER} -input ${DIR_TESTS_QML}


test-clean:
	@# Cleans up the compiled resources in the test directory

	@rm -rf ${FILE_RESOURCES_TEST}


develop-build: \
	develop-clean \
	compile-resources

	@# Generates resources and copies them into the source directory
	@# This allows to develop/debug the project normally

	@cp ${FILE_RESOURCES} ${DIR_PY}


develop-clean:
	@# Cleans up the compiled resources in the source directory

	@rm -rf ${FILE_RESOURCES_DEVELOP}


update-translations: \
	xtask-prepare-translation-extractions

	@# Traverses qml & .py files to update translation files
	@# Requires translations in .py:   QCoreApplication.translate("context", "string")
	@# Requires translations in .qml:  qsTranslate("context", "string")

	@cd ${DIR_BUILD_TRANSLATIONS}; ${TOOL_LUPDATE} \
		-locations none \
		-project ${FILE_TRANSLATIONS}
	@cp -r ${DIR_BUILD_TRANSLATIONS}/i18n/*.ts ${DIR_I18N}


create-new-translation: \
	xtask-prepare-translation-extractions

	@# Allows to add translations to the project: make create-new-translation lang=<locale>

ifeq ($(lang), $(''))
	@echo "Usage: 'make create-new-translation lang=<locale>'"
else
	@cd ${DIR_BUILD_TRANSLATIONS}; ${TOOL_LUPDATE} \
		-verbose \
		-source-language en \
		-target-language $(lang) \
		-ts ${DIR_I18N}/$(lang).ts
	@$(MAKE) -s -f $(MAKE_FILE) update-translations
endif


clean: \
	build-clean \
	develop-clean \
	test-clean

	@# Cleans up all generated files

#######################################
# Mid Level Tasks
#######################################
compile-resources: \
	xtask-clean-resources \
	xtask-generate-qrc-data \
	xtask-generate-qrc-i18n \
	xtask-generate-qrc-qml

	@mkdir -p ${DIR_BUILD_RESOURCES}
	@cp -r \
		${DIR_BUILD_QRC_QML}/. \
	 	${DIR_BUILD_QRC_DATA}/. \
	 	${DIR_BUILD_QRC_I18N}/. \
	 	${DIR_BUILD_RESOURCES}
	@${TOOL_RCC} \
		${DIR_BUILD_RESOURCES}/data.qrc \
		${DIR_BUILD_RESOURCES}/i18n.qrc \
		${DIR_BUILD_RESOURCES}/qml.qrc \
		-o ${FILE_RESOURCES}


#######################################
# Low Level Tasks
#######################################
xtask-clean-resources:
	@rm -rf ${DIR_BUILD_RESOURCES}

xtask-generate-qrc-data:
	@rm -rf ${DIR_BUILD_QRC_DATA}
	@mkdir -p ${DIR_BUILD_QRC_DATA}
	@cp -r data ${DIR_BUILD_QRC_DATA}
	@cd ${DIR_BUILD_QRC_DATA}/data; ${TOOL_RCC} --project | sed 's,<file>./,<file>data/,' > ${FILE_QRC_DATA}

xtask-generate-qrc-i18n:
	@rm -rf ${DIR_BUILD_QRC_I18N}
	@mkdir -p ${DIR_BUILD_QRC_I18N}
	@cp -r i18n ${DIR_BUILD_QRC_I18N}
	@${DIR_BUILD_SCRIPTS}/generate-lupdate-project-file.py \
		--relative-to ${DIR_BUILD_QRC_I18N} \
		--out-file ${FILE_QRC_I18N_JSON}
	@cd ${DIR_BUILD_QRC_I18N}; ${TOOL_LRELEASE} \
		 -project ${FILE_QRC_I18N_JSON}
	@cd ${DIR_BUILD_QRC_I18N}/i18n; rm ${FILE_QRC_I18N_JSON} *.ts
	@cd ${DIR_BUILD_QRC_I18N}/i18n; ${TOOL_RCC} --project | sed 's,<file>./,<file>i18n/,' > ${FILE_QRC_I18N}

xtask-generate-qrc-qml:
	@rm -rf ${DIR_BUILD_QRC_QML}
	@mkdir -p ${DIR_BUILD_QRC_QML}
	@cp -r qml ${DIR_BUILD_QRC_QML}
	@cd ${DIR_BUILD_QRC_QML}/qml; ${TOOL_RCC} --project | sed 's,<file>./,<file>qml/,' > ${FILE_QRC_QML}

xtask-prepare-translation-extractions:
	@rm -rf ${DIR_BUILD_TRANSLATIONS}
	@mkdir -p ${DIR_BUILD_TRANSLATIONS}
	@cp -r \
		i18n \
		mpvqc \
		qml \
		${DIR_BUILD_TRANSLATIONS}
	@${DIR_BUILD_SCRIPTS}/generate-lupdate-project-file.py \
		--relative-to ${DIR_BUILD_TRANSLATIONS} \
		--out-file ${FILE_TRANSLATIONS}
