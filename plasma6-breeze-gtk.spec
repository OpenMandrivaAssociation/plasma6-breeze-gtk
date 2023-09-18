%define stable %([ "`echo %{version} |cut -d. -f3`" -ge 70 ] && echo -n un; echo -n stable)
%undefine _debugsource_packages
%define git 20230918

Summary:	The Breeze theme for GTK+ windows
Name:		plasma6-breeze-gtk
Version:	5.240.0
Release:	%{?git:0.%{git}.}1
License:	GPL
Group:		Graphical desktop/KDE
Url:		http://www.kde.org
%if 0%{?git:1}
Source0:	https://invent.kde.org/plasma/breeze-gtk/-/archive/master/breeze-gtk-master.tar.bz2#/breeze-gtk-%{git}.tar.bz2
%else
Source0:	http://download.kde.org/%{stable}/plasma/%(echo %{version} |cut -d. -f1-3)/%{name}-%{version}.tar.xz
%endif
# FIXME this is a really weird issue: On aarch64, the
# build fails with a crash in pycairo, but as soon as
# any sort of debugging is enabled, the problem goes
# away.
# This is obviously not the right "fix" - but in the
# mean time, it does allow the package to be built and
# if the problem returns, at least we'll get some
# information about it.
Patch0:		debug.patch
BuildRequires:	cmake(ECM)
BuildRequires:	cmake(Breeze)
BuildRequires:	cmake(Qt6)
BuildRequires:	cmake(Qt6Core)
BuildRequires:	pkgconfig(cairo)
BuildRequires:	pkgconfig(python3)
BuildRequires:	python3dist(pycairo)
BuildRequires:	gtk2-modules
BuildRequires:	sassc
#Supplements:	gtk+2.0
#Supplements:	gtk2-modules

%description
This package contains a version of the KDE Breeze theme for GTK applications
and environments, such as GNOME.

%files
%{_datadir}/themes/Breeze
%{_datadir}/themes/Breeze-Dark

#-----------------------------------------------------------------------------

%prep
%autosetup -p1 -n breeze-gtk-%{?git:master}%{!?git:%{version}}
%cmake \
	-DBUILD_QCH:BOOL=ON \
	-DBUILD_WITH_QT6:BOOL=ON \
	-DKDE_INSTALL_USE_QT_SYS_PATHS:BOOL=ON \
	-G Ninja

%build
%ninja_build -C build

%install
%ninja_install -C build
