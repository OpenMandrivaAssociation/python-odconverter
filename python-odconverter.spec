%define	oname	pyodconverter
%define	module	odconverter
%define revno	r27

Summary:	Python OpenDocument Converter
Name:		python-%{module}
Version:	1.2
Release:	%mkrel 0.%{revno}.1
License:	LGPLv2.1+
Group:		Development/Python
Url:		http://www.artofsolving.com/opensource/pyodconverter
# Based on my branch at http://launchpad.net/pyodconverter, heavily adapted
# for use with DocMGR package, please don't replace, but rather just merge
# the diff between previous upstream version if ever updating, or even better,
# check with me first. (hopefully upstream author will agree on merging when
# suggested sometime soon...)
Source0:	%{oname}-%{version}.tar.gz
%py_requires -d
# Backport for MES 5 where unfortunately we need to make the package arch
# specific to get the necessary dependency on the desired OOo package to
# have the document converter working with 64 bit java...
%if "%{mdvver}" == "200900" && "%{_lib}" == "lib64"
%define ext64 64
%define _enable_debug_packages %{nil}
%define debug_package %{nil}
%else
BuildArch:	noarch
%endif
Requires:	openoffice.org%{?ext64}-pyuno openoffice.org%{?ext64}-writer
Requires:	openoffice.org%{?ext64}-calc openoffice.org%{?ext64}-impress
BuildRequires:	python-setuptools
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-buildroot

%description
PyODConverter is a Python module for automating office document conversions
from the command line using OpenOffice.org.

%prep
%setup -qn %{oname}-%{version}

%build
python setup.py build

%install
rm -rf %{buildroot}
python setup.py install --root=%{buildroot}

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root)
%{_bindir}/DocumentConverter
%{python_sitelib}/%{module}.py*
%{python_sitelib}/%{oname}*.egg-info

