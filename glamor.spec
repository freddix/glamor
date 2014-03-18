Summary:	OpenGL based 2D rendering acceleration library
Name:		glamor
Version:	0.6.0
Release:	1
License:	MIT
Group:		Libraries
Source0:	http://xorg.freedesktop.org/releases/individual/driver/%{name}-egl-%{version}.tar.bz2
# Source0-md5:	b3668594675f71a75153ee52dbd35535
URL:		http://www.freedesktop.org/wiki/Software/Glamor
BuildRequires:	Mesa-libEGL-devel
BuildRequires:	Mesa-libGL-devel
BuildRequires:	Mesa-libgbm-devel
BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	libdrm-devel
BuildRequires:	libtool
BuildRequires:	pixman-devel
BuildRequires:	pkg-config
BuildRequires:	xorg-util-macros
BuildRequires:	xorg-xserver-server-devel
Requires:	%{name}-libs = %{version}-%{release}
Requires:	xorg-xserver-server
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

# relies on symbols from X server
%define		skip_post_check_so	libglamor.so.*

%description
OpenGL based 2D rendering acceleration library.

%package libs
Summary:	Glamor shared library
Group:		Libraries

%description libs
Glamor shared library.

%package devel
Summary:	Header file for Glamor modules API
Group:		Development/Libraries
Requires:	%{name}-libs = %{version}-%{release}
Requires:	Mesa-libEGL-devel
Requires:	Mesa-libGL-devel
Requires:	libdrm-devel
Requires:	pixman-devel
Requires:	xorg-xserver-server-devel

%description devel
Header file for Glamor modules API.

%prep
%setup -qn %{name}-egl-%{version}

%build
%{__libtoolize}
%{__aclocal}
%{__autoconf}
%{__autoheader}
%{__automake}
%configure \
	--disable-static    \
	--enable-glx-tls
%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

%{__rm} $RPM_BUILD_ROOT%{_libdir}/{,xorg/modules/}*.la

%clean
rm -rf $RPM_BUILD_ROOT

%post	libs -p /usr/sbin/ldconfig
%postun	libs -p /usr/sbin/ldconfig

%files
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/xorg/modules/libglamoregl.so
%{_datadir}/X11/xorg.conf.d/glamor.conf

%files libs
%defattr(644,root,root,755)
%doc COPYING ChangeLog README
%attr(755,root,root) %ghost %{_libdir}/libglamor.so.0
%attr(755,root,root) %{_libdir}/libglamor.so.*.*.*

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libglamor.so
%{_includedir}/xorg/*.h
%{_pkgconfigdir}/*.pc

