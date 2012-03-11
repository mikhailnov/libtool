%define major	7
%define libname	%mklibname ltdl %{major}
%define devname	%mklibname -d ltdl

# for the testsuite:
%define _disable_ld_no_undefined 1
%define _disable_ld_as_needed 1

# allow --with bootstrap
%bcond_with	bootstrap

%define arch_has_java 1
%ifarch %{arm} %{mips}
%define arch_has_java 0
%endif
%if %{with bootstrap}
%define arch_has_java 0
%endif

%define fortran_compiler gfortran

Summary:	The GNU libtool, which simplifies the use of shared libraries
Name:		libtool
Version:	2.4.2
Release:	2
License:	GPLv2+
Group:		Development/Other
URL:		http://www.gnu.org/software/libtool/libtool.html

Source0:	ftp://ftp.gnu.org/gnu/%{name}/%{name}-%{version}.tar.xz
Source1:	%{SOURCE0}.sig

# deprecated: introduced in July 2003
# (cf http://lists.mandriva.com/cooker-amd64/2003-12/msg00046.php)
# but is not needed anymore since Sept 2003 change in rpm "Make "x86_64" the
# canonical arch on amd64"

# (Abel) Patches please only modify ltmain.in and don't touch ltmain.sh
# otherwise ltmain.sh will not be regenerated, and patches will be lost

# (cjw) when a library that is produced in the build is also linked against, 
#       make sure that the library in the rpm install dir is used for relinking 
#	even if (an older version of) the lib is installed on the system
Patch0:		relink.patch
#
Patch1:		libtool-2.2.10-rpath.patch
Patch2:		ltmain-SED.patch
Patch12:	do-not-link-against-deplibs.patch
Patch13:	drop-ld-no-undefined-for-shared-lib-modules.patch
Patch14:	fix-checking-libltdl-is-installed-installable.patch
# (cjw) do not use CFLAGS when running gcj
Patch16:	libtool-2.2.6-use-gcjflags-for-gcj.patch
# (cjw) in the libltdl install test, use --enable-ltdl-install to make sure 
#       the library is built even if it is installed on the system
Patch17:	libtool-2.2.6b-libltdl-install-test-fix.patch
# (cjw) mdemo-dryrun test may fail because file sizes are incorrect in 'before' 
#       file list
Patch18:	libtool-2.4-dryrun-sleepmore.patch
Patch19:	libtool-2.4.2-drop-soname-for-modules.patch
# (fwang) detect libltdl.so rather than libltdl.la, as we will delete them
Patch20:	libtool-2.4.2-use-so-to-detect-libltdl.patch

BuildRequires:	automake
Buildrequires:	autoconf
# For test 37 to succeed
Buildrequires:	locales-de
%if ! %{with bootstrap}
BuildRequires:	gcc-%{fortran_compiler}
%endif
%if %{arch_has_java}
BuildRequires:	gcc-java libgcj-static-devel
%endif
Requires:	%{name}-base = %{EVRD}

%description
The libtool package contains the GNU libtool, a set of shell scripts
which automatically configure UNIX and UNIX-like architectures to
generically build shared libraries.  Libtool provides a consistent,
portable interface which simplifies the process of using shared
libraries.

If you are developing programs which will use shared libraries, you
should install libtool.

%package	base
Group:		Development/C
Summary:	Basic package for %{name}
Requires:	file
Requires(post):	info-install
Requires(preun):info-install

%description	base
The libtool package contains the GNU libtool, a set of shell scripts
which automatically configure UNIX and UNIX-like architectures to
generically build shared libraries.  Libtool provides a consistent,
portable interface which simplifies the process of using shared
libraries.

If you are developing programs which will use shared libraries, you
should install libtool.

%package -n	%{libname}
Group:		Development/C
Summary:	Shared library files for libtool
License:	LGPLv2.1+
# old libextractor wrongly provided its own libltdl:
Conflicts:	%{_lib}extractor1 < 0.5.18a

%description -n	%{libname}
Shared library files for libtool DLL library from the libtool package.

%package -n	%{devname}
Group:		Development/C
Summary:	Development files for libtool
License:	LGPLv2.1+
Requires:	%{name} = %{EVRD}
Requires:	%{libname} = %{EVRD}
Provides:	%{name}-devel = %{EVRD}
Obsoletes:	%{mklibname ltdl 3}-devel

%description -n	%{devname}
Development headers, and files for development from the libtool package.

%prep
%setup -q
%apply_patches
./bootstrap

%build
# don't use configure macro - it forces libtoolize, which is bad -jgarzik
# Use configure macro but define __libtoolize to be /bin/true -Geoff
%define __libtoolize /bin/true
# And don't overwrite config.{sub,guess} in this package as well -- Abel
%define __cputoolize /bin/true

%configure2_5x
%make

#%%check
#pushd    build-%{_target_cpu}-%{_target_os}
#set +x
#echo ====================TESTING=========================
#set -x
## all tests must pass here
## disabling icecream since some tests check the output of gcc
#ICECC=no %make check
#set +x
#echo ====================TESTING END=====================
#set -x
#
#popd

%install
%makeinstall_std

%post base
%_install_info %{name}.info

%preun base
%_remove_install_info %{name}.info

%files
%doc AUTHORS NEWS README
%doc THANKS TODO ChangeLog*
%{_bindir}/libtool
%{_mandir}/man1/libtool.1.*

%files base
%{_bindir}/libtoolize
%{_mandir}/man1/libtoolize.*
%{_infodir}/libtool.info*
%{_datadir}/libtool
%{_datadir}/aclocal/*.m4

%files -n %{libname}
%{_libdir}/libltdl.so.%{major}*

%files -n %{devname}
%doc libltdl/README
%doc tests/demo
%{_includedir}/*
%{_libdir}/*.a
%{_libdir}/*.so
%{_libdir}/*.la
