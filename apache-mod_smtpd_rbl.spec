#Module-Specific definitions
%define mod_name mod_smtpd_rbl
%define mod_conf A40_%{mod_name}.conf
%define mod_so %{mod_name}.so

%define snap r239351

Summary:	Mod_smtpd_rbl brings "RBL" (DNSBL/RHSBL) support to mod_smtpd
Name:		apache-%{mod_name}
Version:	0
Release:	%mkrel 1.%{snap}.11
Group:		System/Servers
License:	Apache License
URL:		https://svn.apache.org/repos/asf/httpd/mod_smtpd/trunk/mod_smtpd_rbl/
Source0: 	%{mod_name}-%{version}-%{snap}.tar.bz2
Source1:	%{mod_conf}.bz2
Requires(pre): rpm-helper
Requires(postun): rpm-helper
Requires(pre):	apache-conf >= 2.0.55
Requires(pre):	apache >= 2.0.55
Requires:	apache-conf >= 2.0.55
Requires:	apache >= 2.0.55
Requires:	apache-mod_smtpd
Requires:	apache-mod_dnsbl_lookup
BuildRequires:	apache-devel >= 2.0.55
BuildRequires:	apache-mod_smtpd-devel
BuildRequires:	apache-mod_dnsbl_lookup-devel
BuildRequires:	file
Epoch:		1
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-buildroot

%description
mod_smtpd_rbl brings "RBL" (DNSBL/RHSBL) support to mod_smtpd.

%prep

%setup -q -n %{mod_name}

rm -f dnsbl_lookup.h mod_smtpd.h

# strip away annoying ^M
find . -type f|xargs file|grep 'CRLF'|cut -d: -f1|xargs perl -p -i -e 's/\r//'
find . -type f|xargs file|grep 'text'|cut -d: -f1|xargs perl -p -i -e 's/\r//'

%build

%{_sbindir}/apxs -c mod_smtpd_rbl.c

%install
[ "%{buildroot}" != "/" ] && rm -rf %{buildroot}

install -d %{buildroot}%{_libdir}/apache-extramodules
install -d %{buildroot}%{_sysconfdir}/httpd/modules.d

install -m0755 .libs/*.so %{buildroot}%{_libdir}/apache-extramodules/
bzcat %{SOURCE1} > %{buildroot}%{_sysconfdir}/httpd/modules.d/%{mod_conf}

install -d %{buildroot}%{_var}/www/html/addon-modules
ln -s ../../../..%{_docdir}/%{name}-%{version} %{buildroot}%{_var}/www/html/addon-modules/%{name}-%{version}

%post
if [ -f %{_var}/lock/subsys/httpd ]; then
    %{_initrddir}/httpd restart 1>&2;
fi

%postun
if [ "$1" = "0" ]; then
    if [ -f %{_var}/lock/subsys/httpd ]; then
	%{_initrddir}/httpd restart 1>&2
    fi
fi

%clean
[ "%{buildroot}" != "/" ] && rm -rf %{buildroot}

%files
%defattr(-,root,root)
%doc README
%attr(0644,root,root) %config(noreplace) %{_sysconfdir}/httpd/modules.d/%{mod_conf}
%attr(0755,root,root) %{_libdir}/apache-extramodules/%{mod_so}
%{_var}/www/html/addon-modules/*


