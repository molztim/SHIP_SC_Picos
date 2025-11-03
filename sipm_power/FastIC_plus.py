# Bibliotheken laden
import machine
import network 
import utime as time
import binascii
import ubinascii

from machine import I2C, Pin
import struct

# Strucutre:
# DATA is saved in the order of the alpahbetically sorted register name
# DATA is saved in UTF-8
# Files are like: <REGISTER_NAME> = <VALUE>

# Register: "Name" : [Register, position of first bit,length of register]
fastic_registers = {
"ASIC_MAJOR_VER" : [127, 4, 4],
"ASIC_MINOR_VER" : [127, 0, 4],
"COMP_ClusterTrg_Enable" : [59, 7, 1],
"COMP_ClusterTrg_ITHCAL" : [59, 0, 7],
"COMP_Time_Enable" : [38, 7, 1],
"COMP_Time_Global_ITH" : [38, 0, 6],
"COMP_Time_Global_ITH_ILSB" : [40, 0, 6],
"COMP_Time_ITHCAL_CH0" : [43, 0, 7],
"COMP_Time_ITHCAL_CH1" : [44, 0, 7],
"COMP_Time_ITHCAL_CH2" : [45, 0, 7],
"COMP_Time_ITHCAL_CH3" : [46, 0, 7],
"COMP_Time_ITHCAL_CH4" : [47, 0, 7],
"COMP_Time_ITHCAL_CH5" : [48, 0, 7],
"COMP_Time_ITHCAL_CH6" : [49, 0, 7],
"COMP_Time_ITHCAL_CH7" : [50, 0, 7],
"COMP_Time_ITH_ILSB" : [41, 0, 6],
"COMP_Trg_Enable" : [39, 7, 1],
"COMP_Trg_Global_ITH" : [39, 0, 6],
"COMP_Trg_Global_ITH_ILSB" : [104, 0, 6],
"COMP_Trg_ITHCAL_CH0" : [51, 0, 7],
"COMP_Trg_ITHCAL_CH1" : [52, 0, 7],
"COMP_Trg_ITHCAL_CH2" : [53, 0, 7],
"COMP_Trg_ITHCAL_CH3" : [54, 0, 7],
"COMP_Trg_ITHCAL_CH4" : [55, 0, 7],
"COMP_Trg_ITHCAL_CH5" : [56, 0, 7],
"COMP_Trg_ITHCAL_CH6" : [57, 0, 7],
"COMP_Trg_ITHCAL_CH7" : [58, 0, 7],
"COMP_Trg_ITH_ILSB" : [42, 0, 6],
"ECOMP_EnablePD" : [74, 7, 1],
"ECOMP_Ibias" : [74, 0, 4],
"ECOMP_Mode" : [74, 6, 1],
"ECOMP_SelInput" : [74, 4, 2],
"ECOMP_VTH_CH0" : [75, 0, 8],
"ECOMP_VTH_CH1" : [76, 0, 8],
"ECOMP_VTH_CH2" : [77, 0, 8],
"ECOMP_VTH_CH3" : [78, 0, 8],
"ECOMP_VTH_CH4" : [79, 0, 8],
"ECOMP_VTH_CH5" : [80, 0, 8],
"ECOMP_VTH_CH6" : [81, 0, 8],
"ECOMP_VTH_CH7" : [82, 0, 8],
"ENABLE_CH0" : [1, 0, 1],
"ENABLE_CH1" : [1, 1, 1],
"ENABLE_CH2" : [1, 2, 1],
"ENABLE_CH3" : [1, 3, 1],
"ENABLE_CH4" : [1, 4, 1],
"ENABLE_CH5" : [1, 5, 1],
"ENABLE_CH6" : [1, 6, 1],
"ENABLE_CH7" : [1, 7, 1],
"ENABLE_TestInput_CH0" : [2, 0, 1],
"ENABLE_TestInput_CH1" : [2, 1, 1],
"ENABLE_TestInput_CH2" : [2, 2, 1],
"ENABLE_TestInput_CH3" : [2, 3, 1],
"ENABLE_TestInput_CH4" : [2, 4, 1],
"ENABLE_TestInput_CH5" : [2, 5, 1],
"ENABLE_TestInput_CH6" : [2, 6, 1],
"ENABLE_TestInput_CH7" : [2, 7, 1],
"FE_Enable" : [19, 7, 1],
"FE_EnergyGain" : [9, 6, 2],
"FE_Input_CAP" : [9, 3, 3],
"FE_IntComp_CAP" : [9, 0, 3],
"FE_NEG_FastInv_Energy" : [8, 0, 1],
"FE_NEG_FastInv_Time" : [8, 1, 1],
"FE_NEG_Ibias_LvlShifter" : [11, 0, 4],
"FE_NEG_Ibias_Main" : [10, 0, 4],
"FE_NEG_Ibias_PVTCalc" : [12, 0, 4],
"FE_NEG_LvlShifter_BiasMode" : [20, 6, 1],
"FE_NEG_LvlShifter_W" : [8, 2, 3],
"FE_NEG_Vd" : [18, 0, 8],
"FE_NEG_VinDC_Replica" : [14, 0, 8],
"FE_NEG_VrefEnergyInv" : [20, 0, 6],
"FE_NEG_VxInt" : [16, 0, 8],
"FE_POS_Ibias_LvlShifter" : [11, 4, 4],
"FE_POS_Ibias_Main" : [10, 4, 4],
"FE_POS_Ibias_PVTCalc" : [12, 4, 4],
"FE_POS_LvlShifter_BiasMode" : [19, 6, 1],
"FE_POS_LvlShifter_W" : [8, 5, 3],
"FE_POS_Vd" : [17, 0, 8],
"FE_POS_VinDC_Replica" : [13, 0, 8],
"FE_POS_VinLim" : [19, 0, 6],
"FE_POS_VxInt" : [15, 0, 8],
"FE_VinDC_NEG_CH0" : [29, 0, 8],
"FE_VinDC_NEG_CH1" : [30, 0, 8],
"FE_VinDC_NEG_CH2" : [31, 0, 8],
"FE_VinDC_NEG_CH3" : [32, 0, 8],
"FE_VinDC_NEG_CH4" : [33, 0, 8],
"FE_VinDC_NEG_CH5" : [34, 0, 8],
"FE_VinDC_NEG_CH6" : [35, 0, 8],
"FE_VinDC_NEG_CH7" : [36, 0, 8],
"FE_VinDC_POS_CH0" : [21, 0, 8],
"FE_VinDC_POS_CH1" : [22, 0, 8],
"FE_VinDC_POS_CH2" : [23, 0, 8],
"FE_VinDC_POS_CH3" : [24, 0, 8],
"FE_VinDC_POS_CH4" : [25, 0, 8],
"FE_VinDC_POS_CH5" : [26, 0, 8],
"FE_VinDC_POS_CH6" : [27, 0, 8],
"FE_VinDC_POS_CH7" : [28, 0, 8],
"FSM_Armed_Timer" : [91, 3, 5],
"FSM_Debug_Enable" : [90, 1, 1],
"FSM_GPIO_Rst_Enable" : [90, 2, 1],
"FSM_Hold_Delay" : [90, 3, 2],
"FSM_Probe_Enable" : [90, 0, 1],
"FSM_Probe_Sel" : [92, 3, 5],
"FSM_Rst_Timer" : [92, 0, 3],
"FSM_Shaper_Delay" : [91, 0, 3],
"FSM_Timeout" : [93, 0, 8],
"GPOTA_Ibias_OTAFold_SuperFast_NMOS" : [6, 4, 4],
"GPOTA_Ibias_OTARR" : [7, 0, 4],
"GPOTA_Ibias_OTAb_NMOS" : [4, 0, 4],
"GPOTA_Ibias_OTAb_PMOS" : [4, 4, 4],
"GPOTA_Ibias_OTAb_SuperFast_PMOS" : [5, 0, 4],
"GPOTA_Ibias_OTAb_SuperSlow" : [5, 4, 4],
"GPOTA_Ibias_OTAsym_LFF_NMOS" : [6, 0, 4],
"I2C_SoftReset_Enable" : [89, 7, 1],
"IBUFFER_Ibias" : [37, 4, 4],
"Mode" : [0, 5, 2],
"OUT_ABUFF_Ccomp" : [95, 4, 3],
"OUT_ABUFF_Ibias_OTA" : [95, 0, 4],
"OUT_ABUFF_SignalSel" : [94, 0, 2],
"OUT_CMOS_DriveStr" : [94, 2, 2],
"OUT_DrvMode_CH0" : [97, 0, 2],
"OUT_DrvMode_CH1" : [97, 2, 2],
"OUT_DrvMode_CH2" : [97, 4, 2],
"OUT_DrvMode_CH3" : [97, 6, 2],
"OUT_DrvMode_CH4" : [98, 0, 2],
"OUT_DrvMode_CH5" : [98, 2, 2],
"OUT_DrvMode_CH6" : [98, 4, 2],
"OUT_DrvMode_CH7" : [98, 6, 2],
"OUT_Enable" : [95, 7, 1],
"OUT_EnergyToTEn_CH0" : [100, 0, 1],
"OUT_EnergyToTEn_CH1" : [100, 1, 1],
"OUT_EnergyToTEn_CH2" : [100, 2, 1],
"OUT_EnergyToTEn_CH3" : [100, 3, 1],
"OUT_EnergyToTEn_CH4" : [100, 4, 1],
"OUT_EnergyToTEn_CH5" : [100, 5, 1],
"OUT_EnergyToTEn_CH6" : [100, 6, 1],
"OUT_EnergyToTEn_CH7" : [100, 7, 1],
"OUT_EnergyZeroSupp" : [96, 7, 1],
"OUT_SLVDS_DriveStr" : [94, 4, 3],
"OUT_TimeNonLin" : [94, 7, 1],
"OUT_TimeToTEn_CH0" : [99, 0, 1],
"OUT_TimeToTEn_CH1" : [99, 1, 1],
"OUT_TimeToTEn_CH2" : [99, 2, 1],
"OUT_TimeToTEn_CH3" : [99, 3, 1],
"OUT_TimeToTEn_CH4" : [99, 4, 1],
"OUT_TimeToTEn_CH5" : [99, 5, 1],
"OUT_TimeToTEn_CH6" : [99, 6, 1],
"OUT_TimeToTEn_CH7" : [99, 7, 1],
"OUT_ToTPolarity_CH0" : [101, 0, 1],
"OUT_ToTPolarity_CH1" : [101, 1, 1],
"OUT_ToTPolarity_CH2" : [101, 2, 1],
"OUT_ToTPolarity_CH3" : [101, 3, 1],
"OUT_ToTPolarity_CH4" : [101, 4, 1],
"OUT_ToTPolarity_CH5" : [101, 5, 1],
"OUT_ToTPolarity_CH6" : [101, 6, 1],
"OUT_ToTPolarity_CH7" : [101, 7, 1],
"PAD_CLK_PullDownEn" : [102, 3, 1],
"PAD_CLK_Term100" : [102, 2, 1],
"PAD_FSMO_Enable" : [102, 5, 1],
"PAD_SDA_DrvStren" : [102, 0, 1],
"PAD_SDA_PullupEnable" : [102, 1, 1],
"PAD_TRGO_DrvStren" : [102, 6, 1],
"PAD_TRGO_Enable" : [102, 7, 1],
"PDH_Chold" : [69, 0, 3],
"PDH_Enable" : [69, 7, 1],
"PDH_Ibias_OTA" : [70, 4, 4],
"PDH_Idschg" : [70, 0, 4],
"PDH_Mode" : [69, 6, 1],
"PDH_Vbaseline" : [71, 0, 6],
"PDH_VcascN_OTA" : [72, 0, 6],
"PDH_VcascP_OTA" : [73, 0, 6],
"PLL_C1CP" : [167, 3, 3],
"PLL_C2SmallCP" : [168, 0, 3],
"PLL_ClockFsmSel" : [185, 0, 3],
"PLL_ClockSerSel" : [185, 3, 3],
"PLL_DelayFall[0]" : [177, 0, 4],
"PLL_DelayFall[10]" : [182, 0, 4],
"PLL_DelayFall[11]" : [182, 4, 4],
"PLL_DelayFall[12]" : [183, 0, 4],
"PLL_DelayFall[13]" : [183, 4, 4],
"PLL_DelayFall[14]" : [184, 0, 4],
"PLL_DelayFall[15]" : [184, 4, 4],
"PLL_DelayFall[1]" : [177, 4, 4],
"PLL_DelayFall[2]" : [178, 0, 4],
"PLL_DelayFall[3]" : [178, 4, 4],
"PLL_DelayFall[4]" : [179, 0, 4],
"PLL_DelayFall[5]" : [179, 4, 4],
"PLL_DelayFall[6]" : [180, 0, 4],
"PLL_DelayFall[7]" : [180, 4, 4],
"PLL_DelayFall[8]" : [181, 0, 4],
"PLL_DelayFall[9]" : [181, 4, 4],
"PLL_DelayRise[0]" : [169, 0, 4],
"PLL_DelayRise[10]" : [174, 0, 4],
"PLL_DelayRise[11]" : [174, 4, 4],
"PLL_DelayRise[12]" : [175, 0, 4],
"PLL_DelayRise[13]" : [175, 4, 4],
"PLL_DelayRise[14]" : [176, 0, 4],
"PLL_DelayRise[15]" : [176, 4, 4],
"PLL_DelayRise[1]" : [169, 4, 4],
"PLL_DelayRise[2]" : [170, 0, 4],
"PLL_DelayRise[3]" : [170, 4, 4],
"PLL_DelayRise[4]" : [171, 0, 4],
"PLL_DelayRise[5]" : [171, 4, 4],
"PLL_DelayRise[6]" : [172, 0, 4],
"PLL_DelayRise[7]" : [172, 4, 4],
"PLL_DelayRise[8]" : [173, 0, 4],
"PLL_DelayRise[9]" : [173, 4, 4],
"PLL_Enable" : [167, 7, 1],
"PLL_IcpCurrent" : [167, 0, 3],
"PLL_LockingCounterLock" : [187, 0, 8],
"PLL_LockingCounterMax" : [186, 0, 8],
"PLL_LockingCounterUnlock" : [188, 0, 8],
"PLL_RCP" : [168, 3, 3],
"PZ_CAP" : [65, 4, 4],
"PZ_Enable" : [64, 7, 1],
"PZ_IoffsetSh" : [65, 0, 4],
"PZ_RES" : [64, 0, 6],
"Polarity" : [0, 7, 1],
"RAMP_Conv_Cap" : [83, 4, 3],
"RAMP_Conv_Iref" : [83, 0, 3],
"RAMP_Ibias_OTA" : [85, 0, 4],
"RAMP_SHTimer_Cap" : [84, 4, 3],
"RAMP_SHTimer_Iref" : [84, 0, 3],
"RAMP_VTH_EoC" : [86, 0, 8],
"RAMP_VTH_EoS" : [88, 0, 8],
"RAMP_VTH_SoC" : [87, 0, 8],
"RAMP_Vbaseline" : [89, 0, 6],
"REF_AdjustGlobalLSB" : [3, 0, 8],
"REF_VBGMode" : [7, 6, 2],
"SH_CAP_LPF1" : [66, 0, 4],
"SH_CAP_LPF2" : [67, 4, 4],
"SH_Enable" : [66, 7, 1],
"SH_Gain" : [66, 5, 1],
"SH_Ibias_OTA" : [67, 0, 4],
"SH_Rout" : [66, 6, 1],
"SH_VoutDC" : [68, 0, 8],
"TDC_ArbModeRR" : [133, 7, 1],
"TDC_AuroraCBCooldown" : [160, 0, 24],
"TDC_AuroraCBCooldown" : [159, 0, 36],
"TDC_AuroraCBCooldown" : [161, 0, 8],
"TDC_AuroraCBLength" : [157, 0, 24],
"TDC_AuroraCBLength" : [154, 4, 36],
"TDC_AuroraCBLength" : [158, 0, 8],
"TDC_AuroraCBWait" : [152, 0, 24],
"TDC_AuroraCBWait" : [149, 4, 36],
"TDC_AuroraCBWait" : [153, 0, 8],
"TDC_AuroraCCLength" : [155, 0, 24],
"TDC_AuroraCCLength" : [154, 0, 36],
"TDC_AuroraCCLength" : [156, 0, 8],
"TDC_AuroraCCWait" : [150, 0, 24],
"TDC_AuroraCCWait" : [149, 0, 36],
"TDC_AuroraCCWait" : [151, 0, 8],
"TDC_AuroraInitWait" : [159, 4, 4],
"TDC_AuroraMaxFrameSize" : [162, 0, 8],
"TDC_AuroraScramblingEn" : [137, 7, 1],
"TDC_CalibSrcExt" : [130, 3, 1],
"TDC_ChanBlockEn[0]" : [128, 0, 1],
"TDC_ChanBlockEn[1]" : [128, 1, 1],
"TDC_ChanBlockEn[2]" : [128, 2, 1],
"TDC_ChanBlockEn[3]" : [128, 3, 1],
"TDC_ChanBlockEn[4]" : [128, 4, 1],
"TDC_ChanBlockEn[5]" : [128, 5, 1],
"TDC_ChanBlockEn[6]" : [128, 6, 1],
"TDC_ChanBlockEn[7]" : [128, 7, 1],
"TDC_ChanCalibEn[0]" : [129, 0, 1],
"TDC_ChanCalibEn[1]" : [129, 1, 1],
"TDC_ChanCalibEn[2]" : [129, 2, 1],
"TDC_ChanCalibEn[3]" : [129, 3, 1],
"TDC_ChanCalibEn[4]" : [129, 4, 1],
"TDC_ChanCalibEn[5]" : [129, 5, 1],
"TDC_ChanCalibEn[6]" : [129, 6, 1],
"TDC_ChanCalibEn[7]" : [129, 7, 1],
"TDC_CoarseExtForce" : [137, 6, 1],
"TDC_CoarseExtPeriod" : [147, 5, 3],
"TDC_DebugMode" : [146, 5, 1],
"TDC_EnergyMaxPW" : [139, 0, 22],
"TDC_EnergyMaxPW" : [138, 0, 8],
"TDC_EnergyMinPW" : [137, 0, 22],
"TDC_EnergyMinPW" : [136, 0, 8],
"TDC_EnergyOptBW" : [143, 7, 1],
"TDC_FifoUnlockTh" : [148, 0, 6],
"TDC_MuxOut_Sel" : [130, 5, 3],
"TDC_SLVDS_DriveStr" : [189, 0, 3],
"TDC_SerializerIdleForce" : [135, 7, 1],
"TDC_SerializerIdleWord" : [165, 0, 24],
"TDC_SerializerIdleWord" : [164, 0, 40],
"TDC_SerializerIdleWord" : [163, 0, 56],
"TDC_SerializerIdleWord" : [166, 0, 8],
"TDC_SkewEn" : [146, 7, 1],
"TDC_SkewFwd" : [146, 6, 1],
"TDC_SkewShift" : [146, 0, 5],
"TDC_SmallBin" : [133, 6, 1],
"TDC_StatisticsPeriod" : [147, 0, 5],
"TDC_TimeEnergyMaxDeltaT" : [145, 0, 24],
"TDC_TimeEnergyMaxDeltaT" : [144, 0, 8],
"TDC_TimeMaxPW" : [135, 0, 22],
"TDC_TimeMaxPW" : [134, 0, 8],
"TDC_TimeMinPW" : [133, 0, 22],
"TDC_TimeMinPW" : [132, 0, 8],
"TDC_TrgValDelay" : [131, 2, 3],
"TDC_TrgValEn" : [131, 0, 1],
"TDC_TrgValSrcExt" : [131, 1, 1],
"TDC_TrgValWindow" : [131, 5, 3],
"TDC_TrigBlockEn" : [130, 0, 1],
"TDC_TrigCalibEn" : [130, 1, 1],
"TDC_TrigEnergyIgnore" : [143, 6, 1],
"TDC_TrigMaxPW" : [143, 0, 22],
"TDC_TrigMaxPW" : [142, 0, 8],
"TDC_TrigMinPW" : [141, 0, 22],
"TDC_TrigMinPW" : [140, 0, 8],
"TDC_TrigSrcExt" : [130, 2, 1],
"TEST_ABUFF_Ccomp" : [96, 4, 3],
"TEST_ABUFF_Ibias_OTA" : [96, 0, 4],
"TIA_CF" : [62, 4, 4],
"TIA_Enable" : [60, 7, 1],
"TIA_Ibias_OTA" : [62, 0, 4],
"TIA_RF" : [61, 0, 3],
"TIA_Replica_Enable" : [60, 6, 1],
"TIA_VinDC" : [63, 0, 8],
"TIA_VoutDCRel" : [60, 0, 6],
"TIME_MuxOut_Sel" : [103, 0, 2],
"TIME_SLVDS_DriveStr" : [90, 5, 3],
"TRG_Conv_Sel" : [103, 5, 2],
"TRG_ExtIn_Polarity" : [103, 7, 1],
"TRG_MuxOut_Sel" : [103, 2, 3],
"VMON_Sel" : [0, 0, 5],
}

