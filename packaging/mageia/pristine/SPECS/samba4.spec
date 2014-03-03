%define pkg_name	samba
%define version		4.0.0alpha11
%define rel		6
#define	subrel		1
%define vscanver 	0.3.6c-beta5
%define libsmbmajor	0
%define netapimajor	0
%define smbsharemodesmajor	0
%define	tallocmajor	1
%define tallocver	1.2.0                                                     
%define tdbmajor	1
%define tdbver		1.1.3                                                     
%define teventmajor	0                                                         
%define teventver	0.9.3                                                     
%define ldbmajor	0                                                         
%define ldbver		0.9.3
%define dcerpcmajor	0
%define dcerpcver	0.0.1
%define hostconfigmajor	0
%define hostconfigver	0.0.1
%define ndrmajor	0
%define ndrver		0.0.1
%define	wbclientmajor	0
#LIBSAMBA-UTIL_VERSION in data.mk
%define sambautilver 0.0.1
%define sambautilmajor	0
# registry_VERSION
%define registrymajor 0
%define registryver 0.0.1
%define gensecver 0.0.1
%define gensecmajor 0


# samba vscan plugins dont link without:
#define _disable_ld_no_undefined 1

%{?!mkver:%define mkver(r:) %{-r:%(perl -e '$_="%{1}";m/(((\\d\\.?)+)(\\w\*))(.\*)/;$pre=$4;if ($pre =~ /\\w\{2,\}/) { print "0.%{-r*}.$pre" } else { print "%{-r*}";}')}%{!-r:%(perl -e '$_="%{1}";m/(((\\d\\.?)+)(\\w\*))(.\*)/;$pre=$4;print "$2";print $pre if $pre !~ /\\w{2,}/')}}

%{!?lib: %global lib lib}
%{!?mklibname: %global mklibname(ds) %lib%{1}%{?2:%{2}}%{?3:_%{3}}%{-s:-static}%{-d:-devel}}

%define libname %mklibname smbclient %libsmbmajor
%define libnetapi %mklibname netapi %netapimajor
%define netapidevel %mklibname -d netapi
%define libsmbsharemodes %mklibname smbsharemodes %smbsharemodesmajor
%define smbsharemodesdevel %mklibname -d smbsharemodes
%define libtalloc %mklibname talloc %tallocmajor
%define tallocdevel %mklibname -d talloc
%define libtdb %mklibname tdb %tdbmajor
%define tdbdevel %mklibname -d tdb
%define libldb %mklibname ldb %ldbmajor
%define ldbdevel %mklibname -d ldb
%define libtevent %mklibname tevent %teventmajor
%define teventdevel %mklibname -d tevent
%define libdcerpc %mklibname dcerpc %dcerpcmajor
%define dcerpcdevel %mklibname -d dcerpc
%define libsambahostconfig %mklibname samba-hostconfig %hostconfigmajor
%define sambahostconfigdevel %mklibname -d samba-hostconfig
%define libndr %mklibname ndr %ndrmajor
%define ndrdevel %mklibname -d ndr
%define libwbclient %mklibname wbclient %wbclientmajor
%define wbclientdevel %mklibname -d wbclient
%define libsambautil %mklibname samba-util %sambautilmajor
%define sambautildevel %mklibname -d samba-util
%define libregistry %mklibname registry %registrymajor
%define registrydevel %mklibname -d registry
%define libgensec %mklibname gensec %gensecmajor
%define gensecdevel %mklibname -d gensec

# Version and release replaced by samba-team at release from samba cvs
%define pversion PVERSION
%define prelease PRELEASE

#Check to see if p(version|release) has been replaced (1 if replaced)
%define have_pversion %(if [ "%pversion" = `echo "pversion" |tr '[:lower:]' '[:upper:]'` ];then echo 0; else echo 1; fi)

%if %have_pversion
%define source_ver 	%{pversion}
%define rel %mkrel 1.%{prelease}
# Don't abort for stupid reasons on builds from tarballs:
%global	_unpackaged_files_terminate_build	0
%global	_missing_doc_files_terminate_build	0
%else
%global source_ver 	%{version}
%endif
%global source_ver 	%{version}

%define prerel %mkver -r %rel %source_ver
%global real_version %mkver %source_ver
%global release %mkrel %prerel
%define have_pre %([ "%version" == "%source_ver" ]; echo $?)

# Check to see if we are running a build from a tarball release from samba.org
# (%have_pversion) If so, disable vscan, unless explicitly requested
# (--with vscan).
#FIXME
%define build_vscan 	0
%if %have_pversion
%define build_vscan 	0
%{?_with_vscan: %define build_vscan 1}
%endif

# We now do detection of the Mandrake release we are building on:

# Default options
%global build_doc 0
%global build_swat 0
%global build_cifs 1
%define build_talloc 1
%define build_tdb 1
%define build_tevent 1
%define build_alternatives	0
%define build_system	0
%define build_acl 	1
%define build_winbind 	0
%define build_wins 	0
%define build_ldap 	0
%define build_ads	1
%define build_scanners	0
%define build_test	1
# CUPS supports functionality for 'printcap name = cups' (9.0 and later):
%define build_cupspc	0
# %_{pre,postun}_service are provided by rpm-helper in 9.0 and later
%define have_rpmhelper	1
%define build_mysql	0
%define build_pgsql 	0

%if %mdkversion >= 201000
%define build_talloc 0
%define build_tdb 0
%define build_tevent 0
%endif

# Allow commandline option overrides (borrowed from Vince's qmail srpm):
# To use it, do rpm [-ba|--rebuild] --with 'xxx'
# Check if the rpm was built with the defaults, otherwise we inform the user
%define build_non_default 0
%{?_with_system: %global build_system 1}
%{?_without_system: %global build_system 0}
%{?_with_acl: %global build_acl 1}
%{?_with_acl: %global build_non_default 1}
%{?_without_acl: %global build_acl 0}
%{?_without_acl: %global build_non_default 1}
%{?_with_winbind: %global build_winbind 1}
%{?_with_winbind: %global build_non_default 1}
%{?_without_winbind: %global build_winbind 0}
%{?_without_winbind: %global build_non_default 1}
%{?_with_wins: %global build_wins 1}
%{?_with_wins: %global build_non_default 1}
%{?_without_wins: %global build_wins 0}
%{?_without_wins: %global build_non_default 1}
%{?_with_ldap: %global build_ldap 1}
%{?_with_ldap: %global build_non_default 1}
%{?_without_ldap: %global build_ldap 0}
%{?_without_ldap: %global build_non_default 1}
%{?_with_ads: %global build_ads 1}
%{?_with_ads: %global build_non_default 1}
%{?_without_ads: %global build_ads 0}
%{?_without_ads: %global build_non_default 1}
%{?_with_scanners: %global build_scanners 1}
%{?_with_scanners: %global build_non_default 1}
%{?_without_scanners: %global build_scanners 0}
%{?_without_scanners: %global build_non_default 1}
%{?_with_vscan: %global build_vscan 1}
%{?_with_vscan: %global build_non_default 1}
%{?_without_vscan: %global build_vscan 0}
%{?_without_vscan: %global build_non_default 1}
%{?_with_test: %global build_test 1}
%{?_with_test: %global build_non_default 1}
%{?_without_test: %global build_test 0}
%{?_without_test: %global build_non_default 1}
%{?_with_mysql: %global build_mysql 1}
%{?_with_pgsql: %global build_pgsql 1}
# As if that weren't enough, we're going to try building with antivirus
# support as an option also
%global build_antivir 	0
%global build_clamav 	0
%global build_fprot 	0
%global build_fsav 	0
%global build_icap 	0
%global build_kaspersky 0
%global build_mks 	0
%global build_nai 	0
%global build_openav	0
%global build_sophos 	0
%global build_symantec 	0
%global build_trend	0
%if %build_vscan
# These we build by default
%global build_clamav 	1
%global build_icap 	1
%endif
%if %build_vscan && %build_scanners
# These scanners are built if scanners are selected
# symantec requires their library present and must be selected 
# individually
%global build_fprot 	1
%global build_fsav 	1
%global build_kaspersky 1
%global build_mks 	1
%global build_nai 	1
%global build_openav	1
%global build_sophos 	1
%global build_trend 	1
%endif
%if %build_vscan
%{?_with_fprot: %{expand: %%global build_fprot 1}}
%{?_with_kaspersky: %{expand: %%global build_kaspersky 1}}
%{?_with_mks: %{expand: %%global build_mks 1}}
%{?_with_openav: %{expand: %%global build_openav 1}}
%{?_with_sophos: %{expand: %%global build_sophos 1}}
#%{?_with_symantec: %{expand: %%global build_symantec 1}}
%{?_with_trend: %{expand: %%global build_trend 1}}
%global vscandir samba-vscan-%{vscanver}
%endif
%global vfsdir examples.bin/VFS

#Standard texts for descriptions:
%define message_bugzilla() %(echo -e -n "Please file bug reports for this package at Mandriva bugzilla \\n(http://qa.mandriva.com) under the product name %{1}")
%define message_system %(echo -e -n "NOTE: These packages of samba-%{version}, are provided, parallel installable\\nwith samba-3.x, to allow easy migration from samba-3.3 to samba-%{version},\\nbut are not officially supported")

#check gcc version to disable some optimisations on gcc-3.3.1
# gcc is not mandatory to do rpm queries on a .src.rpm, which is what the buildsystem
# ends up doing, so we need to guard against that
%define gcc331 %((gcc -dumpversion 2>/dev/null || echo 4.1.2) |awk '{if ($1>3.3) print 1; else print 0}')

#Define sets of binaries that we can use in globs and loops:
%global commonbin net,ntlm_auth,testparm,regdiff,regpatch,regshell,regtree,setnttoken

%global serverbin 	oLschema2ldif
%global serversbin samba,provision,upgradeprovision

%global clientbin 	nmblookup,smbclient,cifsdd
%global client_sbin 	mount.smb,mount.smbfs
%if %mdkversion >= 200800
%global cifs_bin	mount.cifs,umount.cifs
%else
%global cifs_bin	mount.cifs,umount.cifs
%endif
%global client_man	man1/findsmb.1,man1/nmblookup.1,man1/smbclient.1,man1/smbget.1,man1/smbtar.1,man5/smbgetrc.5,man8/smbspool.8

%global testbin 	smbtorture,masktest,locktest,nsstest,gentest,ndrdump,getntacl

%ifarch alpha
%define build_expsam xml
%else
%define build_expsam xml%{?_with_pgsql:,pgsql}%{?_with_mysql:,mysql}
%endif

#Workaround missing macros in 8.x:
%{!?perl_vendorlib: %{expand: %%global perl_vendorlib %{perl_sitearch}/../}}

# Determine whether this is the system samba or not.
%if %build_system
%global samba_major	%{nil}
%else
%global samba_major	4
%endif
# alternatives_major is %{nil} if we aren't system and not using alternatives
%if !%build_system || %build_alternatives
%define alternative_major 4
%else
%define alternative_major %{nil}
%endif

Summary: Samba SMB server
Name: %{pkg_name}%{samba_major}

Version: %{real_version}
Release: %{release}

License: GPL
Group: System/Servers
Source: http://www.samba.org/samba/ftp/samba4/samba-%{source_ver}.tar.gz
Source99: http://www.samba.org/samba/ftp/samba4/samba-%{source_ver}.tar.asc
Source98: http://www.samba.org/samba/ftp/samba-pubkey.asc
URL:	http://www.samba.org
Source1: samba.log
Source3: samba.xinetd
%if %build_swat
Source4: swat_48.png.bz2
Source5: swat_32.png.bz2
Source6: swat_16.png.bz2
%endif
Source7: README.%{name}-mandrake-rpm
#Source8: samba-vscan-%{vscanver}.tar.gz
%if %build_vscan
%endif
%if %build_vscan && %mdkversion >= 920
BuildRequires: file-devel
%endif
Source10: samba-print-pdf.sh.bz2
Source11: smb-migrate.bz2

#Sources that used to be in packaging patch:
Source20:	smbusers
Source21:	smbprint
#Source22:	smbadduser
Source23:	findsmb
Source24:	smb.init
Source25:	winbind.init
Source26:	wrepld.init
Source27:	samba.pamd
Source28:	samba.pamd0_9
Source29:	system-auth-winbind.pamd


