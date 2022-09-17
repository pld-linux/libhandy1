#
# Conditional build:
%bcond_without	apidocs	# API documentation
%bcond_without	glade	# Glade module+catalog
%bcond_without	vala	# Vala API

Summary:	Library with GTK+ widgets for mobile phones
Summary(pl.UTF-8):	Biblioteka z kontrolkami GTK+ dla telefonów komórkowych
Name:		libhandy1
Version:	1.8.0
Release:	1
License:	LGPL v2.1+
Group:		Libraries
Source0:	https://download.gnome.org/sources/libhandy/1.8/libhandy-%{version}.tar.xz
# Source0-md5:	663afbc6c0448c254363c1a90f13a4ee
URL:		https://gitlab.gnome.org/GNOME/libhandy/
# -std=gnu11
BuildRequires:	gcc >= 6:4.7
BuildRequires:	fribidi-devel
BuildRequires:	gi-docgen >= 2021.1
%{?with_glade:BuildRequires:	glade-devel >= 3.38}
BuildRequires:	glib2-devel >= 1:2.44
BuildRequires:	gobject-introspection-devel
BuildRequires:	gtk+3-devel >= 3.24.1
BuildRequires:	meson >= 0.49.0
BuildRequires:	ninja >= 1.5
BuildRequires:	pkgconfig
BuildRequires:	rpm-build >= 4.6
BuildRequires:	rpmbuild(macros) >= 1.752
BuildRequires:	tar >= 1:1.22
%{?with_vala:BuildRequires:	vala >= 2:0.27.0}
BuildRequires:	xz
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
Requires:	glade >= 3.38

%description glade
libhandy module for Glade.

%description glade -l pl.UTF-8
Moduł libhandy dla Glade.

%package apidocs
Summary:	API documentation for libhandy library
Summary(pl.UTF-8):	Dokumentacja API biblioteki libhandy
Group:		Documentation
BuildArch:	noarch

%description apidocs
API documentation for libhandy library.

%description apidocs -l pl.UTF-8
Dokumentacja API biblioteki libhandy

%package -n vala-libhandy1
Summary:	Vala API for libhandy libraries
Summary(pl.UTF-8):	API języka Vala do bibliotek libhandy
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}
Requires:	vala >= 2:0.16.0
BuildArch:	noarch

%description -n vala-libhandy1
Vala API for libhandy library.

%description -n vala-libhandy1 -l pl.UTF-8
API języka VALA do biblioteki libhandy.

%prep
%setup -q -n libhandy-%{version}

%build
%meson build \
	-Dexamples=false \
	%{!?with_glade:-Dglade_catalog=disabled} \
	%{?with_apidocs:-Dgtk_doc=true} \
	%{!?with_vala:-Dvapi=false}

%ninja_build -C build

%install
rm -rf $RPM_BUILD_ROOT

%ninja_install -C build

%if %{with apidocs}
# FIXME: where to package gi-docgen generated docs?
install -d $RPM_BUILD_ROOT%{_gtkdocdir}
%{__mv} $RPM_BUILD_ROOT%{_docdir}/libhandy-1 $RPM_BUILD_ROOT%{_gtkdocdir}
%endif

%find_lang libhandy

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files -f libhandy.lang
%defattr(644,root,root,755)
%doc AUTHORS NEWS README.md
%attr(755,root,root) %{_libdir}/libhandy-1.so.0
%{_libdir}/girepository-1.0/Handy-1.typelib

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libhandy-1.so
%{_includedir}/libhandy-1
%{_pkgconfigdir}/libhandy-1.pc
%{_datadir}/gir-1.0/Handy-1.gir

%if %{with glade}
%files glade
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/glade/modules/libglade-handy-1.so
%{_datadir}/glade/catalogs/libhandy-1.xml
%endif

%if %{with apidocs}
%files apidocs
%defattr(644,root,root,755)
%{_gtkdocdir}/libhandy-1
%endif

%if %{with vala}
%files -n vala-libhandy1
%defattr(644,root,root,755)
%{_datadir}/vala/vapi/libhandy-1.deps
%{_datadir}/vala/vapi/libhandy-1.vapi
%endif
