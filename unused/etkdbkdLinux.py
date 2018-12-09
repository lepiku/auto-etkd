# kinerja Linux
#-----------------------------------------------------------------------

# import all required modules
import pyautogui as pag
from time import sleep as tsleep, time as ttime
from pyautogui import screenshotUtil

def gM():
	"""Get mouse location and the color on the mouse coordinate
	for every quarter of a second."""
	while True:
		try:
			mpos = pag.position()
			pcolor = pag.screenshot(region=(mpos[0], mpos[1], 1, 1))
			pcolor = pcolor.getpixel((0, 0))
			xcolor = ''.join('{:02x}'.format(i) for i in pcolor)
			pcolor = list(map(str, pcolor))
			print('X: {:<5}Y: {:<5}Color: {:11} #{}'.format(mpos[0], mpos[1],
					','.join(pcolor), xcolor))
			tsleep(0.24)

		except KeyboardInterrupt:
			print('\nSTOPPED')
			break

'''# OLD VERSION
def checkKinerja():
	"""Check if zoom is at 100% and home is at the right position.

	The browser should be Firefox.
	The Firefox window should be half opened on the right side.
	"""
	sshot = screenshotUtil.screenshot()
	zoom100 = [217, 249, 50, 50, 50, 249, 50, 50, 249]
	home100 = [163, 163, 190, 190, 50, 50, 163]
	zoomData = []
	homeData = []
	for x in range(1718, 1727):
		zoomData.append(sshot.getpixel((x, 50))[1])
	for x in range(1070, 1077):
		homeData.append(sshot.getpixel((x, 54))[1])
	if (zoom100 == zoomData) and (home100 == homeData):
		print('Fucntions are loaded successfully!')
	else:
		raise Exception('THE FUNCTIONS MAY NOT WORK PROPERLY!')
'''
def checkKinerja2():
	"""Check if the website link is 'etkdbkd.jakarta.go.id'

	The browser should be Firefox.
	The Firefox window should be half opened on the right side.
	"""
	#checkKinerja('/home/dimas/Dropbox/Python/autoKinerja/etkdbkdLink.png',
	#				(1234, 80, 70, 6))
	return checkKinerja('/home/dimas/lnket.png', (1315, 13, 115, 5))

def checkKinerja():
	"""Check if the window name is 'eKinerja DKI Jakarta - Mozilla Firefox'

	The browser should be Firefox.
	The Firefox window should be half opened on the right side.
	"""
	imagePath = '/home/dimas/Dropbox/Python/autoKinerja/ekinerjaWindow.png'
	windowLocation = (1315, 13, 115, 5)

	topRegion = pag.screenshot(region=(0, 0, 1920, 100))
	windowFind = pag.locate(imagePath, topRegion)
	if windowFind == windowLocation:
		print('Link location is correct.')
		return True
	elif windowFind == None:
		print('THE FUNCTIONS MAY NOT WORK PROPERLY!')
		return False
	else:
		print(windowFind, 'should be')
		print(windowLocation)
		print('Window location is not correct')
		return False

def calibrate():
	global button1x, button1y
	"""Calibrates the coordinate of button1x and button1y."""
	pag.moveTo(1700, button1y[2])
	scrollPrep()

	butLoc = pag.locateOnScreen('/home/dimas/Dropbox/Python/autoKinerja/laporkanButtonL.png')
	print(butLoc)
	if butLoc == None:
		print('ERROR 404: Calibration unsuccessful, button not found.')
	elif (1831, 246) == (butLoc[0] - 16, butLoc[1] + 10):
		print('The buttons are at the right position')
	else:
		button1x = butLoc[0] - 1
		#button1y = [butLoc[1] + 13, butLoc[1] + 161, butLoc[1] + 309, butLoc[1] + 457, butLoc[1] + 604]
		button1y = [butLoc[1] + 10, butLoc[1] + 158, butLoc[1] + 306, butLoc[1] + 454, butLoc[1] + 601]
		print('button1x =', button1x)
		print('button1y =', button1y)
		print([429, 577, 725, 873, 1020])

	pag.scroll(20)

def mengetes():
	"""change the value of testVar everytime it's called

	testVar should be True if you are testing,
	and testVar should be False if you are actually doing it.
	"""
	global testVar
	testVar = not testVar
	if testVar:
		pag.PAUSE = 0.5
	else:
		pag.PAUSE = 0.00390625
	print('testVar is set to', testVar)

def scrollPrep():
	"""To readjust before clicking 'laporkan'."""
	scrollS = 20 # scroll value
	scrollD = 0.3 # delay after scolling

	pag.moveTo(1750, button1y[2])
	pag.scroll(scrollS)
	pag.scroll(scrollS)
	tsleep(scrollD)
	pag.scroll(- scrollS)
	tsleep(scrollD)

def waitClockInput(button):
	"""Wait until we can click on 'Jam Mulai'."""
	blueEdgey = 681 # blue edge Y coordinate
	#blueEdgey = 707 # blue edge Y coordinate
	blueEdgex = 1375 # clock X coordinate

	while pag.screenshot(region=(button1x, button1y[button], 1, 1)).getpixel((0, 0))[0] in (26, 28):
		tsleep(shortDelay)

	# wait until we can input the time
	while screenshotUtil.screenshot().getpixel((blueEdgex, blueEdgey))[0] != 26:
		tsleep(shortDelay)
		pag.click(blueEdgex, blueEdgey)

	pag.click(1750, blueEdgey) # click somewhere so it can be triple clicked
	pag.click(x=blueEdgex, y=blueEdgey, clicks=3, interval=0.01)

