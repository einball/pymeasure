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


TrueFalse 			= {True:"ON", False:"OFF"}
AttenuationMode 	= {'LOW_NOISE':'LOWN', 'LOW_DISTORTION':'LOWD'}
IFBandWidth 		= {'IF_200HZ':'200 H', 'IF_9KHZ':'9 K', 'IF_120KHZ':'120 K', 'IF_1MHZ':'1 M'}
DemodulationMode 	= {'FM':'F', 'AM':'AM', 'ZEROBEAT' :'A0', 'OFF':'O'}
DetectionMode 		= {'AVG':'A', 'PEAK':'P', 'QUASIPEAK' :'Q', 'RMS':'R'}
FrequencyVariation 	= {'STEP':'S', 'COARSE':'C', 'FINE' :'F', 'LOCK':'L'}
DataFormat 			= {'ASCII' :'AS', 'BINARY':'BIN'}
AnalysisMode 		= {'RF' :'R', 'IF':'I'}
LinLog 				= {'LINEAR' :'LI', 'LOGARITHMIC':'LO'}
ScanMode 			= {'CHANNEL':'C', 'NORMAL':'N', 'OVERVIEW' :'O', 'TIME_DOMAIN':'T'}
DisplayStyle 		= {'CURVE' :'C', 'LINE':'L'}
RepetitiveScanMode 	= {'MAXHOLD':'MAXH', 'MAXCLR' :'MAXC', 'OFF':'O'}
BlockElement 		= {'COMBINED':'M', 'TRACE':'T', 'SUBMAX':'S', 'DET1':'DET1', 'DET2' :'DET2', 'VALID':'V'}
BlockFormat 		= {'ASCII':'A','BINARY':'B', 'DUMP' :'D', 'SDUMP':'SD'}
GridSimulatorPhase	= {'N':'N', 'L1':'L1', 'L2':'L2', 'L3':'L3'}
GridSimulatorGround = {'GROUNDED': 'GR', 'FLOATING': 'FL'} 


