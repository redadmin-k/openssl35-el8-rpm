%global debug_package %{nil}
%global openssl35_prefix /opt/openssl35

%global __provides_exclude_from ^%{openssl35_prefix}/.*\\.so.*$
%global __requires_exclude ^lib(ssl|crypto)\\.so\\.3.*$

Name: openssl35
Version: 3.5.6
Release: 1%{?dist}
Summary: Private OpenSSL 3.5.6 LTS build for applications

License: Apache-2.0
URL: https://www.openssl.org/
Source0: openssl-%{version}.tar.gz

BuildRequires: gcc
BuildRequires: make
BuildRequires: perl-core
BuildRequires: zlib-devel

Provides: openssl35-libs = %{version}-%{release}
Provides: openssl35-devel = %{version}-%{release}

%description
Private OpenSSL 3.5.6 LTS build for applications.

This package installs OpenSSL 3.5.6 under /opt/openssl35.
It does not replace the system OpenSSL libraries provided by AlmaLinux.

%prep
%setup -q -n openssl-%{version}

%build
./Configure linux-x86_64 shared zlib \
  --prefix=%{openssl35_prefix} \
  --openssldir=%{openssl35_prefix}/ssl \
  --libdir=lib64 \
  -fPIC \
  -Wl,-rpath,%{openssl35_prefix}/lib64

make %{?_smp_mflags}

%install
rm -rf %{buildroot}
make install_sw DESTDIR=%{buildroot}

%files
%{openssl35_prefix}

%changelog
* Sat Jun 06 2026 Akiyoshi Kurita <weibu@redadmin.org> - 3.5.6-1
- Initial private OpenSSL 3.5.6 LTS build for EL8
