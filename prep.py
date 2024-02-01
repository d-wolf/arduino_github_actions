# arduino-cli compile LED/LED.ino --fqbn arduino:mbed_nano:nano33ble --output-dir out


from intelhex import IntelHex
import binascii

repl = '<<<<XXXXXXXXXXXXX>>>>'
strToReplace = '<<<<SERIALNUMBERX>>>>'
replaceBytes = str.encode(strToReplace)
print('change')
print(replaceBytes.hex().upper())
print('to')
print(str.encode(repl).hex().upper())

ih = IntelHex()                     # create empty object
ih.loadhex('out/LED.ino.hex')               # load from hex
file = open('myfile.txt', 'a')
modhex = open('modHex.hex', 'a')
ih.dump(file)               # load from hex
found = ih.find(replaceBytes)
print('start index')
print(found)
ih.puts(found, str.encode(repl))
ih.write_hex_file(modhex, write_start_addr=False)
