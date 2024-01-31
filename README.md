# arduino_github_actions
Demonstrates how to build arduino sketches with github actions using the [Arduino CLI](https://arduino.github.io/arduino-cli/).

# Arduino CLI

## Common Commands
* `arduino-cli board list` - reads out full qualified name (FQBN) of your board (needed for compile)
* `arduino-cli compile --fqbn arduino:mbed_nano:nano33ble --output-dir out`