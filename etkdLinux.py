# kinerja Linux
#-----------------------------------------------------------------------

# import all required packages
import pyautogui as pag
from time import sleep as tsleep

# setting variables and delays
realPause = 0
testPause = 0
testVar = False
waitDelay = 0.001

scrollS = 20 # scroll value
scrollD = 0.24 # delay after scolling

#   coodinates for every 'laporkan' button that should be 1 pixel above
# the border between the bottom line of the button and the background
button1x = 1831
button1y = [246, 394, 542, 690, 837]

# calibration settings
windowNamePath = '/home/dimas/Dropbox/Python/autoKinerja/ekinerjaWindow.png'
laporkanButtonPath = '/home/dimas/Dropbox/Python/autoKinerja/' + \
			'laporkanButtonL.png'
clockButtonPath = '/home/dimas/Dropbox/Python/autoKinerja/clockButton.png'

windowLocation = (1315, 13, 115, 5)
lapOffsetx = -9
lapOffsety = 10
clockOffsetx = 7
clockOffsety = 129

blueEdgex = 1375 # blue edge X coordinate
blueEdgey = 683 # blue edge Y coordinate

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
		print('Link location is correct.')
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

	# get button location
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
	while pag.screenshot(region=(button1x, button1y[3], 1, 1)).getpixel(
			(0, 0))[0] in (26, 28):
		tsleep(waitDelay)

	# get button location
	clockLoc = pag.locateOnScreen(clockButtonPath)

	if clockLoc == None:
		print('Calibration UNSUCCESSFUL: button not found.')
	elif blueEdgey == clockLoc[1] + clockOffsety:
		print('Calibration Successful: Clock Buttons are already correct!')
	else:
		print('OLD =', blueEdgex, blueEdgey)

		blueEdgex, blueEdgey = clockLoc[0] + clockOffsetx, \
			clockLoc[1] + clockOffsety

		print('NEW =', blueEdgex, blueEdgey)
		print('Calibration Successful!')

	waitClockInput(3)
	pag.typewrite('\t\t\t\t\t\n')
	#pag.scroll(20)

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
	pag.scroll(scrollS)
	pag.scroll(scrollS)
	tsleep(scrollD)
	pag.scroll(- scrollS)
	tsleep(scrollD)

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

def waitClockInput( button):
	'''Wait until we can click on 'Jam Mulai'.'''

	while pag.screenshot(region=(button1x, button1y[button], 1, 1)).getpixel(
			(0, 0))[0] in (26, 28):
		tsleep(waitDelay)

	# wait until we can input the time
	while pag.screenshot(region=(blueEdgex, blueEdgey, 1, 1)
			).getpixel((0, 0))[0] != 26:
		tsleep(waitDelay)
		pag.click(blueEdgex, blueEdgey)

	pag.click(1750, blueEdgey) # click somewhere so it can be triple clicked
	pag.click(x=blueEdgex, y=blueEdgey, clicks=3, interval=0)

def autoChangeNum():
	'''Automatically press down until it doesn't move anymore.'''
	for i in range(5):
		pag.press('down')
	pag.press('tab')

def waitSubmit():
	'''Wait after you clicked 'Simpan' or 'Batal'.'''
	while pag.screenshot(region=(1375, 1000, 1, 1)).getpixel((0, 0))[0] in \
			(26, 28):
		tsleep(0.03125)

def submit():
	'''Clicks 'Simpan' if testVar is false
	and clicks 'Batal' if testVar is True.

	testVar should be True if you are testing,
	and testVar should be False if you are actually doing it.
	'''
	if testVar == False:
		return '\t\n'
	return '\t\t\n'

def tindak( tindakan, tOpt):
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

def kocam( pasien, tOpt):
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
def meTindak(tindakan):
	'''Normal 'tindakan'.'''
	tOpt = ['07:30', '09:00', '10:30', '12:00']
	tindak(tindakan, tOpt)
def seTindak(tindakan):
	'''Senam 'tindakan'.'''
	tOpt = ['08:30', '10:00', '11:00', '12:00']
	tindak(tindakan, tOpt)
def diTindak(tindakan):
	'''Only a few 'tindakan'.'''
	tOpt = ['07:30', '09:00', '10:30']
	tindak(tindakan, tOpt)

# Saved 'rujukan' preset
def meRujuk(rujukan):
	'''Normal 'rujukan'.'''
	tOpt = ['12:00', '12:30']
	rujuk(rujukan, tOpt)
def diRujuk(rujukan):
	'''Only a few 'rujukan'.'''
	tOpt = ['10:30', '11:00']
	rujuk(rujukan, tOpt)

# Saved 'konsultasi dan catatan medik' preset
def meKocam(pasien):
	'''Normal 'konsultasi dan catatan medik'.'''
	tOpt = ['12:30', '13:30', '14:00']
	kocam(pasien, tOpt)
def saKocam(pasien):
	'''Saturday 'konsultasi dan catatan medik'.'''
	tOpt = ['12:00', '12:30', '13:00']
	kocam(pasien, tOpt)
def diKocam(pasien):
	'''Only a few 'konsultasi dan catatan medik'.'''
	tOpt = ['11:00', '11:30', '12:00']
	kocam(pasien, tOpt)

# Daftar fungsi-fungsi yang bisa dijalankan
def normal():
	'''Untuk hari-hari biasa.'''
	global j_tindak, j_rujuk, j_pasien
	meTindak(j_tindak)
	meRujuk(j_rujuk)
	meKocam(j_pasien)
def senam():
	'''Untuk hari rabu saat ada senam.'''
	global j_tindak, j_rujuk, j_pasien
	meTindak(j_tindak)
	meRujuk(j_rujuk)
	meKocam(j_pasien)
def sabtu():
	''' Untuk hari sabtu yang tanpa rujukan.'''
	global j_tindak, j_pasien
	meTindak(j_tindak)
	meKocam(j_pasien)
def dikit():
	global j_tindak, j_rujuk, j_pasien
	'''Untuk hari biasa saat pasien sedikit.'''
	meTindak(j_tindak)
	meRujuk(j_rujuk)
	meKocam(j_pasien)

def main():
	while not checkKinerja():
		tsleep(1)

if __name__ == '__main__':
	main()