%if !%have_pversion
# Version specific patches: current version
Patch1: samba4-fix-tevent-link-order.patch
Patch2: samba4-fix-glue-linking.patch
Patch3: samba4a11-fix-linking.patch
#Patch11: samba-3.0-mandriva-packaging.patch
Patch18: http://samba.org/~metze/samba3-default-quota-ignore-error-01.diff
# https://bugzilla.samba.org/show_bug.cgi?id=3571, bug 21387
#Patch19: samba-3.0.21c-swat-fr-translaction.patch
# (oe) http://bugs.debian.org/cgi-bin/bugreport.cgi?bug=385389
#Patch20: samba-3.2.6-10_include_signalh.diff
#Patch21: samba-include_fix.diff
#Patch22: samba-3.0.30-fix-recursive-ac-macro.patch
#Patch23: samba-3.2.8-separate-modules.patch
#Patch24: samba-3.2.2-fix-cifsupcall-linkorder.patch
#https://bugzilla.samba.org/show_bug.cgi?id=5886 :
#Patch25: samba-3.2.4-fix-ldap-passmod-exop.patch
%else
# Version specific patches: upcoming version
%endif
# Limbo patches (applied to prereleases, but not preleases, ie destined for
# samba CVS)
%if %have_pversion && %have_pre
%endif
Requires: pam >= 0.64, samba-common = %{version}
BuildRequires: pam-devel readline-devel libncurses-devel popt-devel
BuildRequires: libxml2-devel
# Samba 3.2 and later should be built with capabilities support:
# http://lists.samba.org/archive/samba/2009-March/146821.html
BuildRequires: libcap-devel
BuildRequires: gnupg
# Required for ldb docs
BuildRequires: xsltproc docbook-style-xsl
%if %build_pgsql
BuildRequires: postgresql-devel
%endif
%ifnarch alpha
%if %build_mysql
BuildRequires: mysql-devel
%endif
%endif
%if %build_acl
BuildRequires: libacl-devel
%endif
BuildRequires: libldap-devel
%if %build_ads
BuildRequires: libldap-devel krb5-devel
%endif
%if %mdkversion >= 200800
BuildRequires: keyutils-devel
%endif
%if %build_tdb != 1
BuildRequires: tdb-devel >= 1:1.2.1
%endif
%if %build_tevent != 1
BuildRequires: tevent-devel
%endif

BuildRoot: %{_tmppath}/%{name}-%{version}-root
Requires(pre): chkconfig mktemp psmisc
Requires(pre): coreutils sed grep

%description
Samba provides an SMB server which can be used to provide
network services to SMB (sometimes called "Lan Manager")
clients, including various versions of MS Windows, OS/2,
and other Linux machines. Samba also provides some SMB
clients, which complement the built-in SMB filesystem
in Linux. Samba uses NetBIOS over TCP/IP (NetBT) protocols
and does NOT need NetBEUI (Microsoft Raw NetBIOS frame)
protocol.

Samba-3.0 features working NT Domain Control capability and
includes the SWAT (Samba Web Administration Tool) that
allows samba's smb.conf file to be remotely managed using your
favourite web browser. For the time being this is being
enabled on TCP port 901 via xinetd. SWAT is now included in
it's own subpackage, samba-swat.

Please refer to the WHATSNEW.txt document for fixup information.
This binary release includes encrypted password support.

Please read the smb.conf file and ENCRYPTION.txt in the
docs directory for implementation details.
%if %have_pversion
%message_bugzilla samba3
%endif 
%if !%build_system
%message_system
%endif
%if %build_non_default
WARNING: This RPM was built with command-line options. Please
see README.%{name}-mandrake-rpm in the documentation for
more information.
%endif

%package server
URL:	http://www.samba.org
Summary: Samba (SMB) server programs
Requires: %{name}-common = %{version}
# provision requires samba4-python
Requires: %{name}-python = %{version}
%if %have_rpmhelper
Requires(pre):		rpm-helper
%endif
Group: Networking/Other
%if %build_system
Provides: samba
Obsoletes: samba
Provides:  samba-server-ldap
Obsoletes: samba-server-ldap
Provides:  samba3-server
Obsoletes: samba3-server
%else
#Provides: samba-server
%endif

%description server
Samba-server provides a SMB server which can be used to provide
network services to SMB (sometimes called "Lan Manager")
clients. Samba uses NetBIOS over TCP/IP (NetBT) protocols
and does NOT need NetBEUI (Microsoft Raw NetBIOS frame)
protocol.

Samba-3.0 features working NT Domain Control capability and
includes the SWAT (Samba Web Administration Tool) that
allows samba's smb.conf file to be remotely managed using your
favourite web browser. For the time being this is being
enabled on TCP port 901 via xinetd. SWAT is now included in
it's own subpackage, samba-swat.

Please refer to the WHATSNEW.txt document for fixup information.
This binary release includes encrypted password support.

Please read the smb.conf file and ENCRYPTION.txt in the
docs directory for implementation details.
%if %have_pversion
%message_bugzilla samba3-server
%endif
%if !%build_system
%message_system
%endif

%package client
URL:	http://www.samba.org
Summary: Samba (SMB) client programs
Group: Networking/Other
Requires: %{name}-common = %{version}
Requires: mount-cifs
%if %build_alternatives
#Conflicts:	samba-client < 2.2.8a-9mdk
%endif
%if %build_system
Provides:  samba3-client
Obsoletes: samba3-client
Obsoletes: smbfs
%else
#Provides: samba-client
%endif
%if !%build_system && %build_alternatives
Provides: samba-client
%endif
%ifarch x86_64
Conflicts:	cups < 1.2.0-0.5361.0mdk
%endif

%description client
Samba-client provides some SMB clients, which complement the built-in
SMB filesystem in Linux. These allow the accessing of SMB shares, and
printing to SMB printers.
%if %have_pversion
%message_bugzilla samba3-client
%endif
%if !%build_system
%message_system
%endif

%package common
URL:	http://www.samba.org
Summary: Files used by both Samba servers and clients
Group: System/Servers
# rpcclient etc. use samba python modules
Requires: %{name}-python = %{version}
%if %build_system
Provides:  samba-common-ldap
Obsoletes: samba-common-ldap
Provides:  samba3-common
Obsoletes: samba3-common
%else
#Provides: samba-common
%endif

%description common
Samba-common provides files necessary for both the server and client
packages of Samba.
%if %have_pversion
%message_bugzilla samba3-common
%endif
%if !%build_system
%message_system
%endif

%if %{build_doc}
%package doc
URL:	http://www.samba.org
Summary: Documentation for Samba servers and clients
Group: System/Servers
Requires: %{name}-common = %{version}
%if %build_system
Obsoletes: samba3-doc
Provides:  samba3-doc
%else
#Provides: samba-doc
%endif

%description doc
Samba-doc provides documentation files for both the server and client
packages of Samba.
%if %have_pversion
%message_bugzilla samba3-doc
%endif
%if !%build_system
%message_system
%endif
%endif

%if %build_swat
%package swat
URL:	http://www.samba.org
Summary: The Samba Web Administration Tool
Requires: %{name}-server = %{version}
Requires: xinetd
Group: System/Servers
%if %build_system
Provides:  samba-swat-ldap
Obsoletes: samba-swat-ldap
Provides:  samba3-swat
Obsoletes: samba3-swat
%else
#Provides: samba-swat
%endif

%description swat
SWAT (the Samba Web Administration Tool) allows samba's smb.conf file
to be remotely managed using your favourite web browser. For the time
being this is being enabled on TCP port 901 via xinetd. Note that
SWAT does not use SSL encryption, nor does it preserve comments in
your smb.conf file. Webmin uses SSL encryption by default, and
preserves comments in configuration files, even if it does not display
them, and is therefore the preferred method for remotely managing
Samba.
%if %have_pversion
%message_bugzilla samba3-swat
%endif
%if !%build_system
%message_system
%endif
%endif

%if %build_winbind
%package winbind
URL:	http://www.samba.org
Summary: Samba-winbind daemon, utilities and documentation
Group: System/Servers
Requires: %{name}-common = %{version}
%endif
%if %build_winbind && !%build_system
Conflicts: samba-winbind
%endif
%if %build_winbind
%description winbind
Provides the winbind daemon and testing tools to allow authentication 
and group/user enumeration from a Windows or Samba domain controller.
%endif
%if %have_pversion
%message_bugzilla samba3-winbind
%endif
%if !%build_system
%message_system
%endif

%if %build_wins
%package -n nss_wins%{samba_major}
URL:	http://www.samba.org
Summary: Name Service Switch service for WINS
Group: System/Servers
Requires: %{name}-common = %{version}
Requires(pre): glibc
%endif
%if %build_wins && !%build_system
Conflicts: nss_wins
%endif
%if %build_wins
%description -n nss_wins%{samba_major}
Provides the libnss_wins shared library which resolves NetBIOS names to 
IP addresses.
%endif
%if %have_pversion
%message_bugzilla nss_wins3
%endif
%if !%build_system
%message_system
%endif

%package python
URL:	http://www.samba.org
Group:	Development/Python
Summary:	Samba Python modules
BuildRequires: python-devel

%description python
Samba Python modules

%if %build_test
%package test
URL:	http://www.samba.org
Summary: Debugging and benchmarking tools for samba
Group: System/Servers
Requires: %{name}-common = %{version}
%endif
%if %build_system && %build_test
Provides:  samba3-test samba3-debug
Obsoletes: samba3-test samba3-debug
%endif
%if !%build_system && %{build_test}
Provides: samba-test samba3-debug
Obsoletes: samba3-debug
%endif
%if %{build_test}

%description test
This package provides tools for benchmarking samba, and debugging
the correct operation of tools against smb servers.
%endif

%if %build_system
%package -n %{libname}
URL:		http://www.samba.org
Summary: 	SMB Client Library
Group:		System/Libraries
Provides:	libsmbclient

%description -n %{libname}
This package contains the SMB client library, part of the samba
suite of networking software, allowing other software to access
SMB shares.
%endif
%if %have_pversion && %build_system
%message_bugzilla %{libname}
%endif

%if %build_system
%package -n %{libname}-devel
URL:		http://www.samba.org
Summary: 	SMB Client Library Development files
Group:		Development/C
Provides:	libsmbclient-devel = %{version}-%{release}
Requires:       %{libname} = %{version}-%{release}

%description -n %{libname}-devel
This package contains the development files for the SMB client
library, part of the samba suite of networking software, allowing
the development of other software to access SMB shares.
%endif
%if %have_pversion && %build_system
%message_bugzilla %{libname}-devel
%endif

%if %build_system
%package -n %{libname}-static-devel
URL:            http://www.samba.org
Summary:        SMB Client Static Library Development files
Group:          Development/C
Provides:       libsmbclient-static-devel = %{version}-%{release}
Requires:       %{libname}-devel = %{version}-%{release}

%description -n %{libname}-static-devel
This package contains the static development files for the SMB
client library, part of the samba suite of networking software,
allowing the development of other software to access SMB shares.
%endif
%if %have_pversion && %build_system
%message_bugzilla %{libname}-devel
%endif

%package devel
Summary: Samba 4 development package
Group: Development/C

%description devel
Samba 4 development libraries

%package pidl
Summary: Perl IDL compiler for Samba4
Group: Development/Perl

%description pidl
Perl Interface Description Language compiler for Samba4

%if 0
%package -n %libnetapi
Summary: Samba library for accessing functions in 'net' binary
Group: System/Libraries

%description -n %libnetapi
Samba library for accessing functions in 'net' binary

%package -n %netapidevel
Group: Development/C
Summary: Samba library for accessing functions in 'net' binary
Provides: netapi-devel = %{version}-%{release}
Requires: %libnetapi = %{version}-%{release}

%description -n %netapidevel
Samba library for accessing functions in 'net' binary

%package -n %libsmbsharemodes
Group: System/Libraries
Summary: Samba Library for accessing smb share modes (locks etc.)

%description -n %libsmbsharemodes
Samba Library for accessing smb share modes (locks etc.)

%package -n %smbsharemodesdevel
Group: Development/C
Summary: Samba Library for accessing smb share modes (locks etc.)
Provides: smbsharemodes-devel = %{version}-%{release}
Requires: %libsmbsharemodes = %{version}-%{release}

%description -n %smbsharemodesdevel
Samba Library for accessing smb share modes (locks etc.)
%endif

%if %build_talloc
%package -n %libtalloc
Group: System/Libraries
Summary: Library implementing Samba's memory allocator

%description -n %libtalloc
Library implementing Samba's memory allocator

