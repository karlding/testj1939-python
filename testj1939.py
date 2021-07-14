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

    parser.parse_args()
