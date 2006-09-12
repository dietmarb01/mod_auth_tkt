
# Use '--define apache 1' to build an 'mod_auth_tkt1' package for apache1
%define httpd httpd
%define name mod_auth_tkt
%{?apache:%define httpd apache}
%{?apache:%define name mod_auth_tkt1}

Summary: Lightweight ticket-based authentication module for Apache.
Name: %{name}
Version: 2.0.0rc1
Release: 1%{?dist}.of
License: GPL
Group: Applications/System
Source: http://www.openfusion.com.au/labs/dist/mod_auth_tkt-%{version}.tar.gz
URL: http://www.openfusion.com.au/labs/nagios-of-plugins/
Packager: Gavin Carr <gavin@openfusion.com.au>
Vendor: Open Fusion Pty. Ltd.
Buildroot: %_tmppath/%{name}-%{version}
Requires: %{httpd}
BuildRequires: %{httpd}-devel
AutoReq: no

%description
mod_auth_tkt provides lightweight, repository-agnostic, ticket-based
authentication for Apache. It implements a single-signon framework that 
works across multiple apache instances and multiple machines. The actual
authentication requires a user-supplied CGI or script of some kind - the 
package includes example CGI scripts in Perl.

%prep
%setup -n mod_auth_tkt-%{version}

%build
test %{httpd} == apache && APXS='--apxs=/usr/sbin/apxs1'
test %{debug} == 1 && DEBUG='--debug'
MOD_PERL=`rpm -q mod_perl | grep '^mod_perl' || /bin/true`
if [ -n "$MOD_PERL" -a %{test} == 1 ]; then
  ./configure --test $DEBUG
  make
  make test
else
  ./configure $APXS $DEBUG
  make
fi

%install
test "$RPM_BUILD_ROOT" != "/" && rm -rf $RPM_BUILD_ROOT
mkdir -p $RPM_BUILD_ROOT%{_libdir}/%{httpd}/modules
mkdir -p $RPM_BUILD_ROOT%{_sysconfdir}/%{httpd}/conf.d
mkdir -p $RPM_BUILD_ROOT/usr/share/doc/%{name}-%{version}/cgi
mkdir -p $RPM_BUILD_ROOT/usr/share/doc/%{name}-%{version}/contrib
if [ %{httpd} == apache ]; then
  apxs1 -i -n "auth_tkt" -S LIBEXECDIR=$RPM_BUILD_ROOT%{_libdir}/%{httpd}/modules src/mod_auth_tkt.so
else
  apxs -i -n "auth_tkt" -S LIBEXECDIR=$RPM_BUILD_ROOT%{_libdir}/%{httpd}/modules src/mod_auth_tkt.la
fi
install -m 644 conf/02_auth_tkt.conf $RPM_BUILD_ROOT%{_sysconfdir}/%{httpd}/conf.d/
cp -pr cgi/* $RPM_BUILD_ROOT/usr/share/doc/%{name}-%{version}/cgi
cp -pr contrib/* $RPM_BUILD_ROOT/usr/share/doc/%{name}-%{version}/contrib
cp -pr README* INSTALL LICENSE ChangeLog CREDITS $RPM_BUILD_ROOT/usr/share/doc/%{name}-%{version}
cd doc
make DESTDIR=$RPM_BUILD_ROOT install

%clean
test "$RPM_BUILD_ROOT" != "/" && rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root)
%{_libdir}/%{httpd}
%doc /usr/share/doc/%{name}-%{version}
%attr(0640,root,apache) %config(noreplace) %{_sysconfdir}/%{httpd}/conf.d/*
/usr/share/man/*

%changelog

* Mon Apr 10 2006 Gavin Carr <gavin@openfusion.com.au> 2.0.0rc1
- Add mod_auth_tkt man page.
- Add TKTAuthDebug support, instead of compile-time debug flag.
- Add TKTAuthPostTimeoutURL support (Michael Peters).

* Mon Oct 24 2005 Gavin Carr <gavin@openfusion.com.au> 2.0.0b7
- Deprecate TKTAuthTimeoutMin, replacing with TKTAuthTimeout, using units like
  TKTAuthCookieExpires.
- Split out TKTAuthCookieSecure functionality from TKTAuthRequireSSL (Larry 
  Lansing).
- Add TKTAuthCookieExpires directive for guest cookies and refreshes.
- Add TKTAuthGuestUser %U format support for UUIDs with Apache 2.
- Add TKTAuthGuestUser support for setting guest user explicitly.
- Fix URI and HTML escaping issues with cgi scripts (Viljo Viitanen).
- Update CGI scripts to get local settings via Apache::AuthTkt parse_conf values.
- Update Apache::AuthTkt to new version (0.03) with parse_conf support.
- Add server config merge support to allow global secrets with vhosts.

* Mon Aug 01 2005 Gavin Carr <gavin@openfusion.com.au> 2.0.0b6
- Update specfile to support basic building against apache 1.
- Fixed bug with non-base64 quoted ticket values not being parsed correctly.

* Tue Jun 14 2005 Gavin Carr <gavin@openfusion.com.au> 2.0.0b5
- Change back url formation to use Host header, not server name/port.
- Get cookie_match to skip empty cookies it finds (e.g. logout misconfigs).
- Add Ian Bicking's AuthTicket python class in contrib.
- Add TKTAuthGuestLogin support based on patch from Ian Bicking.
- Add DEBUG_VERBOSE support based on patch from Ian Bicking.
- Fixed bug with test harness not generating local module correctly.

* Mon May 30 2005 Gavin Carr <gavin@openfusion.com.au> 2.0.0b4
- Change build to include 'make test' only if mod_perl is available.

* Sat Apr 30 2005 Gavin Carr <gavin@openfusion.com.au> 2.0.0b3

* Thu Feb 21 2005 Gavin Carr <gavin@openfusion.com.au> 2.0.0b2
- Initial release.


# arch-tag: 56c36703-99d8-409e-97dc-1b81e565b29a