%package -n %tallocdevel
Group: Development/C
Summary: Library implementing Samba's memory allocator
Provides: talloc-devel = %{version}-%{release}
Requires: %libtalloc = %{version}-%{release}
BuildRequires: swig

%description -n %tallocdevel
Library implementing Samba's memory allocator

%endif
%if %build_tevent
%package -n %libtevent
Group: System/Libraries
Summary: Samba4's event management library

%description -n %libtevent
Samba4's event management library

%package -n %teventdevel
Group: Development/C
Summary: Development files for Samba4's event management library
Provides: talloc-devel = %{version}-%{release}
Requires: %libtevent = %{version}-%{release}

%description -n %teventdevel
Development files for Samba4's event management library

%endif

%package -n %libdcerpc
Group: System/Libraries
Summary: Library implementing DCE/RPC for Samba4
Version: %dcerpcver

%description -n %libdcerpc
Library implementing DCE/RPC for Samba4

%package -n %dcerpcdevel
Group: Development/C
Summary: Library implementing Samba's memory allocator
Provides: dcerpc-devel = %dcerpcver
Version: %dcerpcver
Requires: %libdcerpc = %{dcerpcver}-%{release}

%description -n %dcerpcdevel
Library implementing Samba's memory allocator

%package -n %libndr
Group: System/Libraries
Summary: Network Data Representation library from Samba4
Version: %ndrver

%description -n %libndr
Network Data Representation library from Samba4

%package -n %ndrdevel
Group: Development/C
Summary: Development files for Network Data Representation library from Samba4
Provides: ndr-devel = %ndrver
Version: %ndrver
Requires: %libndr = %{ndrver}-%{release}

%description -n %ndrdevel
Development files for Network Data Representation library from Samba4

%package -n %libsambahostconfig
Group: System/Libraries
Summary: Samba4's host configuration library
Version: %hostconfigver

%description -n %libsambahostconfig
Samba4's host configuration library

%package -n %sambahostconfigdevel
Group: Development/C
Summary: Samba4's host configuration library
Version: %hostconfigver
Provides: samba-hostconfig-devel = %hostconfigver
Requires: %libsambahostconfig = %{hostconfigver}-%{release}

%description -n %sambahostconfigdevel
Samba4's host configuration library

# Should probably use the libraries version, but we shipped it in samba3
# versioned with the samba3 version ... so we will probably need to epoch it too
#Version: %tdbver
%if %build_tdb
%package -n %libtdb
Group: System/Libraries
Summary: Library implementing Samba's embedded database
Version: %{real_version}

%description -n %libtdb
Library implementing Samba's embedded database

%package -n tdb-utils
Group: Databases
Summary: Tools for backing up, restoring, and manipulating Samba's embedded database
Conflicts: samba-server < 3.3.2-2

%description -n tdb-utils
Tools for backing up, restoring, and manipulating Samba's embedded database

%package -n %tdbdevel
Group: Development/C
Summary: Library implementing Samba's embedded database
Provides: tdb-devel = %{version}-%{release}
#Version: %tdbver
Requires: %libtdb = %{version}-%{release}
# because /usr/include/tdb.h was moved from libsmbclient0-devel to libtdb-devel
Conflicts: %{mklibname smbclient 0 -d} < 3.2.6-3

%description -n %tdbdevel
Library implementing Samba's embedded database

%endif
%package -n %libldb
Group: System/Libraries
Version: %ldbver
Summary: Library implementing Samba's LDAP-like interface to tdb or LDAP

%description -n %libldb
Library implementing Samba's LDAP-like interface to tdb or LDAP

%package -n ldb-utils
Group: Databases
Summary: LDAP-like clients for Samba's ldb abstraction layer to tdb or LDAP
Version: %ldbver
Conflicts: samba-server < 3.3.2-2
Requires: %libldb = %{ldbver}-%{release}

%description -n ldb-utils
LDAP-like clients for Samba's ldb abstraction layer to tdb or LDAP

%package -n %ldbdevel
Group: Development/C
Summary: Library implementing Samba's embedded database
Version: %ldbver
Provides: ldb-devel = %{ldbver}-%{release}
Requires: %libldb

%description -n %ldbdevel
Library implementing Samba's embedded database

%if 0
%package -n %libwbclient
Group: System/Libraries
Summary: Library providing access to winbindd
Version: %{real_version}

%description -n %libwbclient
Library providing access to winbindd

%package -n %wbclientdevel
Group: Development/C
Summary: Library providing access to winbindd
Provides: wbclient-devel = %{version}-%{release}

%description -n %wbclientdevel
Library providing access to winbindd
%endif

%package -n %libsambautil
Group: System/Libraries
Summary: Samba4 utility library
Version: %ndrver

%description -n %libsambautil
Samba4 utility library

%package -n %sambautildevel
Group: Development/C
Summary: Development files for Samba4 utility library
Provides: samba-util-devel = %sambautilver
Version: %sambautilver
Requires: %libsambautil = %{sambautilver}-%{release}

%description -n %sambautildevel
Development files for Samba4 utility library

%package -n %libregistry
Group: System/Libraries
Summary: Samba4 registry library
Version: %registryver

%description -n %libregistry
Samba4 registry library

%package -n %registrydevel
Group: Development/C
Summary: Development files for Samba4 registry library
Provides: registry-devel = %registryver
Version: %registryver
Requires: %libregistry = %{registryver}-%{release}

%description -n %registrydevel
Development files for Samba4 registry library

%package -n %libgensec
Group: System/Libraries
Summary: Samba4 generic security library
Version: %gensecver

%description -n %libgensec
Samba4 generic security library

%package -n %gensecdevel
Group: Development/C
Summary: Development files for Samba4 generic security library
Provides: gensecdevel = %gensecver
Version: %gensecver
Requires: %libgensec = %{gensecver}-%{release}

%description -n %gensecdevel
Development files for Samba4 generic security library


#%package passdb-ldap
#URL:		http://www.samba.org
#Summary:	Samba password database plugin for LDAP
#Group:		System/Libraries
#
#%description passdb-ldap
#The passdb-ldap package for samba provides a password database
#backend allowing samba to store account details in an LDAP
#database
#_if %have_pversion
#_message_bugzilla samba3-passdb-ldap
#_endif
#_if !%build_system
#_message_system
#_endif

%ifnarch alpha
%if %{build_mysql}
%package passdb-mysql
URL:		http://www.samba.org
Summary:	Samba password database plugin for MySQL
Group:		System/Libraries
Requires:	%{name}-server = %{version}-%{release}
%endif
%endif
%ifnarch alpha
%if %build_system && %{build_mysql}
Obsoletes:	samba3-passdb-mysql 
Provides:	samba3-passdb-mysql 
%endif
%endif
%ifnarch alpha
%if %{build_mysql}

%description passdb-mysql
The passdb-mysql package for samba provides a password database
backend allowing samba to store account details in a MySQL
database
%endif
%endif

#does postgresql build on alpha?
#ifnarch alpha
%if %{build_pgsql}
%package passdb-pgsql
URL:		http://www.samba.org
Summary:	Samba password database plugin for PostgreSQL
Group:		System/Libraries
Requires:	%{name}-server = %{version}-%{release}
#endif
#ifnarch alpha && %build_system
%endif
%if %build_system && %{build_pgsql}
Obsoletes:	samba3-passdb-pgsql
Provides:	samba3-passdb-pgsql
%endif
%if %{build_pgsql}

%description passdb-pgsql
The passdb-pgsql package for samba provides a password database
backend allowing samba to store account details in a PostgreSQL
database
%endif

#Antivirus packages:
%if %build_antivir
%package vscan-antivir
Summary: On-access virus scanning for samba using Antivir
Group: System/Servers
Requires: %{name}-server = %{version}
Provides: %{name}-vscan
%description vscan-antivir
A vfs-module for samba to implement on-access scanning using the
Antivir antivirus scanner daemon.
%endif


%if %build_clamav
%package vscan-clamav
Summary: On-access virus scanning for samba using Clam Antivirus
Group: System/Servers
Requires: %{name}-server = %{version}
Provides: %{name}-vscan
Requires: clamd
%description vscan-clamav
A vfs-module for samba to implement on-access scanning using the
Clam antivirus scanner daemon.
%endif

%if %build_fprot
%package vscan-fprot
Summary: On-access virus scanning for samba using FPROT
Group: System/Servers
Requires: %{name}-server = %{version}
Provides: %{name}-vscan
%description vscan-fprot
A vfs-module for samba to implement on-access scanning using the
FPROT antivirus software (which must be installed to use this).
%endif

%if %build_fsav
%package vscan-fsecure
Summary: On-access virus scanning for samba using F-Secure
Group: System/Servers
Requires: %{name}-server = %{version}
Provides: %{name}-vscan
%description vscan-fsecure
A vfs-module for samba to implement on-access scanning using the
F-Secure antivirus software (which must be installed to use this).
%endif

%if %build_icap
%package vscan-icap
Summary: On-access virus scanning for samba using ICAP
Group: System/Servers
Requires: %{name}-server = %{version}
Provides: %{name}-icap
%description vscan-icap
A vfs-module for samba to implement on-access scanning using
ICAP-capable antivirus software.
%endif

%if %build_kaspersky
%package vscan-kaspersky
Summary: On-access virus scanning for samba using Kaspersky
Group: System/Servers
Requires: %{name}-server = %{version}
Provides: %{name}-vscan
%description vscan-kaspersky
A vfs-module for samba to implement on-access scanning using the
Kaspersky antivirus software (which must be installed to use this).
%endif

%if %build_mks
%package vscan-mks
Summary: On-access virus scanning for samba using MKS
Group: System/Servers
Requires: %{name}-server = %{version}
Provides: %{name}-vscan
%description vscan-mks
A vfs-module for samba to implement on-access scanning using the
MKS antivirus software (which must be installed to use this).
%endif

%if %build_nai
%package vscan-nai
Summary: On-access virus scanning for samba using NAI McAfee
Group: System/Servers
Requires: %{name}-server = %{version}
Provides: %{name}-vscan
%description vscan-nai
A vfs-module for samba to implement on-access scanning using the
NAI McAfee antivirus software (which must be installed to use this).
%endif

%if %build_openav
%package vscan-openav
Summary: On-access virus scanning for samba using OpenAntivirus
Group: System/Servers
Requires: %{name}-server = %{version}
Provides: %{name}-vscan
%description vscan-openav
A vfs-module for samba to implement on-access scanning using the
OpenAntivirus antivirus software (which must be installed to use this).
%endif

%if %build_sophos
%package vscan-sophos
Summary: On-access virus scanning for samba using Sophos
Group: System/Servers
Requires: %{name}-server = %{version}
Provides: %{name}-vscan
%description vscan-sophos
A vfs-module for samba to implement on-access scanning using the
Sophos antivirus software (which must be installed to use this).
%endif

%if %build_symantec
%package vscan-symantec
Summary: On-access virus scanning for samba using Symantec
Group: System/Servers
Requires: %{name}-server = %{version}
Provides: %{name}-vscan
Autoreq: 0
%description vscan-symantec
A vfs-module for samba to implement on-access scanning using the
Symantec antivirus software (which must be installed to use this).
%endif


%if %build_trend
%package vscan-trend
Summary: On-access virus scanning for samba using Trend
Group: System/Servers
Requires: %{name}-server = %{version}
Provides: %{name}-vscan
%description vscan-trend
A vfs-module for samba to implement on-access scanning using the
Trend antivirus software (which must be installed to use this).
%endif

%if %build_cifs
%package -n mount-cifs%{samba_major}
URL:	http://www.samba.org
Summary: CIFS filesystem mount helper
Group: Networking/Other
Version: %{real_version}
Conflicts:	%{name}-client <= 3.0.11-1mdk
Requires:	keyutils > 1.2-%{mkrel 4}

%description -n mount-cifs%{samba_major}
This package provides the mount.cifs helper to mount cifs filesystems
using the cifs filesystem driver
%endif

%prep