class ESCS30(Instrument):
	""" Represents the Rohde&Schwarz ESCS30 EMV Measurement Receiver
	"""

	id = Instrument.measurement("*IDN?", """Reads the instrument identification string """)

	cal_correction = Instrument.setting(
		"CALIBRATION:CORRECTION %s", """Apply calibration correction during power measurement""",
		validator=truncated_discrete_set, values=TrueFalse, map_values=True)

	attenuation = Instrument.control(
		"A?", "A %d DB", """Set instrument attenuation (0dB .. 60dB)""",
		validator=strict_range, values=[0, 60], get_process=lambda str: str.replace('DB', '') )

	def incrementAttenuation():
		self.ask("A:I")

	def decrementAttenuation():
		self.ask("A:D")

	use_autoranging = Instrument.control(
		"A:A?", "A:A %s", """Allow attenuation autorange""",
		validator=truncated_discrete_set, values=TrueFalse, map_values=True)

	attenuation_mode = Instrument.control(
		"A:M?", "A:M?", """Attenuator mode: {}""".format([mode.name for mode in AttenuationMode]),
		validator=truncated_discrete_set, values=AttenuationMode, map_values=True)

	autorange_includes_preamp = Instrument.control(
		"A:P?", "A:P %s", """Enables or disables the use of the internal preamplifier in autoranging""",
		validator=truncated_discrete_set, values=TrueFalse, map_values=True)

	zero_scale_deflection = Instrument.measurement("A:Z?", """Zero Scale Deflection""")

	if_bandwidth = Instrument.control(
		"B:I?", "B:I %s", """IF bandwidth selection: {}""".format([bw.name for bw in IFBandWidth]),
		validator=truncated_discrete_set, values=IFBandWidth, map_values=True)

	demodulation_mode = Instrument.control(
		"DEM?", "DEM %s", """Sets the demodulation mode: {}""".format([mode.name for mode in DemodulationMode]),
		validator=truncated_discrete_set, values=DemodulationMode, map_values=True)

	detector_mode = Instrument.control(
		"DET?", "DET %s", """Sets the detection mode: {}""".format([mode.name for mode in DetectionMode]),
		validator=truncated_discrete_set, values=DetectionMode, map_values=True)

	# TODO: Combined Validator and formatter for SI Units instead of plain kHz numbers
	frequency = Instrument.control(
		"FR?", "FR %d", """Reception Frequency (9kHz .. 2750MHz) in kHz""",
		validator=strict_range, values=[9, 2750e3])

	def incrementFrequency():
		self.ask("FR:I")

	def decrementFrequency():
		self.ask("FR:D")

	frequency_variation = Instrument.control(
		"FR:V?", "FR:V %s", """Sets the step size of the internal knob: {}""".format([var.name for var in FrequencyVariation]),
		validator=truncated_discrete_set, values=FrequencyVariation, map_values=True)

	use_extref = Instrument.control(
		"FR:E?", "FR:E %s", """Enables or disables the external frequency reference""",
		validator=truncated_discrete_set, values=TrueFalse, map_values=True)

	use_generator = Instrument.control(
		"G?", "G %s", """Enables or disables the internal tracking generator""",
		validator=truncated_discrete_set, values=TrueFalse, map_values=True)

	level = Instrument.measurement("LE?", """Starts a power measurement and returns the value""")

	# Skip Continue and Lastvalue

	data_format = Instrument.control(
		"LE:F?", "LE:F %s","""Result format: {}""".format([element.name for element in DataFormat]),
		validator=truncated_discrete_set, values=DataFormat, map_values=True)

	measurement_time = Instrument.control(
		"ME:T?", "ME:T %d","""Time for a M power measurement (0.1ms .. 100s) in ms""",
		validator=strict_range, values=[0.1, 100e3])

	M_measurement = Instrument.control(
		"MEASUREMENT:M?", "MEASUREMENT:M %s","""When True, only aquire a M measurement instead of running continuously""",
		validator=truncated_discrete_set, values=TrueFalse, map_values=True)

	use_preamp = Instrument.control(
		"PREA?", "PREA %s","""Enables or disables the internal preamplifier""",
		validator=truncated_discrete_set, values=TrueFalse, map_values=True)

	# Skip SpecialFunction

	unit = Instrument.measurement("UN?", """Requests the unit of measurement""")

	analysis_mode = Instrument.control(
		"MO?", "MO %s","""Sets the analysis mode: {}""".format([mode.name for mode in AnalysisMode]),
		validator=truncated_discrete_set, values=AnalysisMode, map_values=True)

	grid_division = Instrument.control(
		"GR:FR?", "GR:FR %s","""Sets the axis division: {}""".format([div.name for div in LinLog]),
		validator=truncated_discrete_set, values=LinLog, map_values=True)

	grid_minlevel = Instrument.control(
		"GR:MI?","GR:MI %dD","""Minimal level displayed in the power diagram (-200dB .. 200dB)""",
		validator=strict_range, values=[-200,200])

	grid_maxlevel = Instrument.control(
		"GR:MA?","GR:MA %dD","""Maximum level displayed in the power diagram (-200dB .. 200dB)""",
		validator=strict_range, values=[-200,200])

	scan_selector = Instrument.control(
		"SC?","SC %d","""Current selected partial scanning interval (1 .. 5)""",
		validator=strict_range, values=[1,5])

	# Skip Scan Run because I don't fully understand the logic 
	# behind the handling of scattered scanning yet

	interrupt_scan = Instrument.setting("SC:I", """Interrupts a repetitive scan in progress""")
	continue_scan = Instrument.setting("SC:CO", """Continues previously aborted scan""")
	stop_scan     = Instrument.setting("SC:ST", """Ends the currently running scan""")

	scan_mode = Instrument.control(
		"SC:M?", "SC:M %s","""Sets the analysis mode: {}""".format([mode.name for mode in ScanMode]),
		validator=truncated_discrete_set, values=ScanMode, map_values=True)

	scan_range = Instrument.control(
		"SC:RA?","SC:RA %d","""Number of scans to be executed (1 .. 5)""",
		validator=strict_range, values=[1,5])

	scan_start_frequency = Instrument.control(
		"SC:STA?","SC:STA %d","""Start frequency of partial scan in kHz""",
		validator=strict_range, values=[9,2750e3])

	scan_stop_frequency = Instrument.control(
		"SC:STA?","SC:STA %d","""Stop frequency of partial scan in kHz""",
		validator=strict_range, values=[9,2750e3])

	scan_stepmode = Instrument.control(
		"SC:STEPM?", "SC:STEPM %s","""Sets the step division: {}""".format([div.name for div in LinLog]),
		validator=truncated_discrete_set, values=LinLog, map_values=True)

	# Combined validator should be used in case of logarighmic steps
	scan_stepsize = Instrument.control(
		"SC:STEPS?","SC:STEPS %d K","""Step size in kHz for linear steps and in \% for logarithmic steps""",
		validator=strict_range, values=[0,2750e3])

	def saveScanParameter():
		self.ask("SC:SA")

	scan_timeout = Instrument.setting(
		"SC:T %d","""Specifies a timeout for time analysis in ms""",
		validator=strict_range, values=[5,10000e3])

	scan_measurement_time = Instrument.control(
		"SC:RE:MT?", "SC:RE:MT %d","""Time for a power measurement (0.1ms .. 100s) in the partial scan in ms""",
		validator=strict_range, values=[0.1, 100e3])

	scan_if_bandwidth = Instrument.control(
		"SC:B:I?", "SC:B:I %d","""IF Filter Bandwidth for partial scan range (200Hz .. 1MHz) in Hz""",
		validator=strict_range, values=[200, 100e6])

	scan_attenuation = Instrument.control(
		"SC:RE:A?", "SC:RE:A %d D","""RF attenuation for partial scan range (0dB .. 60dB)""",
		validator=strict_range, values=[0, 60])

	scan_use_autoranging = Instrument.control(
		"SC:RE:A:A?", "SC:RE:A:A %s","""Use autoranging within the partial scan range""",
		validator=truncated_discrete_set, values=TrueFalse, map_values=True)

	scan_attenuation_mode = Instrument.control(
		"SC:RE:A:M?", "SC:RE:A:M %s","""Attenuation mode for scan range: {}""".format([mode.name for mode in AttenuationMode]),
		validator=truncated_discrete_set, values=AttenuationMode, map_values=True)

	scan_number_subranges = Instrument.control(
		"SC:O:SU?","SC:O:SU %d","""Specifies the number of subranges: (8,16,25,50,100,200,400)""",
		validator=truncated_discrete_set, values=[8,16,25,50,100,200,400]) 

	scan_fast = Instrument.control(
		"SC:O:FA?", "SC:O:FA %s","""Use autoranging within the partial scan range""",
		validator=truncated_discrete_set, values=TrueFalse, map_values=True)

	scan_margin = Instrument.control(
		"SC:O:M?", "SC:O:M %d D","""Sets the minimal margin of the acceptance line to the limit""",
		validator=strict_range, values=[-200, 200])

	scan_special = Instrument.control(
		"SC:O:SP?", "SC:O:SP %s","""Channel Scan setting""",
		validator=truncated_discrete_set, values=TrueFalse, map_values=True)

	scan_special_style = Instrument.control(
		"SC:O:SP:S?", "SC:O:SP:S %s",""""Display Style of measurements""",
		validator=truncated_discrete_set, values=DisplayStyle, map_values=True)

	scan_special_min_level = Instrument.control(
		"SC:O:SP:MINL?","SC:O:SP:MINL %dD","""Minimal level displayed in the power diagram (-200dB .. 200dB)""",
		validator=strict_range, values=[-200,200])

	scan_special_max_level = Instrument.control(
		"SC:O:SP:MAXL?","SC:O:SP:MAXL %dD","""Maximum level displayed in the power diagram (-200dB .. 200dB)""",
		validator=strict_range, values=[-200,200])

	scan_special_min_frequency = Instrument.control(
		"SC:O:SP:MINF?","SC:O:SP:MINF %d K","""Minimum frequency displayed in the power diagram in kHz""",
		validator=strict_range, values=[9,2750e3])

	scan_special_max_frequency = Instrument.control(
		"SC:O:SP:MAXF?","SC:O:SP:MAXF %d K","""Maximum frequency displayed in the power diagram in khz""",
		validator=strict_range, values=[-200,2750e3])

	# TODO: Fix it 
	#scan_special_frequencies = Instrument.control(
	#	"SC:O:FR?","SC:O:FR %d")

	scan_special_repetitive_scan = Instrument.control(
		"SC:O:R?", "SC:O:R %s","""Sets the analysis mode: {}""".format([mode.name for mode in RepetitiveScanMode]),
		validator=truncated_discrete_set, values=RepetitiveScanMode, map_values=True)

	scan_block_num_samples = Instrument.control(
		"SC:B:C?","SC:B:C %d","""Number of samples transferred in one block of data""")

	scan_block_set_max_num_samples = Instrument.setting(
		"SC:B:C M", """Sets the maximum Blockcount""")

	scan_block_element = Instrument.control(
		"SC:B:E?", "SC:B:E %s",""""Transmission Style Selector: {}""".format([mode.name for mode in BlockElement]),
		validator=truncated_discrete_set, values=BlockElement, map_values=True)

	scan_block_blocksize = Instrument.measurement("SC:B:S?","""Size of a block element in bytes. Using ASCII, the size is not fixed""")

	scan_block_template = Instrument.measurement("SC:B:T?", """Layout template of elements""")

	# Mental breakdown right here

