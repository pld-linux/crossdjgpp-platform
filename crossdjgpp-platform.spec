Summary:	DJGPP GNU Binary Utility Development Utilities - libraries
Name:		crossdjgpp-platform
Version:	203
Release:	1
Epoch:		1
License:	GPL
Group:		Development/Libraries
Group(de):	Entwicklung/Libraries
Group(fr):	Development/Librairies
Group(pl):	Programowanie/Biblioteki
URL:		http://www.delorie.com/djgpp
Source0:	ftp://ftp.simtel.net/pub/simtelnet/gnu/djgpp/v2/djcrx%{version}.zip
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)
BuildRequires: 	unzip
PreReq:		fix-info-dir

%define		target		i386-pc-msdosdjgpp
%define		arch		%{_prefix}/%{target}

%description
DJGPP is a port of GNU GCC to the DOS environment. (It stands for
DJ's Gnu Programming Platform, if it has to stand for something, but
it's best left ambiguous.)

This package contains DOS API includes and libraries.

%prep
%setup -q -c -T -n djcrx-%{version}
unzip -a %{SOURCE0} > /dev/null

%build
%{__cc} %{rpmcflags} -o stubify src/stub/stubify.c
%{__cc} %{rpmcflags} -o stubedit src/stub/stubedit.c

%install
rm -rf $RPM_BUILD_ROOT

install -d $RPM_BUILD_ROOT{%{_infodir},%{arch}/{include,lib,bin},%{_bindir}}
cp -fa include/* $RPM_BUILD_ROOT%{arch}/include
cp -fa lib/* $RPM_BUILD_ROOT%{arch}/lib
# required by linker... strange
ln -sf ../lib/djgpp.djl $RPM_BUILD_ROOT%{arch}/bin

( cat <<EOF
This is foobarbaz.

INFO-DIR-SECTION Libraries:
START-INFO-DIR-ENTRY
* DJGPP Libc: (djgpp-libc)		Libc for cross-djgpp
END-INFO-DIR-ENTRY
EOF
  cat info/libc.info ) | \
	sed -e 's/libc\.info/djgpp-libc.info/g' \
		> $RPM_BUILD_ROOT%{_infodir}/djgpp-libc.info

install stubify stubedit $RPM_BUILD_ROOT/%{_bindir}

%post
[ ! -x /usr/sbin/fix-info-dir ] || /usr/sbin/fix-info-dir -c %{_infodir} >/dev/null 2>&1

%postun
[ ! -x /usr/sbin/fix-info-dir ] || /usr/sbin/fix-info-dir -c %{_infodir} >/dev/null 2>&1

%files
%defattr(644,root,root,755)
%{arch}
%{_infodir}/*
%attr(755,root,root) %{_bindir}/*

%clean
rm -rf $RPM_BUILD_ROOT