# Allow users to query build options with --with options:
#%%define opt_status(%1)	%(echo %{1})
%if %{?_with_options:1}%{!?_with_options:0}
%define opt_status(%{1})	%(if [ %{1} -eq 1 ];then echo enabled;else echo disabled;fi)
#exit 1
%{error: }
%{error:Build options available are:}
%{error:--with[out] system   Build as the system samba package [or as samba3]}
%{error:--with[out] acl      Build with support for file ACLs          - %opt_status %build_acl}
%{error:--with[out] winbind  Build with Winbind support                - %opt_status %build_winbind}
%{error:--with[out] wins     Build with WINS name resolution support   - %opt_status %build_wins}
%{error:--with[out] ldap     Build with legacy (samba2) LDAP support   - %opt_status %build_ldap}
%{error:--with[out] ads      Build with Active Directory support       - %opt_status %build_ads}
%{error:--with[out] mysql    Build MySQL passdb backend                - %opt_status %build_mysql}
%{error:--with[out] pgsql    Build PostgreSQL passdb backend           - %opt_status %build_pgsql}
%{error:--with[out] scanners Enable on-access virus scanners           - %opt_status %build_scanners}
%{error:--with[out] test     Enable testing and benchmarking tools     - %opt_status %build_test}
%{error: }
%else
#{error: }
#{error: This rpm has build options available, use --with options to see them}
#{error: }
echo -e "\n This rpm has build options available, use --with options to see them\n" >&2
sleep 1
%endif

%if %{?_with_options:1}%{!?_with_options:0} && %build_scanners
#{error:--with scanners enables the following:%{?build_clamav:clamav,}%{?build_icap:icap,}%{?build_fprot:fprot,}%{?build_mks:mks,}%{?build_openav:openav,}%{?build_sophos:sophos,}%{?build_symantec:symantec,}%{?build_trend:trend}}
%{error:--with scanners enables the following: antivir,clamav,icap,fprot,fsav,mks,nai,openav,sophos,trend}
%{error: }
%{error:To enable others (requires development libraries for the scanner):}
%{error:--with symantec           Enable on-access scanning with Symantec        - %opt_status %build_symantec}
%{error: }
%endif

%if %{?_with_options:1}%{!?_with_options:0}
clear
exit 1
%endif


%if %build_non_default
RPM_EXTRA_OPTIONS="\
%{?_with_system: --with system}\
%{?_without_system: --without system}\
%{?_with_acl: --with acl}\
%{?_without_acl: --without acl}\
%{?_with_winbind: --with winbind}\
%{?_without_winbind: --without winbind}\
%{?_with_wins: --with wins}\
%{?_without_wins: --without wins}\
%{?_with_ldap: --with ldap}\
%{?_without_ldap: --without ldap}\
%{?_with_ads: --with ads}\
%{?_without_ads: --without ads}\
%{?_with_scanners: --with scanners}\
%{?_without_scanners: --without scanners}\
"
echo "Building a non-default rpm with the following command-line arguments:"
echo "$RPM_EXTRA_OPTIONS"
echo "This rpm was built with non-default options, thus, to build ">%{SOURCE7}
echo "an identical rpm, you need to supply the following options">>%{SOURCE7}
echo "at build time: $RPM_EXTRA_OPTIONS">>%{SOURCE7}
echo -e "\n%{name}-%{version}-%{release}\n">>%{SOURCE7}
%else
echo "This rpm was built with default options">%{SOURCE7}
echo -e "\n%{name}-%{version}-%{release}\n">>%{SOURCE7}
%endif


#Try and validate signatures on source:
# FIXME: find public key used to sign samba4 releases
export GNUPGHOME=%{_tmppath}/samba-gpghome
if [ -d "$GNUPGHOME" ]
then echo "Error, GNUPGHOME $GNUPGHOME exists, remove it and try again"; exit 1
fi
install -d -m700 $GNUPGHOME
gpg --import %{SOURCE98}
VERIFYSOURCE=`basename %{SOURCE0}`
VERIFYSOURCE=%{_tmppath}/${VERIFYSOURCE%%.gz}
gzip -dc %{SOURCE0} > $VERIFYSOURCE
pushd %{_tmppath}
cp %{SOURCE99} .
#gpg --trust-model always --verify `basename %{SOURCE99}`
#VERIFIED=$?
VERIFIED=1
rm -f `basename %{SOURCE99}`
popd
rm -Rf $GNUPGHOME

rm -f $VERIFYSOURCE
if [ "$VERIFIED" -eq 0 ]
then
	echo "Verification of %{SOURCE0} against %{SOURCE99} with key %{SOURCE98} succeeded"
else
	echo "Source verification failed!" >&2
	#exit 1
fi


%if %build_vscan
%setup -q -a 8 -n %{pkg_name}-%{source_ver}
%else
%setup -q -n %{pkg_name}-%{source_ver}
%endif
#%patch111 -p1
# Version specific patches: current version
%if !%have_pversion
echo "Applying patches for current version: %{ver}"
%patch1 -p1 -b .linkorder
#patch2 -p1 -b .linkglue
#%patch7 -p1 -b .lib64
#%patch10 -p1 -b .rpcclient-libs
#patch11 -p1 -b .mdk
#%patch14 -p1 -b .fixdocs
#%patch15 -p1
pushd source4
#%patch17
# XXX - andreas - doesn't apply to 3.0.25a and no new upstream version
# (there were VFS changes in samba)
#%patch18
popd
#FIXME
#patch19 -p1
#patch21 -p1
#patch20 -p0
#patch22 -p1
#patch23 -p1
#patch24 -p1 -b .cifslinkorder
#patch25 -p1 -b .fixldapexop

# patches from cvs/samba team
pushd source4
popd
%else
# Version specific patches: upcoming version
echo "Applying patches for new versions: %{pversion}"
%endif

mkdir standalone
#for i in replace talloc tdb tevent ../source4/lib/ldb
#do
#  cp -a lib/$i standalone
#done
#perl -pi -e 's/-ltevent/-ltevent -ltalloc/g' standalone/ldb/external/libevents.m4
perl -pi -e 's/-ltevent/-ltevent -ltalloc/g' source4/lib/ldb/external/libevents.m4
# Tries to fetch docbook xsl files from the network
#perl -pi -e 's/(EXTRA_TARGETS =) \@DOC_TARGET\@/$1/' standalone/talloc/Makefile.in
perl -pi -e 's/(EXTRA_TARGETS =) \@DOC_TARGET\@/$1/' lib/talloc/Makefile.in
perl -pi -e 's,http://docbook.sourceforge.net/release/xsl/current,/usr/share/sgml/docbook/xsl-stylesheets/,g' source4/lib/ldb/docs/builddocs.sh

#Should be fixed somewhere in smb_build

%build
%serverbuild

%define shared_build_dir %{_sourcedir}/standalone/instroot
SAVE_LDLPATH=$LD_LIBRARY_PATH
SAVE_CFLAGS=$CFLAGS
SAVE_LDFLAGS=$LDFLAGS
export LD_LIBRARY_PATH=%{shared_build_dir}/lib
export LDFLAGS="$LDFLAGS -L%{shared_build_dir}/lib"
export CPPFLAGS="$CPPFLAGS -I%{shared_build_dir}/include"
export PKG_CONFIG_PATH=%{shared_build_dir}/

rm -Rf %{shared_build_dir}
for i in \
%if %build_talloc
lib/talloc \
%endif
%if %build_tdb
lib/tdb \
%endif
%if %build_tevent
lib/tevent \
%endif
 source4/lib/ldb
do
  pushd $i
  ./autogen.sh
  if [ "$i" == "source4/lib/db" ];then perl -p -i.fixbuild -e 's/LIBS="-ltevent  \$LIBS"/LIBS="-ltevent -ltalloc \$LIBS"/g' configure;fi
  %configure2_5x --with-shared-build-dir=%{shared_build_dir}
  make shared-build
  cp -f *.pc %{shared_build_dir}
  #make install DESTDIR=%{shared_build_dir}
  popd
done
#cp -a standalone/ldb/include/ldb_module.h %{shared_build_dir}/include
cp -a source4/lib/ldb/include/ldb_module.h %{shared_build_dir}/include
rm -f ./source4/lib/ldb/include/config.h ./lib/talloc/config.h ./lib/tevent/config.h ./lib/tdb/include/config.h

#export LD_LIBRARY_PATH=$SAVE_LDLPATH
#export CFLAGS=$SAVE_CFLAGS
#export LD_LIBRARY_PATH="$SAVE_LDLPATH %{shared_build_dir}/%{_libdir}"
#export CFLAGS="$SAVE_CFLAGS -I%{shared_build_dir}/%{_includedir}"
#export LDFLAGS="$SAVE_LDFLAGS -L%{shared_build_dir}/%{_libdir}"
#export PKG_CONFIG_PATH="%{shared_build_dir}/%{_libdir}/pkgconfig"

pushd source4
CFLAGS="`echo "$RPM_OPT_FLAGS"|sed -e 's/-g//g'` -DLDAP_DEPRECATED"
%if %gcc331
CFLAGS=`echo "$CFLAGS"|sed -e 's/-O2/-O/g'`
%endif
perl -pi -e 's,samba(\"|/),%{name}$1,g' build/m4/check_path.m4
./autogen.sh
# Don't use --with-fhs now, since it overrides libdir, it sets configdir, 
# lockdir,piddir logfilebase,privatedir and swatdir
%configure2_5x     --enable-fhs \
		--prefix=%{_prefix} \
		--enable-dso \
		--enable-external-libtalloc \
		--enable-external-libtdb \
		--enable-external-libtevent \
		--program-suffix=%{samba_major} 
# Results in too many unresolved symbols

# Samba4 build system is too screwed up for this to work
#		--enable-external-libldb \

#                --with-configdir=%{_sysconfdir}/%{name} \
#                --with-pammodulesdir=%{_lib}/security/ \
#                --with-modulesdir=%{_libdir}/%{name} \
#                --with-rootsbindir=/bin \
#                --with-pam \
#                --with-automount \
#                --with-pam_smbpass \
#                --with-swatdir=%{_datadir}/swat%{samba_major} \
#                --with-syslog \
#                --with-quotas \
#		--with-acl-support      \
#                --with-utmp \
#		--with-shared-modules=idmap_rid,idmap_ad \
#		--with-cifsmount \
#		--with-cifsupcall \
#		--with-expsam=%build_expsam \
#		--with-shared-modules=pdb_ldap,idmap_ldap \
#		--with-manpages-langs=en,ja,pl	\
#_if !%build_system
#                --with-smbwrapper \
#_endif		
#		--with-nisplussam \


patch -p2 -b -z .link < %{_sourcedir}/samba4a11-fix-linking.patch
#%patch3 -p1 -b .link

#Build PIDL for installation into vendor directories before 'make proto' gets to it
(cd ../pidl && %{__perl} Makefile.PL INSTALLDIRS=vendor )

#Fix the make file so we don't create debug information on 9.2
%if %mdkversion == 920
perl -pi -e 's/-g //g' Makefile
%endif

perl -pi -e 's|-Wl,-rpath,%{_libdir}||g;s|-Wl,-rpath -Wl,%{_libdir}||g' Makefile
perl -pi -e 's/^TALLOC_LIBS = /TALLOC_LIBS = -ltalloc/g' mkconfig.mk

#Builds using PIDL the IDL and many other things 
make prefix=%{_prefix} proto

make prefix=%{_prefix} modulesdir=%{_libdir}/%{name} everything
#make all libsmbclient smbfilter wins %{?_with_test: torture debug2html bin/log2pcap} bin/smbget

popd

%install
rm -rf $RPM_BUILD_ROOT
mkdir -p $RPM_BUILD_ROOT

#Ensure all docs are readable
#chmod a+r docs -R

# Any entries here mean samba makefile is *really* broken:
mkdir -p $RPM_BUILD_ROOT%{_sysconfdir}/%{name}
mkdir -p $RPM_BUILD_ROOT/%{_datadir}
mkdir -p $RPM_BUILD_ROOT%{_libdir}/%{name}/vfs

pushd source4
%makeinstall_std prefix=%{_prefix}
#make DESTDIR=$RPM_BUILD_ROOT install installclientlib installmodules
#Undo the PIDL install, we want to try again with the right options
rm -rf $RPM_BUILD_ROOT/%{_libdir}/perl5
rm -rf $RPM_BUILD_ROOT/%{_datadir}/perl5

#Install PIDL
( cd ../pidl && make install PERL_INSTALL_ROOT=$RPM_BUILD_ROOT )
popd

# we ship docs in the docs supackage, and lik it into swat, delete the extra copy:
rm -Rf %{buildroot}/%{_datadir}/swat/using_samba

#install -m755 source/bin/smbget %{buildroot}/%{_bindir}


