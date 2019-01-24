# kinerja Linux
#-----------------------------------------------------------------------

# import all required packages
import pyautogui as pag
from time import sleep as tsleep

# setting variables and delays, sometimes different for every OS
realPause = 0.2
testPause = 0.5
testVar = False
waitDelay = 0.001

scrollValue = 20 # scroll value
scrollDelay = 0.24 # delay after scolling

#   coodinates for every 'laporkan' button that should be 1 pixel above
# the border between the bottom line of the button and the background
button1x = 1831
button1y = [246, 394, 542, 690, 837]

# calibration settings
windowNamePath = '/home/dimas/Dropbox/Python/auto-etkd/images/' + \
		'ekinerjaWindow.png'
laporkanButtonPath = '/home/dimas/Dropbox/Python/auto-etkd/images/' + \
		'laporkanButton.png'
clockButtonPath = '/home/dimas/Dropbox/Python/auto-etkd/images/' + \
		'clockButton.png'

windowLocation = (1315, 13, 115, 5)
lapOffsetx = -9
lapOffsety = 10
clockOffsetx = 7
clockOffsety = 129

blueEdgex = 1375
blueEdgey = 683

# failsafe and settings
pag.PAUSE = 0
pag.FAILSAFE = True
j_tindak = 0
j_rujuk = 0
j_pasien = 0

def checkKinerja():
	'''Check if the window name is 'eKinerja DKI Jakarta - Mozilla Firefox'

	The browser should be Firefox.
	The Firefox window should be half opened on the right side.
	'''

	# scan 100 pixel from top
	topRegion = pag.screenshot(region=(0, 0, 1920, 100))
	windowFind = pag.locate(windowNamePath, topRegion)

	if windowFind == windowLocation:
		print('Window location is correct.')
		return True
	elif windowFind == None:
		print('window CANNOT be found!')
		return False
	else:
		print(windowFind, 'should be')
		print(windowLocation)
		print('Window location is NOT correct!')
		return False

def calibrate1():
	'''Calibrates the coordinate of button1x and button1y.'''
	global button1x, button1y

	# preparation
	scrollPrep()

	butLoc = pag.locateOnScreen(laporkanButtonPath)

	if butLoc == None:
		print('Calibration UNSUCCESSFUL: button not found.')
	elif button1y[0] == butLoc[1] + lapOffsety:
		print('Calibration Successful: Button1s are already correct!')
	else:
		print('OLD =', button1x, button1y)

		button1x = butLoc[0] + lapOffsetx
		button1y = [butLoc[1] + lapOffsety, butLoc[1] + lapOffsety + 148,
				butLoc[1] + lapOffsety + 296, butLoc[1] + lapOffsety + 444,
				butLoc[1] + lapOffsety + 591]

		print('NEW =', button1x, button1y)
		print('Calibration Successful: Button1s are calibrated!')

	pag.scroll(20)

def calibrate2():
	'''Calibrates the coordinate for waitClockInput button.'''
	global blueEdgex, blueEdgey

	# preparation
	button1Check()
	pag.click(button1x, button1y[3])
	checkPixel(button1x, button1y[3], (26, 28))
#	while pag.screenshot(region=(button1x, button1y[3], 1, 1)).getpixel(
#			(0, 0))[0] in (26, 28):
#		tsleep(waitDelay)

	clockLoc = pag.locateOnScreen(clockButtonPath)

	if clockLoc == None:
		print('Calibration UNSUCCESSFUL: button not found.')
	elif blueEdgey == clockLoc[1] + clockOffsety:
		print('Calibration Successful: Clock Buttons are already correct!')
	else:
		print('OLD =', blueEdgex, blueEdgey)

		blueEdgex = clockLoc[0] + clockOffsetx
		blueEdgey = clockLoc[1] + clockOffsety

		print('NEW =', blueEdgex, blueEdgey)
		print('Calibration Successful!')

	waitClockInput(3)
	pag.typewrite('\t\t\t\t\t\n', interval=0.005)
	waitSubmit()
	pag.scroll(20)

def mengetes():
	'''change the value of testVar everytime it's called

	testVar should be True if you are just testing,
	and testVar should be False if you are actually doing it.
	'''
	global testVar

	testVar = not testVar
	if testVar:
		pag.PAUSE = testPause
	else:
		pag.PAUSE = realPause
	print('testVar is {}, PAUSE is {}'.format(testVar, pag.PAUSE))

