import time

# Define some constants
class opcodes(object):
    nop = 0
    digit_0 = 1
    digit_1 = 2
    digit_2 = 3
    digit_3 = 4
    digit_4 = 5
    digit_5 = 6
    digit_6 = 7
    digit_7 = 8
    decode_mode = 9
    intensity = 0xa
    scan_limit = 0xb
    shutdown = 0xc
    display_test = 0xf

class matrix(object):
    def __init__(self):
        # Open the SPI device
        import spidev
        self._bugger = [0] * 32
        self._spi = spidev.SpiDev()
        self._spi.open(0,0)

        # Run some initialisation commands
        self.command(opcodes.scan_limit, 7)
        self.command(opcodes.decode_mode, 0)
        self.command(opcodes.display_test, 0)
        self.command(opcodes.shutdown, 1)
        self.command(opcodes.intensity, 15)

    def command(self, register, data, count=4):
        """This function writes the same data to a number of matrices"""
        self._write([register,data]*count)
    
    def _write(self,data):
        """This function uses the SPI interface to send data to the matrix"""
        self._spi.xfer2(list(data))
    

