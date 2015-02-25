#-------------------------------------------------------------------------------------
#
# Start Configuration
#
#-------------------------------------------------------------------------------------

# name of the file in the SPECS directory
SPEC := httpd.spec

# name of the file in the SRPMS directory
SRPM := httpd-2.4.6-18.el6.cpanel.2.src.rpm

# name of the configuration file in /etc/mock (excluding .cfg)
CFG := ea4-httpd24-cent6-x86_64

# the upstream project
OBS_PROJECT := EA4

# the package name in OBS
OBS_PACKAGE := httpd 

#-------------------------------------------------------------------------------------
#
# End Configuration
#
#-------------------------------------------------------------------------------------

#-------------------------------------------------------------------------------------
#
# TODO
#
#-------------------------------------------------------------------------------------
# Cleaning the OBS target when files are removed from git
# 
# add a obs_dependencies target to rebuild the package and all of it's dependencies
#
# 

#-------------------
# Variables
#-------------------

whoami := $(shell whoami)

ifeq (root, $(whoami))
	MOCK := /usr/bin/mock
else
	MOCK := /usr/sbin/mock
endif

CACHE := /var/cache/mock/$(CFG)/root_cache/cache.tar.gz
MOCK_CFG := /etc/mock/$(CFG).cfg

OBS_USERNAME := $(shell grep -A5 '[build.dev.cpanel.net]' ~/.oscrc | awk -F= '/user=/ {print $$2}')
GIT_BRANCH := $(shell git branch | awk '/^*/ { print $$2 }')
BUILD_TARGET := home:$(OBS_USERNAME):$(OBS_PROJECT):$(GIT_BRANCH)
OBS_WORKDIR := OBS/$(BUILD_TARGET)/$(OBS_PACKAGE)

.PHONY: all pristine clean

#-----------------------
# Primary make targets
#-----------------------



# (Re)Build SRPMs and RPMs
#all: $(MOCK_CFG) clean make-build
all: 
	echo "$(OBS_USERNAME)"

# Same as 'all', but also rebuilds all cached data
pristine: $(MOCK_CFG) clean make-pristine make-build

# Remove per-build temp directory
clean:
	rm -rf RPMS SRPMS
	$(MOCK) -v -r $(CFG) --clean


# kick off the build to OBS
obs: .git ~/.oscrc
	rm -rf OBS
	mkdir OBS
	osc branch $(OBS_PROJECT) $(OBS_PACKAGE) $(BUILD_TARGET) $(OBS_PACKAGE) 2>/dev/null || exit 0
	cd OBS && osc co $(BUILD_TARGET)
	cp --remove-destination -pr SOURCES/* SPECS/* $(OBS_WORKDIR)
	cd $(OBS_WORKDIR) && osc add `osc status | awk '/^\?/ {print $$2}' | tr "\n" " "` 2> /dev/null || exit 0
	cd $(OBS_WORKDIR) && osc ci -m "Makefile check-in - $(shell date)"
	rm -rf OBS

# DEBUG
vars:
	@echo "OBS_USERNAME: $(OBS_USERNAME)"
	@echo "GIT_BRANCH: $(GIT_BRANCH)"
	@echo "BUILD_TARGET: $(BUILD_TARGET)"
	@echo "OBS_WORKDIR: $(OBS_WORKDIR)"

#-----------------------
# Helper make targets
#-----------------------

# Remove the root filesystem tarball used for the build environment
make-pristine:
	$(MOCK) -v -r $(CFG) --scrub=all
	rm -rf SRPMS RPMS

# Build SRPM
make-srpm-build: $(CACHE)
	$(MOCK) -v -r $(CFG) --unpriv --resultdir SRPMS --buildsrpm --spec SPECS/$(SPEC) --sources SOURCES

# Build RPMs
make-rpm-build: $(CACHE)
	$(MOCK) -v -r $(CFG) --unpriv --resultdir RPMS SRPMS/$(SRPM)

# Build both SRPM and RPMs
make-build: make-srpm-build make-rpm-build

# Create/update the root cache containing chroot env used by mock
$(CACHE):
	$(MOCK) -v -r $(CFG) --init --update

# Ensure the mock configuration is installed
$(MOCK_CFG):
	sudo cp $(CFG).cfg $@