def scrollPrep():
	'''To readjust before clicking 'laporkan'.'''

	pag.moveTo(1750, button1y[2])
	pag.scroll(scrollValue)
	pag.scroll(scrollValue)
	tsleep(scrollDelay)
	pag.scroll(-scrollValue)
	tsleep(scrollDelay)

def button1Check():
	'''Check if the first 'laporkan' button is correct.

	It will keep rechecking and prints hashtag
	until the button is at the right spot.
	'''
	counter = 1
	scrollPrep()
	while True:
		bshot = pag.screenshot(region=(button1x, button1y[0] + 1, 1, 2))
		if (bshot.getpixel((0, 0))[0] <= 32
				and bshot.getpixel((0, 1))[0] == 245):
			break

		# calibrate after 10 ScrollPrep
		if counter == 10:
			calibrate1()

		counter += 1
		scrollPrep()

def waitClockInput(button):
	'''Wait until we can click on 'Jam Mulai'.'''
	checkPixel(button1x, button1y[button], (26, 28))
#	while pag.screenshot(region=(button1x, button1y[button], 1, 1)).getpixel(
#			(0, 0))[0] in (26, 28):
#		tsleep(waitDelay)

	# wait until we can input the time
	while pag.screenshot(region=(blueEdgex, blueEdgey, 1, 1)
			).getpixel((0, 0))[0] != 26:
		tsleep(waitDelay)
		pag.click(blueEdgex, blueEdgey)

	pag.click(1750, blueEdgey) # click somewhere so it can be triple clicked
	pag.click(x=blueEdgex, y=blueEdgey, clicks=3, interval=0)

def autoChangeNum():
	'''Automatically press down arrow key until it reached the maximum.'''
	for i in range(5):
		pag.press('down')
	pag.press('tab')

def waitSubmit():
	'''Wait after you clicked 'Simpan' or 'Batal'.
	It checks the simpan button until it isn't blue.
	'''
	checkPixel(blueEdgex, blueEdgey + 317, (26, 28))
#	while pag.screenshot(region=(1375, 1000, 1, 1)).getpixel((0, 0))[0] in \
#			(26, 28):
#		tsleep(waitDelay)

def submit():
	'''Clicks 'Simpan' if testVar is false
	and clicks 'Batal' if testVar is True.

	testVar should be True if you are testing,
	and testVar should be False if you are actually doing it.
	'''
	if testVar == False:
		return '\t\n'
	return '\t\t\n'

def checkPixel(x, y, color):
	'''Check the pixel color of x and y.'''
	if type(color) in (tuple, list):
		while pag.screenshot(region=(x, y, 1, 1)).getpixel((0, 0))[0] in color:
			tsleep(waitDelay)
	elif type(color) == int:
		while pag.screenshot(region=(x, y, 1, 1)).getpixel((0, 0))[0] == color:
			tsleep(waitDelay)
	else:
		print("wrong type of color")

