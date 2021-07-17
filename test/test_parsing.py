import socket
import unittest

from testj1939 import parse_j1939_canaddr


class TestUtils(unittest.TestCase):
    def test_parse_j1939_canaddr_only_interface(self):
        iface, name, pgn, addr = parse_j1939_canaddr("vcan0")

        self.assertEqual(iface, "vcan0")
        self.assertEqual(name, socket.J1939_NO_NAME)
        self.assertEqual(pgn, socket.J1939_NO_PGN)
        self.assertEqual(addr, socket.J1939_NO_ADDR)

    def test_parse_j1939_canaddr_interface_source_addr(self):
        iface, name, pgn, addr = parse_j1939_canaddr("vcan0:0x80")

        self.assertEqual(iface, "vcan0")
        self.assertEqual(name, socket.J1939_NO_NAME)
        self.assertEqual(pgn, socket.J1939_NO_PGN)
        self.assertEqual(addr, 0x80)

    def test_parse_j1939_canaddr_interface_pgn(self):
        iface, name, pgn, addr = parse_j1939_canaddr("vcan0:,0x3ffff")

        self.assertEqual(iface, "vcan0")
        self.assertEqual(name, socket.J1939_NO_NAME)
        self.assertEqual(pgn, 0x3FFFF)
        self.assertEqual(addr, socket.J1939_NO_ADDR)

    def test_parse_j1939_canaddr_interface_pgn_addr(self):
        iface, name, pgn, addr = parse_j1939_canaddr("vcan0:0x40,0x12300")

        self.assertEqual(iface, "vcan0")
        self.assertEqual(name, socket.J1939_NO_NAME)
        self.assertEqual(pgn, 0x12300)
        self.assertEqual(addr, 0x40)


if __name__ == "__main__":
    unittest.main()
