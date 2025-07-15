#
# Conditional build:
%bcond_without	static_libs	# static library

Summary:	A C library for scfg
Name:		libscfg
Version:	0.1.1
Release:	1
License:	MIT
Group:		Libraries
Source0:	https://git.sr.ht/~emersion/libscfg/archive/v%{version}.tar.gz
# Source0-md5:	8ef49c4566816029e5bb3da06d5fac38
Patch0:		lib-version.patch
URL:		https://wayland.emersion.fr/libscfg/
BuildRequires:	meson >= 0.54.0
BuildRequires:	ninja
BuildRequires:	rpmbuild(macros) >= 1.736
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
A C library for scfg (simple configuration file format).

%package devel
Summary:	Header files for libscfg library
Group:		Development/Libraries
Requires:	%{name}%{?_isa} = %{version}-%{release}

%description devel
Header files for libscfg library.

%package static
Summary:	Static libscfg library
Group:		Development/Libraries
Requires:	%{name}-devel%{?_isa} = %{version}-%{release}

%description static
Static libscfg library.

%prep
%setup -q -n %{name}-v%{version}
%patch -P0 -p1

%build
%meson \
	%{!?with_static_libs:--default-library=shared} \
	-Dwerror=false

%meson_build

%install
rm -rf $RPM_BUILD_ROOT

%meson_install

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig


%files
%defattr(644,root,root,755)
%doc LICENSE README.md
%attr(755,root,root) %{_libdir}/libscfg.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libscfg.so.1

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libscfg.so
%{_includedir}/scfg.h
%{_pkgconfigdir}/scfg.pc

%if %{with static_libs}
%files static
%defattr(644,root,root,755)
%{_libdir}/libscfg.a
%endif
