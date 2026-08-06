# Installer Dev (Docker)

`./install.sh -t` (see [Kconfig & Installer Architecture](Dev-Kconfig-Structure.md#running-installsh-without-touching-your-printer))
already sandboxes *where the installer writes* - but it still runs on your
own machine's Python and OS. `installer-dev/` sandboxes the other half: it
runs the installer inside a container built to look like a genuinely
different target, so environment-specific bugs show up before a user hits
them, not after.

## Why this exists

The two `docker-compose.yaml` targets aren't two flavours of the same thing -
they're chosen to bracket the real range of machines the installer has to
work on:

- **`debian`** - Python 3.11, mimicking Mainsail OS / Raspberry Pi OS - the
  common case.
- **`alpine`** - **Python 2.7**, mimicking the busybox environment on a
  Creality K1. This is the one that actually catches bugs your own dev
  machine cannot: Python-2-vs-3 syntax, `apk` vs `apt` assumptions, and -
  since Alpine containers have no real `systemd` - the two Dockerfiles
  install `service.sh`/`systemctl.sh` stand-ins for `/etc/init.d` and
  `systemctl` so the installer's own service-restart logic has something to
  call instead of failing outright. Nothing in the `test/` harness or a
  plain `-t` run exercises the Python-2.7 code path at all.

Both containers **bind-mount your actual working checkout** in place
(`../:/home/klippy/Happy-Hare` for debian, the equivalent for alpine) -
you edit code on your host with your normal tools, and the container just
runs it; only a genuine OS/dependency change needs a rebuild. `./config`
similarly bind-mounts to the container's `printer_data/config`, so rendered
output lands at `installer-dev/config` on your host afterward, inspectable
or disposable exactly like `/tmp/mmu_test` is for `-t`.

`F_SKIP_UPDATE=y` is set for both services in `docker-compose.yaml` - the
container-equivalent of `-z` (see [Kconfig & Installer Architecture](Dev-Kconfig-Structure.md#running-installsh-without-touching-your-printer)),
since git-self-updating a repo that's bind-mounted from the host makes no
sense.

## Usage

```shell
docker compose run --build --rm <target> '<command>'
```

For example, to run the installer with a Debian base:

```shell
docker compose run --build --rm debian 'make install'
```

Or against the Python-2.7 Alpine target, which is the one worth reaching for
specifically when a change touches anything that could plausibly behave
differently on Python 2 (string/byte handling, `print`, dict ordering
assumptions):

```shell
docker compose run --build --rm alpine 'make install'
```

## Where to go next

- [Kconfig & Installer Architecture](Dev-Kconfig-Structure.md) - what
  `make install` actually does, and the non-Docker `-t` sandbox this
  complements.
- [Testing](Dev-Testing.md) - the non-Docker way to exercise Happy Hare
  without a printer, on your own host Python.

---

<pre class="hh-footer-art">
  (\_/)
  ( *,*)
  (")_(") Happy Hare Ready
</pre>
<p class="hh-footer-copyright">Copyright (C) 2022-2026 Paul Morgan</p>

