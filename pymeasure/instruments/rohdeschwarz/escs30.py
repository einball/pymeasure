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
from pymeasure.instruments.validators import strict_range, truncated_discrete_set

from enum import Enum


class AttenuationMode(Enum):
	LOW_NOISE 		= "LOWNOISE"
	LOW_DISTORTION 	= "LOWDISTORTION"

class IFBandWidth(Enum):
	pass

class DemodulationMode(Enum):
	FM 				= "FM"
	AM 				= "AM"
	ZEROBEAT 		= "A0"
	OFF 			= "OFF"

class DetectionMode(Enum):
	AVG 			= "AVERAGE"
	PEAK 			= "PEAK"
	QUASIPEAK 		= "QUASIPEAK"
	RMS 			= "RMS"



class ESCS30(Instrument):
    """ Represents the Rohde&Schwarz ESCS30 EMV Measurement Receiver
    """



    id = Instrument.measurement("*IDN?", """Reads the instrument identification string """)

    cal_correction = Instrument.setting(
    	"CALIBRATION:CORRECTION %s",
    	"""Apply calibration correction during power measurement""",
    	validator=truncated_discrete_set,
    	values={True : "ON",False : "OFF"},
    	map_values=True)

    attenuation = Instrument.control(
    	"ATTENUATION?", "ATTENUATION %ddB",
    	"""Set instrument attenuation (0dB .. 60dB)""",
    	validator=strict_range,
    	values=[0, 60],
    	get_process=lambda str: str.replace('DB', '') )

    attenuation_mode = Instrument.control(
    	"ATTENUATION:MODE?", "ATTENUATION:MODE?",
    	"""Attenuator mode [LOW_NOISE | LOW_DISTORTION]""",
    	validator=truncated_discrete_set,
    	values=AttenuationMode,
    	map_values=True)

    preamp_enabled = Instrument.control(
    	"PREAMPLIFIER?", "PREAMPLIFIER %s",
    	"""Enables or disables the integrated preamplifier""",
    	validator=truncated_discrete_set,
    	values={True : "ON",False : "OFF"},
    	map_values=True)

    single_measurement = Instrument.control(
    	"MEASUREMENT:SINGLE?", "MEASUREMENT:SINGLE %s",
    	"""When True, only aquire a single measurement instead of running continuously""",
    	validator=truncated_discrete_set,
    	values={True : "ON",False : "OFF"},
    	map_values=True)




    def __init__(self, resourceName, **kwargs):
        super().__init__(
            resourceName,
            "ESCS 30",
            **kwargs
        )

        def check_errors():
        	pass



def setAttenuation(att, autorange=None,mode=None,preamp=None):

	self.attenuation = att

	if autorange:
		self.att_autorange = autorange
	if mode:
		self.attenuation_mode = mode
	if preamp:
		self.preamp_enabled = preamp


system_error = {	0 : "No error",
					2 : "Parameter out of range",
					3 : "Setting does not apply",
					4 : "Value out of range",
					9 : "Invalid Unit",
					16 : "Exeeds minimum frequency limit",
					17 : "Exceeds maximum frequency limit",
					18 : "Exceeds minimum power level",
					19 : "Exceeds maximum power level",
					20 : "Frequency values out of order",
					100: "No scan defined",
					-100 : "Internal Error",
					-101 : "Syntax Error",
					-102 : "Invalid Data Type",
					-113 : "Unknown or ambiguous Command",
					-130 : "Wrong or ambiguous unit",
					-141 : "Wrong or ambiguous character data",
					-161 : "Invalid block data",
					-221 : "Invalid Input",
					-222 : "Data out of range",
					-400 : "Output Buffer Overflow",
					-410 : "Output data has been overwritten due to timeout",
					-420 : "Read exception: No output data present",
				}

cal_error = {		6 : "CAL Error ZF Bandwidth",
					25 : "CAL Error 5.9MHz Reference",
					65 : "CAL Error ZF AGC",
					81 :  "CAL Error 30dB Attenuator",
					103 :  "CAL Error Peak Detector Band A",
					105 :  "CAL Error Peak Detector Band B",
					107 :  "CAL Error Peak Detector Band C/D"
				}

self_test_error	= {	0 : "Passed without errors",
					1 : "+5V supply out of specification",
					2 : "+10V supply our of specification",
					3 : "-10V supply out of specification",
					4 : "+28V supply out of specification",
					15 : "Mainboard Error",
					18 : "RTC Error",
					19 : "Serial Bus Error",
					99 : "Synthesizer Error",
					100 : "Frontend Error",
					106 : "IF Selection Error",
					107 : "Second Mixer Error",
					111 : "Detector Error" 
				}

