# Mono — Linux companion (experimental)

This is an experimental, partial port of the Mac-side companion for Linux.
It is **not** feature-complete and does not yet implement the full encrypted
pairing protocol or the iOS screen-capture flow. Contributions welcome.

## Requirements

- Python 3.10+
- `mss`, `Pillow`, `requests`, `flask`, `zeroconf`

## Install

```sh
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## Run (screen capture probe)

```sh
python capture.py
```

This captures the primary display to `/tmp/mono-capture.png` once.
