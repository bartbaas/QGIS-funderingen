#/***************************************************************************
# *                                                                         *
# *   This program is free software; you can redistribute it and/or modify  *
# *   it under the terms of the GNU General Public License as published by  *
# *   the Free Software Foundation; either version 2 of the License, or     *
# *   (at your option) any later version.                                   *
# *                                                                         *
# ***************************************************************************/



# Makefile for a PyQGIS plugin 

# global
PLUGINNAME = funderingsherstel
PY_FILES = __init__.py $(PLUGINNAME).py $(wildcard core/*.py)
EXTRAS = metadata.txt
TOOL_DIR = core ui
ICONS_DIR = icons

UI_SOURCES=$(wildcard ui/*.ui)
UI_FILES=$(join $(dir $(UI_SOURCES)), $(notdir $(UI_SOURCES:%.ui=%.py)))
RC_SOURCES=$(wildcard *.qrc)
RC_FILES=$(patsubst %.qrc,%.py,$(RC_SOURCES))
LN_SOURCES=$(wildcard i18n/*.ts)
LN_FILES=$(join $(dir $(LN_SOURCES)), $(notdir $(LN_SOURCES:%.ts=%.qm)))

GEN_FILES = ${UI_FILES} ${RC_FILES}

all: $(GEN_FILES)
ui: $(UI_FILES)
resources: $(RC_FILES)

$(UI_FILES): ui/%.py: ui/%.ui
	pyuic4 -o $@ $<

$(RC_FILES): %.py: %.qrc
	pyrcc4 -o $@ $<

$(LN_FILES): i18n/%.qm: i18n/%.ts
	lrelease-qt4 $<

clean:
	rm -f $(GEN_FILES) *.pyc

compile: $(UI_FILES) $(RC_FILES) $(LN_FILES)

transup:
	pylupdate4 -noobsolete $(UI_SOURCES) $(PLUGINNAME).py core/*.py -ts i18n/$(PLUGINNAME)_nl.ts

deploy: clean compile
	mkdir -p $(HOME)/.qgis2/python/plugins/$(PLUGINNAME)
	cp -rvf * $(HOME)/.qgis2/python/plugins/$(PLUGINNAME)/

# The dclean target removes compiled python files from plugin directory
# also delets any .svn entry
dclean:
	find . -iname "*.pyc" -delete
	find . -name .DS_Store -exec rm "{}" ';'

# The zip target deploys the plugin and creates a zip file with the deployed
# content. You can then upload the zip file on http://plugins.qgis.org
zip: dclean deploy
	rm -f $(PLUGINNAME).zip
	cd $(HOME)/.qgis2/python/plugins; zip -9r $(CURDIR)/$(PLUGINNAME).zip $(PLUGINNAME)
	echo "Created package: $(PLUGINNAME).zip"

# Create a zip package of the plugin named $(PLUGINNAME).zip.
# This requires use of git (your plugin development directory must be a
# git repository).
# To use, pass a valid commit or tag as follows:
# make package VERSION=Version_0.3.2
package: compile
	rm -f $(PLUGINNAME).zip
	git archive --prefix=$(PLUGINNAME)/ -o $(PLUGINNAME).zip $(VERSION)
	echo "Created package: $(PLUGINNAME).zip"