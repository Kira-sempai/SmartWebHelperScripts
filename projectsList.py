
from scripts.project import Project, Device

def getAvailableProjectsList():
	return [
		Project('SW1',         'stdc'        , 'SmartWeb S'    , Device('STDC'    , 'S20' , 3), 'rom'),
		Project('SW1_special', 'stdc_lin'    , 'SmartWeb S LIN', Device('STDC_LIN', 'S28' , 3), 'rom'),
		Project('SW1',         'ltdc'        , 'SmartWeb L'    , Device('LTDC'    , 'S40' , 3), 'rom'),
		Project('SW1',         'ltdc_s45'    , 'SmartWeb L2'   , Device('LTDC_S45', 'S45' , 1), 'rom'),
		Project('SW2',         'ltdc_s45_l4' , 'SmartWeb L3'   , Device('LTDC_S45_L4', 'S45' , 1, 4, False, 'cubemx', 'stm32l4x.cfg'), 'rom'),
		Project('Other',       'swndin'      , 'SmartWeb N'    , Device('SWNDIN'  , 'S41N', 1), 'rom'),
		
		Project('SW2_deprecated', 'DataLogger'       , 'DataLogger'        , Device('DL'    , 'L30', None, 1, True), 'rom'),
		Project('SW2',            'DataLoggerSW'     , 'DataLogger SW'     , Device('DL_SW' , 'L30', None, 1, True), 'rom'),
		Project('SW2',            'DataLoggerKSE'    , 'DataLogger KSE'    , Device('DL_KSE', 'L30', None, 1, True), 'rom'),
		
		Project('SW2', 'disco'       , 'SmartWeb Disco', Device('DISCO'   , '32F746GDISCOVERY',    1, 1, True, 'stm32', 'stm32f7x.cfg')),
		Project('SW2', 'xhcc'        , 'SmartWeb X'    , Device('XHCC'    , 'S61'             ,    2, 1, True, 'stm32', 'stm32f2x.cfg')),
		Project('SW2', 'xhcc_s62'    , 'SmartWeb X2'   , Device('XHCC-S62', 'S62'             ,    2, 1, True, 'stm32', 'stm32f2x.cfg')),
		Project('Other', 'xhcc_s62_unitTest', 'SmartWeb X2 Unit Test', Device('XHCC-S62', 'S62',   2, 1, True, 'stm32', 'stm32f2x.cfg')),
		
		Project('SW2', 'swk'     , 'SmartWeb K'     , Device('SWK', 'SW-N2', 1, None, True, 'stm32', 'stm32f2x.cfg'), 'west', 'old', False, 'OID_HLOGO'),
		Project('SW2', 'swk_base', 'SmartWeb K Base', Device('SWK', 'SW-N2', 1, None, False, 'stm32', 'stm32f2x.cfg'), 'west', 'old', False, 'OID_HLOGO'),
		Project('Other', 'swk_unitTest', 'SmartWeb K UnitTest', Device('SWK', 'SW-N2', 1, None, False, 'stm32', 'stm32f2x.cfg'), 'west', 'old', False, 'OID_HLOGO'),
		
		Project('SW2', 'swk_at32', 'SmartWeb K2', Device('SWK2', 'SW-N3', 1, None, True, 'at32', 'at32f4x.cfg'), 'west', 'old', False, 'OID_HLOGO'),
		
		Project('Caleon', 'caleon_clima', 'Caleon'        , Device('caleon_clima', 'RC40',    1, None, False, 'stm32n'), 'rom', 'new'),
		Project('Other',  'caleon_brv'  , 'Caleon BRV'    , Device('caleon_brv'  , 'RC50', None, None, False, 'stm32n'), 'rom', 'new'),
		Project('Other',  'domvs'       , 'Domvs'         , Device('Domvs'       , 'RC40', None, None, False, 'stm32n'), 'rom', 'new'),
		
		Project('Other',  'caleon_clima_smart_controller'    , 'Caleon SW', Device('caleon_clima_smart_controller'    , 'RC50', None, None, False, 'cubemx', 'stm32f7x.cfg'), 'rom', 'new'),
		Project('Other',  'caleon_clima_smart_web_controller', 'Caleon SW', Device('SmartWeb-Caleon', 'RC50', 1, None, False, 'cubemx', 'stm32f7x.cfg'), 'rom', 'new', False, 'OID_HYDROLOGO'),
		Project('Other', 'caleonbox_clima'   , 'CaleonBox'         , Device('caleonbox_clima', 'S70', 1, None, False, 'cubemx', 'stm32f2x.cfg', True), 'rom', 'new', False, 'OID_SOREL'),
		Project('SW4', 'caleonbox_smartweb', 'CaleonBox SmartWeb', Device('caleonbox_sw'   , 's70', 1, None, False, 'cubemx', 'stm32f2x.cfg', True), 'rom', 'new', False, 'OID_HYDROLOGO'),
		Project('SW4', 'caleon_sw_base'  , 'Caleon Base'  , Device('caleon_sw_base'  , 'rc50', 1, None, False, 'cubemx', 'stm32f7x.cfg'), 'rom', 'new', False, 'OID_HYDROLOGO'),
		Project('SW4', 'caleon_sw_clima' , 'Caleon Clima' , Device('caleon_sw_clima' , 'rc50', 1, None, False, 'cubemx', 'stm32f7x.cfg'), 'rom', 'new', False, 'OID_HYDROLOGO'),
		Project('SW4', 'caleon_sw_master', 'Caleon Master', Device('caleon_sw_master', 'rc50', 1, None, False, 'cubemx', 'stm32f7x.cfg'), 'rom', 'new', False, 'OID_HYDROLOGO'),
		
		Project('Other',  'tece_floor', 'Caleon TECE', Device('tece_floor', 'RC50', None, None, False, 'cubemx'), 'rom', 'new'),
		Project('Other',  'tece_floor_clima_smart', 'Caleon TECE Clima', Device('tece_floor', 'RC50', None, None, False, 'cubemx'), 'rom', 'new'),
		
		Project('Other', 'lfwc'                 , 'LFWC'              , Device('LFWC'       , 'S40', None, None, False, 'stm32'), 'rom'),
		Project('Other', 'lfwc_mt_v01'          , 'LFWC'              , Device('LFWC-MT-V01', 'S40', None, None, False, 'stm32'), 'rom'),
		Project('Other', 'lfwc_mt_v02'          , 'LFWC'              , Device('LFWC-MT-V02', 'S40', None, None, False, 'stm32'), 'rom'),
		Project('Other', 'lfwc_mt_s47'          , 'LFWC'              , Device('LFWC-MT-S47', 'S47', None, None, False, 'stm32'), 'rom'),
		Project('Other', 'lfwc_mt_s47_unitTest' , 'LFWC Unit Test'    , Device('LFWC-MT-S47', 'S47', None, None, False, 'stm32'), 'rom'),
		Project('Other', 'charlie'              , 'CHARLIE'           , Device('CHARLIE'    , 'S48',    1, None, False, 'stm32'), 'rom', 'old', False, 'OID_Kemper'),
		Project('Other', 'charlie_runTimeTest'  , 'CHARLIE Runtime Test', Device('CHARLIE'    , 'S48',    1, None, False, 'stm32'), 'rom', 'old', False, 'OID_Kemper'),
		Project('Other', 'charlie_unitTest'     , 'CHARLIE Unit Test' , Device('CHARLIE'    , 'S48',    1, None, False, 'stm32'), 'rom', 'old', False, 'OID_Kemper'),

		Project('Other', 'DataLoggerCharlie'            , 'DataLogger Charlie'             , Device('DataLoggerCharlie' , 'L30', None, None, False, 'stm32'), 'rom', 'old', False, 'OID_SOREL'),
		Project('Other', 'DataLoggerCharlie_unitTest'   , 'DataLogger Charlie Unit Test'   , Device('DataLoggerCharlie' , 'L30', None, None, False, 'stm32'), 'rom', 'old', False, 'OID_SOREL'),
		Project('Other', 'DataLoggerCharlie_runTimeTest', 'DataLogger Charlie Runtime Test', Device('DataLoggerCharlie' , 'L30', None, None, False, 'stm32'), 'rom', 'old', False, 'OID_SOREL'),
	]
