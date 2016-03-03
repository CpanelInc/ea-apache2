#-------------------------------------------------------------------------------------
#
# Start Configuration
#
#-------------------------------------------------------------------------------------

# the upstream project
OBS_PROJECT := EA4

# the package name in OBS
OBS_PACKAGE := ea-apache2

#-------------------------------------------------------------------------------------
#
# End Configuration
#
#-------------------------------------------------------------------------------------

#-------------------
# Variables
#-------------------

OSC := /usr/bin/osc
BUILD := /usr/bin/build
RPMLINT := /usr/bin/rpmlint

# allows developers to branch off of a project in different OBS repo that may not
# exist in $(OBS_PROJECT) yet (e.g. new packages)
ifndef BRANCH_PROJECT
BRANCH_PROJECT := $(OBS_PROJECT)
endif

# allow developer to override which pacakge to debug when doing 'make chroot'
ifndef ARCH
ARCH := $(shell uname -m)
endif

DISPMSG := $(shell echo -en "You haven't set up OBS correctly on your machine.\nPlease read, https://cpanel.wiki/display/AL/Setting+up+yourself+for+using+OBS")
OBS_USERNAME := $(shell grep -A5 '[build.dev.cpanel.net]' ~/.oscrc 2>/dev/null| awk -F= '/user=/ {print $$2}')

# NOTE: OBS only like ascii alpha-numeric characters
ORIG_GIT_BRANCH := $(shell git branch 2>/dev/null | awk '/^*/ { print $$2 }')
ifdef bamboo_repository_git_branch
GIT_BRANCH := $(bamboo_repository_git_branch)
else
GIT_BRANCH := $(ORIG_GIT_BRANCH)
endif

# OBS only supports alpha-numeric branch names
GIT_BRANCH := $(shell echo "$(GIT_BRANCH)" | sed -e 's/[^a-z0-9]/-/ig')

# if we're pushing to master, push to the upstream project
ifeq ($(bamboo_repository_git_branch),master)
BUILD_TARGET := $(OBS_PROJECT)
# otherwise, push to a local integration area.  we substitute ':' because
# OBS doesn't properly create the directory when it has : in it
else
BUILD_TARGET := home:$(OBS_USERNAME):$(subst :,-,$(OBS_PROJECT)):$(GIT_BRANCH)
endif

# the name of the spec file (hopefully there's only 1)
SPEC := $(shell ls -1 SPECS | head -1)

# Temporary variable used by build-init
TMP_OSC := $(shell echo .osc.tmp.$$$$)

OBS_WORKDIR := $(BUILD_TARGET)/$(OBS_PACKAGE)

.PHONY: clean local vars chroot obs check build-clean build-init warnmsg errmsg help

#-----------------------
# Primary make targets
#-----------------------

all: local

clean: build-clean

help:
	@echo "This Makefile supports the following targets:"
	@echo " * clean -- Removes build and temporary files"
	@echo " * local -- Builds a package using a local chroot build environment"
	@echo " * chroot -- Log into the local chroot build environment (useful for debugging)"
	@echo " * obs -- Instruct OBS to start building your package"
	@echo " * check -- Verify that you have a suitable build environment"
	@echo " * vars -- Debugging routine that displays the variables used in this Makefile"

# Builds the RPMs on your local machine using the OBS infrstructure.
# This is useful to test before submitting to OBS.
#
# For example, if you wanted to build PHP without running tests:
#	OSC_BUILD_OPTS='--define="runselftest 0"' make local
local:
	make build-init
	cd OBS/$(OBS_WORKDIR) && $(OSC) build $(OSC_BUILD_OPTS) --clean --noverify --disable-debuginfo CentOS_6.5_standard $(ARCH) $(SPEC)
	make build-clean

# This allows you to debug your build if it fails by logging into the
# build environment and letting you manually run commands.
#
# TODO: Stop hard-coding CentOS_6.5_standard, and look up a matching upstream repo
chroot:
	make build-init
	cd OBS/$(OBS_WORKDIR) && $(OSC) chroot --local-package -o CentOS_6.5_standard $(ARCH) $(OBS_PACKAGE)
	make build-clean