def isiSenam():
	'''Input 'senam' activity in 'Aktifitas Umum'.'''
	tabButtonx = 1400
	tabButtony = 600
	button2x = 1800
	button2y = 920

	button1Check()
	pag.scroll(scrollValue // 2)
	tsleep(scrollDelay)
	pag.click(tabButtonx, tabButtony) # click aktivitas umum

	# check until 'Tambah Laporan' can be clicked
	checkPixel(tabButtonx - 50, tabButtony, 220)
	pag.click(button2x, button2y)
	checkPixel(button2x, button2y, (26, 28))

	while pag.screenshot(region=(button2x - 280, button2y + 50, 1, 1)
			).getpixel((0, 0))[0] != 246:
		tsleep(waitDelay)
	pag.click(button2x - 280, button2y + 50)
	pag.typewrite("mengikuti senam\n\t07:30\t08:30\t\tSenam pagi karyawan RSUD Jagakarsa" + submit())

	checkPixel(1340, 1040, (26, 28))
	tsleep(1)

	pag.click(tabButtonx - 125, tabButtony + 195)
	checkPixel(tabButtonx - 125, tabButtony + 195, 220)
	print('done!')



def tindak(tindakan, tOpt):
	'''Inputs 'Melakukan tindakan / terapi pengobatan'

	Keyword arguments:
	tindakan -- how many activities did you do (integer)
	tOpt     -- the list of times you do different activities (hh:mm)
	'''
	ketindakan = 'Anamnesa, pemeriksaan fisik, diagnosa, terapi : penambalan, pencabutan, curetage, pemberian resep : '
	kali = len(tOpt) - 1

	tind = [tindakan // kali] * kali
	if tindakan % kali == 1:
		tind[0] += 1
	elif tindakan % kali == 2:
		tind[0] += 1
		tind[1] += 1

	for yangKe in range(kali):
		button1Check()
		pag.click(button1x, button1y[3])

		waitClockInput(3)

		pag.typewrite(tOpt[yangKe] + '\t')
		pag.typewrite(tOpt[yangKe + 1] + '\t')

		autoChangeNum()

		pag.typewrite(ketindakan + str(tind[yangKe]) + submit())
		waitSubmit()

	print('Finished Tindakan')

def rujuk(rujukan, tOpt):
	'''Inputs 'Melakukan rujukan'

	Keyword arguments:
	rujukan --	how many 'rujukan' did you do. (integer)
				usually half of 'tindakan'
	tOpt    --	the list of times you do different activities (hh:mm)
	'''
	button1Check()
	pag.click(button1x, button1y[2])

	waitClockInput(2)

	pag.typewrite(tOpt[0] + '\t')
	pag.typewrite(tOpt[1] + '\t\t') # double tab karena jumlah pasti satu

	pag.typewrite('Jumlah rujukan : ' + str(rujukan) + submit())
	waitSubmit()

	print('Finished Rujukan')

def kocam(pasien, tOpt):
	'''Inputs 'Melaksanakan / Melayani Konsultasi Individu / Kelompok'
	and 'Membuat catatan medik gigi dan mulut pasien rawat inap / jalan'

	Keyword arguments:
	pasien -- how many patient did you work on (integer)
	tOpt   -- the list of times you do different activities (hh:mm)
	'''
	buttons = [0, 4]
	ket = ['Jumlah konsultasi individu : ', 'Jumlah catatan medik : ']
	# [0] : Konsultasi individu
	# [1] : Catatan medik

	for y in range(2):

		button1Check()
		pag.click(button1x, button1y[buttons[y]])

		waitClockInput(buttons[y])

		pag.typewrite(tOpt[y] + '\t')
		pag.typewrite(tOpt[y + 1] + '\t')

		autoChangeNum()

		pag.typewrite(ket[y] + str(pasien) + submit())
		waitSubmit()

	print('Finished Konsultasi and Catatan Medik')
	pag.scroll(20)

# Saved 'tindakan' preset
def meTindak():
	'''Normal 'tindakan'.'''
	tOpt = ['07:30', '09:00', '10:30', '12:00']
	tindak(j_tindak, tOpt)
def seTindak():
	'''Senam 'tindakan'.'''
	tOpt = ['08:30', '10:00', '11:00', '12:00']
	tindak(j_tindak, tOpt)
def diTindak():
	'''Only a few 'tindakan'.'''
	tOpt = ['07:30', '09:00', '10:30']
	tindak(j_tindak, tOpt)

# Saved 'rujukan' preset
def meRujuk():
	'''Normal 'rujukan'.'''
	tOpt = ['12:00', '12:30']
	rujuk(j_rujuk, tOpt)
def diRujuk():
	'''Only a few 'rujukan'.'''
	tOpt = ['10:30', '11:00']
	rujuk(j_rujuk, tOpt)

# Saved 'konsultasi dan catatan medik' preset
def meKocam():
	'''Normal 'konsultasi dan catatan medik'.'''
	tOpt = ['12:30', '13:30', '14:00']
	kocam(j_pasien, tOpt)
def saKocam():
	'''Saturday 'konsultasi dan catatan medik'.'''
	tOpt = ['12:00', '12:30', '13:00']
	kocam(j_pasien, tOpt)
def diKocam():
	'''Only a few 'konsultasi dan catatan medik'.'''
	tOpt = ['11:00', '11:30', '12:00']
	kocam(j_pasien, tOpt)

# Daftar fungsi-fungsi yang bisa dijalankan
def normal():
	'''Untuk hari-hari biasa.'''
	meTindak()
	meRujuk()
	meKocam()
def senam():
	'''Untuk hari rabu saat ada senam.'''
	isiSenam()
	meTindak()
	meRujuk()
	meKocam()
def sabtu():
	''' Untuk hari sabtu yang tanpa rujukan.'''
	meTindak()
	meKocam()
def dikit():
	'''Untuk hari biasa saat pasien sedikit.'''
	meTindak()
	meRujuk()
	meKocam()

if __name__ == '__main__':
	# check until etkd website is opened
	while not checkKinerja():
		tsleep(1)
