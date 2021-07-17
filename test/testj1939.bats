# Maybe it's better to diff against the binaries from can-utils?
# For now just diff output so the only dependency is on cansend/candump
PYTHON_BIN=python3
CAN_IFACE_NAME=vcan0
DELAY_TIME=0.1s
WAIT_TIME=1
WAIT_TIME_MILLIS=2000

setup() {
  load 'libs/test_helper/bats-support/load'
  load 'libs/test_helper/bats-assert/load'
}

@test "receive without source address" {
  sleep ${DELAY_TIME} && cansend ${CAN_IFACE_NAME} 1823ff40#0123 &
  run ${PYTHON_BIN} testj1939.py -w${WAIT_TIME} -B -r ${CAN_IFACE_NAME}

  assert_success
  assert_output "40 02300: 01 23"
}

@test "receive with source address" {
  sleep ${DELAY_TIME} && cansend ${CAN_IFACE_NAME} 18238040#0123 &
  run ${PYTHON_BIN} testj1939.py -w${WAIT_TIME} -r ${CAN_IFACE_NAME}:0x80

  assert_success
  assert_output "40 02300: 01 23"
}

@test "send" {
  # TODO: this should be '-s' instead of '-s8', but that requires some
  # argparse setup to propery parse the positional arguments after.
  #
  # For now, just use '-s8'
  sleep ${DELAY_TIME} && ${PYTHON_BIN} testj1939.py -w${WAIT_TIME} -B -s8 ${CAN_IFACE_NAME}:0x80 ${CAN_IFACE_NAME}:,0x3ffff &
  run candump -T${WAIT_TIME_MILLIS} -L ${CAN_IFACE_NAME}

  assert_success
  assert_output --partial "1BFFFF80#0123456789ABCDEF"
}

@test "Multiple source addresses on 1 CAN device" {
  # TODO: this should be '-s' instead of '-s8', but that requires some
  # argparse setup to propery parse the positional arguments after.
  #
  # For now, just use '-s8'
  sleep ${DELAY_TIME} && ${PYTHON_BIN} testj1939.py -w${WAIT_TIME} -B -s8 ${CAN_IFACE_NAME}:0x90 ${CAN_IFACE_NAME}:,0x3ffff &
  run candump -T${WAIT_TIME_MILLIS} -L ${CAN_IFACE_NAME}

  assert_success
  assert_output --partial "1BFFFF90#0123456789ABCDEF"
}

@test "Use PDU1 PGN" {
  # TODO: this should be '-s' instead of '-s8', but that requires some
  # argparse setup to propery parse the positional arguments after.
  #
  # For now, just use '-s8'
  sleep ${DELAY_TIME} && ${PYTHON_BIN} testj1939.py -w${WAIT_TIME} -B -s8 ${CAN_IFACE_NAME}:0x80 ${CAN_IFACE_NAME}:,0x12300 &
  run candump -T${WAIT_TIME_MILLIS} -L ${CAN_IFACE_NAME}

  assert_success
  assert_output --partial "1923FF80#0123456789ABCDEF"
}

@test "Use destination address info: during sendto()" {
  # TODO: this should be '-s' instead of '-s8', but that requires some
  # argparse setup to propery parse the positional arguments after.
  #
  # For now, just use '-s8'
  sleep ${DELAY_TIME} && ${PYTHON_BIN} testj1939.py -w${WAIT_TIME} -s8 ${CAN_IFACE_NAME}:0x80 ${CAN_IFACE_NAME}:0x40,0x12300 &
  run candump -T${WAIT_TIME_MILLIS} -L ${CAN_IFACE_NAME}

  assert_success
  assert_output --partial "19234080#0123456789ABCDEF"
}

@test "Use destination address info: during bind()" {
  # TODO: this should be '-s' instead of '-s8', but that requires some
  # argparse setup to propery parse the positional arguments after.
  #
  # For now, just use '-s8'
  # TODO: Fix the shorthand parsing of interface names
  sleep ${DELAY_TIME} && ${PYTHON_BIN} testj1939.py -w${WAIT_TIME} -s8 ${CAN_IFACE_NAME}:0x80 ${CAN_IFACE_NAME}:0x40,0x12300 &
  run candump -T${WAIT_TIME_MILLIS} -L ${CAN_IFACE_NAME}

  assert_success
  assert_output --partial "19234080#0123456789ABCDEF"
}

@test "Emit different PGNs using the same socket: broadcast transmission" {
  # TODO: this should be '-s' instead of '-s8', but that requires some
  # argparse setup to propery parse the positional arguments after.
  #
  # For now, just use '-s8'
  # TODO: Fix the shorthand parsing of interface names
  sleep ${DELAY_TIME} && ${PYTHON_BIN} testj1939.py -w${WAIT_TIME} -B -s8 ${CAN_IFACE_NAME}:0x80 ${CAN_IFACE_NAME}:,0x32100 &
  run candump -T${WAIT_TIME_MILLIS} -L ${CAN_IFACE_NAME}

  assert_success
  assert_output --partial "1B21FF80#0123456789ABCDEF"
}

@test "Larger packets" {
  # TODO: Fix the shorthand parsing of interface names
  sleep ${DELAY_TIME} && ${PYTHON_BIN} testj1939.py -w${WAIT_TIME} -B -s20 ${CAN_IFACE_NAME}:0x80 ${CAN_IFACE_NAME}:,0x12300 &
  run candump -T${WAIT_TIME_MILLIS} -L ${CAN_IFACE_NAME}

  assert_success
  assert_output --partial "18ECFF80#20140003FF002301"
  assert_output --partial "18EBFF80#010123456789ABCD"
  assert_output --partial "18EBFF80#02EF0123456789AB"
  assert_output --partial "18EBFF80#03CDEF01234567FF"
}

@test "Larger packets: using testj1939 to receive" {
  # TODO: Fix the shorthand parsing of interface names
  sleep ${DELAY_TIME} && ${PYTHON_BIN} testj1939.py -w${WAIT_TIME} -s20 ${CAN_IFACE_NAME}:0x80 ${CAN_IFACE_NAME}:0x90,0x12300 &
  run ${PYTHON_BIN} testj1939.py -w${WAIT_TIME} ${CAN_IFACE_NAME}:0x90 -r

  assert_success
  assert_output --partial "80 12300: 01 23 45 67 89 ab cd ef"
  assert_output --partial "00008     01 23 45 67 89 ab cd ef"
  assert_output --partial "00010     01 23 45 67"
}