#need to stay
mkdir -p $RPM_BUILD_ROOT/{sbin,bin}
mkdir -p $RPM_BUILD_ROOT%{_sysconfdir}/{logrotate.d,pam.d,xinetd.d}
mkdir -p $RPM_BUILD_ROOT/%{_initrddir}
mkdir -p $RPM_BUILD_ROOT/var/cache/%{name}
mkdir -p $RPM_BUILD_ROOT/var/log/%{name}
mkdir -p $RPM_BUILD_ROOT/var/run/%{name}
mkdir -p $RPM_BUILD_ROOT/var/spool/%{name}
mkdir -p $RPM_BUILD_ROOT/%{_localstatedir}/lib/%{name}/{netlogon,profiles,printers}
mkdir -p $RPM_BUILD_ROOT/%{_localstatedir}/lib/%{name}/printers/{W32X86,WIN40,W32ALPHA,W32MIPS,W32PPC}
mkdir -p $RPM_BUILD_ROOT/%{_localstatedir}/lib/%{name}/codepages/src
mkdir -p $RPM_BUILD_ROOT/%{_lib}/security
mkdir -p $RPM_BUILD_ROOT%{_libdir}/pkgconfig
mkdir -p $RPM_BUILD_ROOT%{_sbindir}
mkdir -p $RPM_BUILD_ROOT%{_bindir}
mkdir -p $RPM_BUILD_ROOT%{_libdir}/%{name}/vfs
mkdir -p $RPM_BUILD_ROOT%{_datadir}/%{name}/scripts

#install -m755 source/bin/lib*.a $RPM_BUILD_ROOT%{_libdir}/

# Development pkgconfig files

## 1. Generate the .pc files that are not done automatically
## (NB: This does not work when done at the same time as configure above)
#for i in talloc tdb; do
#	pushd source4/lib/$i
#	./autogen.sh -V && ./configure --prefix=%{_prefix} --libdir=%{_libdir}
#	popd
#done
#
## 2. Install them
#for i in smbclient smbsharemodes netapi wbclient; do
#	install -m 644 source4/pkgconfig/$i.pc $RPM_BUILD_ROOT%{_libdir}/pkgconfig/
#done
#install -m 644 source4/lib/talloc/talloc.pc $RPM_BUILD_ROOT%{_libdir}/pkgconfig/
#install -m 644 source4/lib/tdb/tdb.pc $RPM_BUILD_ROOT%{_libdir}/pkgconfig/
#for i in talloc tdb tevent ldb                                                      
#for i in lib/talloc lib/tdb lib/tevent source4/lib/ldb
for i in \
%if %build_talloc
lib/talloc \
%endif
%if %build_tdb
lib/tdb \
%endif
%if %build_tevent
lib/tevent \
%endif
 source4/lib/ldb
do
  #pushd standalone/$i                                                               
  pushd $i                                                               
  %makeinstall_std                                                                  
  popd                                                                              
  #for j in 0 1                                                                     
  #do [ -e %{buildroot}/%{_libdir}/lib${i}.so.${j} ] && ln -s %{buildroot}/%{_libdir}/lib${i}.so.${j} lib${i}.so                                                         
  #done                                                                             
done                                                                                
pushd %{buildroot}/%{_libdir}
%if %build_talloc
[ -e libtalloc.so ] || ln -s libtalloc.so.%{tallocmajor} libtalloc.so
%endif
%if %build_tdb
[ -e libtdb.so ] || ln -s libtdb.so.%{tdbmajor} libtdb.so
%endif
%if %build_tevent
[ -e libtevent.so ] || ln -s libtevent.so.%{teventmajor} libtevent.so
%endif
[ -e libldb.so ] || ln -s libldb.so.%{ldbmajor} libldb.so
popd
# Fix some paths so provision works:
perl -pi -e 's,default_ldb_modules_dir = None,default_ldb_modules_dir = \"%{_libdir}/%{name}/ldb\",g' %{buildroot}/%{python_sitearch}/samba/__init__.py
perl -pi -e 's,share/samba/setup,share/%{name}/setup,g' %{buildroot}/%{python_sitearch}/samba/provision.py

# FIXME potential license issues with schema license vs GPL?
cp -a source4/setup/ad-schema/ %{buildroot}/%{_datadir}/%{name}/setup

# smbsh forgotten
#install -m 755 source/bin/smbsh $RPM_BUILD_ROOT%{_bindir}/

%if %build_vscan
%makeinstall_std -C %{vfsdir}/%{vscandir}
install -m 644 %{vfsdir}/%{vscandir}/*/vscan-*.conf %{buildroot}/%{_sysconfdir}/%{name}
%endif
	
#libnss_* still not handled by make:
# Install the nsswitch library extension file
#for i in wins winbind; do
#  install -m755 source4/nsswitch/libnss_${i}.so $RPM_BUILD_ROOT/%{_lib}/libnss_${i}.so
#done
# Make link for wins and winbind resolvers
#( cd $RPM_BUILD_ROOT/%{_lib}; ln -s libnss_wins.so libnss_wins.so.2; ln -s libnss_winbind.so libnss_winbind.so.2)
#install -d %{buildroot}/%{_libdir}/krb5/plugins
#install -m755 source4/bin/winbind_krb5_locator.so %{buildroot}/%{_libdir}/krb5/plugins

%if %{build_test}
for i in {%{testbin}};do
  #install -m755 source/bin/${i} $RPM_BUILD_ROOT/%{_bindir}/${i}%{samba_major}
  mv %{buildroot}/%{_bindir}/$i %{buildroot}/%{_bindir}/${i}%{samba_major} || :
done
%endif

%if !%{build_winbind}
rm -f %{buildroot}%{_bindir}/wbinfo %{buildroot}%{_sysconfdir}/pam.d/system-auth-winbind* %{buildroot}%{_libdir}/libnss_winbind*
%endif

rm -fr %{buildroot}%py_platsitedir/subunit

# Install other stuff

#        install -m644 examples/VFS/recycle/recycle.conf $RPM_BUILD_ROOT%{_sysconfdir}/samba/
        #install -m644 %{SOURCE20} $RPM_BUILD_ROOT%{_sysconfdir}/%{name}/smbusers
        #install -m755 %{SOURCE21} $RPM_BUILD_ROOT/%{_bindir}
        #install -m755 %{SOURCE22} $RPM_BUILD_ROOT/usr/bin
        #install -m755 %{SOURCE23} $RPM_BUILD_ROOT/%{_bindir}
        install -m755 %{SOURCE24} $RPM_BUILD_ROOT/%{_initrddir}/%{name}
        #install -m755 %{SOURCE24} $RPM_BUILD_ROOT/%{_sbindir}/%{name}
	#install -m755 %{SOURCE25} $RPM_BUILD_ROOT/%{_initrddir}/winbind
#	install -m755 %{SOURCE25} $RPM_BUILD_ROOT/%{_sbindir}/winbind
#	install -m755 %{SOURCE26} $RPM_BUILD_ROOT/%{_initrddir}/wrepld%{samba_major}
%if %mdkversion < 200700
        install -m644 %{SOURCE27} $RPM_BUILD_ROOT/%{_sysconfdir}/pam.d/%{name}
%else
        install -m644 %{SOURCE28} $RPM_BUILD_ROOT/%{_sysconfdir}/pam.d/%{name}
%endif
%if %{build_winbind}
	install -m644 %{SOURCE29} $RPM_BUILD_ROOT/%{_sysconfdir}/pam.d/system-auth-winbind
%endif
#
        install -m644 %{SOURCE1} $RPM_BUILD_ROOT/%{_sysconfdir}/logrotate.d/%{name}
#	install -m644 packaging/Mandrake/samba-slapd-include.conf $RPM_BUILD_ROOT%{_sysconfdir}/%{name}/samba-slapd.include

# install pam_winbind.conf sample file
mkdir -p %{buildroot}%{_sysconfdir}/security
#install -m 0644 examples/pam_winbind/pam_winbind.conf %{buildroot}%{_sysconfdir}/security/pam_winbind.conf

#install -m755 examples/LDAP/convertSambaAccount $RPM_BUILD_ROOT/%{_datadir}/%{name}/scripts/

# make a conf file for winbind from the default one:
#	cat packaging/Mandrake/smb.conf|sed -e  's/^;  winbind/  winbind/g;s/^;  obey pam/  obey pam/g;s/   printer admin = @adm/#  printer admin = @adm/g; s/^#   printer admin = @"D/   printer admin = @"D/g;s/^;   password server = \*/   password server = \*/g;s/^;  template/  template/g; s/^   security = user/   security = domain/g' > packaging/Mandrake/smb-winbind.conf
#        install -m644 packaging/Mandrake/smb-winbind.conf $RPM_BUILD_ROOT/%{_sysconfdir}/%{name}/smb-winbind.conf

# Some inline fixes for smb.conf for non-winbind use
#install -m644 packaging/Mandrake/smb.conf $RPM_BUILD_ROOT/%{_sysconfdir}/%{name}/smb.conf
#cat packaging/Mandrake/smb.conf | \
#touch %{buildroot}/%{_sysconfdir}/%{name}/smb.conf
#sed -e 's/^;   printer admin = @adm/   printer admin = @adm/g' >$RPM_BUILD_ROOT/%{_sysconfdir}/%{name}/smb.conf
%if %build_cupspc
perl -pi -e 's/printcap name = lpstat/printcap name = cups/g' $RPM_BUILD_ROOT/%{_sysconfdir}/%{name}/smb.conf
perl -pi -e 's/printcap name = lpstat/printcap name = cups/g' $RPM_BUILD_ROOT/%{_sysconfdir}/%{name}/smb-winbind.conf
# Link smbspool to CUPS (does not require installed CUPS)

        mkdir -p $RPM_BUILD_ROOT/%{_prefix}/lib/cups/backend
        ln -s %{_bindir}/smbspool%{alternative_major} $RPM_BUILD_ROOT/%{_prefix}/lib/cups/backend/smb%{alternative_major}
%endif

#%if !%build_system
# Fix script paths in smb.conf
#perl -pi -e 's,%{_datadir}/samba,%{_datadir}/%{name},g' %{buildroot}/%{_sysconfdir}/%{name}/smb*.conf
#%endif


## cifs.upcall moved for no reason
#rm -f %{buildroot}/%{_sbindir}/cifs.upcall.old
#mv %{buildroot}/%{_sbindir}/cifs.upcall %{buildroot}/bin
##install mount.cifs
for i in {%{cifs_bin}};do
##install -m755 source/bin/${i} %{buildroot}/bin/${i}%{alternative_major}
mv %{buildroot}/usr/bin/${i} %{buildroot}/bin/${i}%{alternative_major}
ln -s ../bin/${i}%{alternative_major} %{buildroot}/sbin/${i}%{alternative_major}
done

        echo 127.0.0.1 localhost > $RPM_BUILD_ROOT/%{_sysconfdir}/%{name}/lmhosts

%if %build_swat
# xinetd support

        mkdir -p $RPM_BUILD_ROOT/%{_sysconfdir}/xinetd.d
        install -m644 %{SOURCE3} $RPM_BUILD_ROOT/%{_sysconfdir}/xinetd.d/swat%{samba_major}

# menu support

mkdir -p %{buildroot}/%{_datadir}/applications
cat > %{buildroot}/%{_datadir}/applications/mandriva-%{name}-swat.desktop << EOF
[Desktop Entry]
Name=Samba Configuration (SWAT)
Comment=The Swat Samba Administration Tool
Exec=www-browser http://localhost:901/
Icon=swat%{samba_major}
Terminal=false
Type=Application
StartupNotify=true
Categories=X-MandrivaLinux-System-Configuration-Networking;
EOF

mkdir -p $RPM_BUILD_ROOT%{_liconsdir} $RPM_BUILD_ROOT%{_iconsdir} $RPM_BUILD_ROOT%{_miconsdir}

# install html man pages for swat
install -d %{buildroot}/%{_datadir}/swat%{samba_major}/help/manpages
#install -m644 docs/htmldocs/manpages-3/* %{buildroot}/%{_datadir}/swat%{samba_major}/help/manpages

bzcat %{SOURCE4} > $RPM_BUILD_ROOT%{_liconsdir}/swat%{samba_major}.png
bzcat %{SOURCE5} > $RPM_BUILD_ROOT%{_iconsdir}/swat%{samba_major}.png
bzcat %{SOURCE6} > $RPM_BUILD_ROOT%{_miconsdir}/swat%{samba_major}.png
%endif

bzcat %{SOURCE10}> $RPM_BUILD_ROOT%{_datadir}/%{name}/scripts/print-pdf
#bzcat %{SOURCE11}> $RPM_BUILD_ROOT%{_datadir}/%{name}/scripts/smb-migrate

