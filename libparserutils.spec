#
# Conditional build:
%bcond_without	static_libs	# don't build static library
#
Summary:	Library for building efficient parsers
Name:		libparserutils
Version:	0.1.2
Release:	1
License:	MIT
Group:		Libraries
Source0:	http://download.netsurf-browser.org/libs/releases/%{name}-%{version}-src.tar.gz
# Source0-md5:	11c2b4ff17406b57dcb718d4fad022bb
URL:		http://www.netsurf-browser.org/projects/libparserutils/
BuildRequires:	netsurf-buildsystem
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
LibParserUtils is a library for building efficient parsers, written in
C. It was developed as part of the NetSurf project and is available
for use by other software under the MIT licence.

Features:

* No mandatory dependencies (iconv() implementation optional
for enhanced charset support)
* A number of built-in character set converters
* Mapping of character set names to/from MIB enum values
* UTF-8 and UTF-16 (host endian) support functions
* Various simple data structures (resizeable buffer, stack, vector)
* A UTF-8 input stream
* Simple C API
* Portable
* Shared library

Charset support

LibParserUtils has the following built-in charset converters.

* UTF-8
* UTF-16 (platform-native endian)
* ISO-8859-n
* Windows-125n
* US-ASCII

%package devel
Summary:	libparserutils library headers
Summary(pl.UTF-8):	Pliki nagłówkowe biblioteki libparserutils
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}

%description devel
This is the libraries, include files and other resources you can use
to incorporate libparserutils into applications.

%description devel -l pl.UTF-8
Pliki nagłówkowe pozwalające na używanie biblioteki libparserutils w
swoich programach.

%package static
Summary:	libparserutils static libraries
Summary(pl.UTF-8):	Statyczne biblioteki libparserutils
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}

%description static
This is package with static libparserutils libraries.

%description static -l pl.UTF-8
Statyczna biblioteka libparserutils.

%prep
%setup -q

%build
%{__make} PREFIX=%{_prefix} COMPONENT_TYPE=lib-shared Q='' \
	CFLAGS="%{rpmcflags} -Iinclude -Isrc" LDFLAGS="%{rpmldflags}"
%if %{with static_libs}
%{__make} PREFIX=%{_prefix} COMPONENT_TYPE=lib-static Q='' \
	CFLAGS="%{rpmcflags} -Iinclude -Isrc" LDFLAGS="%{rpmldflags}"
%endif

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT \
	PREFIX=%{_prefix} \
	COMPONENT_TYPE=lib-shared \
	Q=''

%if %{with static_libs}
%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT \
	PREFIX=%{_prefix} \
	COMPONENT_TYPE=lib-static \
	Q=''
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/lib*.so.*.*.*

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/lib*.so
%{_includedir}/parserutils
%{_pkgconfigdir}/*pc

%if %{with static_libs}
%files static
%defattr(644,root,root,755)
%{_libdir}/lib*.a
%endif
