# arduino-cli compile LED/LED.ino --fqbn arduino:mbed_nano:nano33ble --output-dir generated
# python3 sn_generator.py -i generated/LED.ino.hex -r "\${XXXXXXXXXXXXXXXXX}" -p "DEV-" -f 0 -t 100

from intelhex import IntelHex
import sys
import getopt
import pathlib
import os


def main(argv):
    # the input firmware file (.hex)
    inFile: str = ''
    # the string to replace within the firmware file
    replace: str = ''
    # the device prefix
    prefix: str = ''
    # serial number start
    snFrom: int = ''
    # serial number end
    snTo: int = ''

    try:
        opts, args = getopt.getopt(argv, 'hi:r:p:f:t:')
    except getopt.GetoptError:
        usage()
        sys.exit(2)
    for opt, arg in opts:
        if opt in ("-h", "--help"):
            usage()
            sys.exit()
        elif opt in ("-i", "--input"):
            inFile = arg
        elif opt in ("-r", "--replace"):
            replace = arg
        elif opt in ("-p", "--prefix"):
            prefix = arg
        elif opt in ("-f", "--from"):
            snFrom = int(arg)
        elif opt in ("-t", "--to"):
            snTo = int(arg)

    generate(inFile, replace, prefix, int(snFrom), int(snTo))


def usage() -> None:
    print(
        f'{sys.argv[0]} -i <hex> -r <str to replace> -p <prefix> -f <num from> -t <num to>')


def generate(inFile: str, replace: str, prefix: str, snFrom: int, snTo: int, out: str = 'generated') -> None:
    """
    Generates .hex files from snFrom to snTo with the pattern <prefix><number>.
    """
    pathlib.Path(out).mkdir(parents=True, exist_ok=True)
    leftPad = len(str.encode(replace)) - len(str.encode(prefix))

    for x in range(snFrom, snTo):
        ih = IntelHex()
        ih.loadhex(inFile)
        found = ih.find(str.encode(replace))
        # left pad zeroes to the number part
        snum = str(x).rjust(leftPad, '0')
        full = prefix + snum

        if len(str.encode(full)) > len(str.encode(replace)):
            print(f'ERROR: Length of the generated serial number {full} exceeds string to replace {
                  replace} in hex file.')
            sys.exit(2)

        ih.puts(found, str.encode(full))

        path = os.path.join(out, full)
        with open(path, 'w') as modhex:
            ih.write_hex_file(modhex, write_start_addr=False)


if __name__ == "__main__":
    main(sys.argv[1:])
