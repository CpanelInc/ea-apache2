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

#-------------------------------------------------------------------------------------
#
# End Configuration
#
#-------------------------------------------------------------------------------------

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

.PHONY: all pristine clean

#-----------------------
# Primary make targets
#-----------------------

# (Re)Build SRPMs and RPMs
all: $(MOCK_CFG) clean make-build

# Same as 'all', but also rebuilds all cached data
pristine: $(MOCK_CFG) clean make-pristine make-build

# Remove per-build temp directory
clean:
	rm -rf RPMS SRPMS
	$(MOCK) -v -r $(CFG) --clean

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
