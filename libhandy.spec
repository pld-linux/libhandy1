# Conditional build:
%bcond_without  apidocs         # do not build and package API docs
%bcond_without  vala            # do not build Vala API

Summary:	Library with GTK+ widgets for mobile phones
Summary(pl.UTF-8):	Biblioteka z kontrolkami GTK+ dla telefonów komórkowych
Name:		libhandy
Version:	0.0.7
Release:	1
License:	LGPL v2+
Group:		Libraries
Source0:	https://source.puri.sm/Librem5/libhandy/-/archive/v%{version}/%{name}-v%{version}.tar.bz2
# Source0-md5:	3319a80b6979d2f2bf8118f7c3677955
URL:		https://source.puri.sm/Librem5/libhandy/
BuildRequires:	gcc
BuildRequires:	glib2-devel
BuildRequires:	gobject-introspection-devel
BuildRequires:	gtk+3-devel
BuildRequires:	gtk-doc
BuildRequires:	meson
BuildRequires:	ninja
%{?with_vala:BuildRequires:     vala >= 2:0.27.0}

%description
libhandy provides GTK+ widgets and GObjects to ease developing
applications for mobile phones.

%description -l pl.UTF-8
libhandy dostarcza kontroliki GTK+ i GObjects upraszczając tworzenie
aplikacji dla telefonów komórkowych

%package devel
Summary:	Header files for libhandy library
Summary(pl.UTF-8):	Pliki nagłówkowe biblioteki libhandy
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}

%description devel
Header files for libhandy library

%description devel -l pl.UTF-8
Pliki nagłówkowe biblioteki libhandy

%package apidocs
Summary:	API documentation for libhandy library
Summary(pl.UTF-8):	Dokumentacja API biblioteki libhandy
Group:		Documentation
%if "%{_rpmversion}" >= "5"
BuildArch:      noarch
%endif

%description apidocs
API documentation for libhandy library.

%description apidocs -l pl.UTF-8
Dokumentacja API biblioteki libhandy

%package -n vala-libhandy
Summary:        Vala API for libhandy libraries
Summary(pl.UTF-8):      API języka Vala do bibliotek libhandy
Group:          Development/Libraries
Requires:       %{name}-devel = %{version}-%{release}
Requires:       vala >= 2:0.16.0
%if "%{_rpmversion}" >= "5"
BuildArch:      noarch
%endif

%description -n vala-libhandy
Vala API for libhandy library.

%description -n vala-libhandy  -l pl.UTF-8
API języka VALA do biblioteki libhandy.

%prep
%setup -q -n %{name}-v%{version}

%build
%meson  %{?with_apidocs:-Dgtk_doc=true} \
        %{!?with_vala:-Dvapi=false} \
        -Dexamples=false build

%ninja_build -C build

%install
rm -rf $RPM_BUILD_ROOT
%ninja_install -C build

%files
%defattr(644,root,root,755)
%doc COPYING
%doc README.md
%{_libdir}/girepository-1.0/
%{_libdir}/libhandy-0.0.so.0*

%files devel
%defattr(644,root,root,755)
%{_includedir}/libhandy-0.0/
%{_libdir}/libhandy-0.0.so
%{_pkgconfigdir}/libhandy-0.0.pc
%{_datadir}/gir-1.0/

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

%clean
rm -rf $RPM_BUILD_ROOT
