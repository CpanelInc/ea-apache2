%define contentdir %{_datadir}/apache2
%define docroot /var/www
%define suexec_caller nobody
%define mmn 20120211
%define oldmmnisa %{mmn}-%{__isa_name}-%{__isa_bits}
%define mmnisa %{mmn}%{__isa_name}%{__isa_bits}
%define vstring cPanel

# Drop automatic provides for module DSOs
%{?filter_setup:
%filter_provides_in %{_libdir}/apache2/modules/.*\.so$
%filter_setup
}

Summary: Apache HTTP Server
Name: ea-apache2
Version: 2.4.12
Release: 2%{?dist}.cpanel.1
Vendor: cPanel, Inc.
URL: http://httpd.apache.org/
Source0: http://www.apache.org/dist/httpd/httpd-%{version}.tar.bz2
Source1: centos-noindex.tar.gz
Source2: httpd.logrotate
Source3: httpd.sysconf

Source6: httpd.init

Source10: httpd.conf
Source14: 01-cgi.conf
Source20: userdir.conf
Source21: ssl.conf
Source22: welcome.conf
Source23: manual.conf

# Documentation
Source30: README.confd
Source40: htcacheclean.init
Source41: htcacheclean.sysconf
# build/scripts patches
Patch1: httpd-2.4.1-apctl.patch
Patch2: httpd-2.4.3-apxs.patch
Patch3: httpd-2.4.1-deplibs.patch
Patch5: httpd-2.4.3-layout.patch

# Features/functional changes
Patch23: httpd-2.4.4-export.patch
Patch24: httpd-2.4.1-corelimit.patch
Patch25: httpd-2.4.1-selinux.patch
Patch26: httpd-2.4.4-r1337344+.patch
Patch27: httpd-2.4.2-icons.patch

Patch30: httpd-2.4.4-cachehardmax.patch
# Bug fixes
Patch55: httpd-2.4.4-malformed-host.patch
Patch59: httpd-2.4.6-r1556473.patch
# cPanel-specific patches
Patch301: 2.2_cpanel_whmserverstatus.patch
Patch302: 2.2.17_cpanel_suexec_script_share.patch
Patch303: 2.2.17_cpanel_mailman_suexec.patch
Patch304: 2.2_cpanel_fileprotect_suexec_httpusergroupallow.patch

License: ASL 2.0
Group: System Environment/Daemons
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root
BuildRequires: autoconf, perl, pkgconfig, findutils, xmlto
BuildRequires: zlib-devel, libselinux-devel, lua-devel
BuildRequires: apr-devel >= 1.5.0, apr-util-devel >= 1.2.0, pcre-devel >= 5.0
Requires: /etc/mime.types, system-logos >= 7.92.1-1, apr >= 1.5.0
Requires: ea-apache2-mpm
Obsoletes: httpd-suexec
Conflicts: webserver
Provides: ea-webserver
Provides: ea-apache2-suexec = %{version}-%{release}
Provides: ea-apache2-mmn = %{mmn}, ea-apache2-mmn = %{mmnisa}
Provides: ea-apache2-mmn = %{oldmmnisa}
Requires: ea-apache2-tools = %{version}-%{release}
Requires(post): chkconfig

%description
The Apache HTTP Server is a powerful, efficient, and extensible
web server.

%package devel
Group: Development/Libraries
Summary: Development interfaces for the Apache HTTP server
Obsoletes: secureweb-devel, apache-devel, stronghold-apache-devel, httpd-devel
Requires: apr-devel >= 1.5.0, apr-util-devel, pkgconfig
Requires: ea-apache2 = %{version}-%{release}

%description devel
The ea-apache2-devel package contains the APXS binary and other files
that you need to build Dynamic Shared Objects (DSOs) for the
Apache HTTP Server.

If you are installing the Apache HTTP server and you want to be
able to compile or develop additional modules for Apache, you need
to install this package.

%package manual
Group: Documentation
Summary: Documentation for the Apache HTTP server
Requires: ea-apache2 = %{version}-%{release}
Obsoletes: secureweb-manual, apache-manual, httpd-manual
BuildArch: noarch

%description manual
The ea-apache2-manual package contains the complete manual and
reference guide for the Apache HTTP server. The information can
also be found at http://httpd.apache.org/docs/2.4/.

%package tools
Group: System Environment/Daemons
Summary: Tools for use with the Apache HTTP Server

%description tools
The ea-apache2-tools package contains tools which can be used with
the Apache HTTP Server.

%package -n ea-mod_mpm_event
Group: System Environment/Daemons
Summary: Threaded event Multi-Processing Module for Apache HTTP Server
Requires: ea-apache2 = 0:%{version}-%{release}, ea-apache2-mmn = %{mmnisa}
Provides: ea-apache2-mpm = threaded
Conflicts: ea-mod_mpm_prefork, ea-mod_mpm_worker, ea-mod_mpm_itk

%description -n ea-mod_mpm_event
The Event MPM provides a threaded model for workers, with the additional
feature that all keepalive connections are handled by a single thread.

%package -n ea-mod_mpm_prefork
Group: System Environment/Daemons
Summary: Prefork Multi-Processing Module for Apache HTTP Server
Requires: ea-apache2 = 0:%{version}-%{release}, ea-apache2-mmn = %{mmnisa}
Provides: ea-apache2-mpm = forked
Conflicts: ea-mod_mpm_event, ea-mod_mpm_worker, ea-mod_mpm_itk

%description -n ea-mod_mpm_prefork
The traditional forked worker model.

%package -n ea-mod_mpm_worker
Group: System Environment/Daemons
Summary: Threaded worker Multi-Processing Module for Apache HTTP Server
Requires: ea-apache2 = 0:%{version}-%{release}, ea-apache2-mmn = %{mmnisa}
Provides: ea-apache2-mpm = threaded
Conflicts: ea-mod_mpm_event, ea-mod_mpm_prefork, ea-mod_mpm_itk

%description -n ea-mod_mpm_worker
The Worker MPM provides a threaded worker model.

%package -n ea-mod_asis
Group: System Environment/Daemons
Summary: As-is provider module for the Apache HTTP Server
Requires: ea-apache2 = 0:%{version}-%{release}, ea-apache2-mmn = %{mmnisa}

%description -n ea-mod_asis
The mod_asis module provides the handler send-as-is which causes
Apache HTTP Server to send the document without adding most of the
usual HTTP headers.

%package -n ea-mod_dav
Group: System Environment/Daemons
Summary: DAV module for the Apache HTTP server
Requires: ea-apache2 = 0:%{version}-%{release}, ea-apache2-mmn = %{mmnisa}

