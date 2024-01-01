import serial
from .myserial import RS485Ext
from .port_handler import PortHandler
 
class PortHandlerExt(PortHandler):
    def __init__(self, *args, **kwargs):
        super(PortHandlerExt, self).__init__(*args, **kwargs)
 
    def setupPort(self, cflag_baud):
        if self.is_open:
            self.closePort()
 
        self.ser = RS485Ext(
            port=self.port_name,
            baudrate=self.baudrate,
            bytesize=serial.EIGHTBITS,
            timeout=0
        )
 
        self.is_open = True
        self.ser.reset_input_buffer()
        self.tx_time_per_byte = (1000.0 / self.baudrate) * 10.0
 
        return True
