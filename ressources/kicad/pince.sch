EESchema Schematic File Version 4
EELAYER 30 0
EELAYER END
$Descr A4 11693 8268
encoding utf-8
Sheet 1 1
Title "Module d'alimentation pince SAE"
Date "2022-04-28"
Rev "1.0"
Comp "IUT GEII"
Comment1 "Alexandre BADER"
Comment2 ""
Comment3 ""
Comment4 ""
$EndDescr
$Comp
L Connector:Screw_Terminal_01x04 J1
U 1 1 626AA26F
P 2300 3000
F 0 "J1" H 2250 2700 50  0000 L CNN
F 1 "Screw_Terminal_01x04" H 1500 3250 50  0000 L CNN
F 2 "TerminalBlock:TerminalBlock_bornier-4_P5.08mm" H 2300 3000 50  0001 C CNN
F 3 "~" H 2300 3000 50  0001 C CNN
	1    2300 3000
	-1   0    0    1   
$EndComp
$Comp
L Device:R R1
U 1 1 626AAD55
P 2950 2900
F 0 "R1" V 2950 2900 50  0000 C CNN
F 1 "1000" V 3050 2900 50  0000 C CNN
F 2 "mes_empuntes:R" V 2880 2900 50  0001 C CNN
F 3 "~" H 2950 2900 50  0001 C CNN
	1    2950 2900
	0    -1   -1   0   
$EndComp
Wire Wire Line
	2500 2800 2800 2800
$Comp
L Device:R R2
U 1 1 626ABA75
P 3150 2750
F 0 "R2" H 3200 2750 50  0000 R CNN
F 1 "2000" V 3050 2850 50  0000 R CNN
F 2 "mes_empuntes:R" V 3080 2750 50  0001 C CNN
F 3 "~" H 3150 2750 50  0001 C CNN
	1    3150 2750
	-1   0    0    1   
$EndComp
Wire Wire Line
	2500 2900 2800 2900
Wire Wire Line
	2800 2800 2800 2600
Wire Wire Line
	3100 2900 3150 2900
Connection ~ 3150 2900
Wire Wire Line
	3150 2900 3500 2900
Wire Wire Line
	2800 2600 2950 2600
Wire Wire Line
	2500 3000 3500 3000
Wire Wire Line
	2500 3100 3500 3100
Wire Wire Line
	3150 2600 3400 2600
Connection ~ 3150 2600
$Comp
L Connector:Screw_Terminal_01x03 J3
U 1 1 626BD496
P 2000 2300
F 0 "J3" H 1918 1975 50  0000 C CNN
F 1 "Screw_Terminal_01x03" H 1918 2066 50  0000 C CNN
F 2 "TerminalBlock:TerminalBlock_bornier-3_P5.08mm" H 2000 2300 50  0001 C CNN
F 3 "~" H 2000 2300 50  0001 C CNN
	1    2000 2300
	-1   0    0    1   
$EndComp
$Comp
L Device:LED D1
U 1 1 626BE91F
P 2800 2200
F 0 "D1" H 2793 1945 50  0000 C CNN
F 1 "LED" H 2793 2036 50  0000 C CNN
F 2 "mes_empuntes:LED_D8.0_mm_mod" H 2800 2200 50  0001 C CNN
F 3 "~" H 2800 2200 50  0001 C CNN
	1    2800 2200
	-1   0    0    1   
$EndComp
$Comp
L Device:LED D2
U 1 1 626BF70B
P 2800 2300
F 0 "D2" H 2793 2045 50  0000 C CNN
F 1 "LED" H 2793 2136 50  0000 C CNN
F 2 "mes_empuntes:LED_D8.0_mm_mod" H 2800 2300 50  0001 C CNN
F 3 "~" H 2800 2300 50  0001 C CNN
	1    2800 2300
	-1   0    0    1   
$EndComp
$Comp
L Device:LED D3
U 1 1 626BF9C6
P 2800 2400
F 0 "D3" H 2793 2145 50  0000 C CNN
F 1 "LED" H 2793 2236 50  0000 C CNN
F 2 "mes_empuntes:LED_D8.0_mm_mod" H 2800 2400 50  0001 C CNN
F 3 "~" H 2800 2400 50  0001 C CNN
	1    2800 2400
	-1   0    0    1   
$EndComp
Wire Wire Line
	2500 2200 2550 2200
Wire Wire Line
	2500 2300 2550 2300
Wire Wire Line
	2500 2400 2550 2400
Wire Wire Line
	2950 2200 2950 2300
Connection ~ 2950 2600
Wire Wire Line
	2950 2600 3150 2600
Connection ~ 2950 2300
Wire Wire Line
	2950 2300 2950 2400
Connection ~ 2950 2400
Wire Wire Line
	2950 2400 2950 2600
$Comp
L Device:R R3
U 1 1 626FDA3D
P 2400 2200
F 0 "R3" V 2193 2200 50  0000 C CNN
F 1 "R" V 2284 2200 50  0000 C CNN
F 2 "mes_empuntes:R" V 2330 2200 50  0001 C CNN
F 3 "~" H 2400 2200 50  0001 C CNN
	1    2400 2200
	0    1    1    0   
$EndComp
$Comp
L Device:R R4
U 1 1 626FE2BD
P 2400 2300
F 0 "R4" V 2193 2300 50  0000 C CNN
F 1 "R" V 2284 2300 50  0000 C CNN
F 2 "mes_empuntes:R" V 2330 2300 50  0001 C CNN
F 3 "~" H 2400 2300 50  0001 C CNN
	1    2400 2300
	0    1    1    0   
$EndComp
$Comp
L Device:R R5
U 1 1 626FE3FD
P 2400 2400
F 0 "R5" V 2193 2400 50  0000 C CNN
F 1 "R" V 2284 2400 50  0000 C CNN
F 2 "mes_empuntes:R" V 2330 2400 50  0001 C CNN
F 3 "~" H 2400 2400 50  0001 C CNN
	1    2400 2400
	0    1    1    0   
$EndComp
Connection ~ 2550 2200
Wire Wire Line
	2550 2200 2650 2200
Connection ~ 2550 2300
Wire Wire Line
	2550 2300 2650 2300
Connection ~ 2550 2400
Wire Wire Line
	2550 2400 2650 2400
Wire Wire Line
	2200 2200 2250 2200
Wire Wire Line
	2200 2300 2250 2300
Wire Wire Line
	2200 2400 2250 2400
$Comp
L power:Earth #PWR0101
U 1 1 62702A29
P 3400 2450
F 0 "#PWR0101" H 3400 2200 50  0001 C CNN
F 1 "Earth" H 3400 2300 50  0001 C CNN
F 2 "" H 3400 2450 50  0001 C CNN
F 3 "~" H 3400 2450 50  0001 C CNN
	1    3400 2450
	-1   0    0    1   
$EndComp
Wire Wire Line
	3400 2600 3400 2450
Connection ~ 3400 2600
Wire Wire Line
	3400 2600 3500 2600
$Comp
L Connector:Screw_Terminal_01x04 J2
U 1 1 626B797D
P 3700 3000
F 0 "J2" H 3780 2992 50  0000 L CNN
F 1 "Screw_Terminal_01x04" H 3780 2901 50  0000 L CNN
F 2 "mes_empuntes:bornier_4_points" H 3700 3000 50  0001 C CNN
F 3 "~" H 3700 3000 50  0001 C CNN
	1    3700 3000
	1    0    0    1   
$EndComp
Wire Wire Line
	3500 2600 3500 2800
$EndSCHEMATC