#	scan_output_results = 
#	scan_clear_results = 


	# Error Handling stuff

	era = Instrument.measurement("ERA?", """Event Status Register A, Device Errors""")
	erae = Instrument.control("ERAE?", "ERAE %d", """Event Status Enable Register A""", validator=strict_range, values=[0,65535])

	erb = Instrument.measurement("ERB?", """Event Status Register B, Synthesizer Errors""")
	erbe = Instrument.control("ERBE?", "ERBE %d", """Event Status Enable Register B""", validator=strict_range, values=[0,65535])

	erc = Instrument.measurement("ERC?", """Event Status Register C, IEC-Bus Errors """)
	erce = Instrument.control("ERCE?", "ERCE %d", """Event Status Enable Register C""", validator=strict_range, values=[0,65535])

	erd = Instrument.measurement("ERD?", """Event Status Register A, """)
	erde = Instrument.control("ERDE?", "ERDE %d", """Event Status Enable Register D""", validator=strict_range, values=[0,65535])

	show_header = Instrument.setting(
		"H %s", """Output header when requesting information""",
		validator=truncated_discrete_set, values=TrueFalse, map_values=True)

	gridsim_phase = Instrument.control(
		"LI:PH?", "LI:PH %s", """Set the phase""",
		validator=truncated_discrete_set, values=GridSimulatorPhase, map_values=True)

	gridsim_ground = Instrument.control(
		"LI:PE?", "LI:PE %s", """PE settings""",
		validator=truncated_discrete_set, values=GridSimulatorGround, map_values=True)


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


