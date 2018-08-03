import sys
f = open(sys.argv[1],'rb')
utf8 = list()

def convertToUTF8(msb, lsb):
	if msb == 0x00 and lsb <= 0x7F:
		return [lsb & 0b01111111]
	elif msb <= 0x07:
		byte1 = 0b10000000
		byte1 = byte1 | (lsb & 0x3F)
		byte0 = 0b11000000
		msb = msb << 2
		byte0 = byte0 | msb
		byte0 = byte0 | ((lsb & 0xC0) >> 6)
		return [byte0, byte1]
	elif msb >= 0x08:
		temp = 0x00
		temp = msb << 2 | ((lsb & 0xC0) >> 6)
		byte0 = 0b11100000 | ((msb & 0xF0) >> 4)
		byte1 = 0b10000000 | (temp & 0x3F)
		byte2 = 0b10000000 | (lsb & 0x3F)
		return [byte0,byte1,byte2]

try:
	utf16 = f.read(2)
	while utf16:
		if len(utf16) is not 1:
			utf8.append(convertToUTF8(ord(utf16[0]), ord(utf16[1])))
		else :
			utf8.append(convertToUTF8(ord(utf16[0]), 0x00))
		utf16 = f.read(2)
finally:
	f.close()
	
try:
	f = open("utf8encoder_out.txt","wb")
	a = bytearray()
	for list in utf8:
		for byte in list:
			a.append(byte)
	f.write(a)
finally:
	f.close()