# Fix configs when not building system samba:

#Client binaries will have suffixes while we use alternatives, even
# if we are system samba
%if !%build_system || %build_alternatives
for OLD in %{buildroot}/%{_bindir}/{%{clientbin},eventlogadm} %{buildroot}/bin/{%{cifs_bin}} %{buildroot}/%{_prefix}/lib/cups/backend/smb
do
    NEW=`echo ${OLD}%{alternative_major}`
    [ -e $OLD ] && mv -f $OLD $NEW
done
for OLD in %{buildroot}/%{_mandir}/man?/{%{clientbin},eventlogadm}* %{buildroot}/%{_mandir}/man?/{%{cifs_bin}}*
do
    if [ -e $OLD ]
    then
        BASE=`perl -e '$_="'${OLD}'"; m,(%buildroot)(.*?)(\.[0-9]),;print "$1$2\n";'`
        EXT=`echo $OLD|sed -e 's,'${BASE}',,g'`
        NEW=`echo ${BASE}%{alternative_major}${EXT}`
        mv $OLD $NEW
    fi
done		
%endif
# Server/common binaries are versioned only if not system samba:
%if !%build_system
for OLD in %{buildroot}/%{_bindir}/{%{commonbin}} %{buildroot}/%{_bindir}/%{serverbin} %{buildroot}/%{_sbindir}/{%{serversbin},swat}
do
    NEW=`echo ${OLD}%{alternative_major}`
    mv $OLD $NEW -f ||:
done
# And the man pages too:
for OLD in %{buildroot}/%{_mandir}/man?/{%{commonbin},%{serverbin},%{serversbin},swat,{%testbin},smb.conf,lmhosts}*
do
    if [ -e $OLD ]
    then
        BASE=`perl -e '$_="'${OLD}'"; m,(%buildroot)(.*?)(\.[0-9]),;print "$1$2\n";'`
#        BASE=`perl -e '$name="'${OLD}'"; print "",($name =~ /(.*?)\.[0-9]/), "\n";'`
	EXT=`echo $OLD|sed -e 's,'${BASE}',,g'`
	NEW=`echo ${BASE}%{samba_major}${EXT}`
	mv $OLD $NEW
    fi
done		
# Replace paths in config files and init scripts:
for i in smb ;do
	perl -pi -e 's,/subsys/'$i',/subsys/'$i'%{samba_major},g' $RPM_BUILD_ROOT/%{_initrddir}/${i}%{samba_major}
done
for i in %{_sysconfdir}/%{name}/smb.conf %{_initrddir}/%{name} %{_initrddir}/winbind /%{_sysconfdir}/logrotate.d/%{name} /%{_sysconfdir}/xinetd.d/swat%{samba_major} %{_initrddir}/wrepld%{samba_major}; do
	perl -pi -e 's,%{pkg_name},%{name},g; s,nmbd,%{_sbindir}/nmbd%{samba_major},g; s,/usr/sbin/swat,%{_sbindir}/swat%{samba_major},g;s,wrepld,%{_sbindir}/wrepld%{samba_major},g;s,samba4.pid,samba.pid,g' $RPM_BUILD_ROOT/$i;
done
# Fix xinetd file for swat:
perl -pi -e 's,/usr/sbin,%{_sbindir},g' $RPM_BUILD_ROOT/%{_sysconfdir}/xinetd.d/swat%{samba_major}
%endif

#Clean up unpackaged files:
#for i in %{_bindir}/pam_smbpass.so %{_bindir}/smbwrapper.so;do
#rm -f %{buildroot}/$i
#done
# the binary gets removed ... but not the man page ...
rm -f %{buildroot}/%{_mandir}/man1/testprns*

# (sb) make a smb.conf.clean we can use for the merge, since an existing
# smb.conf won't get overwritten
#cp $RPM_BUILD_ROOT/%{_sysconfdir}/%{name}/smb.conf $RPM_BUILD_ROOT/%{_datadir}/%{name}/smb.conf.clean

# (sb) leave a README.mdk.conf to explain what has been done
cat << EOF > $RPM_BUILD_ROOT/%{_datadir}/%{name}/README.mdk.conf
In order to facilitate upgrading an existing samba install, and merging
previous configuration data with any new syntax used by samba3, a merge
script has attempted to combine your local configuration data with the
new conf file format.  The merged data is in smb.conf, with comments like

	# *** merged from original smb.conf: ***

near the additional entries.  Any local shares should have been appended to
smb.conf.  A log of what took place should be in: 

	/var/log/samba/smb-migrate.log

A clean samba3 smb.conf is in /usr/share/samba, named smb.conf.clean.
Your original conf should be /etc/samba/smb.conf.tomerge.

The actual merge script is /usr/share/samba/scripts/smb-migrate.

EOF


%if %build_winbind
%find_lang pam_winbind
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%post server

%_post_service %{name}
#%_post_service wrepld%{samba_major}

# Add a unix group for samba machine accounts
groupadd -frg 421 machines

# Migrate tdb's from /var/lock/samba (taken from official samba spec file):
for i in /var/lock/samba/*.tdb
do
if [ -f $i ]; then
	newname=`echo $i | sed -e's|var\/lock\/samba|var\/cache\/samba|'`
	echo "Moving $i to $newname"
	mv $i $newname
fi
done

%post common
# Basic migration script for pre-2.2.1 users,
# since smb config moved from /etc to %{_sysconfdir}/samba

# Let's create a proper %{_sysconfdir}/samba/smbpasswd file
[ -f %{_sysconfdir}/%{name}/smbpasswd ] || {
	echo "Creating password file for samba..."
	touch %{_sysconfdir}/%{name}/smbpasswd
}

# And this too, in case we don't have smbd to create it for us
[ -f /var/cache/%{name}/unexpected.tdb ] || {
	touch /var/cache/%{name}/unexpected.tdb
}

# Let's define the proper paths for config files
perl -pi -e 's/(\/etc\/)(smb)/\1%{name}\/\2/' %{_sysconfdir}/%{name}/smb.conf

# Fix the logrotate.d file from smb and nmb to smbd and nmbd
if [ -f %{_sysconfdir}/logrotate.d/samba ]; then
        perl -pi -e 's/smb /smbd /' %{_sysconfdir}/logrotate.d/samba
        perl -pi -e 's/nmb /nmbd /' %{_sysconfdir}/logrotate.d/samba
fi

# And not loose our machine account SID
[ -f %{_sysconfdir}/MACHINE.SID ] && mv -f %{_sysconfdir}/MACHINE.SID %{_sysconfdir}/%{name}/ ||:

%triggerpostun common -- samba-common < 3.0.1-3mdk
# (sb) merge any existing smb.conf with new syntax file
if [ $1 = 2 ]; then
	# (sb) save existing smb.conf for merge
	echo "Upgrade: copy smb.conf to smb.conf.tomerge for merging..."
	cp -f %{_sysconfdir}/%{name}/smb.conf %{_sysconfdir}/%{name}/smb.conf.tomerge
	echo "Upgrade: merging previous smb.conf..."
	if [ -f %{_datadir}/%{name}/smb.conf.clean ]; then
		cp %{_datadir}/%{name}/smb.conf.clean %{_sysconfdir}/%{name}/smb.conf
		cp %{_datadir}/%{name}/README.mdk.conf %{_sysconfdir}/%{name}/
		%{_datadir}/%{name}/scripts/smb-migrate commit
	fi
fi

%postun common
if [ -f %{_sysconfdir}/%{name}/README.mdk.conf ];then rm -f %{_sysconfdir}/%{name}/README.mdk.conf;fi

%if %build_winbind
%post winbind
if [ $1 = 1 ]; then
    /sbin/chkconfig winbind on
    cp -af %{_sysconfdir}/nsswitch.conf %{_sysconfdir}/nsswitch.conf.rpmsave
    cp -af %{_sysconfdir}/nsswitch.conf %{_sysconfdir}/nsswitch.conf.rpmtemp
    for i in passwd group;do
        grep ^$i %{_sysconfdir}/nsswitch.conf |grep -v 'winbind' >/dev/null
        if [ $? = 0 ];then
            echo "Adding a winbind entry to the $i section of %{_sysconfdir}/nsswitch.conf"
            awk '/^'$i'/ {print $0 " winbind"};!/^'$i'/ {print}' %{_sysconfdir}/nsswitch.conf.rpmtemp >%{_sysconfdir}/nsswitch.conf;
	    cp -af %{_sysconfdir}/nsswitch.conf %{_sysconfdir}/nsswitch.conf.rpmtemp
        else
            echo "$i entry found in %{_sysconfdir}/nsswitch.conf"
        fi
    done
    if [ -f %{_sysconfdir}/nsswitch.conf.rpmtemp ];then rm -f %{_sysconfdir}/nsswitch.conf.rpmtemp;fi
fi

%preun winbind
if [ $1 = 0 ]; then
	echo "Removing winbind entries from %{_sysconfdir}/nsswitch.conf"
	perl -pi -e 's/ winbind//' %{_sysconfdir}/nsswitch.conf

	/sbin/chkconfig winbind reset
fi
%endif %build_winbind

%if %build_wins
%post -n nss_wins%{samba_major}
if [ $1 = 1 ]; then
    cp -af %{_sysconfdir}/nsswitch.conf %{_sysconfdir}/nsswitch.conf.rpmsave
    grep '^hosts' %{_sysconfdir}/nsswitch.conf |grep -v 'wins' >/dev/null
    if [ $? = 0 ];then
        echo "Adding a wins entry to the hosts section of %{_sysconfdir}/nsswitch.conf"
        awk '/^hosts/ {print $0 " wins"};!/^hosts/ {print}' %{_sysconfdir}/nsswitch.conf.rpmsave >%{_sysconfdir}/nsswitch.conf;
    else
        echo "wins entry found in %{_sysconfdir}/nsswitch.conf"
    fi
#    else
#        echo "Upgrade, leaving nsswitch.conf intact"
fi

%preun -n nss_wins%{samba_major}
if [ $1 = 0 ]; then
	echo "Removing wins entry from %{_sysconfdir}/nsswitch.conf"
	perl -pi -e 's/ wins//' %{_sysconfdir}/nsswitch.conf
#else
#	echo "Leaving %{_sysconfdir}/nsswitch.conf intact"
fi
%endif %build_wins

%preun server

%_preun_service %{name}
#%_preun_service wrepld%{samba_major}

#if [ $1 = 0 ] ; then
#    /sbin/chkconfig --level 35 smb reset
# Let's not loose /var/cache/samba
#
#    if [ -d /var/cache/%{name} ]; then
#      mv -f /var/cache/%{name} /var/cache/%{name}.BAK
#    fi
#fi

%if %build_swat
%post swat
if [ -f /var/lock/subsys/xinetd ]; then
        service xinetd reload >/dev/null 2>&1 || :
fi
%if %mdkversion < 200900
%update_menus
%endif

%postun swat

# Remove swat entry from xinetd
if [ $1 = 0 -a -f %{_sysconfdir}/xinetd.conf ] ; then
rm -f %{_sysconfdir}/xinetd.d/swat%{samba_major}
	service xinetd reload &>/dev/null || :
fi

if [ "$1" = "0" -a -x /usr/bin/update-menus ]; then /usr/bin/update-menus || true ; fi
%if %mdkversion < 200900
%clean_menus
%endif
%endif

%if %build_system
%if %mdkversion < 200900
%post -n %{libname} -p /sbin/ldconfig
%endif
%if %mdkversion < 200900
%postun -n %{libname} -p /sbin/ldconfig
%endif
%endif

%if %build_alternatives
%post client

update-alternatives --install %{_bindir}/smbclient smbclient \
%{_bindir}/smbclient%{alternative_major} 10 \
$(for i in {/sbin/{%{client_sbin}},%{_bindir}/{%{clientbin}}};do
j=`basename $i`
[ "$j" = "smbclient" ] || \
echo -n " --slave ${i} ${j} ${i}%{alternative_major}";done) \
$(for i in %{_mandir}/{%{client_man}};do
echo -n " --slave ${i}%{_extension} `basename $i` ${i%%.?}%{alternative_major}.${i##*.}%{_extension}";done) \
--slave %{_prefix}/lib/cups/backend/smb cups_smb %{_prefix}/lib/cups/backend/smb%{alternative_major} || \
update-alternatives --auto smbclient

%preun client
[ $1 = 0 ] && update-alternatives --remove smbclient %{_bindir}/smbclient%{alternative_major} ||:
%endif

%if %build_alternatives
%triggerpostun client -- samba-client, samba2-client
[ ! -e %{_bindir}/smbclient ] && update-alternatives --auto smbclient || :
%endif

%if %build_alternatives
%post -n mount-cifs%{samba_major}
update-alternatives --install /bin/mount.cifs mount.cifs \
/bin/mount.cifs%{alternative_major} 10 \
--slave /sbin/mount.cifs smount.cifs /sbin/mount.cifs%{alternative_major} \
--slave /bin/umount.cifs umount.cifs /bin/umount.cifs%{alternative_major} \
--slave /sbin/umount.cifs sumount.cifs /sbin/umount.cifs%{alternative_major} \
--slave /sbin/cifs.upcall cifs.upcall /sbin/cifs.upcall%{alternative_major} \
--slave %{_mandir}/man8/mount.cifs.8%{_extension} mount.cifs.8 %{_mandir}/man8/mount.cifs%{alternative_major}.8%{_extension} \
--slave %{_mandir}/man8/umount.cifs.8%{_extension} umount.cifs.8 %{_mandir}/man8/umount.cifs%{alternative_major}.8%{_extension} \
--slave %{_mandir}/man8/cifs.upcall.8%{_extension} cifs.upcall.8 %{_mandir}/man8/cifs.upcall%{alternative_major}.8%{_extension} \
|| update-alternatives --auto mount.cifs

%preun -n mount-cifs%{samba_major}
[ $1 = 0 ] && update-alternatives --remove mount.cifs /bin/mount.cifs%{alternative_major} ||:

%triggerpostun -n mount-cifs%{samba_major} -- %{name}-client < 3.0.11-1mdk
update-alternatives --auto mount.cifs

%endif


%files server
%defattr(-,root,root)
%(for i in %{_sbindir}/{%{serversbin}}%{samba_major};do echo $i;done)
%(for i in %{_bindir}/%{serverbin}%{samba_major};do echo $i;done)
#attr(755,root,root) /%{_lib}/security/pam_smbpass*
#dir %{_libdir}/%{name}/vfs
#{_libdir}/%{name}/vfs/*.so
%if %build_vscan
%exclude %{_libdir}/%{name}/vfs/vscan*.so
%endif
#{_libdir}/samba/fi.msg
#dir %{_libdir}/%{name}/pdb
%{_libdir}/%{name}/ldb
#{_libdir}/%{name}/auth
#{_libdir}/%{name}/*.so
#dir %{_libdir}/%{name}/nss_info
#{_libdir}/%{name}/nss_info/rfc2307.so
#{_libdir}/%{name}/nss_info/sfu*.so

#attr(-,root,root) %config(noreplace) %{_sysconfdir}/%{name}/smbusers
%attr(-,root,root) %config(noreplace) %{_initrddir}/%{name}
#%attr(-,root,root) %config(noreplace) %{_initrddir}/wrepld%{samba_major}
%attr(-,root,root) %config(noreplace) %{_sysconfdir}/logrotate.d/%{name}
%attr(-,root,root) %config(noreplace) %{_sysconfdir}/pam.d/%{name}
#%attr(-,root,root) %config(noreplace) %{_sysconfdir}/%{name}/samba-slapd.include
%(for i in %{_mandir}/man?/{%{serverbin}%{samba_major},ad2oLschema}\.[0-9]*;do echo $i;done)
%attr(775,root,adm) %dir %{_localstatedir}/lib/%{name}/netlogon
%attr(755,root,root) %dir %{_localstatedir}/lib/%{name}/profiles
%attr(755,root,root) %dir %{_localstatedir}/lib/%{name}/printers
%attr(2775,root,adm) %dir %{_localstatedir}/lib/%{name}/printers/*
%attr(1777,root,root) %dir /var/spool/%{name}
%dir %{_datadir}/%{name}
%dir %{_datadir}/%{name}/scripts
%{_datadir}/%{name}/setup
%attr(0755,root,root) %{_datadir}/%{name}/scripts/print-pdf
#attr(0755,root,root) %{_datadir}/%{name}/scripts/convertSambaAccount
#{_mandir}/man8/idmap_*.8*
#{_mandir}/man8/vfs_*.8*

%if %build_doc
%files doc
%defattr(-,root,root)
%doc README COPYING Manifest Read-Manifest-Now
%doc WHATSNEW.txt Roadmap
%doc README.%{name}-mandrake-rpm
%doc clean-docs/samba-doc/docs/*
%doc clean-docs/samba-doc/examples
#%attr(-,root,root) %{_datadir}/swat%{samba_major}/using_samba/
%attr(-,root,root) %{_datadir}/swat%{samba_major}/help/
%endif

%if %build_swat
%files swat
%defattr(-,root,root)
%config(noreplace) %{_sysconfdir}/xinetd.d/swat%{samba_major}
#%attr(-,root,root) /sbin/*
%{_sbindir}/swat%{samba_major}
%{_datadir}/applications/mandriva-%{name}-swat.desktop
%{_miconsdir}/*.png
%{_liconsdir}/*.png
%{_iconsdir}/*.png
#%attr(-,root,root) %{_datadir}/swat%{samba_major}/help/
%attr(-,root,root) %{_datadir}/swat%{samba_major}/images/
%attr(-,root,root) %{_datadir}/swat%{samba_major}/include/
%lang(ja) %{_datadir}/swat%{samba_major}/lang/ja
%lang(tr) %{_datadir}/swat%{samba_major}/lang/tr
%{_mandir}/man8/swat*.8*
%lang(de) %{_libdir}/%{name}/de.msg
%lang(en) %{_libdir}/%{name}/en.msg
%lang(fr) %{_libdir}/%{name}/fr.msg
%lang(it) %{_libdir}/%{name}/it.msg
%lang(ja) %{_libdir}/%{name}/ja.msg
%lang(nl) %{_libdir}/%{name}/nl.msg
%lang(pl) %{_libdir}/%{name}/pl.msg
%lang(tr) %{_libdir}/%{name}/tr.msg
#%doc swat/README
%endif

%files client
%defattr(-,root,root)
%(for i in %{_bindir}/{%{clientbin}}%{alternative_major};do echo $i;done)
#(for i in %{_mandir}/man?/{%{clientbin}}%{alternative_major}.?.*;do echo $i|grep -v smbprint;done)
#xclude %{_mandir}/man?/smbget*
#{_mandir}/man5/smbgetrc%{alternative_major}.5*
%ifnarch alpha
#(for i in /sbin/{%{client_sbin}}%{alternative_major};do echo $i|grep -v "smb.*m.*nt";done)
%else
%exclude %{_bindir}/smb*m*nt%{samba_major}
%exclude %{_mandir}/man8/smb*m*nt*.8*
%endif
#{_mandir}/man8/eventlogadm3.8*
# Link of smbspool to CUPS
%if %build_cupspc
%{_prefix}/lib*/cups/backend/smb%{alternative_major}
%endif

