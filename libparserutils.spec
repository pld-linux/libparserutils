#
# Conditional build:
%bcond_without	static_libs	# don't build static library

Summary:	Library for building efficient parsers
Summary(pl.UTF-8):	Biblioteka do tworzenia wydajnych analizatorów
Name:		libparserutils
Version:	0.2.0
Release:	1
License:	MIT
Group:		Libraries
Source0:	http://download.netsurf-browser.org/libs/releases/%{name}-%{version}-src.tar.gz
# Source0-md5:	3a52cff73006e9b7feb6dd23410373c2
URL:		http://www.netsurf-browser.org/projects/libparserutils/
BuildRequires:	netsurf-buildsystem >= 1.1
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
LibParserUtils is a library for building efficient parsers, written in
C. It was developed as part of the NetSurf project and is available
for use by other software under the MIT licence.

Features:
- No mandatory dependencies (iconv() implementation optional for
  enhanced charset support)
- A number of built-in character set converters
- Mapping of character set names to/from MIB enum values
- UTF-8 and UTF-16 (host endian) support functions
- Various simple data structures (resizeable buffer, stack, vector)
- A UTF-8 input stream
- Simple C API
- Portable

%description -l pl.UTF-8
LibParserUtils to napisana w C biblioteka do tworzenia wydajnych
analizatorów. Powstała jako część projektu NetSurf i jest dostępna do
użycia w innych programach na licencji MIT.

Cechy:
- brak obowiązkowych zależności (opcjonalnie: implementacja iconv() do
  obsługi rozszerzonych zestawów znaków)
- wiele wbudowanych konwerterów zestawów znaków
- odwzorowanie nazw zestawów znaków na/z wartości enum MIB
- funkcje obsługujące UTF-8 i UTF-16 (o kolejności bajtów zgodnej z
  procesorem)
- różne proste struktury danych (bufor o zmiennym rozmiarze, stos,
  wektor)
- strumień wejściowy UTF-8
- proste API dla języka C
- przenośność

%package devel
Summary:	libparserutils library headers
Summary(pl.UTF-8):	Pliki nagłówkowe biblioteki libparserutils
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}

%description devel
This package contains the include files and other resources you can
use to incorporate libparserutils into applications.

%description devel -l pl.UTF-8
Pliki nagłówkowe pozwalające na używanie biblioteki libparserutils w
swoich programach.

%package static
Summary:	libparserutils static library
Summary(pl.UTF-8):	Statyczna biblioteka libparserutils
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}

%description static
This is package with static libparserutils library.

%description static -l pl.UTF-8
Statyczna biblioteka libparserutils.

%prep
%setup -q

%build
export CC="%{__cc}"
export CFLAGS="%{rpmcflags}"
export LDFLAGS="%{rpmldflags}"

%{__make} \
	Q= \
	PREFIX=%{_prefix} \
	LIBDIR=%{_lib} \
	COMPONENT_TYPE=lib-shared

%if %{with static_libs}
%{__make} \
	Q= \
	PREFIX=%{_prefix} \
	LIBDIR=%{_lib} \
	COMPONENT_TYPE=lib-static
%endif

%install
rm -rf $RPM_BUILD_ROOT
%{__make} install \
	Q= \
	PREFIX=%{_prefix} \
	LIBDIR=%{_lib} \
	COMPONENT_TYPE=lib-shared \
	DESTDIR=$RPM_BUILD_ROOT

%if %{with static_libs}
%{__make} install \
	Q= \
	PREFIX=%{_prefix} \
	LIBDIR=%{_lib} \
	COMPONENT_TYPE=lib-static \
	DESTDIR=$RPM_BUILD_ROOT
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc COPYING README
%attr(755,root,root) %{_libdir}/libparserutils.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libparserutils.so.0

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libparserutils.so
%{_includedir}/parserutils
%{_pkgconfigdir}/libparserutils.pc

%if %{with static_libs}
%files static
%defattr(644,root,root,755)
%{_libdir}/libparserutils.a
%endif
