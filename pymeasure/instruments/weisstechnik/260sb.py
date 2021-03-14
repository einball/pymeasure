#
# This file is part of the PyMeasure package.
#
# Copyright (c) 2013-2021 PyMeasure Developers
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.
#

from pymeasure.instruments import Instrument
from enum import Enum
import struct

class DigitalState(Enum):
	CHAMBER_ENABLE 	= 0x80
	DIRECT_INPUT	= 0x40
	DEW_PROTECTION	= 0x20
	DEWPOINT_EXP	= 0x10
	CHANNEL_1		= 0x08
	CHANNEL_2		= 0x04
	CHANNEL_3		= 0x02
	CHANNEL_4		= 0x01 


class 260SB(Instrument):
    """ 
	Climate Chamber, Weiss Technik 260SB with Prodicon Controller
    """

    setpoint_temp 		= 25.0
    setpoint_humidity	= 0
    digital_state		= 0x00
    printer_stat 		= False


    def __init__(self, resourceName, **kwargs):
        super().__init__(
            resourceName,
            "WeissTechnik260SB",
            **kwargs
        )


	def setTemperature(temperature):
		pass
	def setHumidity(humidity):
		pass
	def setDigitalState(channel, value = False):
		if value:
			self.digital_state = self.digital_state | channel
		else:
			self.digital_state = self.digital_state & (0xFF - channel)
		makeMessage()

	def makeMessage():
		response = self.ask("T{:0=-5,.1f}F{}R{:b}".format(self.setpoint_temp,self.setpoint_humidity,self.digital_state))
		parseResponse(response)

	def parseResponse(msg):

		line = bytes(' 18.4F00P1>TEMP-SOLL:  42.03C  0T-99.9#--T 42.0F00R11100000','utf8')

		formatString = '5s 1x 2s 1x 1s 1s 10x 7s 1x 3s 1x 5s 21x'

		try:
			fields = struct.unpack(formatString,bytes(msg, 'utf-8'))

			self.is_temp		= float(fields[0])
			self.is_hum			= int(fields[1])
			self.printer_stat	= True if fields[2] == b'1' else False
			self.indicator		= fields[3]
			self.set_temp		= fields[4]
			#self._				= fields[5]
			#self._				= fields[6]	
			print("Fields: {}".format(fields))
			print("Current Temp: {}\nCurrent Humidity: {}\n \
				Heating/Cooling Indicator: {}\nSetpoint Temperature: {}\nPrinter: {}\n".format(is_temp,is_hum,indicator,set_temp,printer_stat))

		except:
			print(struct.err)