%files common
%defattr(-,root,root)
%dir /var/cache/%{name}
%dir /var/log/%{name}
%dir /var/run/%{name}
%(for i in %{_bindir}/{%{commonbin}}%{samba_major};do echo $i;done)
#(for i in %{_mandir}/man?/{%{commonbin}}%{samba_major}\.[0-9]*;do echo $i;done)
#%{_libdir}/smbwrapper%{samba_major}.so
#dir %{_libdir}/%{name}
%dir %{_datadir}/%{name}
%{_datadir}/%{name}/*.dat
#{_libdir}/%{name}/charset
#%{_libdir}/%{name}/lowcase.dat
#%{_libdir}/%{name}/valid.dat
%dir %{_sysconfdir}/%{name}
#attr(-,root,root) %config(noreplace) %{_sysconfdir}/%{name}/smb.conf
#attr(-,root,root) %config(noreplace) %{_sysconfdir}/%{name}/smb-winbind.conf
%attr(-,root,root) %config(noreplace) %{_sysconfdir}/%{name}/lmhosts
%dir %{_localstatedir}/lib/%{name}
%attr(-,root,root) %{_localstatedir}/lib/%{name}/codepages
#{_mandir}/man5/smb.conf*.5*
#{_mandir}/man5/lmhosts*.5*
#{_mandir}/man8/tdbtool.8*
#%{_mandir}/man7/Samba*.7*
#dir %{_datadir}/swat%{samba_major}
#attr(0750,root,adm) %{_datadir}/%{name}/scripts/smb-migrate
#attr(-,root,root) %{_datadir}/%{name}/smb.conf.clean
%attr(-,root,root) %{_datadir}/%{name}/README.mdk.conf

%if %build_winbind
%files winbind -f pam_winbind.lang
%defattr(-,root,root)
%config(noreplace) %{_sysconfdir}/security/pam_winbind.conf
%{_sbindir}/winbindd
%{_sbindir}/winbind
%{_bindir}/wbinfo
%attr(755,root,root) /%{_lib}/security/pam_winbind*
%attr(755,root,root) /%{_lib}/libnss_winbind*
%{_libdir}/%{name}/idmap
%{_libdir}/krb5/plugins/winbind_krb5_locator.so
%attr(-,root,root) %config(noreplace) %{_initrddir}/winbind
%attr(-,root,root) %config(noreplace) %{_sysconfdir}/pam.d/system-auth-winbind*
%{_mandir}/man8/winbindd*.8*
%{_mandir}/man7/pam_winbind.7*
%{_mandir}/man7/winbind_krb5_locator.7.*
%{_mandir}/man1/wbinfo*.1*
%endif

%if %build_wins
%files -n nss_wins%{samba_major}
%defattr(-,root,root)
%attr(755,root,root) /%{_lib}/libnss_wins.so*
%endif

%files python
%defattr(-,root,root)
%{python_sitearch}/*.so
%{python_sitearch}/samba

%if %{build_test}
%files test
%defattr(-,root,root)
%(for i in %{_bindir}/{%{testbin}}%{samba_major};do echo $i;done)
#{_mandir}/man1/vfstest%{samba_major}*.1*
#exclude %{_mandir}/man1/log2pcap*.1*
%else
#exclude %{_mandir}/man1/vfstest%{samba_major}*.1*
#exclude %{_mandir}/man1/log2pcap*.1*
%endif

%if %build_system
%files -n %{libname}
%defattr(-,root,root)
%{_libdir}/libsmbclient.so.%{libsmbmajor}
#else
exclude %{_libdir}/libsmbclient.so.*
%endif

%if %build_system
%files -n %{libname}-devel
%defattr(-,root,root)
%{_includedir}/libsmbclient.h
%exclude %{_includedir}/tdb.h
%{_libdir}/libsmbclient.so
%doc clean-docs/libsmbclient/*
%{_mandir}/man7/libsmbclient.7*
%{_libdir}/pkgconfig/smbclient.pc
#else
%exclude %{_includedir}/*
%exclude %{_libdir}/libsmbclient.so
%exclude %{_mandir}/man8/libsmbclient.8*
%exclude %{_libdir}/pkgconfig/smbclient.pc
%endif

%if %build_system
%files -n %{libname}-static-devel
%defattr(-,root,root)
%{_libdir}/lib*.a
#else
%exclude %{_libdir}/lib*.a
%endif

%if 0
%files libs
%defattr(-,root,root)
%else
%{_libdir}/libtorture.so.*
%endif

%files devel
%defattr(-,root,root)
%{_includedir}/samba-4.0/charset.h
%dir %{_includedir}/samba-4.0/core
%{_includedir}/samba-4.0/core/*.h
%{_includedir}/samba-4.0/credentials.h
%{_includedir}/samba-4.0/dlinklist.h
%{_includedir}/samba-4.0/domain_credentials.h
%dir %{_includedir}/samba-4.0/gen_ndr
%{_includedir}/samba-4.0/gen_ndr/*.h
%{_includedir}/samba-4.0/ldap*.h
%{_includedir}/samba-4.0/ldb*.h
%{_includedir}/samba-4.0/ndr.h
%{_includedir}/samba-4.0/param.h
%{_includedir}/samba-4.0/samba/
%{_includedir}/samba-4.0/share.h
%{_includedir}/samba-4.0/smbtorture.h
%{_includedir}/samba-4.0/tdb_wrap.h
%{_includedir}/samba-4.0/tdr.h
%{_includedir}/samba-4.0/tsocket.h
%{_includedir}/samba-4.0/tsocket_internal.h
%{_includedir}/samba-4.0/torture.h
%{_includedir}/samba-4.0/util.h
%dir %{_includedir}/samba-4.0/util/
%{_includedir}/samba-4.0/util/*.h
%{_includedir}/samba-4.0/util_ldb.h
%{_libdir}/pkgconfig/torture.pc
%{_libdir}/libtorture.so

%files pidl
%defattr(-,root,root)
%{_bindir}/pidl
%{perl_vendorlib}/Parse/Pidl*
%{perl_vendorlib}/Parse/Yapp/*.pm
%{_mandir}/man1/pidl.1.*
%{_mandir}/man3/Parse::Pidl*.3pm.*

%if 0
%files -n %libnetapi
%defattr(-,root,root)
%{_libdir}/libnetapi.so.%{netapimajor}*

%files -n %netapidevel
%defattr(-,root,root)
%{_libdir}/libnetapi*.so
%{_includedir}/netapi.h
%{_libdir}/pkgconfig/netapi.pc

%files -n %libsmbsharemodes
%defattr(-,root,root)
%{_libdir}/libsmbsharemodes.so.%{smbsharemodesmajor}*

%files -n %smbsharemodesdevel
%defattr(-,root,root)
%{_libdir}/libsmbsharemodes.so
%{_includedir}/smb_share_modes.h
%{_libdir}/pkgconfig/smbsharemodes.pc
%endif

%if %build_talloc
%files -n %libtalloc
%defattr(-,root,root)
%{_libdir}/libtalloc.so.%{tallocmajor}*

%files -n %tallocdevel
%defattr(-,root,root)
%{_libdir}/libtalloc.so
%{_libdir}/libtalloc.a
%{_includedir}/talloc.h
%{_libdir}/pkgconfig/talloc.pc
%{_mandir}/man3/talloc*
%{_datadir}/swig/*/talloc.i
%endif

