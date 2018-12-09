# kinerja v L
#-----------
# import all required modules
import time
import pyautogui as pag
from pyautogui import screenshotUtil

# setting failsafe and testing
pag.PAUSE = 0.00390625
pag.FAILSAFE = True
testVar = False

# coodinates for every 'laporkan' button
button1x = 1831
# button1y = [421, 569, 717, 865, 1012]
button1y = [429, 577, 725, 873, 1020]

def scrollPrep():
	"""To readjust before clicking 'laporkan'."""
	pag.moveTo(1700, button1y[2])
	pag.scroll(20)
	pag.scroll(20)
	time.sleep(0.5)
	pag.scroll(-20)
	time.sleep(0.5)
	button1Check()

def waitClockInput(button):
	"""Wait until we can click on 'Jam Mulai'."""
	while screenshotUtil.screenshot().getpixel((button1x, button1y[button]))[0] in (26, 28):
		time.sleep(0.03125)

	while screenshotUtil.screenshot().getpixel((1375, 681))[0] != 26: # Loading sampai input jam
		pag.click(1375, 682)
		time.sleep(0.03125)

	pag.click(1750, 682)
	pag.click(x=1375, y=682, clicks=3, interval=0.01)

def autoChangeNum():
	"""Automatically press down until it doesn't move anymore."""
	for i in range(5):
		pag.press('down')
	pag.press('tab')

def waitSubmit():
	"""Wait after you clicked 'Simpan' or 'Batal'."""
	while screenshotUtil.screenshot().getpixel((1375, 1000))[0] in (26, 28):
		time.sleep(0.03125)

def gM():
	"""Get mouse location and the color on the mouse coordinate
	for every half a second."""
	while True:
		try:
			mpos = pag.position()
			pcolor = screenshotUtil.screenshot().getpixel(mpos)
			pcolor = list(map(str, pcolor))
			print('X: ' + str(mpos[0]), end=' ')
			print('Y: ' + str(mpos[1]), end=' ')
			print('Color: ' + ','.join(pcolor))
			time.sleep(0.24)
		except KeyboardInterrupt:
			print('\nSTOPPED')
			break

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

def checkKinerja2():
	"""Check if the website link is 'etkdbkd.jakarta.go.id'

	The browser should be Firefox.
	The Firefox window should be half opened on the right side.
	"""
	linkLoc = pag.locateOnScreen('/home/dimas/Dropbox/Python/autoKinerja/etkdbkdLink.png')
	if linkLoc == (1234, 80, 70, 6):
		print('Link location is correct.')
	elif linkLoc == None:
		raise Exception('THE FUNCTIONS MAY NOT WORK PROPERLY!')
	else:
		print(linkLoc)
		raise Exception('Window location is not correct')

def button1Check():
	"""Check if the first 'laporkan' button is correct.

	It will keep rechecking and prints hashtag
	until the button is at the right spot.
	"""
	while True:
		bshot = screenshotUtil.screenshot()
		if (bshot.getpixel((button1x, button1y[0] + 1))[0] <= 32
				and bshot.getpixel((button1x, button1y[0] + 2))[0]) == 245:
			break

		print('#')
		pag.scroll(20)
		pag.scroll(20)
		time.sleep(0.5)
		pag.scroll(-20)
		time.sleep(0.5)

def calibrate():
	global button1x, button1y
	"""Calibrates the coordinate of button1x and button1y."""
	pag.moveTo(1700, button1y[2])
	pag.scroll(20)
	pag.scroll(20)
	time.sleep(0.5)
	pag.scroll(-20)
	time.sleep(0.5)

	butLoc = pag.locateOnScreen('/home/dimas/Dropbox/Python/autoKinerja/laporkanButtonL.png')
	if butLoc == None:
		print('The buttons cannot be found')
	elif (1831, 429) == (butLoc[0] - 1, butLoc[1] + 13):
		print('The buttons are at the right position')
	else:
		button1x = butLoc[0] - 1
		#button1y = [butLoc[1] + 13, butLoc[1] + 161, butLoc[1] + 309, butLoc[1] + 457, butLoc[1] + 604]
		button1y = [butLoc[1] + 10, butLoc[1] + 158, butLoc[1] + 306, butLoc[1] + 454, butLoc[1] + 601]
		print('button1x =', button1x)
		print('button1y =', button1y)
		print([429, 577, 725, 873, 1020])

	pag.scroll(20)

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
		scrollPrep()
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
	scrollPrep()
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

		scrollPrep()
		pag.click(button1x, button1y[buttons[y]])

		waitClockInput(buttons[y])

		pag.typewrite(tOpt[y] + '\t')
		pag.typewrite(tOpt[y + 1] + '\t')

		autoChangeNum()

		pag.typewrite(ket[y] + str(pasien) + submit())
		waitSubmit()

	print('Finished Konsultasi and Catatan Medik\n')

	pag.scroll(20)

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

def mengetes():
	"""change the value of testVar everytime it's called

	testVar should be True if you are testing,
	and testVar should be False if you are actually doing it.
	"""
	global testVar
	if testVar == False:
		testVar = True
		pag.PAUSE = 1
	else:
		testVar = False
		pag.PAUSE = 0.00390625
	print('testVar is set to', testVar)

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
	meTindak(tindakan)
	meRujuk(rujukan)
	meKocam(pasien)
def senam(tindakan, rujukan, pasien):
	"""Untuk hari rabu saat ada senam."""
	seTindak(tindakan)
	meRujuk(rujukan)
	meKocam(pasien)
def sabtu(tindakan, pasien):
	""" Untuk hari sabtu yang tanpa rujukan."""
	meTindak(tindakan)
	saKocam(pasien)
def dikit(tindakan, rujukan, pasien):
	"""Untuk hari biasa saat pasien sedikit."""
	diTindak(tindakan)
	diRujuk(rujukan)
	diKocam(pasien)

checkKinerja2()
calibrate()
mengetes()
