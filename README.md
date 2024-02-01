# arduino_github_actions
Demonstrates how to compile an arduino sketch for Nano 33 BLE with github actions using the [Arduino CLI](https://arduino.github.io/arduino-cli/).

# Common CLI Commands
* `arduino-cli board list` - reads out full qualified name (FQBN) of your board (needed for compile command)
* `arduino-cli compile --fqbn arduino:mbed_nano:nano33ble --output-dir out`