all:
	git clean -dxf
	mock -v -r ea4-httpd24-cent6-x86_64 --clean
	mock -v -r ea4-httpd24-cent6-x86_64 --unpriv --buildsrpm --resultdir SRPMS --sources SOURCES --spec SPECS/httpd.spec
	mock -v -r ea4-httpd24-cent6-x86_64 --unpriv --resultdir RPMS SRPMS/httpd-2.4.6-17.el6.centos.1.src.rpm 