%if %build_tdb
%files -n %libtdb
%defattr(-,root,root)
%{_libdir}/libtdb.so.%{tdbmajor}*

%files -n %tdbdevel
%defattr(-,root,root)
%{_libdir}/libtdb.so
%{_libdir}/libtdb.a
%{_includedir}/tdb.h
%{_libdir}/pkgconfig/tdb.pc

%files -n tdb-utils
%defattr(-,root,root)
%{_bindir}/tdb*
%endif

%files -n %libldb
%defattr(-,root,root)
%{_libdir}/libldb.so.%{ldbmajor}*

%files -n %ldbdevel
%defattr(-,root,root)
%{_libdir}/libldb.so
%{_libdir}/libldb.a
%{_includedir}/ldb*.h
%{_libdir}/pkgconfig/ldb.pc
%{_mandir}/man3/ldb*

%files -n ldb-utils
%defattr(-,root,root)
%{_bindir}/ldb*
%{_mandir}/man1/ldb*


%if %build_tevent
%files -n %libtevent
%defattr(-,root,root)
%{_libdir}/libtevent.so.%{teventmajor}*

%files -n %teventdevel
%defattr(-,root,root)
%{_libdir}/libtevent.so
%{_libdir}/libtevent.a
%{_includedir}/tevent.h
%{_includedir}/tevent_internal.h
%{_libdir}/pkgconfig/tevent.pc
%endif

%files -n %libdcerpc
%defattr(-,root,root)
%{_libdir}/libdcerpc.so.*
%{_libdir}/libdcerpc_samr.so.*
%{_libdir}/libdcerpc_atsvc.so.*

%files -n %dcerpcdevel
%defattr(-,root,root)
%{_libdir}/pkgconfig/dcerpc*.pc
%{_includedir}/samba-4.0/dcerpc*.h
%dir %{_includedir}/samba-4.0/dcerpc_server
%{_includedir}/samba-4.0/dcerpc_server/*.h
%{_libdir}/libdcerpc.so
%{_libdir}/libdcerpc_samr.so
%{_libdir}/libdcerpc_atsvc.so

%files -n %libndr
%defattr(-,root,root)
%{_libdir}/libndr*.so.*

%files -n %ndrdevel
%defattr(-,root,root)
%{_libdir}/pkgconfig/ndr*.pc
%{_libdir}/libndr*.so

%files -n %libsambautil
%defattr(-,root,root)
%{_libdir}/libsamba-util.so.*

%files -n %sambautildevel
%defattr(-,root,root)
%{_libdir}/libsamba-util.so

%files -n %libregistry
%defattr(-,root,root)
%{_libdir}/libregistry.so.*
%{_libdir}/pkgconfig/registry.pc

%files -n %registrydevel
%defattr(-,root,root)
%{_includedir}/samba-4.0/registry.h
%{_libdir}/libregistry.so

%files -n %libgensec
%defattr(-,root,root)
%{_libdir}/libgensec.so.*
%{_libdir}/pkgconfig/gensec.pc

%files -n %gensecdevel
%defattr(-,root,root)
%{_includedir}/samba-4.0/gensec.h
%{_libdir}/libgensec.so

%files -n %libsambahostconfig
%defattr(-,root,root)
%{_libdir}/libsamba-hostconfig.so.*

%files -n %sambahostconfigdevel
%defattr(-,root,root)
%{_libdir}/libsamba-hostconfig.so
%{_libdir}/pkgconfig/samba-hostconfig.pc

%if 0
%files -n %libwbclient
%defattr(-,root,root)
%{_libdir}/libwbclient.so.%{wbclientmajor}

%files -n %wbclientdevel
%defattr(-,root,root)
%{_libdir}/libwbclient.so
%{_includedir}/wbclient.h
%{_libdir}/pkgconfig/wbclient.pc
%endif

#%files passdb-ldap
#%defattr(-,root,root)
#%{_libdir}/%{name}/*/*ldap.so

%ifnarch alpha
%if %{build_mysql}
%files passdb-mysql
%defattr(-,root,root)
%{_libdir}/%{name}/pdb/*mysql.so
%endif
%endif

%if %{build_pgsql}
%files passdb-pgsql
%defattr(-,root,root)
%{_libdir}/%{name}/pdb/*pgsql.so
%endif

#Files for antivirus support:
%if %build_antivir
%files vscan-antivir
%defattr(-,root,root)
%{_libdir}/%{name}/vfs/vscan-antivir.so
%config(noreplace) %{_sysconfdir}/%{name}/vscan-antivir.conf
%doc %{vfsdir}/%{vscandir}/INSTALL
%endif
%if !%build_antivir && %build_vscan
%exclude %{_libdir}/%{name}/vfs/vscan-antivir.so
%exclude %{_sysconfdir}/%{name}/vscan-antivir.conf
%endif

%if %build_clamav
%files vscan-clamav
%defattr(-,root,root)
%{_libdir}/%{name}/vfs/vscan-clamav.so
%config(noreplace) %{_sysconfdir}/%{name}/vscan-clamav.conf
%doc %{vfsdir}/%{vscandir}/INSTALL
%endif
%if !%build_clamav && %build_vscan
%exclude %{_libdir}/%{name}/vfs/vscan-clamav.so
%exclude %{_sysconfdir}/%{name}/vscan-clamav.conf
%endif

%if %build_fprot
%files vscan-fprot
%defattr(-,root,root)
%{_libdir}/%{name}/vfs/vscan-fprotd.so
%config(noreplace) %{_sysconfdir}/%{name}/vscan-fprotd.conf
%doc %{vfsdir}/%{vscandir}/INSTALL
%endif
%if !%build_fprot && %build_vscan
%exclude %{_libdir}/%{name}/vfs/vscan-fprotd.so
%exclude %{_sysconfdir}/%{name}/vscan-fprotd.conf
%endif

%if %build_fsav
%files vscan-fsecure
%defattr(-,root,root)
%{_libdir}/%{name}/vfs/vscan-fsav.so
%config(noreplace) %{_sysconfdir}/%{name}/vscan-fsav.conf
%doc %{vfsdir}/%{vscandir}/INSTALL
%endif
%if !%build_fsav && %build_vscan
%exclude %{_libdir}/%{name}/vfs/vscan-fsav.so
%exclude %{_sysconfdir}/%{name}/vscan-fsav.conf
%endif

%if %build_icap
%files vscan-icap
%defattr(-,root,root)
%{_libdir}/%{name}/vfs/vscan-icap.so
%config(noreplace) %{_sysconfdir}/%{name}/vscan-icap.conf
%doc %{vfsdir}/%{vscandir}/INSTALL
%endif
%if !%build_icap && %build_vscan
%exclude %{_libdir}/%{name}/vfs/vscan-icap.so
%exclude %{_sysconfdir}/%{name}/vscan-icap.conf
%endif


%if %build_kaspersky
%files vscan-kaspersky
%defattr(-,root,root)
%{_libdir}/%{name}/vfs/vscan-kavp.so
%config(noreplace) %{_sysconfdir}/%{name}/vscan-kavp.conf
%doc %{vfsdir}/%{vscandir}/INSTALL
%endif
%if !%build_kaspersky && %build_vscan
%exclude %{_libdir}/%{name}/vfs/vscan-kavp.so
%exclude %{_sysconfdir}/%{name}/vscan-kavp.conf
%endif

%if %build_mks
%files vscan-mks
%defattr(-,root,root)
%{_libdir}/%{name}/vfs/vscan-mksd.so
%config(noreplace) %{_sysconfdir}/%{name}/vscan-mks*.conf
%doc %{vfsdir}/%{vscandir}/INSTALL
%endif
%if !%build_mks && %build_vscan
%exclude %{_libdir}/%{name}/vfs/vscan-mksd.so
%exclude %{_sysconfdir}/%{name}/vscan-mks*.conf
%endif

%if %build_nai
%files vscan-nai
%defattr(-,root,root)
%{_libdir}/%{name}/vfs/vscan-mcdaemon.so
%config(noreplace) %{_sysconfdir}/%{name}/vscan-mcdaemon.conf
%doc %{vfsdir}/%{vscandir}/INSTALL
%endif
%if !%build_nai && %build_vscan
%exclude %{_libdir}/%{name}/vfs/vscan-mcdaemon.so
%exclude %{_sysconfdir}/%{name}/vscan-mcdaemon.conf
%endif

%if %build_openav
%files vscan-openav
%defattr(-,root,root)
%{_libdir}/%{name}/vfs/vscan-oav.so
%config(noreplace) %{_sysconfdir}/%{name}/vscan-oav.conf
%doc %{vfsdir}/%{vscandir}/INSTALL
%endif
%if !%build_openav && %build_vscan
%exclude %{_libdir}/%{name}/vfs/vscan-oav.so
%exclude %{_sysconfdir}/%{name}/vscan-oav.conf
%endif

%if %build_sophos
%files vscan-sophos
%defattr(-,root,root)
%{_libdir}/%{name}/vfs/vscan-sophos.so
%config(noreplace) %{_sysconfdir}/%{name}/vscan-sophos.conf
%doc %{vfsdir}/%{vscandir}/INSTALL
%endif
%if !%build_sophos && %build_vscan
%exclude %{_libdir}/%{name}/vfs/vscan-sophos.so
%exclude %{_sysconfdir}/%{name}/vscan-sophos.conf
%endif

%if %build_symantec
%files vscan-symantec
%defattr(-,root,root)
%{_libdir}/%{name}/vfs/vscan-symantec.so
%config(noreplace) %{_sysconfdir}/%{name}/vscan-symantec.conf
%doc %{vfsdir}/%{vscandir}/INSTALL
%endif
%if !%build_symantec && %build_vscan
%exclude %{_sysconfdir}/%{name}/vscan-symantec.conf
%endif

%if %build_trend
%files vscan-trend
%defattr(-,root,root)
%{_libdir}/%{name}/vfs/vscan-trend.so
%config(noreplace) %{_sysconfdir}/%{name}/vscan-trend.conf
%doc %{vfsdir}/%{vscandir}/INSTALL
%endif
%if !%build_trend && %build_vscan
%exclude %{_libdir}/%{name}/vfs/vscan-trend.so
%exclude %{_sysconfdir}/%{name}/vscan-trend.conf
%endif

%if %build_cifs
%files -n mount-cifs%{samba_major}
%defattr(-,root,root)
%attr(4755,root,root) /*bin/*mount.cifs%{alternative_major}
#/*bin/cifs.upcall%{alternative_major}
#{_mandir}/man8/*mount.cifs*.8*
#{_mandir}/man8/cifs.upcall*.8*
%endif

#%exclude %{_mandir}/man1/smbsh*.1*
#%exclude %{_mandir}/man1/editreg*

# todo:
# fix alternatives for mount.cifs





