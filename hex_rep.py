# Writes a serial number (SN) in the pattern <prefix><number> to an already compiled firmware.
# Make sure to define a fixed string to the coude in the length the serial number should be.
# The -r argument needs to match the fixed string from the source code exactly.
#
# usage:
# `python3 sn_generator.py -i generated/LED.ino.hex -r "\${XXXXXXXXXXXXXXXXX}" -p "DEV-" -f 0 -t 3`
#
# generates the following firmware firmware files with serial numbers:
# [DEV-0000000000000000, DEV-0000000000000001, DEV-0000000000000002]

from intelhex import IntelHex
import sys
import getopt
import pathlib
import os


def main(argv):
    # the input firmware file (.hex)
    input_file_path: str = ''
    # the string to replace within the firmware file
    string_to_replace: str = ''
    # the device prefix
    sn_prefix: str = ''
    # serial number start
    sn_start: int = ''
    # serial number end
    sn_end: int = ''

    try:
        cmd_args = argv[1:]
        if (len(cmd_args) == 0):
            raise Exception('Args cant be empty.')
        opts, args = getopt.getopt(cmd_args, 'hi:r:p:f:t:')
        print(opts)
        print(args)
    except getopt.GetoptError:
        usage()
        sys.exit(2)
    except Exception:
        usage()
        sys.exit(2)
    for opt, arg in opts:
        if opt in ("-h", "--help"):
            usage()
            sys.exit()
        elif opt in ("-i", "--input"):
            input_file_path = arg
        elif opt in ("-r", "--replace"):
            string_to_replace = arg
        elif opt in ("-p", "--prefix"):
            sn_prefix = arg
        elif opt in ("-f", "--from"):
            sn_start = int(arg)
        elif opt in ("-t", "--to"):
            sn_end = int(arg)

    generate(input_file_path, string_to_replace,
             sn_prefix, int(sn_start), int(sn_end))


def usage() -> None:
    print("""
          Usage:
            hex_rep [flags...]
          
          Flags:
            -h, --help                  help for hex_rep.py
            -i, --input                 The hex file to modify.
            -r, --replace               The string to replace in input hex file.
            -p, --prefix                The prefix for the SN of the generated hex files.
            -f, --from                  Generate hex files with SN starting from.
            -t, --to                    Generate hex files with SN starting to (exclusive).
          """)


def generate(input_file: str, string_to_replace: str, sn_prefix: str, sn_start: int, sn_end: int, out: str = 'generated') -> None:
    """
    Generates .hex files from sn_start to sn_end (-1) following the scheme <prefix><number>.
    """
    pathlib.Path(out).mkdir(parents=True, exist_ok=True)
    len_of_num_part = len(str.encode(string_to_replace)
                          ) - len(str.encode(sn_prefix))

    for x in range(sn_start, sn_end):
        ih = IntelHex()
        ih.loadhex(input_file)
        # find the start index of the string to replace
        found = ih.find(str.encode(string_to_replace))
        # left pad the number part
        padded_num = str(x).rjust(len_of_num_part, '0')
        full = sn_prefix + padded_num

        if len(str.encode(full)) > len(str.encode(string_to_replace)):
            print(f'ERROR: Length of the generated serial number {full} exceeds the string to replace {
                  string_to_replace} in hex file.')
            sys.exit(2)

        # override the string with the gernerated one
        ih.puts(found, str.encode(full))
        path = os.path.join(out, f'{full}.hex')
        with open(path, 'w') as modhex:
            # write the modified firmware
            ih.write_hex_file(modhex, write_start_addr=False)


if __name__ == "__main__":
    main(sys.argv)