%description -n ea-mod_dav
The mod_dav module provides class 1 and class 2 WebDAV ('Web-based
Distributed Authoring and Versioning') functionality for Apache. This
extension to the HTTP protocol allows creating, moving, copying, and
deleting resources and collections on a remote web server.

%package -n ea-mod_dav_fs
Group: System Environment/Daemons
Summary: DAV filesystem provider module for the Apache HTTP server
Requires: ea-apache2 = 0:%{version}-%{release}, ea-apache2-mmn = %{mmnisa}
Requires: ea-mod_dav = 0:%{version}-%{release}

%description -n ea-mod_dav_fs
The mod_dav_fs module acts as a support module for mod_dav and
provides access to resources located in the file system.  The formal
name of this provider is filesystem.

%package -n ea-mod_dav_lock
Group: System Environment/Daemons
Summary: Generic DAV locking module for the Apache HTTP server
Requires: ea-apache2 = 0:%{version}-%{release}, ea-apache2-mmn = %{mmnisa}
Requires: ea-mod_dav = 0:%{version}-%{release}

%description -n ea-mod_dav_lock
The mod_dav_lock implements a generic locking API which can be used by
any backend provider of mod_dav.  Without a backend provider which
makes use of it, however, it should not be loaded into the server.

%package -n ea-mod_ssl
Group: System Environment/Daemons
Summary: SSL/TLS module for the Apache HTTP Server
Epoch: 1
BuildRequires: openssl-devel
Requires(post): openssl, /bin/cat
Requires(pre): ea-apache2
Requires: ea-apache2 = 0:%{version}-%{release}, ea-apache2-mmn = %{mmnisa}
Obsoletes: stronghold-mod_ssl, mod_ssl

%description -n ea-mod_ssl
The mod_ssl module provides strong cryptography for the Apache Web
server via the Secure Sockets Layer (SSL) and Transport Layer
Security (TLS) protocols.

%package -n ea-mod_proxy_html
Group: System Environment/Daemons
Summary: HTML and XML content filters for the Apache HTTP Server
Requires: ea-apache2 = 0:%{version}-%{release}, ea-apache2-mmn = %{mmnisa}
BuildRequires: libxml2-devel
Epoch: 1
Obsoletes: mod_proxy_html < 1:2.4.1-2

%description -n ea-mod_proxy_html
The mod_proxy_html and mod_xml2enc modules provide filters which can
transform and modify HTML and XML content.

%package -n ea-mod_ldap
Group: System Environment/Daemons
Summary: LDAP authentication modules for the Apache HTTP Server
Requires: ea-apache2 = 0:%{version}-%{release}, ea-apache2-mmn = %{mmnisa}
Requires: apr-util-ldap

%description -n ea-mod_ldap
The mod_ldap and mod_authnz_ldap modules add support for LDAP
authentication to the Apache HTTP Server.

%package -n ea-mod_session
Group: System Environment/Daemons
Summary: Session interface for the Apache HTTP Server
Requires: ea-apache2 = 0:%{version}-%{release}, ea-apache2-mmn = %{mmnisa}

%description -n ea-mod_session
The mod_session module and associated backends provide an abstract
interface for storing and accessing per-user session data.

%prep
%setup -q -n httpd-%{version}
%patch1 -p1 -b .apctl
%patch2 -p1 -b .apxs
%patch3 -p1 -b .deplibs
%patch5 -p1 -b .layout

%patch23 -p1 -b .export
%patch24 -p1 -b .corelimit
%patch25 -p1 -b .selinux
%patch26 -p1 -b .r1337344+
%patch27 -p1 -b .icons

%patch30 -p1 -b .cachehardmax

%patch55 -p1 -b .malformedhost
%patch59 -p1 -b .r1556473

%patch301 -p1 -b .cpWHM
%patch302 -p1 -b .cpsuexec1
%patch303 -p1 -b .cpsuexec2
%patch304 -p1 -b .cpsuexec3

# Patch in the vendor string and the release string
sed -i '/^#define PLATFORM/s/Unix/%{vstring}/' os/unix/os.h
sed -i 's/@RELEASE@/%{release}/' server/core.c

# Prevent use of setcap in "install-suexec-caps" target.
sed -i '/suexec/s,setcap ,echo Skipping setcap for ,' Makefile.in

# Safety check: prevent build if defined MMN does not equal upstream MMN.
vmmn=`echo MODULE_MAGIC_NUMBER_MAJOR | cpp -include include/ap_mmn.h | sed -n '/^2/p'`
if test "x${vmmn}" != "x%{mmn}"; then
   : Error: Upstream MMN is now ${vmmn}, packaged MMN is %{mmn}
   : Update the mmn macro and rebuild.
   exit 1
fi

: Building with MMN %{mmn}, MMN-ISA %{mmnisa} and vendor string '%{vstring}'

%build
# forcibly prevent use of bundled apr, apr-util, pcre
rm -rf srclib/{apr,apr-util,pcre}

# regenerate configure scripts
autoheader && autoconf || exit 1

# Before configure; fix location of build dir in generated apxs
%{__perl} -pi -e "s:\@exp_installbuilddir\@:%{_libdir}/apache2/build:g" \
	support/apxs.in

export CFLAGS=$RPM_OPT_FLAGS
export LDFLAGS="-Wl,-z,relro,-z,now"

%ifarch ppc64
CFLAGS="$CFLAGS -O3"
%endif

# Hard-code path to links to avoid unnecessary builddep
export LYNX_PATH=/usr/bin/links

# Build the daemon
./configure \
 	--prefix=%{_sysconfdir}/apache2 \
 	--exec-prefix=%{_prefix} \
 	--bindir=%{_bindir} \
 	--sbindir=%{_sbindir} \
 	--mandir=%{_mandir} \
	--libdir=%{_libdir} \
	--sysconfdir=%{_sysconfdir}/apache2/conf \
	--includedir=%{_includedir}/apache2 \
	--libexecdir=%{_libdir}/apache2/modules \
	--datadir=%{contentdir} \
        --enable-layout=cPanel \
        --with-installbuilddir=%{_libdir}/apache2/build \
        --enable-mpms-shared=all \
        --with-apr=%{_prefix} --with-apr-util=%{_prefix} \
	--enable-suexec --with-suexec \
        --enable-suexec-capabilities \
	--with-suexec-caller=%{suexec_caller} \
	--with-suexec-docroot=%{docroot} \
	--without-suexec-logfile \
        --with-suexec-syslog \
	--with-suexec-bin=%{_sbindir}/suexec \
	--with-suexec-uidmin=500 --with-suexec-gidmin=100 \
        --enable-pie \
        --with-pcre \
        --enable-mods-shared=all \
	--enable-ssl --with-ssl --disable-distcache \
	--enable-proxy \
        --enable-cache \
        --enable-disk-cache \
        --enable-ldap --enable-authnz-ldap \
        --enable-cgid --enable-cgi \
        --enable-authn-anon --enable-authn-alias \
        --disable-imagemap  \
	$*
make %{?_smp_mflags}

%install
rm -rf $RPM_BUILD_ROOT

make DESTDIR=$RPM_BUILD_ROOT install

# install SYSV init stuff
mkdir -p $RPM_BUILD_ROOT%{_initrddir}
for s in httpd htcacheclean; do
	install -p -m 755 $RPM_SOURCE_DIR/${s}.init \
		$RPM_BUILD_ROOT%{_initrddir}/${s}
done

# install conf file/directory
mkdir $RPM_BUILD_ROOT%{_sysconfdir}/apache2/conf.d \
      $RPM_BUILD_ROOT%{_sysconfdir}/apache2/conf.modules.d
install -m 644 $RPM_SOURCE_DIR/README.confd \
    $RPM_BUILD_ROOT%{_sysconfdir}/apache2/conf.d/README
for f in 01-cgi.conf ; do
  install -m 644 -p $RPM_SOURCE_DIR/$f \
        $RPM_BUILD_ROOT%{_sysconfdir}/apache2/conf.modules.d/$f
done

for f in welcome.conf ssl.conf manual.conf userdir.conf; do
  install -m 644 -p $RPM_SOURCE_DIR/$f \
        $RPM_BUILD_ROOT%{_sysconfdir}/apache2/conf.d/$f
done

# Split-out extra config shipped as default in conf.d:
for f in autoindex; do
  mv docs/conf/extra/httpd-${f}.conf \
        $RPM_BUILD_ROOT%{_sysconfdir}/apache2/conf.d/${f}.conf
done

# Extra config trimmed:
rm -v docs/conf/extra/httpd-{ssl,userdir}.conf

rm $RPM_BUILD_ROOT%{_sysconfdir}/apache2/conf/*.conf
install -m 644 -p $RPM_SOURCE_DIR/httpd.conf \
   $RPM_BUILD_ROOT%{_sysconfdir}/apache2/conf/httpd.conf

mkdir $RPM_BUILD_ROOT%{_sysconfdir}/sysconfig
for s in httpd htcacheclean; do
  install -m 644 -p $RPM_SOURCE_DIR/${s}.sysconf \
                    $RPM_BUILD_ROOT%{_sysconfdir}/sysconfig/${s}
done

# Other directories
mkdir -p $RPM_BUILD_ROOT%{_localstatedir}/lib/dav \
         $RPM_BUILD_ROOT%{_localstatedir}/run/apache2/htcacheclean

# Create cache directory
mkdir -p $RPM_BUILD_ROOT%{_localstatedir}/cache/apache2 \
         $RPM_BUILD_ROOT%{_localstatedir}/cache/apache2/proxy \
         $RPM_BUILD_ROOT%{_localstatedir}/cache/apache2/ssl

# Make the MMN accessible to module packages
echo %{mmnisa} > $RPM_BUILD_ROOT%{_includedir}/apache2/.mmn
mkdir -p $RPM_BUILD_ROOT%{_sysconfdir}/rpm
cat > $RPM_BUILD_ROOT%{_sysconfdir}/rpm/macros.apache2 <<EOF
%%_httpd_mmn %{mmnisa}
%%_httpd_apxs %{_bindir}/apxs
%%_httpd_modconfdir %{_sysconfdir}/apache2/conf.modules.d
%%_httpd_confdir %{_sysconfdir}/apache2/conf.d
%%_httpd_contentdir %{contentdir}
%%_httpd_moddir %{_libdir}/apache2/modules
EOF

# Handle contentdir
mkdir $RPM_BUILD_ROOT%{contentdir}/noindex
tar xzf $RPM_SOURCE_DIR/centos-noindex.tar.gz \
        -C $RPM_BUILD_ROOT%{contentdir}/noindex/ \
        --strip-components=1

rm -rf %{contentdir}/htdocs

# remove manual sources
find $RPM_BUILD_ROOT%{contentdir}/manual \( \
    -name \*.xml -o -name \*.xml.* -o -name \*.ent -o -name \*.xsl -o -name \*.dtd \
    \) -print0 | xargs -0 rm -f

# Strip the manual down just to English and replace the typemaps with flat files:
set +x
for f in `find $RPM_BUILD_ROOT%{contentdir}/manual -name \*.html -type f`; do
   if test -f ${f}.en; then
      cp ${f}.en ${f}
      rm ${f}.*
   fi
done
set -x

# Clean Document Root
rm -v $RPM_BUILD_ROOT%{docroot}/html/*.html \
      $RPM_BUILD_ROOT%{docroot}/cgi-bin/*

# Symlink for the powered-by-$DISTRO image:
ln -s ../noindex/images/poweredby.png \
        $RPM_BUILD_ROOT%{contentdir}/icons/poweredby.png

# symlinks for /etc/httpd
ln -s ../..%{_localstatedir}/log/apache2 $RPM_BUILD_ROOT/etc/apache2/logs
ln -s ../..%{_localstatedir}/run/apache2 $RPM_BUILD_ROOT/etc/apache2/run
ln -s ../..%{_libdir}/apache2/modules $RPM_BUILD_ROOT/etc/apache2/modules

# Install logrotate config
mkdir -p $RPM_BUILD_ROOT/etc/logrotate.d
install -m 644 -p $RPM_SOURCE_DIR/httpd.logrotate \
	$RPM_BUILD_ROOT/etc/logrotate.d/apache2

# fix man page paths
sed -e "s|/usr/local/apache2/conf/httpd.conf|/etc/apache2/conf/httpd.conf|" \
    -e "s|/usr/local/apache2/conf/mime.types|/etc/mime.types|" \
    -e "s|/usr/local/apache2/conf/magic|/etc/apache2/conf/magic|" \
    -e "s|/usr/local/apache2/logs/error_log|/var/log/apache2/error_log|" \
    -e "s|/usr/local/apache2/logs/access_log|/var/log/apache2/access_log|" \
    -e "s|/usr/local/apache2/logs/httpd.pid|/var/run/apache2/httpd.pid|" \
    -e "s|/usr/local/apache2|/etc/apache2|" < docs/man/httpd.8 \
  > $RPM_BUILD_ROOT%{_mandir}/man8/httpd.8

# Make ap_config_layout.h libdir-agnostic
sed -i '/.*DEFAULT_..._LIBEXECDIR/d;/DEFAULT_..._INSTALLBUILDDIR/d' \
    $RPM_BUILD_ROOT%{_includedir}/apache2/ap_config_layout.h

# Fix path to instdso in special.mk
sed -i '/instdso/s,top_srcdir,top_builddir,' \
    $RPM_BUILD_ROOT%{_libdir}/apache2/build/special.mk

# Make individual module package files
# We'll number the conf.modules.d files, so we can force load order,
# and since there's a lot of them, we'll use 3 digits

for mod in mpm_event mpm_prefork mpm_worker
do
    printf -v modname "000_mod_%s.conf" $mod
    cat > $RPM_BUILD_ROOT%{_sysconfdir}/apache2/conf.modules.d/${modname} <<EOF
# Enable mod_${mod}
LoadModule ${mod}_module modules/mod_${mod}.so
EOF
    cat > files.${mod} <<EOF
%attr(755,root,root) %{_libdir}/apache2/modules/mod_${mod}.so
%config(noreplace) %attr(644,root,root) %{_sysconfdir}/apache2/conf.modules.d/${modname}
EOF
done

# Modules we're not splitting out... yet
  #cgi cgid \

modnum=5

for mod in \
  access_compat actions alias allowmethods asis auth_basic auth_digest \
  authn_anon authn_core authn_dbd authn_dbm authn_file authn_socache \
  authz_core authz_dbd authz_dbm authz_groupfile authz_host authz_owner \
  authz_user autoindex buffer cache cache_disk cache_socache \
  charset_lite data dav dav_fs dav_lock dbd deflate dialup dir dumpio \
  echo env expires ext_filter file_cache filter headers \
  heartmonitor include info log_config log_debug log_forensic logio lua \
  macro mime mime_magic negotiation \
  proxy lbmethod_bybusyness lbmethod_byrequests lbmethod_bytraffic \
  lbmethod_heartbeat proxy_ajp proxy_balancer proxy_connect \
  proxy_express proxy_fcgi proxy_fdpass proxy_ftp proxy_http proxy_scgi \
  proxy_wstunnel ratelimit reflector remoteip reqtimeout request rewrite \
  sed setenvif slotmem_plain slotmem_shm socache_dbm socache_memcache \
  socache_shmcb speling status substitute suexec unique_id unixd userdir \
  usertrack version vhost_alias watchdog heartbeat \
  ssl \
  proxy_html xml2enc \
  ldap authnz_ldap \
  session session_cookie session_dbd auth_form session_crypto
do
    printf -v modname "%03d_mod_%s.conf" $modnum $mod
    cat > $RPM_BUILD_ROOT%{_sysconfdir}/apache2/conf.modules.d/${modname} <<EOF
# Enable mod_${mod}
LoadModule ${mod}_module modules/mod_${mod}.so
EOF
    cat > files.${mod} <<EOF
%attr(755,root,root) %{_libdir}/apache2/modules/mod_${mod}.so
%config(noreplace) %attr(644,root,root) %{_sysconfdir}/apache2/conf.modules.d/${modname}
EOF
    # Let's stride by 5, in case there is need to insert things
    # between two modules
    modnum=$(($modnum+5))
done

# proxy_html package needs xml2enc
cat files.xml2enc >> files.proxy_html

# ldap and authnz_ldap belong in the same package
cat files.authnz_ldap >> files.ldap

# Session-related modules
cat files.session_cookie files.session_dbd files.auth_form \
  files.session_crypto >> files.session

# The rest of the modules, into the main list
cat files.access_compat files.actions files.alias files.allowmethods \
  files.auth_basic files.auth_digest files.authn_anon \
  files.authn_core files.authn_dbd files.authn_dbm files.authn_file \
  files.authn_socache files.authz_core files.authz_dbd files.authz_dbm \
  files.authz_groupfile files.authz_host files.authz_owner \
  files.authz_user files.autoindex files.buffer files.cache \
  files.cache_disk files.cache_socache \
  files.charset_lite files.data \
  files.dbd files.deflate files.dialup files.dir files.dumpio files.echo \
  files.env files.expires files.ext_filter files.file_cache files.filter \
  files.headers files.heartbeat files.heartmonitor files.include \
  files.info files.log_config files.log_debug files.log_forensic \
  files.logio files.lua files.macro files.mime files.mime_magic \
  files.negotiation \
  files.proxy files.lbmethod_bybusyness files.lbmethod_byrequests \
  files.lbmethod_bytraffic files.lbmethod_heartbeat files.proxy_ajp \
  files.proxy_balancer files.proxy_connect files.proxy_express \
  files.proxy_fcgi files.proxy_fdpass files.proxy_ftp files.proxy_http \
  files.proxy_scgi files.proxy_wstunnel files.ratelimit files.reflector \
  files.remoteip files.reqtimeout files.request files.rewrite files.sed \
  files.setenvif files.slotmem_plain files.slotmem_shm files.socache_dbm \
  files.socache_memcache files.socache_shmcb files.speling files.status \
  files.substitute files.suexec files.unique_id files.unixd \
  files.userdir files.usertrack files.version files.vhost_alias \
  files.watchdog > files.httpd

# Remove unpackaged files
rm -vf \
      $RPM_BUILD_ROOT%{_libdir}/*.exp \
      $RPM_BUILD_ROOT/etc/apache2/conf/mime.types \
      $RPM_BUILD_ROOT%{_libdir}/apache2/modules/*.exp \
      $RPM_BUILD_ROOT%{_libdir}/apache2/build/config.nice \
      $RPM_BUILD_ROOT%{_bindir}/{ap?-config,dbmmanage} \
      $RPM_BUILD_ROOT%{_sbindir}/{checkgid,envvars*} \
      $RPM_BUILD_ROOT%{contentdir}/htdocs/* \
      $RPM_BUILD_ROOT%{_mandir}/man1/dbmmanage.* \
      $RPM_BUILD_ROOT%{contentdir}/cgi-bin/*

rm -rf $RPM_BUILD_ROOT/etc/apache2/conf/{original,extra}

%pre
# Make sure /etc/apache2 is not already there, as a symlink
if [ -L /etc/apache2 ] ; then
  rm -f /etc/apache2
fi

%post
# Register the httpd service
/sbin/chkconfig --add httpd
/sbin/chkconfig --add htcacheclean

%preun
if [ $1 = 0 ]; then
        /sbin/service httpd stop > /dev/null 2>&1
        /sbin/chkconfig --del httpd
        /sbin/service htcacheclean stop > /dev/null 2>&1
        /sbin/chkconfig --del htcacheclean
fi

%posttrans
test -f /etc/sysconfig/httpd-disable-posttrans || \
 /sbin/service httpd condrestart >/dev/null 2>&1 || :

%define sslcert %{_sysconfdir}/pki/tls/certs/localhost.crt
%define sslkey %{_sysconfdir}/pki/tls/private/localhost.key

%post -n ea-mod_ssl
umask 077

if [ -f %{sslkey} -o -f %{sslcert} ]; then
   exit 0
fi

if [ ! -f %{sslkey} ] ; then
%{_bindir}/openssl genrsa -rand /proc/apm:/proc/cpuinfo:/proc/dma:/proc/filesystems:/proc/interrupts:/proc/ioports:/proc/pci:/proc/rtc:/proc/uptime 2048 > %{sslkey} 2> /dev/null
fi

FQDN=`hostname`
if [ "x${FQDN}" = "x" ]; then
   FQDN=localhost.localdomain
fi

if [ ! -f %{sslcert} ] ; then
cat << EOF | %{_bindir}/openssl req -new -key %{sslkey} \
         -x509 -sha256 -days 365 -set_serial $RANDOM -extensions v3_req \
         -out %{sslcert} 2>/dev/null
--
SomeState
SomeCity
SomeOrganization
SomeOrganizationalUnit
${FQDN}
root@${FQDN}
EOF
fi

%check
# Check the built modules are all PIC
if readelf -d $RPM_BUILD_ROOT%{_libdir}/apache2/modules/*.so | grep TEXTREL; then
   : modules contain non-relocatable code
   exit 1
fi

%clean
rm -rf $RPM_BUILD_ROOT

%files -f files.httpd
%defattr(-,root,root)

%doc ABOUT_APACHE README CHANGES LICENSE VERSIONING NOTICE
%doc docs/conf/extra/*.conf

%dir %{_sysconfdir}/apache2
%{_sysconfdir}/apache2/modules
%{_sysconfdir}/apache2/logs
%{_sysconfdir}/apache2/run
%dir %{_sysconfdir}/apache2/conf
%config(noreplace) %{_sysconfdir}/apache2/conf/httpd.conf
%config(noreplace) %{_sysconfdir}/apache2/conf/magic

%config(noreplace) %{_sysconfdir}/logrotate.d/apache2
%{_initrddir}/httpd
%{_initrddir}/htcacheclean

%dir %{_sysconfdir}/apache2/conf.d
%{_sysconfdir}/apache2/conf.d/README
%config(noreplace) %{_sysconfdir}/apache2/conf.d/*.conf
%exclude %{_sysconfdir}/apache2/conf.d/ssl.conf
%exclude %{_sysconfdir}/apache2/conf.d/manual.conf

%dir %{_sysconfdir}/apache2/conf.modules.d
%config(noreplace) %{_sysconfdir}/apache2/conf.modules.d/01-cgi.conf

%config(noreplace) %{_sysconfdir}/sysconfig/ht*

%{_sbindir}/ht*
%{_sbindir}/fcgistarter
%{_sbindir}/apachectl
%{_sbindir}/rotatelogs
%caps(cap_setuid,cap_setgid+pe) %attr(510,root,%{suexec_caller}) %{_sbindir}/suexec

%dir %{_libdir}/apache2
%dir %{_libdir}/apache2/modules
%{_libdir}/apache2/modules/mod_cgi*.so

%dir %{contentdir}
%dir %{contentdir}/icons
%dir %{contentdir}/error
%dir %{contentdir}/error/include
%dir %{contentdir}/noindex
%{contentdir}/icons/*
%{contentdir}/error/README
%{contentdir}/error/*.var
%{contentdir}/error/include/*.html
%{contentdir}/noindex/*

%dir %{docroot}
%dir %{docroot}/cgi-bin
%dir %{docroot}/html

%attr(0710,root,nobody) %dir %{_localstatedir}/run/apache2
%attr(0700,nobody,nobody) %dir %{_localstatedir}/run/apache2/htcacheclean
%attr(0700,root,root) %dir %{_localstatedir}/log/apache2
%attr(0700,nobody,nobody) %dir %{_localstatedir}/cache/apache2
%attr(0700,nobody,nobody) %dir %{_localstatedir}/cache/apache2/proxy

%{_mandir}/man8/*

%files tools
%defattr(-,root,root)
%{_bindir}/*
%{_mandir}/man1/*
%doc LICENSE NOTICE
%exclude %{_bindir}/apxs
%exclude %{_mandir}/man1/apxs.1*

%files manual
%defattr(-,root,root)
%{contentdir}/manual
%config(noreplace) %{_sysconfdir}/apache2/conf.d/manual.conf

%files -n ea-mod_mpm_event -f files.mpm_event
%files -n ea-mod_mpm_prefork -f files.mpm_prefork
%files -n ea-mod_mpm_worker -f files.mpm_worker

%files -n ea-mod_asis -f files.asis

%files -n ea-mod_dav -f files.dav
%attr(0700,nobody,nobody) %dir %{_localstatedir}/lib/dav
%files -n ea-mod_dav_fs -f files.dav_fs
%files -n ea-mod_dav_lock -f files.dav_lock

%files -n ea-mod_ldap -f files.ldap

%files -n ea-mod_proxy_html -f files.proxy_html

%files -n ea-mod_session -f files.session

%files -n ea-mod_ssl -f files.ssl
%config(noreplace) %{_sysconfdir}/apache2/conf.d/ssl.conf
%attr(0700,nobody,root) %dir %{_localstatedir}/cache/apache2/ssl

%files devel
%defattr(-,root,root)
%{_includedir}/apache2
%{_bindir}/apxs
%{_mandir}/man1/apxs.1*
%dir %{_libdir}/apache2/build
%{_libdir}/apache2/build/*.mk
%{_libdir}/apache2/build/*.sh
%{_sysconfdir}/rpm/macros.apache2

%changelog
* Fri Feb 27 2015 Trinity Quirk <trinity.quirk@cpanel.net> - 2.4.12-1.el6.cpanel.1
- Upgrade to 2.4.12
- Remove inappropriate or already-applied patches

* Thu Feb 26 2015 Trinity Quirk <trinity.quirk@cpanel.net> - 2.4.6-21.el6.cpanel.1
- Split the MPMs into their own packages
- mod_heartbeat needs to be loaded after mod_status and mod_watchdog

* Wed Feb 25 2015 Trinity Quirk <trinity.quirk@cpanel.net> - 2.4.6-20.el6.cpanel.1
- Each module now has its own conf.modules.d file
- conf.modules.d files are created programmatically
- Simplified ssl, proxy_html, ldap, and session package file lists

* Thu Jan 29 2015 Trinity Quirk <trinity.quirk@cpanel.net> - 2.4.6-17.el6.cpanel.1
- Added cPanel-specific patches
- Removed apache user creation, configured to run as nobody
- Repaired incorrect run directories

* Tue Dec 30 2014 Kurt Newman <kurt.newman@cpanel.net> - 2.4.6-17.el6.centos.1
- Converted from CentOS 7, to CentOS 6

* Tue Jun 17 2014 Jim Perrin <jperrin@centos.org> - 2.4.6-17.el7.centos.1
- Remove index.html, add centos-noindex.tar.gz
- update welcome.conf with proper aliases
- change symlink for poweredby.png

* Thu Mar 20 2014 Jan Kaluza <jkaluza@redhat.com> - 2.4.6-17
- mod_dav: add security fix for CVE-2013-6438 (#1077907)
- mod_log_config: add security fix for CVE-2014-0098 (#1077907)

* Wed Mar  5 2014 Joe Orton <jorton@redhat.com> - 2.4.6-16
- mod_ssl: improve DH temp key handling (#1057687)

* Wed Mar  5 2014 Joe Orton <jorton@redhat.com> - 2.4.6-15
- mod_ssl: use 2048-bit RSA key with SHA-256 signature in dummy certificate (#1071276)

* Fri Jan 24 2014 Daniel Mach <dmach@redhat.com> - 2.4.6-14
- Mass rebuild 2014-01-24

* Mon Jan 13 2014 Joe Orton <jorton@redhat.com> - 2.4.6-13
- mod_ssl: sanity-check use of "SSLCompression" (#1036666)
- mod_proxy_http: fix brigade memory usage (#1040447)

* Fri Jan 10 2014 Joe Orton <jorton@redhat.com> - 2.4.6-12
- rebuild

* Thu Jan  9 2014 Joe Orton <jorton@redhat.com> - 2.4.6-11
- build with -O3 on ppc64 (#1051066)

* Tue Jan  7 2014 Joe Orton <jorton@redhat.com> - 2.4.6-10
- mod_dav: fix locktoken handling (#1004046)

* Fri Dec 27 2013 Daniel Mach <dmach@redhat.com> - 2.4.6-9
- Mass rebuild 2013-12-27

* Fri Dec 20 2013 Joe Orton <jorton@redhat.com> - 2.4.6-8
- use unambiguous httpd-mmn (#1029360)

* Fri Nov   1 2013 Jan Kaluza <jkaluza@redhat.com> - 2.4.6-7
- mod_ssl: allow SSLEngine to override Listen-based default (#1023168)

* Thu Oct  31 2013 Jan Kaluza <jkaluza@redhat.com> - 2.4.6-6
- systemd: Use {MAINPID} notation in service file (#969972)

* Thu Oct 24 2013 Jan Kaluza <jkaluza@redhat.com> - 2.4.6-5
- systemd: send SIGWINCH signal without httpd -k in ExecStop (#969972)

* Thu Oct 03 2013 Jan Kaluza <jkaluza@redhat.com> - 2.4.6-4
- expand macros in macros.httpd (#1011393)

* Mon Aug 26 2013 Jan Kaluza <jkaluza@redhat.com> - 2.4.6-3
- fix "LDAPReferrals off" to really disable LDAP Referrals

* Wed Jul 31 2013 Jan Kaluza <jkaluza@redhat.com> - 2.4.6-2
- revert fix for dumping vhosts twice

* Mon Jul 22 2013 Joe Orton <jorton@redhat.com> - 2.4.6-1
- update to 2.4.6
- mod_ssl: use revised NPN API (r1487772)

* Thu Jul 11 2013 Jan Kaluza <jkaluza@redhat.com> - 2.4.4-12
- mod_unique_id: replace use of hostname + pid with PRNG output (#976666)
- apxs: mention -p option in manpage

* Tue Jul  2 2013 Joe Orton <jorton@redhat.com> - 2.4.4-11
- add patch for aarch64 (Dennis Gilmore, #925558)

* Mon Jul  1 2013 Joe Orton <jorton@redhat.com> - 2.4.4-10
- remove duplicate apxs man page from httpd-tools

* Mon Jun 17 2013 Joe Orton <jorton@redhat.com> - 2.4.4-9
- remove zombie dbmmanage script

* Fri May 31 2013 Jan Kaluza <jkaluza@redhat.com> - 2.4.4-8
- return 400 Bad Request on malformed Host header

* Mon May 20 2013 Jan Kaluza <jkaluza@redhat.com> - 2.4.4-6
- htpasswd/htdbm: fix hash generation bug (#956344)
- do not dump vhosts twice in httpd -S output (#928761)
- mod_cache: fix potential crash caused by uninitialized variable (#954109)

* Thu Apr 18 2013 Jan Kaluza <jkaluza@redhat.com> - 2.4.4-5
- execute systemctl reload as result of apachectl graceful
- mod_ssl: ignore SNI hints unless required by config
- mod_cache: forward-port CacheMaxExpire "hard" option
- mod_ssl: fall back on another module's proxy hook if mod_ssl proxy
  is not configured.

* Tue Apr 16 2013 Jan Kaluza <jkaluza@redhat.com> - 2.4.4-4
- fix service file to not send SIGTERM after ExecStop (#906321, #912288)

* Tue Mar 26 2013 Jan Kaluza <jkaluza@redhat.com> - 2.4.4-3
- protect MIMEMagicFile with IfModule (#893949)

* Tue Feb 26 2013 Joe Orton <jorton@redhat.com> - 2.4.4-2
- really package mod_auth_form in mod_session (#915438)

* Tue Feb 26 2013 Joe Orton <jorton@redhat.com> - 2.4.4-1
- update to 2.4.4
- fix duplicate ownership of mod_session config (#914901)

* Fri Feb 22 2013 Joe Orton <jorton@redhat.com> - 2.4.3-17
- add mod_session subpackage, move mod_auth_form there (#894500)

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.4.3-16
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Tue Jan  8 2013 Joe Orton <jorton@redhat.com> - 2.4.3-15
- add systemd service for htcacheclean

* Tue Nov 13 2012 Joe Orton <jorton@redhat.com> - 2.4.3-14
- drop patch for r1344712

* Tue Nov 13 2012 Joe Orton <jorton@redhat.com> - 2.4.3-13
- filter mod_*.so auto-provides (thanks to rcollet)
- pull in syslog logging fix from upstream (r1344712)

* Fri Oct 26 2012 Joe Orton <jorton@redhat.com> - 2.4.3-12
- rebuild to pick up new apr-util-ldap

* Tue Oct 23 2012 Joe Orton <jorton@redhat.com> - 2.4.3-11
- rebuild

* Wed Oct  3 2012 Joe Orton <jorton@redhat.com> - 2.4.3-10
- pull upstream patch r1392850 in addition to r1387633

* Mon Oct  1 2012 Joe Orton <jorton@redhat.com> - 2.4.3-9.1
- restore "ServerTokens Full-Release" support (#811714)

* Mon Oct  1 2012 Joe Orton <jorton@redhat.com> - 2.4.3-9
- define PLATFORM in os.h using vendor string

* Mon Oct  1 2012 Joe Orton <jorton@redhat.com> - 2.4.3-8
- use systemd script unconditionally (#850149)

* Mon Oct  1 2012 Joe Orton <jorton@redhat.com> - 2.4.3-7
- use systemd scriptlets if available (#850149)
- don't run posttrans restart if /etc/sysconfig/httpd-disable-posttrans exists

* Mon Oct 01 2012 Jan Kaluza <jkaluza@redhat.com> - 2.4.3-6
- use systemctl from apachectl (#842736)

* Wed Sep 19 2012 Joe Orton <jorton@redhat.com> - 2.4.3-5
- fix some error log spam with graceful-stop (r1387633)
- minor mod_systemd tweaks

* Thu Sep 13 2012 Joe Orton <jorton@redhat.com> - 2.4.3-4
- use IncludeOptional for conf.d/*.conf inclusion

* Fri Sep 07 2012 Jan Kaluza <jkaluza@redhat.com> - 2.4.3-3
- adding mod_systemd to integrate with systemd better

* Tue Aug 21 2012 Joe Orton <jorton@redhat.com> - 2.4.3-2
- mod_ssl: add check for proxy keypair match (upstream r1374214)

* Tue Aug 21 2012 Joe Orton <jorton@redhat.com> - 2.4.3-1
- update to 2.4.3 (#849883)
- own the docroot (#848121)

* Mon Aug  6 2012 Joe Orton <jorton@redhat.com> - 2.4.2-23
- add mod_proxy fixes from upstream (r1366693, r1365604)

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.4.2-22
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Fri Jul  6 2012 Joe Orton <jorton@redhat.com> - 2.4.2-21
- drop explicit version requirement on initscripts

* Thu Jul  5 2012 Joe Orton <jorton@redhat.com> - 2.4.2-20
- mod_ext_filter: fix error_log warnings

* Mon Jul  2 2012 Joe Orton <jorton@redhat.com> - 2.4.2-19
- support "configtest" and "graceful" as initscripts "legacy actions"

* Fri Jun  8 2012 Joe Orton <jorton@redhat.com> - 2.4.2-18
- avoid use of "core" GIF for a "core" directory (#168776)
- drop use of "syslog.target" in systemd unit file

* Thu Jun  7 2012 Joe Orton <jorton@redhat.com> - 2.4.2-17
- use _unitdir for systemd unit file
- use /run in unit file, ssl.conf

* Thu Jun  7 2012 Joe Orton <jorton@redhat.com> - 2.4.2-16
- mod_ssl: fix NPN patch merge

* Wed Jun  6 2012 Joe Orton <jorton@redhat.com> - 2.4.2-15
- move tmpfiles.d fragment into /usr/lib per new guidelines
- package /run/httpd not /var/run/httpd
- set runtimedir to /run/httpd likewise

* Wed Jun  6 2012 Joe Orton <jorton@redhat.com> - 2.4.2-14
- fix htdbm/htpasswd crash on crypt() failure (#818684)

* Wed Jun  6 2012 Joe Orton <jorton@redhat.com> - 2.4.2-13
- pull fix for NPN patch from upstream (r1345599)

* Thu May 31 2012 Joe Orton <jorton@redhat.com> - 2.4.2-12
- update suexec patch to use LOG_AUTHPRIV facility

* Thu May 24 2012 Joe Orton <jorton@redhat.com> - 2.4.2-11
- really fix autoindex.conf (thanks to remi@)

* Thu May 24 2012 Joe Orton <jorton@redhat.com> - 2.4.2-10
- fix autoindex.conf to allow symlink to poweredby.png

* Wed May 23 2012 Joe Orton <jorton@redhat.com> - 2.4.2-9
- suexec: use upstream version of patch for capability bit support

* Wed May 23 2012 Joe Orton <jorton@redhat.com> - 2.4.2-8
- suexec: use syslog rather than suexec.log, drop dac_override capability

* Tue May  1 2012 Joe Orton <jorton@redhat.com> - 2.4.2-7
- mod_ssl: add TLS NPN support (r1332643, #809599)

* Tue May  1 2012 Joe Orton <jorton@redhat.com> - 2.4.2-6
- add BR on APR >= 1.4.0

* Fri Apr 27 2012 Joe Orton <jorton@redhat.com> - 2.4.2-5
- use systemctl from logrotate (#221073)

* Fri Apr 27 2012 Joe Orton <jorton@redhat.com> - 2.4.2-4
- pull from upstream:
  * use TLS close_notify alert for dummy_connection (r1326980+)
  * cleanup symbol exports (r1327036+)

* Fri Apr 27 2012 Joe Orton <jorton@redhat.com> - 2.4.2-3.2
- rebuild

* Fri Apr 20 2012 Joe Orton <jorton@redhat.com> - 2.4.2-3
- really fix restart

* Fri Apr 20 2012 Joe Orton <jorton@redhat.com> - 2.4.2-2
- tweak default ssl.conf
- fix restart handling (#814645)
- use graceful restart by default

* Wed Apr 18 2012 Jan Kaluza <jkaluza@redhat.com> - 2.4.2-1
- update to 2.4.2

* Fri Mar 23 2012 Joe Orton <jorton@redhat.com> - 2.4.1-6
- fix macros

* Fri Mar 23 2012 Joe Orton <jorton@redhat.com> - 2.4.1-5
- add _httpd_moddir to macros

* Tue Mar 13 2012 Joe Orton <jorton@redhat.com> - 2.4.1-4
- fix symlink for poweredby.png
- fix manual.conf

* Tue Mar 13 2012 Joe Orton <jorton@redhat.com> - 2.4.1-3
- add mod_proxy_html subpackage (w/mod_proxy_html + mod_xml2enc)
- move mod_ldap, mod_authnz_ldap to mod_ldap subpackage

* Tue Mar 13 2012 Joe Orton <jorton@redhat.com> - 2.4.1-2
- clean docroot better
- ship proxy, ssl directories within /var/cache/httpd
- default config:
 * unrestricted access to (only) /var/www
 * remove (commented) Mutex, MaxRanges, ScriptSock
 * split autoindex config to conf.d/autoindex.conf
- ship additional example configs in docdir

* Tue Mar  6 2012 Joe Orton <jorton@redhat.com> - 2.4.1-1
- update to 2.4.1
- adopt upstream default httpd.conf (almost verbatim)
- split all LoadModules to conf.modules.d/*.conf
- include conf.d/*.conf at end of httpd.conf
- trim %%changelog

* Mon Feb 13 2012 Joe Orton <jorton@redhat.com> - 2.2.22-2
- fix build against PCRE 8.30

* Mon Feb 13 2012 Joe Orton <jorton@redhat.com> - 2.2.22-1
- update to 2.2.22

* Fri Feb 10 2012 Petr Pisar <ppisar@redhat.com> - 2.2.21-8
- Rebuild against PCRE 8.30

* Mon Jan 23 2012 Jan Kaluza <jkaluza@redhat.com> - 2.2.21-7
- fix #783629 - start httpd after named

* Mon Jan 16 2012 Joe Orton <jorton@redhat.com> - 2.2.21-6
- complete conversion to systemd, drop init script (#770311)
- fix comments in /etc/sysconfig/httpd (#771024)
- enable PrivateTmp in service file (#781440)
- set LANG=C in /etc/sysconfig/httpd

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.2.21-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Tue Dec 06 2011 Jan Kaluza <jkaluza@redhat.com> - 2.2.21-4
- fix #751591 - start httpd after remote-fs

* Mon Oct 24 2011 Jan Kaluza <jkaluza@redhat.com> - 2.2.21-3
- allow change state of BalancerMember in mod_proxy_balancer web interface

* Thu Sep 22 2011 Ville Skyttä <ville.skytta@iki.fi> - 2.2.21-2
- Make mmn available as %%{_httpd_mmn}.
- Add .svgz to AddEncoding x-gzip example in httpd.conf.

* Tue Sep 13 2011 Joe Orton <jorton@redhat.com> - 2.2.21-1
- update to 2.2.21

* Mon Sep  5 2011 Joe Orton <jorton@redhat.com> - 2.2.20-1
- update to 2.2.20
- fix MPM stub man page generation

* Wed Aug 10 2011 Jan Kaluza <jkaluza@redhat.com> - 2.2.19-5
- fix #707917 - add httpd-ssl-pass-dialog to ask for SSL password using systemd

* Fri Jul 22 2011 Iain Arnell <iarnell@gmail.com> 1:2.2.19-4
- rebuild while rpm-4.9.1 is untagged to remove trailing slash in provided
  directory names

* Wed Jul 20 2011 Jan Kaluza <jkaluza@redhat.com> - 2.2.19-3
- fix #716621 - suexec now works without setuid bit

* Thu Jul 14 2011 Jan Kaluza <jkaluza@redhat.com> - 2.2.19-2
- fix #689091 - backported patch from 2.3 branch to support IPv6 in logresolve

* Fri Jul  1 2011 Joe Orton <jorton@redhat.com> - 2.2.19-1
- update to 2.2.19
- enable dbd, authn_dbd in default config

* Thu Apr 14 2011 Joe Orton <jorton@redhat.com> - 2.2.17-13
- fix path expansion in service files

* Tue Apr 12 2011 Joe Orton <jorton@redhat.com> - 2.2.17-12
- add systemd service files (#684175, thanks to Jóhann B. Guðmundsson)

* Wed Mar 23 2011 Joe Orton <jorton@redhat.com> - 2.2.17-11
- minor updates to httpd.conf
- drop old patches

* Wed Mar  2 2011 Joe Orton <jorton@redhat.com> - 2.2.17-10
- rebuild

* Wed Feb 23 2011 Joe Orton <jorton@redhat.com> - 2.2.17-9
- use arch-specific mmn

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.2.17-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Mon Jan 31 2011 Joe Orton <jorton@redhat.com> - 2.2.17-7
- generate dummy mod_ssl cert with CA:FALSE constraint (#667841)
- add man page stubs for httpd.event, httpd.worker
- drop distcache support
- add STOP_TIMEOUT support to init script

* Sat Jan  8 2011 Joe Orton <jorton@redhat.com> - 2.2.17-6
- update default SSLCipherSuite per upstream trunk

* Wed Jan  5 2011 Joe Orton <jorton@redhat.com> - 2.2.17-5
- fix requires (#667397)

* Wed Jan  5 2011 Joe Orton <jorton@redhat.com> - 2.2.17-4
- de-ghost /var/run/httpd

* Tue Jan  4 2011 Joe Orton <jorton@redhat.com> - 2.2.17-3
- add tmpfiles.d configuration, ghost /var/run/httpd (#656600)

* Sat Nov 20 2010 Joe Orton <jorton@redhat.com> - 2.2.17-2
- drop setuid bit, use capabilities for suexec binary

* Wed Oct 27 2010 Joe Orton <jorton@redhat.com> - 2.2.17-1
- update to 2.2.17

* Fri Sep 10 2010 Joe Orton <jorton@redhat.com> - 2.2.16-2
- link everything using -z relro and -z now

* Mon Jul 26 2010 Joe Orton <jorton@redhat.com> - 2.2.16-1
- update to 2.2.16

* Fri Jul  9 2010 Joe Orton <jorton@redhat.com> - 2.2.15-3
- default config tweaks:
 * harden httpd.conf w.r.t. .htaccess restriction (#591293)
 * load mod_substitute, mod_version by default
 * drop proxy_ajp.conf, load mod_proxy_ajp in httpd.conf
 * add commented list of shipped-but-unloaded modules
 * bump up worker defaults a little
 * drop KeepAliveTimeout to 5 secs per upstream
- fix LSB compliance in init script (#522074)
- bundle NOTICE in -tools
- use init script in logrotate postrotate to pick up PIDFILE
- drop some old Obsoletes/Conflicts

* Sun Apr 04 2010 Robert Scheck <robert@fedoraproject.org> - 2.2.15-1
- update to 2.2.15 (#572404, #579311)

