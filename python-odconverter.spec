%define	oname	pyodconverter
%define	module	odconverter
%define	user	oooconvert
%define	service	ooo-converter
%define revno	r27

Summary:	Python OpenDocument Converter
Name:		python-%{module}
Version:	1.2
Release:	0.%{revno}.4
License:	LGPLv2.1+
Group:		Development/Python
Url:		http://www.artofsolving.com/opensource/pyodconverter
# Based on my branch at http://launchpad.net/pyodconverter, heavily adapted
# for use with DocMGR package, please don't replace, but rather just merge
# the diff between previous upstream version if ever updating, or even better,
# check with me first. (hopefully upstream author will agree on merging when
# suggested sometime soon...)
Source0:	%{oname}-%{version}.tar.gz
Source1:	ooo-converter.init
BuildArch:	noarch
Requires:	libreoffice-pyuno
Requires:	libreoffice-writer
Requires:	libreoffice-calc
Requires:	libreoffice-impress
Requires:	python-pkg-resources
Requires(pre):	rpm-helper
Requires(preun):	rpm-helper
BuildRequires:	python-setuptools

%description
PyODConverter is a Python module for automating office document conversions
from the command line using OpenOffice.org.

%prep
%setup -qn %{oname}-%{version}

%build
python setup.py build

tee %{service}.sysconf << EOH
# OpenOffice.org
OOFFICE_HOST="localhost"
OOFFICE_PORT="8100"
# Any additional options to pass to ooffice can be set here
OOFFICE_OPTIONS="-norestore -nofirststartwizard -invisible -nodefault -nologo -nolockcheck"
EOH

%install
python setup.py install --root=%{buildroot}

install -d %{buildroot}%{_localstatedir}/run/%{service}
install -m755 %{SOURCE1} -D %{buildroot}%{_initrddir}/%{service}
install -m644 %{service}.sysconf -D %{buildroot}%{_sysconfdir}/sysconfig/%{service}

%pre
%_pre_useradd %{user} %{_localstatedir}/run/%{service} /sbin/nologin

%post
%_post_service %{service}

%postun
%_postun_userdel %{user}

%preun
%_preun_service %{service}

%files
%{_bindir}/DocumentConverter
%{_initrddir}/%{service}
%{_sysconfdir}/sysconfig/%{service}
%{python_sitelib}/%{module}.py*
%{python_sitelib}/%{oname}*.egg-info
%attr(700,%{user},%{user}) %dir %{_localstatedir}/run/%{service}

