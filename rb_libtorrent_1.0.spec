%define gtag libtorrent-1_0_7

Name:       rb_libtorrent
Version:    1.0.7
Release:    1%{?dist}
Summary:    A C++ BitTorrent library aiming to be the best alternative

Group:      System Environment/Libraries
License:    BSD
URL:        http://www.rasterbar.com/products/libtorrent/
Source0:    https://github.com/arvidn/libtorrent/releases/download/%{gtag}/libtorrent-rasterbar-%{version}.tar.gz
Source1:    %{name}-README-renames.Fedora
Source2:    %{name}-COPYING.Boost
Source3:    %{name}-COPYING.zlib
Patch0:     %{name}-1.0.1-boost_noncopyable.patch

BuildRequires:  asio-devel
BuildRequires:  boost-devel
BuildRequires:  GeoIP-devel
BuildRequires:  libtool
BuildRequires:  python-devel
BuildRequires:  python-setuptools
BuildRequires:  zlib-devel
BuildRequires:  util-linux
BuildRequires:  autoconf
BuildRequires:  automake
BuildRequires:  libtool

## The following is taken from it's website listing...mostly.
%description
%{name} is a C++ library that aims to be a good alternative to all
the other BitTorrent implementations around. It is a library and not a full
featured client, although it comes with a few working example clients.

Its main goals are to be very efficient (in terms of CPU and memory usage) as
well as being very easy to use both as a user and developer. 


%package    devel
Summary:    Development files for %{name}
Group:      Development/Libraries
License:    BSD and zlib and Boost
Requires:   %{name} = %{version}-%{release}
Requires:   pkgconfig
## FIXME: Same include directory. :(
Conflicts:  libtorrent-devel
## Needed for various headers used via #include directives...
Requires:   asio-devel
Requires:   boost-devel
Requires:   openssl-devel
Requires:   GeoIP-devel

%description    devel
The %{name}-devel package contains libraries and header files for
developing applications that use %{name}.

The various source and header files included in this package are licensed
under the revised BSD, zlib/libpng, and Boost Public licenses. See the various
COPYING files in the included documentation for the full text of these
licenses, as well as the comments blocks in the source code for which license
a given source or header file is released under.


%package    examples
Summary:    Example clients using %{name}
Group:      Applications/Internet
License:    BSD
Requires:   %{name} = %{version}-%{release}

%description    examples
The %{name}-examples package contains example clients which intend to
show how to make use of its various features. (Due to potential
namespace conflicts, a couple of the examples had to be renamed. See the
included documentation for more details.)


%package    python
Summary:    Python bindings for %{name}
Group:      Development/Languages
License:    Boost
Requires:   %{name} = %{version}-%{release}

%description    python
The %{name}-python package contains Python language bindings
(the 'libtorrent'module) that allow it to be used from within 
Python applications.


%prep
%setup -q -n "libtorrent-rasterbar-%{version}"
%patch0 -p1
./autotool.sh
## The RST files are the sources used to create the final HTML files; and are
## not needed.
rm -f docs/*.rst
## Ensure that we get the licenses installed appropriately.
install -p -m 0644 COPYING COPYING.BSD
install -p -m 0644 %{SOURCE2} COPYING.Boost
install -p -m 0644 %{SOURCE3} COPYING.zlib
## Finally, ensure that everything is UTF-8, as it should be.
iconv -t UTF-8 -f ISO_8859-15 AUTHORS -o AUTHORS.iconv
mv AUTHORS.iconv AUTHORS

## Fix the interpreter for the example clients
sed -i -e 's:^#!/bin/python$:#!/usr/bin/python:' bindings/python/{simple_,}client.py

# safer and less side-effects than using LIBTOOL=/usr/bin/libtool -- Rex
# else, can use the autoreconf -i hammer
%if "%{_libdir}" != "/usr/lib"
sed -i -e 's|"/lib /usr/lib|"/%{_lib} %{_libdir}|' configure
%endif


%build
%configure                  \
    --disable-static            \
    --enable-examples           \
    --enable-python-binding         \
    --with-boost-system=boost_system    \
    --with-boost-python=boost_python    \
    --with-libgeoip=system          \
    --with-libiconv             \
    --enable-export-all

make V=1 %{?_smp_mflags}

%check
make check

%install
## Ensure that we preserve our timestamps properly.
export CPPROG="%{__cp} -p"
make install DESTDIR=%{buildroot} INSTALL="%{__install} -c -p"
## Do the renaming due to the somewhat limited %%_bindir namespace. 
rename client torrent_client %{buildroot}%{_bindir}/*
install -p -m 0644 %{SOURCE1} ./README-renames.Fedora
## Install the python binding module.
pushd bindings/python
    %{__python} setup.py install -O1 --skip-build --root %{buildroot}
popd 

## unpackged files
# .la files
rm -fv %{buildroot}%{_libdir}/lib*.la
# static libs
rm -fv %{buildroot}%{_libdir}/lib*.a

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%files
%doc AUTHORS ChangeLog COPYING README.rst
%{_libdir}/libtorrent-rasterbar.so.8*

%files  devel
%doc COPYING.Boost COPYING.BSD COPYING.zlib docs/ 
%{_libdir}/pkgconfig/libtorrent-rasterbar.pc
%{_includedir}/libtorrent/
%{_libdir}/libtorrent-rasterbar.so

%files examples
%doc COPYING README-renames.Fedora
%{_bindir}/*torrent*
%{_bindir}/connection_tester
%{_bindir}/parse_*
%{_bindir}/rss_reader
%{_bindir}/upnp_test

%files  python
%doc AUTHORS ChangeLog COPYING.Boost
%{python_sitearch}/python_libtorrent-%{version}-py?.?.egg-info
%{python_sitearch}/libtorrent.so

%changelog
* Mon Nov 16 2015 Evgeny Lensky <surfernsk@gmail.com> - 1.0.7-1
- update release 1.0.7

* Sun Aug 02 2015 Evgeny Lensky <surfernsk@gmail.com> - 1.0.6-1
- update release 1.0.6

* Sun Dec 28 2014 Evgeny Lensky <surfernsk@gmail.com> - 0.16.19-1
- upstream release 0.16.19

* Fri Sep 26 2014 Evgeny Lensky <surfernsk@gmail.com> - 0.16.18-1
- upstream release 0.16.18

* Sun Jun 22 2014 Evgeny Lensky <surfernsk@gmail.com> - 0.16.17-1
- upstream release 0.16.17

* Sat May 03 2014 Evgeny Lensky <surfernsk@gmail.com> - 0.16.16-1
- upstream release 0.16.16

* Tue Mar 11 2014 Evgeny Lensky <surfernsk@gmail.com> - 0.16.15-1
- fix mingw time_t 64 bit issue
- fix use of SetFileValidData on windows
- fix crash when using full allocation storage mode
- improve error_code and error_category support in python bindings
- fix python binding for external_ip_alert

* Mon Feb 03 2014 Evgeny Lensky <surfernsk@gmail.com> - 0.16.14-1
- upstream release 0.16.14

* Fri Jan 03 2014 Evgeny Lensky <surfernsk@gmail.com> - 0.16.13-1
- upstream release 0.16.13