alpha_keylist = ["ASIC_MAJOR_VER","ASIC_MINOR_VER","COMP_ClusterTrg_Enable","COMP_ClusterTrg_ITHCAL","COMP_Time_Enable","COMP_Time_Global_ITH","COMP_Time_ITHCAL_CH0","COMP_Time_ITHCAL_CH1","COMP_Time_ITHCAL_CH2","COMP_Time_ITHCAL_CH3","COMP_Time_ITHCAL_CH4","COMP_Time_ITHCAL_CH5","COMP_Time_ITHCAL_CH6","COMP_Time_ITHCAL_CH7","COMP_Time_ITH_ILSB","COMP_Trg_Enable","COMP_Trg_Global_ITH","COMP_Trg_ITHCAL_CH0","COMP_Trg_ITHCAL_CH1","COMP_Trg_ITHCAL_CH2","COMP_Trg_ITHCAL_CH3","COMP_Trg_ITHCAL_CH4","COMP_Trg_ITHCAL_CH5","COMP_Trg_ITHCAL_CH6","COMP_Trg_ITHCAL_CH7","COMP_Trg_ITH_ILSB","ECOMP_EnablePD","ECOMP_Ibias","ECOMP_Mode","ECOMP_SelInput","ECOMP_VTH_CH0","ECOMP_VTH_CH1","ECOMP_VTH_CH2","ECOMP_VTH_CH3","ECOMP_VTH_CH4","ECOMP_VTH_CH5","ECOMP_VTH_CH6","ECOMP_VTH_CH7","ENABLE_CH0","ENABLE_CH1","ENABLE_CH2","ENABLE_CH3","ENABLE_CH4","ENABLE_CH5","ENABLE_CH6","ENABLE_CH7","ENABLE_TestInput_CH0","ENABLE_TestInput_CH1","ENABLE_TestInput_CH2","ENABLE_TestInput_CH3","ENABLE_TestInput_CH4","ENABLE_TestInput_CH5","ENABLE_TestInput_CH6","ENABLE_TestInput_CH7","FE_Enable","FE_EnergyGain","FE_Input_CAP","FE_IntComp_CAP","FE_NEG_FastInv_Energy","FE_NEG_FastInv_Time","FE_NEG_Ibias_LvlShifter","FE_NEG_Ibias_Main","FE_NEG_Ibias_PVTCalc","FE_NEG_LvlShifter_BiasMode","FE_NEG_LvlShifter_W","FE_NEG_Vd","FE_NEG_VinDC_Replica","FE_NEG_VrefEnergyInv","FE_NEG_VxInt","FE_POS_Ibias_LvlShifter","FE_POS_Ibias_Main","FE_POS_Ibias_PVTCalc","FE_POS_LvlShifter_BiasMode","FE_POS_LvlShifter_W","FE_POS_Vd","FE_POS_VinDC_Replica","FE_POS_VinLim","FE_POS_VxInt","FE_VinDC_NEG_CH0","FE_VinDC_NEG_CH1","FE_VinDC_NEG_CH2","FE_VinDC_NEG_CH3","FE_VinDC_NEG_CH4","FE_VinDC_NEG_CH5","FE_VinDC_NEG_CH6","FE_VinDC_NEG_CH7","FE_VinDC_POS_CH0","FE_VinDC_POS_CH1","FE_VinDC_POS_CH2","FE_VinDC_POS_CH3","FE_VinDC_POS_CH4","FE_VinDC_POS_CH5","FE_VinDC_POS_CH6","FE_VinDC_POS_CH7","FSM_Armed_Timer","FSM_Debug_Enable","FSM_GPIO_Rst_Enable","FSM_Hold_Delay","FSM_Probe_Enable","FSM_Probe_Sel","FSM_Rst_Timer","FSM_Shaper_Delay","FSM_Timeout","GPOTA_Ibias_OTAFold_SuperFast_NMOS","GPOTA_Ibias_OTARR","GPOTA_Ibias_OTAb_NMOS","GPOTA_Ibias_OTAb_PMOS","GPOTA_Ibias_OTAb_SuperFast_PMOS","GPOTA_Ibias_OTAb_SuperSlow","GPOTA_Ibias_OTAsym_LFF_NMOS","IBUFFER_Ibias","Mode","OUT_ABUFF_Ccomp","OUT_ABUFF_Ibias_OTA","OUT_ABUFF_SignalSel","OUT_CMOS_DriveStr","OUT_DrvMode_CH0","OUT_DrvMode_CH1","OUT_DrvMode_CH2","OUT_DrvMode_CH3","OUT_DrvMode_CH4","OUT_DrvMode_CH5","OUT_DrvMode_CH6","OUT_DrvMode_CH7","OUT_Enable","OUT_EnergyToTEn_CH0","OUT_EnergyToTEn_CH1","OUT_EnergyToTEn_CH2","OUT_EnergyToTEn_CH3","OUT_EnergyToTEn_CH4","OUT_EnergyToTEn_CH5","OUT_EnergyToTEn_CH6","OUT_EnergyToTEn_CH7","OUT_EnergyZeroSupp","OUT_SLVDS_DriveStr","OUT_TimeNonLin","OUT_TimeToTEn_CH0","OUT_TimeToTEn_CH1","OUT_TimeToTEn_CH2","OUT_TimeToTEn_CH3","OUT_TimeToTEn_CH4","OUT_TimeToTEn_CH5","OUT_TimeToTEn_CH6","OUT_TimeToTEn_CH7","OUT_ToTPolarity_CH0","OUT_ToTPolarity_CH1","OUT_ToTPolarity_CH2","OUT_ToTPolarity_CH3","OUT_ToTPolarity_CH4","OUT_ToTPolarity_CH5","OUT_ToTPolarity_CH6","OUT_ToTPolarity_CH7","PAD_CLK_PullDownEn","PAD_CLK_Term100","PAD_FSMO_Enable","PAD_SDA_DrvStren","PAD_SDA_PullupEnable","PAD_TRGO_DrvStren","PAD_TRGO_Enable","PDH_Chold","PDH_Enable","PDH_Ibias_OTA","PDH_Idschg","PDH_Mode","PDH_Vbaseline","PDH_VcascN_OTA","PDH_VcascP_OTA","PZ_CAP","PZ_Enable","PZ_IoffsetSh","PZ_RES","Polarity","RAMP_Conv_Cap","RAMP_Conv_Iref","RAMP_Ibias_OTA","RAMP_SHTimer_Cap","RAMP_SHTimer_Iref","RAMP_VTH_EoC","RAMP_VTH_EoS","RAMP_VTH_SoC","RAMP_Vbaseline","REF_AdjustGlobalLSB","SH_CAP_LPF1","SH_CAP_LPF2","SH_Enable","SH_Gain","SH_Ibias_OTA","SH_Rout","SH_VoutDC","TEST_ABUFF_Ccomp","TEST_ABUFF_Ibias_OTA","TIA_CF","TIA_Enable","TIA_Ibias_OTA","TIA_RF","TIA_Replica_Enable","TIA_VinDC","TIA_VoutDCRel","TIME_MuxOut_Sel","TIME_SLVDS_DriveStr","TRG_Conv_Sel","TRG_ExtIn_Polarity","TRG_MuxOut_Sel","VMON_Sel","COMP_Time_Global_ITH_ILSB","COMP_Trg_Global_ITH_ILSB","REF_VBGMode","I2C_SoftReset_Enable","PLL_C1CP","PLL_C2SmallCP","PLL_ClockFsmSel","PLL_ClockSerSel","PLL_DelayFall[0]","PLL_DelayFall[10]","PLL_DelayFall[11]","PLL_DelayFall[12]","PLL_DelayFall[13]","PLL_DelayFall[14]","PLL_DelayFall[15]","PLL_DelayFall[1]","PLL_DelayFall[2]","PLL_DelayFall[3]","PLL_DelayFall[4]","PLL_DelayFall[5]","PLL_DelayFall[6]","PLL_DelayFall[7]","PLL_DelayFall[8]","PLL_DelayFall[9]","PLL_DelayRise[0]","PLL_DelayRise[10]","PLL_DelayRise[11]","PLL_DelayRise[12]","PLL_DelayRise[13]","PLL_DelayRise[14]","PLL_DelayRise[15]","PLL_DelayRise[1]","PLL_DelayRise[2]","PLL_DelayRise[3]","PLL_DelayRise[4]","PLL_DelayRise[5]","PLL_DelayRise[6]","PLL_DelayRise[7]","PLL_DelayRise[8]","PLL_DelayRise[9]","PLL_Enable","PLL_IcpCurrent","PLL_LockingCounterLock","PLL_LockingCounterMax","PLL_LockingCounterUnlock","PLL_RCP","TDC_ArbModeRR","TDC_AuroraInitWait","TDC_AuroraMaxFrameSize","TDC_AuroraScramblingEn","TDC_CalibSrcExt","TDC_ChanBlockEn[0]","TDC_ChanBlockEn[1]","TDC_ChanBlockEn[2]","TDC_ChanBlockEn[3]","TDC_ChanBlockEn[4]","TDC_ChanBlockEn[5]","TDC_ChanBlockEn[6]","TDC_ChanBlockEn[7]","TDC_ChanCalibEn[0]","TDC_ChanCalibEn[1]","TDC_ChanCalibEn[2]","TDC_ChanCalibEn[3]","TDC_ChanCalibEn[4]","TDC_ChanCalibEn[5]","TDC_ChanCalibEn[6]","TDC_ChanCalibEn[7]","TDC_CoarseExtForce","TDC_CoarseExtPeriod","TDC_DebugMode","TDC_EnergyOptBW","TDC_FifoUnlockTh","TDC_MuxOut_Sel","TDC_SLVDS_DriveStr","TDC_SerializerIdleForce","TDC_SkewEn","TDC_SkewFwd","TDC_SkewShift","TDC_SmallBin","TDC_StatisticsPeriod","TDC_TrgValDelay","TDC_TrgValEn","TDC_TrgValSrcExt","TDC_TrgValWindow","TDC_TrigBlockEn","TDC_TrigCalibEn","TDC_TrigEnergyIgnore","TDC_TrigSrcExt","TDC_TimeMaxPW","TDC_TimeMinPW","TDC_EnergyMaxPW","TDC_EnergyMinPW","TDC_TrigMaxPW","TDC_TrigMinPW","TDC_TimeEnergyMaxDeltaT","TDC_AuroraCBCooldown","TDC_AuroraCBLength","TDC_AuroraCBWait","TDC_AuroraCCLength","TDC_AuroraCCWait","TDC_SerializerIdleWord"]