event_status_reg = {	0x80: 'Power On',
						0x40: 'User Request',
						0x20: 'Command Error',
						0x10: 'Execution Error',
						0x08: 'Device Dependent Error',
						0x04: 'Query Error',
						0x02: 'Request Control',
						0x01: 'Operation'
						}

system_error = {	0:"No error",
					2:"Parameter out of range",
					3:"Setting does not apply",
					4:"Value out of range",
					9:"Invalid Unit",
					16:"Exeeds minimum frequency limit",
					17:"Exceeds maximum frequency limit",
					18:"Exceeds minimum power level",
					19:"Exceeds maximum power level",
					20:"Frequency values out of order",
					100: "No scan defined",
					-100:"Internal Error",
					-101:"Syntax Error",
					-102:"Invalid Data Type",
					-113:"Unknown or ambiguous Command",
					-130:"Wrong or ambiguous unit",
					-141:"Wrong or ambiguous character data",
					-161:"Invalid block data",
					-221:"Invalid Input",
					-222:"Data out of range",
					-400:"Output Buffer Overflow",
					-410:"Output data has been overwritten due to timeout",
					-420:"Read exception: No output data present",
				}

cal_error = {		6:"CAL Error ZF Bandwidth",
					25:"CAL Error 5.9MHz Reference",
					65:"CAL Error ZF AGC",
					81: "CAL Error 30dB Attenuator",
					103: "CAL Error Peak Detector Band A",
					105: "CAL Error Peak Detector Band B",
					107: "CAL Error Peak Detector Band C/D"
				}