# Commits local file changes to OBS, then ensures that changes are queued for a build and
# are published once complete.
obs:
	make build-init
	cd OBS/$(OBS_WORKDIR) && $(OSC) addremove -r 2> /dev/null || exit 0
	cd OBS/$(OBS_WORKDIR) && $(OSC) ci -m "action(commit) make(obs.mk) hostname($(shell hostname)) date($(shell date)) branch($(ORIG_GIT_BRANCH))"
	$(OSC) api -X POST "/source/$(BUILD_TARGET)?cmd=set_flag&flag=publish&status=enable"
	$(OSC) api -X POST "/source/$(BUILD_TARGET)?cmd=set_flag&flag=build&status=enable"
	make build-clean

# Debug target: Prints out variables to ensure they're correct
vars: check
	@echo "ARCH: $(ARCH)"
	@echo "OBS_USERNAME: $(OBS_USERNAME)"
	@echo "GIT_BRANCH: $(GIT_BRANCH) ($(ORIG_GIT_BRANCH))"
	@echo "BUILD_TARGET: $(BUILD_TARGET)"
	@echo "OBS_WORKDIR: $(OBS_WORKDIR)"
	@echo "OBS_PROJECT: $(OBS_PROJECT)"
	@echo "BRANCH_PROJECT: $(BRANCH_PROJECT)"
	@echo "OBS_PACKAGE: $(OBS_PACKAGE)"
	@echo "TMP_OSC: $(TMP_OSC)"
	@echo "SPEC: $(SPEC)"
	@echo

#-----------------------
# Helper make targets
#-----------------------

build-init: check build-clean
	mkdir OBS
	$(OSC) branch $(BRANCH_PROJECT) $(OBS_PACKAGE) $(BUILD_TARGET) $(OBS_PACKAGE) &>$(TMP_OSC) || ( grep -q "already exists" $(TMP_OSC) && ( rm -f $(TMP_OSC) ; exit 0 ) || ( rm -rf $(TMP_OSC) ; exit 1 ) )
	cd OBS && $(OSC) co $(BUILD_TARGET)
	mv OBS/$(OBS_WORKDIR)/.osc OBS/$(TMP_OSC)
	rm -rf OBS/$(OBS_WORKDIR)/*
	mkdir -p OBS/$(BUILD_TARGET)/$(OBS_PACKAGE)
	cp --remove-destination -pr SOURCES/* SPECS/* OBS/$(OBS_WORKDIR)
	mv OBS/$(TMP_OSC) OBS/$(OBS_WORKDIR)/.osc

build-clean:
	rm -rf ./OBS ./.osc.tmp.*

# place PATH before this because cpanel overrides python location
rpmlint:
	@echo "Check(rpmlint):"; PATH=/bin:/usr/bin $(RPMLINT) SPECS/$(SPEC); echo

check:
	@[ -n "$(OBS_PACKAGE)" ] || DISPMSG="You must define the OBS_PACKAGE variable in your Makefile" make -e errmsg
	@[ -n "$(OBS_PROJECT)" ] || DISPMSG="You must define the OBS_PROJECT variable in your Makefile" make -e errmsg
	@[ -d .git ] || DISPMSG="This isn't a git repository." make -e errmsg
	@[ -n "$(GIT_BRANCH)" ] || DISPMSG="Are you sure you're in a git repository?" make -e errmsg
	@[ -z "$(bamboo_repository_git_branch)" ] && ( rpm -q osc &>/dev/null || make errmsg ) || exit 0
	@[ -z "$(bamboo_repository_git_branch)" ] && ( rpm -q build &>/dev/null || make errmsg ) || exit 0
	@[ -z "$(bamboo_repository_git_branch)" ] && ( [ -x $(RPMLINT) ] || DISPMSG="You should use YUM to install the 'rpmlint' package" make -e warnmsg ) || exit 0
	@[ -e ~/.oscrc ] || make errmsg
	@[ -n "$(OBS_USERNAME)" ] || make errmsg
	@[ -n "$(SPEC)" ] || DISPMSG="Unable to find a SPEC file" make -e errmsg
	@[ -x $(OSC) ] || make errmsg
	@[ -x $(BUILD) ] || make errmsg
	@[ -n "$(ARCH)" ] || DISPMSG="Unable to determine host architecture type using ARCH environment variable" make -e errmsg
	@$(OSC) api -X GET /source/$(BRANCH_PROJECT)/$(OBS_PACKAGE) &>/dev/null || DISPMSG="Failed to find the $(BRANCH_PROJECT):$(OBS_PACKAGE) OBS project" make -e errmsg

warnmsg:
	@echo -e "\nWARNING: $(DISPMSG)\n";
	@exit 0

errmsg:
	@echo -e "\nERROR: $(DISPMSG)\n"
	@exit 1
