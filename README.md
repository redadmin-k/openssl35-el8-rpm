# openssl35-el8-rpm

Unofficial private OpenSSL 3.5.x RPM package for AlmaLinux 8.

This package installs OpenSSL 3.5.x under `/opt/openssl35`.
It does not replace the system OpenSSL libraries provided by AlmaLinux.

## Disclaimer

This is an unofficial, personal RPM packaging project for AlmaLinux.

This package is not provided, endorsed, reviewed, or supported by the AlmaLinux OS Foundation or the AlmaLinux project.

Use at your own risk.

## Purpose

This package is intended for:

* post-quantum cryptography testing
* application-specific OpenSSL testing
* compatibility testing
* private OpenSSL evaluation

## License

OpenSSL itself is licensed under the Apache License 2.0.

This RPM packaging project follows the same license unless otherwise noted.

See the upstream OpenSSL license for details.

## Install

```bash
sudo dnf install ./openssl35-3.5.*.el8.x86_64.rpm
```

Verify:

```bash
/opt/openssl35/bin/openssl version -a
ldd /opt/openssl35/bin/openssl | grep -E 'ssl|crypto'
readelf -d /opt/openssl35/bin/openssl | grep -E 'RPATH|RUNPATH'
```

Expected library path:

```text
/opt/openssl35/lib64/libssl.so.3
/opt/openssl35/lib64/libcrypto.so.3
```

## Build integration

Applications must be explicitly built or configured to use `/opt/openssl35`.

Common build environment:

```bash
export CPPFLAGS="-I/opt/openssl35/include"
export LDFLAGS="-L/opt/openssl35/lib64 -Wl,-rpath,/opt/openssl35/lib64"
export PKG_CONFIG_PATH="/opt/openssl35/lib64/pkgconfig"
```

## Nginx example

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

## Apache httpd / mod_ssl example

```bash
./configure \
  --enable-ssl \
  --with-ssl=/opt/openssl35

make
make install
```

Verify:

```bash
ldd /path/to/mod_ssl.so | grep -E 'ssl|crypto'
```

## Erlang/OTP / BEAM example

```bash
./configure --with-ssl=/opt/openssl35

make
make install
```

Verify:

```bash
ldd /path/to/erlang/lib/crypto-*/priv/lib/crypto.so | grep -E 'ssl|crypto'
```

You can also check from Erlang:

```bash
erl -noshell -eval 'io:format("~p~n", [crypto:info_lib()]), halt().'
```

## STARTTLS note

For STARTTLS testing, rebuild the component that actually terminates STARTTLS.

Examples:

* If Erlang/BEAM handles STARTTLS, rebuild Erlang/OTP with `/opt/openssl35`.
* If Postfix handles STARTTLS, rebuild Postfix with `/opt/openssl35`.
* If Dovecot handles STARTTLS, rebuild Dovecot with `/opt/openssl35`.

Nginx and Apache are only relevant when they terminate TLS/HTTPS.

## RPM dependency note

This package is intended to be used explicitly as `openssl35`.

It should not provide generic system library capabilities such as:

```text
libssl.so.3
libcrypto.so.3
```

Applications that use this package should explicitly depend on:

```spec
BuildRequires: openssl35-devel
Requires: openssl35-libs
```

and should be built with `/opt/openssl35` specified.