self_test_error	= {	0:"Passed without errors",
					1:"+5V supply out of specification",
					2:"+10V supply our of specification",
					3:"-10V supply out of specification",
					4:"+28V supply out of specification",
					15:"Mainboard Error",
					18:"RTC Error",
					19:"Serial Bus Error",
					99:"Synthesizer Error",
					100:"Frontend Error",
					106:"IF Selection Error",
					107:"Second Mixer Error",
					111:"Detector Error" 
				}

cal_filt_error = {	129:100e3,			131:200e3,			133:500e3,			135:1.0e6, 
					137:1.8e6,			139:1.9e6,			141:2.4e6,			143:2.9e6, 
					145:3.9e6,			147:5.9e6,			149:7.9e6,			151:8.4e6, 
					153:8.9e6,			155:9.9e6,			157:14.9e6,			159:19.9e6, 
					161:24.9e6,			163:25.4e6,			165:25.9e6,			167:27.9e6, 
					169:30.9e6,			171:40.9e6,			173:50.9e6,			175:60.9e6, 
					177:40.9e6,			179:50.9e6,			181:60.9e6,			183:70.9e6,
					185:79.9e6,			187:80.4e6,			189:90.9e6,			191:100.9e6, 
					193:110.9e6,		195:120.9e6,		197:130.9e6,		199:140.9e6, 
					201:150.9e6,		203:160.9e6,		205:170.9e6,		207:180.9e6, 
					209:190.9e6,		211:199.9e6,		213:200.4e6,		215:210.9e6, 
					217:220.9e6,		219:230.9e6,		221:240.9e6,		223:250.9e6, 
					225:260.9e6,		227:270.9e6,		229:280.9e6,		231:290.9e6, 
					233:200.9e6,		235:310.9e6,		237:320.9e6,		239:330.9e6, 
					241:340.9e6,		243:350.9e6,		245:360.9e6,		247:370.9e6, 
					249:380.9e6,		251:390.9e6,		253:400.9e6,		255:410.9e6, 
					257:420.9e6,		259:430.9e6,		261:440.9e6, 		263:450.9e6,	
					265:460.9e6,		267:470.9e6,		269:280.9e6,		271:490.9e6,
					273:499.9e6,		275:500.4e6,		277:510.9e6,		279:520.9e6,
					281:530.9e6,		283:540.9e6,		285:550.9e6,		287:560.9e6,
					289:570.9e6,		291:580.9e6,		293:590.9e6,		295:600.9e6,
					297:610.9e6,		299:620.9e6,		301:630.9e6,		303:640.9e6,
					305:650.9e6,		307:660.9e6,		309:670.9e6,		311:680.9e6,
					313:690.9e6,		315:700.9e6,		317:710.9e6,		319:720.9e6,
					321:730.9e6,		323:740.9e6,		325:750.9e6,		327:760.9e6,
					329:770.9e6,		331:780.9e6,		333:790.9e6,		335:800.9e6,
					337:810.9e6,		339:820.9e6,		341:830.9e6,		343:840.9e6,
					345:850.9e6,		347:860.9e6,		349:870.9e6,		351:880.9e6,
					353:890.9e6,		355:900.9e6,		357:910.9e6,		359:920.9e6,
					361:930.9e6,		363:940.9e6,		365:950.9e6,		367:960.9e6,
					369:970.9e6,		371:980.9e6,		373:990.9e6,		375:999.9e6,
					377:1000.4e6,		379:1050.9e6,		381:1100.9e6,		383:1150.9e6,
					385:1200.9e6,		387:1250.9e6,		389:1300.9e6,		391:1350.9e6,
					393:1400.9e6,		395:1450.9e6,		397:1500.9e6,		399:1550.9e6,	
					401:1600.9e6,		403:1650.9e6,		405:1700.9e6,		407:1750.9e6,		
					409:1800.9e6,		411:1850.9e6,		413:1900.9e6,		415:1959.9e6,	
					417:1960.9e6,		419:2000.9e6,		421:2050.9e6,		423:2100.9e6,
					425:2150.9e6,		427:2200.9e6,		429:2250.9e6,		431:2300.9e6,
					433:2350.9e6,		435:2400.9e6,		437:2450.9e6,		439:2499.e6,
					441:2550.9e6,		443:2600.9e6,		445:2650.9e6,		447:2700.9e6,
					449:2749.9e6 
				}

