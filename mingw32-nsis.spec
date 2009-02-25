%define sconsopts VERSION=%{version} PREFIX=%{_prefix} PREFIX_CONF=%{_sysconfdir} SKIPPLUGINS=System SKIPUTILS='NSIS Menu' DEBUG_SYMBOLS=1 OPTS=1
%define _default_patch_fuzz 2

Name:           mingw32-nsis
Version:        2.43
Release:        4%{?dist}
Summary:        Nullsoft Scriptable Install System

License:        zlib and CPL
Group:          Development/Libraries
URL:            http://nsis.sourceforge.net/
Source0:        http://dl.sourceforge.net/sourceforge/nsis/nsis-%{version}-src.tar.bz2
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

# This patch fixes NSIS to actually build 64-bit versions.
# Originally from Debian, updated by Kevin Kofler.
Patch0:         nsis-2.43-64bit-fixes.patch
# Patches from Debian (mainly by Paul Wise).
Patch1:         nsis-2.43-debian-debug-opt.patch

BuildRequires:  mingw32-filesystem >= 40
BuildRequires:  mingw32-gcc
BuildRequires:  mingw32-gcc-c++
BuildRequires:  mingw32-binutils
BuildRequires:  python
BuildRequires:  scons

# Don't build NSIS Menu as it doesn't actually work on POSIX systems: 1. it
# doesn't find its index.html file without patching, 2. it has various links to
# .exe files such as the makensisw.exe W32 GUI which are not available in the
# POSIX version at all and 3. the documentation links have backslashes in the
# URLs and the relative paths are wrong. Almost none of the links worked when I
# tested it (after patching problem 1.).
# Also removes unnecessary wxGTK dependency for this otherwise GUI-less package.
# (Does it really make sense to drag in wxGTK just to display a HTML file?)
# If you really want to reenable this, it needs a lot of fixing.
# -- Kevin Kofler
# BuildRequires:  wxGTK-devel

# upgrade path for CalcForge users
Obsoletes:      nsis < %{version}-%{release}
Provides:       nsis = %{version}-%{release}
Obsoletes:      nsis-data < %{version}-%{release}
Provides:       nsis-data = %{version}-%{release}


%description
NSIS, the Nullsoft Scriptable Install System, is a script-driven
Windows installation system.

This package includes native Fedora binaries of makensis (etc.) and
all plugins except for System.dll.  The System.dll plugin cannot be
built natively at this time since it includes inline Microsoft
assembler code.


%prep
%setup -q -n nsis-%{version}-src

%patch0 -p1 -b .64bit
%patch1 -p1 -b .debug


%build
scons %{sconsopts}


%install
rm -rf $RPM_BUILD_ROOT

mkdir $RPM_BUILD_ROOT
scons %{sconsopts} PREFIX_DEST=$RPM_BUILD_ROOT install

mv $RPM_BUILD_ROOT%{_docdir}/nsis $RPM_BUILD_ROOT%{_docdir}/%{name}-%{version}


%clean
rm -rf $RPM_BUILD_ROOT


%files
%defattr(-,root,root)
%doc %{_docdir}/%{name}-%{version}
%config(noreplace) %{_sysconfdir}/nsisconf.nsh
%{_bindir}/*
#{_includedir}/nsis
%{_datadir}/nsis


%changelog
* Wed Feb 25 2009 Kevin Kofler <Kevin@tigcc.ticalc.org> - 2.43-4
- Updated 64bit-fixes patch (remove some more -m32 use).
- Drop ExclusiveArch, not needed with the above.
- Obsoletes/Provides nsis and nsis-data for migration path from CalcForge.
- Disable NSIS Menu (does not work on *nix, see specfile comment for details).
- Drop BR wxGTK-devel.

* Sat Feb 21 2009 Richard W.M. Jones <rjones@redhat.com> - 2.43-3
- Restore ExclusiveArch line (Levente Farkas).

* Fri Feb 20 2009 Richard W.M. Jones <rjones@redhat.com> - 2.43-2
- Rebuild for mingw32-gcc 4.4

* Fri Feb 13 2009 Levente Farkas <lfarkas@lfarkas.org> - 2.43-1
- update to the latest upstream

* Wed Jan 14 2009 Levente Farkas <lfarkas@lfarkas.org> - 2.42-1
- update to the latest upstream
- a few small changes

* Fri Oct 17 2008 Richard W.M. Jones <rjones@redhat.com> - 2.39-5
- Fix the Summary line.

* Wed Oct  8 2008 Richard W.M. Jones <rjones@redhat.com> - 2.39-4
- Initial RPM release.