def autoChangeNum():
	"""Automatically press down until it doesn't move anymore."""
	for i in range(5):
		pag.press('down')
	pag.press('tab')

def waitSubmit():
	"""Wait after you clicked 'Simpan' or 'Batal'."""
	while screenshotUtil.screenshot().getpixel((1375, 1000))[0] in (26, 28):
		tsleep(0.03125)

def button1Check():
	"""Check if the first 'laporkan' button is correct.

	It will keep rechecking and prints hashtag
	until the button is at the right spot.
	"""

	scrollPrep()
	while True:
		bshot = screenshotUtil.screenshot()
		if (bshot.getpixel((button1x, button1y[0] + 1))[0] <= 32
				and bshot.getpixel((button1x, button1y[0] + 2))[0]) == 245:
			break

		scrollPrep()

def submit():
	"""Clicks 'Simpan' if testVar is false
	and clicks 'Batal' if testVar is True.

	testVar should be True if you are testing,
	and testVar should be False if you are actually doing it.
	"""
	global testVar
	if testVar == False:
		return '\t\n'
	return '\t\t\n'

def tindak(tindakan, tOpt):
	"""Inputs 'Melakukan tindakan / terapi pengobatan'

	Keyword arguments:
	tindakan -- how many activities did you do (integer)
	tOpt     -- the list of times you do different activities (hh:mm)
	"""
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
	"""Inputs 'Melakukan rujukan'

	Keyword arguments:
	rujukan --	how many 'rujukan' did you do. (integer)
				usually half of 'tindakan'
	tOpt    --	the list of times you do different activities (hh:mm)
	"""
	button1Check()
	pag.click(button1x, button1y[2])

	# print(screenshotUtil.screenshot().getpixel((button1x, button1y[2])))
	waitClockInput(2)

	pag.typewrite(tOpt[0] + '\t')
	pag.typewrite(tOpt[1] + '\t\t') # double tab karena jumlah pasti satu

	pag.typewrite('Jumlah rujukan : ' + str(rujukan) + submit())
	waitSubmit()

	print('Finished Rujukan')

def kocam(pasien, tOpt):
	"""Inputs 'Melaksanakan / Melayani Konsultasi Individu / Kelompok'
	and 'Membuat catatan medik gigi dan mulut pasien rawat inap / jalan'

	Keyword arguments:
	pasien -- how many patient did you work on (integer)
	tOpt   -- the list of times you do different activities (hh:mm)
	"""
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
	"""Normal 'tindakan'."""
	tOpt = ['07:30', '09:00', '10:30', '12:00']
	tindak(tindakan, tOpt)
def seTindak(tindakan):
	"""Senam 'tindakan'."""
	tOpt = ['08:30', '10:00', '11:00', '12:00']
	tindak(tindakan, tOpt)
def diTindak(tindakan):
	"""Only a few 'tindakan'."""
	tOpt = ['07:30', '09:00', '10:30']
	tindak(tindakan, tOpt)

# Saved 'rujukan' preset
def meRujuk(rujukan):
	"""Normal 'rujukan'."""
	tOpt = ['12:00', '12:30']
	rujuk(rujukan, tOpt)
def diRujuk(rujukan):
	"""Only a few 'rujukan'."""
	tOpt = ['10:30', '11:00']
	rujuk(rujukan, tOpt)

# Saved 'konsultasi dan catatan medik' preset
def meKocam(pasien):
	"""Normal 'konsultasi dan catatan medik'."""
	tOpt = ['12:30', '13:30', '14:00']
	kocam(pasien, tOpt)
def saKocam(pasien):
	"""Saturday 'konsultasi dan catatan medik'."""
	tOpt = ['12:00', '12:30', '13:00']
	kocam(pasien, tOpt)
def diKocam(pasien):
	"""Only a few 'konsultasi dan catatan medik'."""
	tOpt = ['11:00', '11:30', '12:00']
	kocam(pasien, tOpt)

# Daftar fungsi (function) yang bisa dijalankan
def kinerja(tindakan, rujukan, pasien):
	"""Untuk hari-hari biasa."""
	timer = ttime()
	meTindak(tindakan)
	meRujuk(rujukan)
	meKocam(pasien)
	print('\tTime = {} seconds\n'.format(ttime() - timer))
def senam(tindakan, rujukan, pasien):
	"""Untuk hari rabu saat ada senam."""
	timer = ttime()
	seTindak(tindakan)
	meRujuk(rujukan)
	meKocam(pasien)
	print('\tTime = {} seconds\n'.format(ttime() - timer))
def sabtu(tindakan, pasien):
	""" Untuk hari sabtu yang tanpa rujukan."""
	timer = ttime()
	meTindak(tindakan)
	saKocam(pasien)
	print('\tTime = {} seconds\n'.format(ttime() - timer))
def dikit(tindakan, rujukan, pasien):
	"""Untuk hari biasa saat pasien sedikit."""
	timer = ttime()
	diTindak(tindakan)
	diRujuk(rujukan)
	diKocam(pasien)
	print('\tTime = {} seconds\n'.format(ttime() - timer))

# ------------------------END OF DEFINITIONS-------------------------- #

# setting failsafe and testing
pag.PAUSE = 0.00390625
pag.FAILSAFE = True
testVar = False
shortDelay = 0.03125

# coodinates for every 'laporkan' button that should be 1 pixel above 
# the border between the bottom line of the button and the background
button1x = 1831
#button1y = [421, 569, 717, 865, 1012]
#button1y = [429, 577, 725, 873, 1020]
button1y = [246, 394, 542, 690, 837]

if __name__ == '__main__':
	while not checkKinerja():
		tsleep(1)
