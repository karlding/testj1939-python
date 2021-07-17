from typing import Tuple

import argparse
import signal
import socket
import sys

# TODO: Should this be exposed in the stdlib as part of J1939 support?
try:
    socket.SOL_CAN_J1939
except AttributeError:
    socket.SOL_CAN_J1939 = socket.SOL_CAN_BASE + socket.CAN_J1939


def onsigalrm(signum, frame):
    sys.exit()


def parse_j1939_canaddr(string: str) -> Tuple[str, int, int, int]:
    """Parses a canaddr string into a (ifname, name, pgn, addr) tuple

    This should be equivalent to libj1939_parse_canaddr
    """
    index = string.find(":")
    if index != -1:
        ifname = string[0:index]
        string = string[index + 1 :]
    else:
        ifname = string
        string = ""
    can_ifindex = socket.if_nametoindex(ifname)

    index = string.find(",")
    if index != -1:
        if len(string[0:index]) == 0:
            # This is the default value of the 'addr' member when the
            # struct sockaddr_can is initialized
            addr = socket.J1939_NO_ADDR
        else:
            addr = int(string[0:index], 0)
        string = string[index + 1 :]
    elif len(string) != 0:
        addr = int(string, 0)
        string = ""
    else:
        # This is the default value of the 'addr' member when the
        # struct sockaddr_can is initialized
        addr = socket.J1939_NO_ADDR

    index = string.find(",")
    if index != -1:
        if len(string[0:index]) == 0:
            # This is the default value of the 'pgn' member when the
            # struct sockaddr_can is initialized
            pgn = socket.J1939_NO_PGN
        else:
            pgn = int(string[0:index], 0)
        string = string[index + 1 :]
    elif len(string) != 0:
        pgn = int(string, 0)
        string = ""
    else:
        # This is the default value of the 'pgn' member when the
        # struct sockaddr_can is initialized
        pgn = socket.J1939_NO_PGN

    index = string.find(",")
    if index != -1:
        if len(string[0:index]) == 0:
            # This is the default value of the 'name' member when the
            # struct sockaddr_can is initialized
            name = socket.J1939_NO_NAME
        else:
            name = int(string[0:index], 0)
    else:
        # This is the default value of the 'name' member when the
        # struct sockaddr_can is initialized
        name = socket.J1939_NO_NAME

    return (ifname, name, pgn, addr)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="demonstrate j1939 use")
    parser.add_argument(
        "-s",
        type=int,
        dest="todo_send",
        metavar="LEN",
        help="Initial send of LEN bytes dummy data",
    )
    parser.add_argument(
        "-r", action="store_true", dest="todo_recv", help="Receive (and print) data"
    )
    parser.add_argument(
        "-e",
        action="store_true",
        dest="todo_echo",
        help="Echo incoming packets back.\nThis atually receives packets",
    )
    parser.add_argument(
        "-p",
        type=int,
        dest="todo_prio",
        metavar="PRIO",
        default=-1,
        help="Set priority to PRIO",
    )
    parser.add_argument(
        "-P",
        action="store_true",
        dest="todo_promisc",
        help="Promiscuous mode. Allow to receive all packets",
    )
    parser.add_argument(
        "-c", action="store_true", dest="todo_connect", help="Issue connect()"
    )
    parser.add_argument(
        "-n", action="store_true", dest="todo_names", help="Emit 64bit NAMEs in output"
    )
    parser.add_argument(
        "-b",
        action="store_true",
        dest="todo_rebind",
        help="Do normal bind with SA+1 and rebind with actual SA",
    )
    parser.add_argument(
        "-B",
        action="store_true",
        dest="todo_broadcast",
        help="Allow to send and receive broadcast packets.",
    )
    parser.add_argument("-o", action="store_true", dest="no_bind", help="Omit bind")
    parser.add_argument(
        "-w",
        type=int,
        dest="todo_wait",
        metavar="TIME",
        default=1,
        help="Return after TIME (default 1) seconds",
    )

    parser.add_argument("from_addr", metavar="FROM", type=parse_j1939_canaddr)
    parser.add_argument("to_addr", metavar="TO", nargs="?", type=parse_j1939_canaddr)

    args = parser.parse_args()

    if args.todo_wait:
        signal.signal(signal.SIGALRM, onsigalrm)
        signal.alarm(args.todo_wait)

    sockname = args.from_addr
    peername = args.to_addr

    with socket.socket(socket.PF_CAN, socket.SOCK_DGRAM, socket.CAN_J1939) as s:
        if args.todo_promisc:
            s.setsockopt(socket.SOL_CAN_J1939, socket.SO_J1939_PROMISC, 1)

        if args.todo_broadcast:
            s.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)

        if args.todo_prio >= 0:
            s.setsockopt(
                socket.SOL_CAN_J1939, socket.SO_J1939_SEND_PRIO, args.todo_prio
            )

        if not args.no_bind:
            s.bind(sockname)

            # if args.todo_rebind:
            #     # rebind with actual SA

        if args.todo_connect:
            s.connect(peername)

        if args.todo_send:
            # initialize test vector
            # Note: This takes the value mod 256 since the C implementation relies on unsigned integer semantics
            dat = bytearray(
                [(((2 * j) << 4) + ((2 * j + 1) & 0xF)) % 256 for j in range(128)]
            )

            # send data
            # when using connect, do not provide additional
            # destination information and use send()
            if args.to_addr and not args.todo_connect:
                s.sendto(dat[0 : args.todo_send], peername)
            else:
                s.send(dat[0 : args.todo_send], 0)

        # main loop
        while args.todo_echo or args.todo_recv:
            dat, peername = s.recvfrom(128)

            if args.todo_echo:
                s.sendto(dat, peername)

            if args.todo_recv:
                ifname, name, pgn, addr = peername
                print(f"{addr:02x} {pgn:05x}:", end="")

                for i, byte in enumerate(dat):
                    if i != 0 and i % 8 == 0:
                        print(f"\n{i:05x}    ", end="")
                    print(f" {byte:02x}", end="")
                print("")
