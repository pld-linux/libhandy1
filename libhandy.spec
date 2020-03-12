#
# Conditional build:
%bcond_without	apidocs	# API documentation
%bcond_without	glade	# Glade module+catalog
%bcond_without	vala	# Vala API

Summary:	Library with GTK+ widgets for mobile phones
Summary(pl.UTF-8):	Biblioteka z kontrolkami GTK+ dla telefonów komórkowych
Name:		libhandy
Version:	0.0.13
Release:	1
License:	LGPL v2.1+
Group:		Libraries
#Source0Download: https://source.puri.sm/Librem5/libhandy/-/tags
Source0:	https://source.puri.sm/Librem5/libhandy/-/archive/v%{version}/%{name}-v%{version}.tar.bz2
# Source0-md5:	932ba6e80908c7579fa0392d6e0d0ceb
URL:		https://source.puri.sm/Librem5/libhandy/
# -std=gnu11
BuildRequires:	gcc >= 6:4.7
%{?with_glade:BuildRequires:	glade-devel >= 2.0}
BuildRequires:	glib2-devel >= 1:2.44
BuildRequires:	gobject-introspection-devel
BuildRequires:	gtk+3-devel >= 3.24.1
BuildRequires:	gtk-doc
BuildRequires:	meson >= 0.49.0
BuildRequires:	ninja >= 1.5
BuildRequires:	pkgconfig
BuildRequires:	rpmbuild(macros) >= 1.736
%{?with_vala:BuildRequires:	vala >= 2:0.27.0}
Requires:	glib2 >= 1:2.44
Requires:	gtk+3 >= 3.24.1
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
libhandy provides GTK+ widgets and GObjects to ease developing
applications for mobile phones.

%description -l pl.UTF-8
libhandy dostarcza kontrolki GTK+ i GObjects, upraszczając tworzenie
aplikacji dla telefonów komórkowych.

%package devel
Summary:	Header files for libhandy library
Summary(pl.UTF-8):	Pliki nagłówkowe biblioteki libhandy
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}
Requires:	glib2-devel >= 1:2.44
Requires:	gtk+3-devel >= 3.24.1

%description devel
Header files for libhandy library

%description devel -l pl.UTF-8
Pliki nagłówkowe biblioteki libhandy

%package glade
Summary:	libhandy module for Glade
Summary(pl.UTF-8):	Moduł libhandy dla Glade
Group:		X11/Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}
Requires:	glade >= 2.0

%description glade
libhandy module for Glade.

%description glade -l pl.UTF-8
Moduł libhandy dla Glade.

%package apidocs
Summary:	API documentation for libhandy library
Summary(pl.UTF-8):	Dokumentacja API biblioteki libhandy
Group:		Documentation
%if "%{_rpmversion}" >= "5"
BuildArch:	noarch
%endif

%description apidocs
API documentation for libhandy library.

%description apidocs -l pl.UTF-8
Dokumentacja API biblioteki libhandy

%package -n vala-libhandy
Summary:	Vala API for libhandy libraries
Summary(pl.UTF-8):	API języka Vala do bibliotek libhandy
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}
Requires:	vala >= 2:0.16.0
%if "%{_rpmversion}" >= "5"
BuildArch:	noarch
%endif

%description -n vala-libhandy
Vala API for libhandy library.

%description -n vala-libhandy -l pl.UTF-8
API języka VALA do biblioteki libhandy.

%prep
%setup -q -n %{name}-v%{version}

%build
%meson build \
	-Dexamples=false \
	%{!?with_glade:-Dglade_catalog=false} \
	%{?with_apidocs:-Dgtk_doc=true} \
	%{!?with_vala:-Dvapi=false}

%ninja_build -C build

%install
rm -rf $RPM_BUILD_ROOT

%ninja_install -C build

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc AUTHORS README.md
%attr(755,root,root) %{_libdir}/libhandy-0.0.so.0
%{_libdir}/girepository-1.0/Handy-0.0.typelib

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libhandy-0.0.so
%{_includedir}/libhandy-0.0
%{_pkgconfigdir}/libhandy-0.0.pc
%{_datadir}/gir-1.0/Handy-0.0.gir

%if %{with glade}
%files glade
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/glade/modules/libglade-handy.so
%{_datadir}/glade/catalogs/libhandy.xml
%endif

%if %{with apidocs}
%files apidocs
%defattr(644,root,root,755)
%{_gtkdocdir}/libhandy
%endif

%if %{with vala}
%files -n vala-libhandy
%defattr(644,root,root,755)
%{_datadir}/vala/vapi/libhandy-0.0.deps
%{_datadir}/vala/vapi/libhandy-0.0.vapi
%endif
