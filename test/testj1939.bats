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
