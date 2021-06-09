#!/bin/bash

source debian/vars.sh

set -x

# pulled from apr-util
mkdir -p config
cp $ea_apr_config config/apr-1-config
cp $ea_apr_config config/apr-config
cp /usr/share/pkgconfig/ea-apr16-1.pc config/apr-1.pc
cp /usr/share/pkgconfig/ea-apr16-util-1.pc config/apr-util-1.pc
cp /usr/share/pkgconfig/ea-apr16-1.pc config
cp /usr/share/pkgconfig/ea-apr16-util-1.pc config

export PKG_CONFIG_PATH="$PKG_CONFIG_PATH:`pwd`/config"
touch configure
# end pulled from apr-util

echo "RPM_FLAGS PREP"
echo "RPM_OPT_FLAGS :$RPM_OPT_FLAGS:" 
echo "RPM_BUILD_ROOT :$DEB_INSTALL_ROOT:"
echo "RPM_SOURCE_DIR :$RPM_SOURCE_DIR:"
# Patch in the vendor string and the release string
sed -i '/^#define PLATFORM/s/Unix/$vstring/' os/unix/os.h
sed -i 's/@RELEASE@/$release/' server/core.c
# Prevent use of setcap in "install-suexec-caps" target.
sed -i '/suexec/s,setcap ,echo Skipping setcap for ,' Makefile.in
# Safety check: prevent build if defined MMN does not equal upstream MMN.
vmmn=`echo MODULE_MAGIC_NUMBER_MAJOR | cpp -include include/ap_mmn.h | sed -n '/^2/p'`
if test "x${vmmn}" != "x$mmn"; then
   : Error: Upstream MMN is now ${vmmn}, packaged MMN is $mmn
   : Update the mmn macro and rebuild.
   exit 1
fi
: Building with MMN $mmn, MMN-ISA $mmnisa and vendor string '$vstring'
echo "RPM_FLAGS BUILD"
echo "RPM_OPT_FLAGS :$RPM_OPT_FLAGS:" 
echo "RPM_BUILD_ROOT :$DEB_INSTALL_ROOT:"
echo "RPM_SOURCE_DIR :$RPM_SOURCE_DIR:"
# Force dependency resolution to pick /usr/bin/perl instead of /bin/perl
# This helps downstream users of our RPMS (see: EA-7468)
export PATH="/usr/bin:$PATH"
# forcibly prevent use of bundled apr, apr-util, pcre
rm -rf srclib/{apr,apr-util,pcre}
# regenerate configure scripts
autoheader && autoconf || exit 1
# Before configure; fix location of build dir in generated apxs
$__perl -pi -e "s:\@exp_installbuilddir\@:$_libdir/apache2/build:g" support/apxs.in
export CFLAGS="$RPM_OPT_FLAGS"
export LDFLAGS="-Wl,-z,relro,-z,now"
# Hard-code path to links to avoid unnecessary builddep
export LYNX_PATH=/usr/bin/links
# Build the daemon
./configure \
    --prefix=/etc/apache2 \
    --exec-prefix=$_prefix \
    --bindir=$_bindir \
    --sbindir=$_sbindir \
    --mandir=$_mandir \
    --libdir=$_libdir \
    --sysconfdir=/etc/apache2/conf \
    --includedir=$_includedir/apache2 \
    --libexecdir=$_libdir/apache2/modules \
    --datadir=$contentdir \
    --enable-layout=cPanel \
    --with-installbuilddir=$_libdir/apache2/build \
    --enable-mpms-shared=all \
    --with-apr=$ea_apr_dir --with-apr-util=$ea_apu_dir \
    --enable-suexec \
    --enable-suexec-capabilities \
    --with-suexec-caller=$suexec_caller \
    --with-suexec-docroot=/ \
    --with-suexec-logfile=/etc/apache2/logs/suexec_log \
    --with-suexec-bin=$_sbindir/suexec \
    --with-suexec-uidmin=100 --with-suexec-gidmin=100 \
    --enable-pie \
    --with-pcre \
    --enable-mods-shared=all \
    --enable-systemd \
    --enable-ssl --with-ssl \
    --enable-ssl-staticlib-deps \
    --enable-http2 \
    --enable-nghttp2-staticlib-deps \
    --disable-distcache \
    --enable-proxy \
    --enable-proxy-fdpass \
    --enable-cache \
    --enable-disk-cache \
    --enable-ldap \
    --enable-authnz-ldap \
    --enable-cgid --enable-cgi \
    --enable-authn-anon \
    --enable-authn-alias \
    --enable-imagemap \
    --disable-echo \
    --enable-libxml2 \
    --disable-v4-mapped \
    --enable-brotli \
    $*
make 

echo "POST MAKE"
grep -R "suexec_log" *

