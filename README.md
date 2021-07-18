# testj1939-python

A reimplementation of `testj1939` using Python APIs

This is mostly intended to:

1. illustrate how to use the J1939 `socket` APIs
2. serve as a series of integration tests of the J1939 functionality

## Goals

These are various examples taken from the J1939 kickstart guide

- [x] receive without source address
- [x] receive with source address
- [x] send
- [x] Multiple source addresses on 1 CAN device
- [x] Use PDU1 PGN
- [x] Use destination address info
- [x] Emit different PGNs using the same socket
- [x] Larger packets

### Advanced topics with j1939

- [ ] Change priority of J1939 packets

## Known issues

- Integration tests are flakey (likely due to needing to synchronize between background processes)
- The `-s` argument doesn't work the same way as `testj1939`
- Add `pyproject.toml`
- Create wheels
- Package as a CLI script