# The fastic class with all the necessary functions and informations to run FastIC+ communication
# The register lsit above is sorted like the devlopmend files from teh dev. board.
# Hence the FastIC registers (legacy) are in alphabeticly, afterwards the FastIC+ registers come alphabeticly
# list of all registers, with their position inside the fastic+. the length of the word and where it starts
# Alphakeylist is just a sorted list aof all keys. handy for loops
# FastIC is the main class whith the I2C interface to communicate with the FastIC+

class FastIC:

    def __init__(self, address,SDA,SCL):
        self.SDA = SDA
        self.SCL = SCL
        self.addr = address
        self.fastic_registers = fastic_registers
        self.alpha_keylist = alpha_keylist

        i2c_sda = Pin(self.SDA) 
        i2c_scl = Pin(self.SCL) 
        
        # On the Connector onboard the FastIC board are Pin9 SCL and Pin10 SDA. Pin9 Goes to Pin 32 / GPIO27 and Pin10 goes to Pin 31 to GPIO 26
        # SDA pin: 26
        # SCL pin: 27
        try:
            #TheFastIC requires 1MHz to run.
            self.i2c = I2C(1,sda=i2c_sda,scl=i2c_scl,freq=1000000)
        except:
            print("Error 01: Init error")
            
    def read_i2c(self,register,reglen=1):
        # The grassroot I2C communication function to read data from the line
        
        binary_register = struct.pack("B",register)
        self.i2c.writeto(self.addr,binary_register)
        rcv_data = self.i2c.readfrom(self.addr,reglen)
        #rcv_data = b'\xFF' #2A is 42
        return rcv_data
    
    def write_i2c(self,register,data):
        # The grassroot I2C communication function to write to the line
        
        binary_register = struct.pack("B",register)
        if type(data) != list:
            binary_data = struct.pack("B",data)
            buffer = binary_register + binary_data
        else:
            buffer = binary_register + struct.pack(f"{len(data)}B", *data)
        #print("WRTING BUFFER: ",buffer)
        self.i2c.writeto(self.addr,buffer)
        
    def read_fastic(self,register):
        # A function to capture the whish for a reading and the register
        reg_value, reg_position, reg_length = self.fastic_registers[register]
        bin_data = self.read_i2c(reg_value)
        #print("Bin data:",bin_data)
        #print("{0:b}".format(2**reg_length - 1 << reg_position))
        int_data = (bin_data[0] & (2**reg_length - 1 << reg_position)) >> reg_position # Takes binary data, creates a mask. The mask is a binary 1 with the length or reg_length, and moved to the right by reg_value
        return int_data
    
    def write_fastic(self, register, data):
        # A function to execute the writing process
        # First: Read back the value from the corresponding register
        reg_value, reg_position, reg_length = self.fastic_registers[register]
        bin_data = self.read_i2c(reg_value)
        data_shifted = data << reg_position
        mask_bin_data = (2**reg_length-1 << reg_position) ^ 0xFF
        #print("{8:b}".format())
        write_data = bin_data[0] & mask_bin_data | data_shifted
        self.write_i2c(reg_value,write_data)
        
    def get_fastic_register(self,register):
        return self.fastic_registers[register]
    
    def read_config(self):
        # This reads en entire configuration from the FastIC+ and returns the VALUES in alphabeitc order
        datalist = []
        for k in alpha_keylist:
            datalist += [self.read_fastic(k)]
        return datalist
    
    def write_config(self,datalist):
        # This gets a full datalist with one entry for each register in the fastic.
        # This is sorted alphabeticly, not by rising register number
        for d,k in zip(datalist,alpha_keylist):
            self.write_fastic(k,d)
            
    def read_calib(self):
        # Reading the local calibration file
        file = open('fastic_calib.txt', 'r')
        content = file.read()
        data = [int(e.split(" = ")[1]) for e in content.split("\n")]
        file.close()
        return data
    
    def write_calib(self,data):
        # Writing the local calibration file in a human readable way
        file = open('fastic_calib.txt', 'w')
        text = ""
        for k,d in zip(alpha_keylist,data):
            text += f"{k} = {d}\n"
        file.write(text[:-1])
        file.close()
        return None
            
#f = FastIC(0x10,26,27)

#calib = f.read_calib()
#f.write_config(calib)
#cc = f.read_config()
#print(calib == cc)

