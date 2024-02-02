# arduino_github_actions

Demonstrates how to compile an arduino sketch for Nano 33 BLE with github actions using the [Arduino CLI](https://arduino.github.io/arduino-cli/).

# Common CLI Commands

- `arduino-cli core install arduino:mbed_nano` - installs the specified board
- `arduino-cli lib install ArduinoBLE@1.3.6` - install a library for a specific version
- `arduino-cli compile LED/LED.ino --fqbn arduino:mbed_nano:nano33ble --output-dir out` - compile .ino to output directory
- `arduino-cli board list` - reads out full qualified name (FQBN) of your board (needed for compile command)