cal_filt_error = {	129 : 100e3,		131 : 200e3,		133 : 500e3,		135 : 1.0e6, 
					137 : 1.8e6,		139 : 1.9e6,		141 : 2.4e6,		143 : 2.9e6, 
					145 : 3.9e6,		147 : 5.9e6,		149 : 7.9e6,		151 : 8.4e6, 
					153 : 8.9e6,		155 : 9.9e6,		157 : 14.9e6,		159 : 19.9e6, 
					161 : 24.9e6,		163 : 25.4e6,		165 : 25.9e6,		167 : 27.9e6, 
					169 : 30.9e6,		171 : 40.9e6,		173 : 50.9e6,		175 : 60.9e6, 
					177 : 40.9e6,		179 : 50.9e6,		181 : 60.9e6,		183 : 70.9e6,
					185 : 79.9e6,		187 : 80.4e6,		189 : 90.9e6,		191 : 100.9e6, 
					193 : 110.9e6,		195 : 120.9e6,		197 : 130.9e6,		199 : 140.9e6, 
					201 : 150.9e6,		203 : 160.9e6,		205 : 170.9e6,		207 : 180.9e6, 
					209 : 190.9e6,		211 : 199.9e6,		213 : 200.4e6,		215 : 210.9e6, 
					217 : 220.9e6,		219 : 230.9e6,		221 : 240.9e6,		223 : 250.9e6, 
					225 : 260.9e6,		227 : 270.9e6,		229 : 280.9e6,		231 : 290.9e6, 
					233 : 200.9e6,		235 : 310.9e6,		237 : 320.9e6,		239 : 330.9e6, 
					241 : 340.9e6,		243 : 350.9e6,		245 : 360.9e6,		247 : 370.9e6, 
					249 : 380.9e6,		251 : 390.9e6,		253 : 400.9e6,		255 : 410.9e6, 
					257 : 420.9e6,		259 : 430.9e6,		261 : 440.9e6, 		263 : 450.9e6,	
					265 : 460.9e6,		267 : 470.9e6,		269 : 280.9e6,		271 : 490.9e6,
					273 : 499.9e6,		275 : 500.4e6,		277 : 510.9e6,		279 : 520.9e6,
					281 : 530.9e6,		283 : 540.9e6,		285 : 550.9e6,		287 : 560.9e6,
					289 : 570.9e6,		291 : 580.9e6,		293 : 590.9e6,		295 : 600.9e6,
					297 : 610.9e6,		299 : 620.9e6,		301 : 630.9e6,		303 : 640.9e6,
					305 : 650.9e6,		307 : 660.9e6,		309 : 670.9e6,		311 : 680.9e6,
					313 : 690.9e6,		315 : 700.9e6,		317 : 710.9e6,		319 : 720.9e6,
					321 : 730.9e6,		323 : 740.9e6,		325 : 750.9e6,		327 : 760.9e6,
					329 : 770.9e6,		331 : 780.9e6,		333 : 790.9e6,		335 : 800.9e6,
					337 : 810.9e6,		339 : 820.9e6,		341 : 830.9e6,		343 : 840.9e6,
					345 : 850.9e6,		347 : 860.9e6,		349 : 870.9e6,		351 : 880.9e6,
					353 : 890.9e6,		355 : 900.9e6,		357 : 910.9e6,		359 : 920.9e6,
					361 : 930.9e6,		363 : 940.9e6,		365 : 950.9e6,		367 : 960.9e6,
					369 : 970.9e6,		371 : 980.9e6,		373 : 990.9e6,		375 : 999.9e6,
					377 : 1000.4e6,		379 : 1050.9e6,		381 : 1100.9e6,		383 : 1150.9e6,
					385 : 1200.9e6,		387 : 1250.9e6,		389 : 1300.9e6,		391 : 1350.9e6,
					393 : 1400.9e6,		395 : 1450.9e6,		397 : 1500.9e6,		399 : 1550.9e6,	
					401 : 1600.9e6,		403 : 1650.9e6,		405 : 1700.9e6,		407 : 1750.9e6,		
					409 : 1800.9e6,		411 : 1850.9e6,		413 : 1900.9e6,		415 : 1959.9e6,	
					417 : 1960.9e6,		419 : 2000.9e6,		421 : 2050.9e6,		423 : 2100.9e6,
					425 : 2150.9e6,		427 : 2200.9e6,		429 : 2250.9e6,		431 : 2300.9e6,
					433 : 2350.9e6,		435 : 2400.9e6,		437 : 2450.9e6,		439 : 2499.e6,
					441 : 2550.9e6,		443 : 2600.9e6,		445 : 2650.9e6,		447 : 2700.9e6,
					449 : 2749.9e6 
				}

