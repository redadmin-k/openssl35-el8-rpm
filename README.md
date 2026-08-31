# openssl35-el8-rpm

Unofficial OpenSSL 3.5.x LTS RPM package for AlmaLinux 8.

This package installs OpenSSL 3.5.x under:

```text
/opt/openssl35
```

It is designed to coexist with the system OpenSSL provided by AlmaLinux 8 and does not replace or overwrite the system OpenSSL installation.

## Disclaimer

This is an unofficial, personal RPM packaging project.

This package is not provided, endorsed, reviewed, or supported by the AlmaLinux OS Foundation or the AlmaLinux project.

Use at your own risk.

## Purpose

This package is intended for:

* post-quantum cryptography testing
* application-specific OpenSSL testing
* TLS compatibility testing
* software development and evaluation
* testing applications against OpenSSL 3.5.x on EL8

It is not intended to replace the system OpenSSL packages.

## Installation layout

OpenSSL 3.5.x is installed under:

```text
/opt/openssl35
```

Important paths include:

```text
/opt/openssl35/bin/openssl
/opt/openssl35/include
/opt/openssl35/lib64/libssl.so.3
/opt/openssl35/lib64/libcrypto.so.3
/opt/openssl35/lib64/pkgconfig
```

The RPM also installs:

```text
/etc/ld.so.conf.d/openssl35.conf
```

containing:

```text
/opt/openssl35/lib64
```

The dynamic linker cache is updated automatically during RPM installation and removal.

## Coexistence with AlmaLinux 8 OpenSSL

AlmaLinux 8 normally provides OpenSSL 1.1.1 libraries such as:

```text
/lib64/libssl.so.1.1
/lib64/libcrypto.so.1.1
```

This package provides OpenSSL 3.5 libraries under:

```text
/opt/openssl35/lib64/libssl.so.3
/opt/openssl35/lib64/libcrypto.so.3
```

Because the libraries use different SONAMEs, OpenSSL 1.1.1 and OpenSSL 3.5 can coexist on the same system.

Example:

```bash
ldconfig -p | grep -E 'libssl|libcrypto'
```

Expected entries include both:

```text
libssl.so.3 => /opt/openssl35/lib64/libssl.so.3
libssl.so.1.1 => /lib64/libssl.so.1.1

libcrypto.so.3 => /opt/openssl35/lib64/libcrypto.so.3
libcrypto.so.1.1 => /lib64/libcrypto.so.1.1
```

## Install

```bash
sudo dnf install ./openssl35-3.5.*.el8.x86_64.rpm
```

Verify the installation:

```bash
/opt/openssl35/bin/openssl version -a
```

Check runtime libraries:

```bash
ldd /opt/openssl35/bin/openssl
```

Expected OpenSSL libraries:

```text
libssl.so.3 => /opt/openssl35/lib64/libssl.so.3
libcrypto.so.3 => /opt/openssl35/lib64/libcrypto.so.3
```

The runtime search path can also be inspected with:

```bash
readelf -d /opt/openssl35/bin/openssl | grep -E 'RPATH|RUNPATH'
```

## Build integration

Installing this RPM does not automatically make applications build against OpenSSL 3.5.

Applications should explicitly use `/opt/openssl35` when they are compiled.

A common build environment is:

```bash
export CPPFLAGS="-I/opt/openssl35/include"
export LDFLAGS="-L/opt/openssl35/lib64 -Wl,-rpath,/opt/openssl35/lib64"
export PKG_CONFIG_PATH="/opt/openssl35/lib64/pkgconfig"
```

This is especially important because both the system OpenSSL development libraries and OpenSSL 3.5 may exist on the same machine.

## Nginx example

Example configuration for dynamically linking Nginx against OpenSSL 3.5:

```bash
./configure \
  --with-http_ssl_module \
  --with-cc-opt="-I/opt/openssl35/include" \
  --with-ld-opt="-L/opt/openssl35/lib64 -Wl,-rpath,/opt/openssl35/lib64"

make
make install
```

Verify:

```bash
ldd /path/to/nginx | grep -E 'ssl|crypto'
```

Expected libraries:

```text
/opt/openssl35/lib64/libssl.so.3
/opt/openssl35/lib64/libcrypto.so.3
```

## Apache httpd / mod_ssl example

```bash
./configure \
  --enable-ssl \
  --with-ssl=/opt/openssl35

make
make install
```

Verify the resulting module:

```bash
ldd /path/to/mod_ssl.so | grep -E 'ssl|crypto'
```

## Erlang/OTP / BEAM example

Configure Erlang/OTP with:

```bash
./configure --with-ssl=/opt/openssl35

make
make install
```

Verify the crypto NIF:

```bash
ldd /path/to/erlang/lib/crypto-*/priv/lib/crypto.so | grep -E 'ssl|crypto'
```

OpenSSL information can also be checked from Erlang:

```bash
erl -noshell \
  -eval 'io:format("~p~n", [crypto:info_lib()]), halt().'
```

## STARTTLS testing

For STARTTLS testing, rebuild or configure the component that actually terminates the TLS connection.

Examples:

* Erlang/BEAM application handles STARTTLS
  → build Erlang/OTP against `/opt/openssl35`

* Postfix handles SMTP STARTTLS
  → build Postfix against `/opt/openssl35`

* Dovecot handles IMAP/POP3 STARTTLS
  → build Dovecot against `/opt/openssl35`

* Nginx terminates HTTPS/TLS
  → build Nginx against `/opt/openssl35`

* Apache httpd/mod_ssl terminates HTTPS/TLS
  → build Apache/mod_ssl against `/opt/openssl35`

Rebuilding Nginx or Apache does not affect STARTTLS handled by a different application.

## RPM dependency model

This package is intentionally isolated from the system OpenSSL RPM dependency namespace.

Libraries under `/opt/openssl35` are not exported as generic RPM Provides such as:

```text
libssl.so.3()(64bit)
libcrypto.so.3()(64bit)
```

This prevents the private OpenSSL installation from accidentally satisfying dependencies intended for the operating system OpenSSL packages.

The RPM instead provides private package capabilities:

```text
openssl35-libs
openssl35-devel
```

Applications packaged specifically for this OpenSSL build may use:

```spec
BuildRequires: openssl35-devel
Requires: openssl35-libs
```

and should explicitly build against:

```text
/opt/openssl35
```

## Verification

To verify that both OpenSSL versions coexist:

```bash
ldconfig -p | grep -E 'libssl|libcrypto'
```

To verify the private OpenSSL executable:

```bash
ldd /opt/openssl35/bin/openssl
```

To verify an application built against OpenSSL 3.5:

```bash
ldd /path/to/application | grep -E 'ssl|crypto'
```

The expected OpenSSL 3.5 paths are:

```text
/opt/openssl35/lib64/libssl.so.3
/opt/openssl35/lib64/libcrypto.so.3
```

## License

OpenSSL is licensed under the Apache License 2.0.

This RPM packaging project follows the same license unless otherwise noted.

See the upstream OpenSSL project for the OpenSSL license and copyright information.

