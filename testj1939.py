import argparse
import socket

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

    args = parser.parse_args()

    # TODO: Port over interface parsing
    # For now, assume the interface is called 'vcan0'
    sockname = "vcan0", socket.J1939_NO_NAME, socket.J1939_NO_PGN, 0x80

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

        # main loop
        while args.todo_echo or args.todo_recv:
            dat, peername = s.recvfrom(128)

            if args.todo_recv:
                ifname, name, pgn, addr = peername
                print(f"{addr:02x} {pgn:05x}:", end="")

                for i in range(len(dat)):
                    if i != 0 and i % 8 == 0:
                        print(f"\n{i:05X} ", end="")
                    print(f" {dat[i]:02X}", end="")
                print("")
