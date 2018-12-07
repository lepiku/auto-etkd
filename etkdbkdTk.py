# For linux
import tkinter as tk
import pyautogui as pag
from time import sleep as tsleep, time as ttime
from pyautogui import screenshotUtil

class Frame(tk.Frame):
	def __init__(self, master):
		super().__init__(master)
		self.master = master
		self.fonts = [("Arial", 14)]

		# setting failsafe and testing
		pag.PAUSE = 0.00390625
		pag.FAILSAFE = True
		self.testVar = False
		self.getMouse = False
		self.shortDelay = 0.03125

		# coodinates for every 'laporkan' button that should be 1 pixel above 
		# the border between the bottom line of the button and the background
		self.button1x = 1831
		#button1y = [421, 569, 717, 865, 1012]
		#button1y = [429, 577, 725, 873, 1020]
		self.button1y = [246, 394, 542, 690, 837]

		# create widgets
		self.widgets()

		# check if the website is opened
		while not self.checkKinerja():
			tsleep(1)

	def widgets(self):
		l_tindak = tk.Label(self, text="Tindakan :", anchor='e', pady=5,
				font=self.fonts[0])
		l_rujuk = tk.Label(self, text="Rujukan :", anchor='e', pady=5,
				font=self.fonts[0])
		l_pasien = tk.Label(self, text="Pasien :", anchor='e', pady=5,
				font=self.fonts[0])

		l_tindak.grid(row=0, column=0, sticky='we')
		l_rujuk.grid(row=1, column=0, sticky='we')
		l_pasien.grid(row=2, column=0, sticky='we')

		self.e_tindak = tk.Entry(self, font=self.fonts[0])
		self.e_rujuk = tk.Entry(self, font=self.fonts[0])
		self.e_pasien = tk.Entry(self, font=self.fonts[0])

		self.e_tindak.grid(row=0, column=1)
		self.e_rujuk.grid(row=1, column=1)
		self.e_pasien.grid(row=2, column=1)

		b_normal = tk.Button(self, text="Normal", font=self.fonts[0],
				command=lambda : self.wrapper(self.normal))
		b_senam = tk.Button(self, text="Senam", font=self.fonts[0],
				command=lambda : self.wrapper(self.senam))
		b_sabtu = tk.Button(self, text="Sabtu", font=self.fonts[0],
				command=lambda : self.wrapper(self.sabtu))

		b_normal.grid(row=3, column=0)
		b_senam.grid(row=3, column=1)
		b_sabtu.grid(row=3, column=2)

		self.l_progress = tk.Label(self, font=self.fonts[0], bg='green')
		self.l_progress.grid(row=4, column=0, columnspan=4, sticky='we')

		# other options
		b_mouse = tk.Checkbutton(self, text="Cek Mouse", font=self.fonts[0],
				anchor='w', command=self.checkMouse)
		b_mengetes = tk.Checkbutton(self, text="Mengetes", font=self.fonts[0],
				anchor='w', command=self.mengetes)
		b_calib = tk.Button(self, text="Calibrate", font=self.fonts[0],
				anchor='w', command=self.calibrate)

		b_mouse.grid(row=0, column=3, sticky='we')
		b_mengetes.grid(row=1, column=3, sticky='we')
		b_calib.grid(row=2, column=3, sticky='we')

	def get(self):
		self.j_tindak = int(self.e_tindak.get())
		self.j_rujuk = int(self.e_rujuk.get())
		self.j_pasien = int(self.e_pasien.get())

		if self.j_tindak + self.j_rujuk + self.j_pasien > 100:
			raise ValueError

	def delete(self):
		self.e_tindak.delete(0, 'end')
		self.e_rujuk.delete(0, 'end')
		self.e_pasien.delete(0, 'end')

	# kinerja Linux
	#-----------------------------------------------------------------------

	# import all required modules
	def checkMouse(self):
		self.getMouse = not self.getMouse
		if self.getMouse:
			self.gM()

	def gM(self):
		"""Get mouse location and the color on the mouse coordinate
		for every quarter of a second."""
		if self.getMouse:
			mpos = pag.position()
			pcolor = pag.screenshot(region=(mpos[0], mpos[1], 1, 1))
			pcolor = pcolor.getpixel((0, 0))
			xcolor = ''.join('{:02x}'.format(i) for i in pcolor)
			pcolor = list(map(str, pcolor))
			print('X: {:<5}Y: {:<5}Color: {:11} #{}'.format(mpos[0],
					mpos[1], ','.join(pcolor), xcolor))

			self.master.after(250, self.gM)

	def gM_old(self):
		"""Get mouse location and the color on the mouse coordinate
		for every quarter of a second."""
		while True:
			try:
				mpos = pag.position()
				pcolor = pag.screenshot(region=(mpos[0], mpos[1], 1, 1))
				pcolor = pcolor.getpixel((0, 0))
				xcolor = ''.join('{:02x}'.format(i) for i in pcolor)
				pcolor = list(map(str, pcolor))
				print('X: {:<5}Y: {:<5}Color: {:11} #{}'.format(mpos[0],
						mpos[1], ','.join(pcolor), xcolor))
				tsleep(0.24)

			except KeyboardInterrupt:
				print('\nSTOPPED')
				break

	def checkKinerja(self):
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
			print('window CANNOT be found!')
			return False
		else:
			print(windowFind, 'should be')
			print(windowLocation)
			print('Window location is NOT correct!')
			return False

	def calibrate(self):
		"""Calibrates the coordinate of self.button1x and self.button1y."""
		pag.moveTo(1700, self.button1y[2])
		self.scrollPrep()

		butLoc = pag.locateOnScreen('/home/dimas/Dropbox/Python/autoKinerja/' +
				'laporkanButtonL.png')
		if butLoc == None:
			print('ERROR 404: Calibration unsuccessful, button not found.')
		elif (1831, 246) == (butLoc[0] - 16, butLoc[1] + 10):
			print('The buttons are at the right position')
		else:
			self.button1x = butLoc[0] - 1
			self.button1y = [butLoc[1] + 10, butLoc[1] + 158, butLoc[1] + 306,
					butLoc[1] + 454, butLoc[1] + 601]

			print('self.button1x =', self.button1x)
			print('self.button1y =', self.button1y)
			print([429, 577, 725, 873, 1020])

		pag.scroll(20)

	def mengetes(self):
		"""change the value of testVar everytime it's called

		testVar should be True if you are testing,
		and testVar should be False if you are actually doing it.
		"""
		self.testVar = not self.testVar
		if self.testVar:
			pag.PAUSE = 0.00390625 #0.5
		else:
			pag.PAUSE = 0.00390625
		print('testVar is set to', self.testVar)

	def scrollPrep(self):
		"""To readjust before clicking 'laporkan'."""
		scrollS = 20 # scroll value
		scrollD = 0.3 # delay after scolling

		pag.moveTo(1750, self.button1y[2])
		pag.scroll(scrollS)
		pag.scroll(scrollS)
		tsleep(scrollD)
		pag.scroll(- scrollS)
		tsleep(scrollD)

	def button1Check(self):
		"""Check if the first 'laporkan' button is correct.

		It will keep rechecking and prints hashtag
		until the button is at the right spot.
		"""

		counter = 1
		self.scrollPrep()
		while True:
			bshot = screenshotUtil.screenshot()
			if (bshot.getpixel((self.button1x, self.button1y[0] + 1))[0] <= 32
					and bshot.getpixel((self.button1x, self.button1y[0] + 2))[0]) == 245:
				break

			# calibrate after 10 ScrollPrep
			if counter == 10:
				self.calibrate()

			counter += 1
			self.scrollPrep()

	def waitClockInput(self, button):
		"""Wait until we can click on 'Jam Mulai'."""
		blueEdgey = 681 # blue edge Y coordinate
		#blueEdgey = 707 # blue edge Y coordinate
		blueEdgex = 1375 # clock X coordinate

		while pag.screenshot(region=(self.button1x, self.button1y[button], 1, 1)).getpixel(
				(0, 0))[0] in (26, 28):
			tsleep(self.shortDelay)

		# wait until we can input the time
		while screenshotUtil.screenshot().getpixel((blueEdgex, blueEdgey))[0] != 26:
			tsleep(self.shortDelay)
			pag.click(blueEdgex, blueEdgey)

		pag.click(1750, blueEdgey) # click somewhere so it can be triple clicked
		pag.click(x=blueEdgex, y=blueEdgey, clicks=3, interval=0.01)

	def autoChangeNum(self):
		"""Automatically press down until it doesn't move anymore."""
		for i in range(5):
			pag.press('down')
		pag.press('tab')

	def waitSubmit(self):
		"""Wait after you clicked 'Simpan' or 'Batal'."""
		while screenshotUtil.screenshot().getpixel((1375, 1000))[0] in (26, 28):
			tsleep(0.03125)

	def submit(self):
		"""Clicks 'Simpan' if self.testVar is false
		and clicks 'Batal' if self.testVar is True.

		self.testVar should be True if you are testing,
		and self.testVar should be False if you are actually doing it.
		"""
		if self.testVar == False:
			return '\t\n'
		return '\t\t\n'

	def tindak(self, tindakan, tOpt):
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
			self.button1Check()
			pag.click(self.button1x, self.button1y[3])

			self.waitClockInput(3)

			pag.typewrite(tOpt[yangKe] + '\t')
			pag.typewrite(tOpt[yangKe + 1] + '\t')

			self.autoChangeNum()

			pag.typewrite(ketindakan + str(tind[yangKe]) + self.submit())
			self.waitSubmit()

		print('Finished Tindakan')

	def rujuk(self, rujukan, tOpt):
		"""Inputs 'Melakukan rujukan'

		Keyword arguments:
		rujukan --	how many 'rujukan' did you do. (integer)
					usually half of 'tindakan'
		tOpt    --	the list of times you do different activities (hh:mm)
		"""
		self.button1Check()
		pag.click(self.button1x, self.button1y[2])

		# print(screenshotUtil.screenshot().getpixel((self.button1x, self.button1y[2])))
		self.waitClockInput(2)

		pag.typewrite(tOpt[0] + '\t')
		pag.typewrite(tOpt[1] + '\t\t') # double tab karena jumlah pasti satu

		pag.typewrite('Jumlah rujukan : ' + str(rujukan) + self.submit())
		self.waitSubmit()

		print('Finished Rujukan')

	def kocam(self, pasien, tOpt):
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

			self.button1Check()
			pag.click(self.button1x, self.button1y[buttons[y]])

			self.waitClockInput(buttons[y])

			pag.typewrite(tOpt[y] + '\t')
			pag.typewrite(tOpt[y + 1] + '\t')

			self.autoChangeNum()

			pag.typewrite(ket[y] + str(pasien) + self.submit())
			self.waitSubmit()

		print('Finished Konsultasi and Catatan Medik')

		pag.scroll(20)

	# Saved 'tindakan' preset
	def meTindak(self, tindakan):
		"""Normal 'tindakan'."""
		tOpt = ['07:30', '09:00', '10:30', '12:00']
		self.tindak(tindakan, tOpt)
	def seTindak(self, tindakan):
		"""Senam 'tindakan'."""
		tOpt = ['08:30', '10:00', '11:00', '12:00']
		self.tindak(tindakan, tOpt)
	def diTindak(self, tindakan):
		"""Only a few 'tindakan'."""
		tOpt = ['07:30', '09:00', '10:30']
		self.tindak(tindakan, tOpt)

	# Saved 'rujukan' preset
	def meRujuk(self, rujukan):
		"""Normal 'rujukan'."""
		tOpt = ['12:00', '12:30']
		self.rujuk(rujukan, tOpt)
	def diRujuk(self, rujukan):
		"""Only a few 'rujukan'."""
		tOpt = ['10:30', '11:00']
		self.rujuk(rujukan, tOpt)

	# Saved 'konsultasi dan catatan medik' preset
	def meKocam(self, pasien):
		"""Normal 'konsultasi dan catatan medik'."""
		tOpt = ['12:30', '13:30', '14:00']
		self.kocam(pasien, tOpt)
	def saKocam(self, pasien):
		"""Saturday 'konsultasi dan catatan medik'."""
		tOpt = ['12:00', '12:30', '13:00']
		self.kocam(pasien, tOpt)
	def diKocam(self, pasien):
		"""Only a few 'konsultasi dan catatan medik'."""
		tOpt = ['11:00', '11:30', '12:00']
		self.kocam(pasien, tOpt)

	# wraps commands with get function and a timer
	def wrapper(self, func):
		timer = ttime()
		self.l_progress.configure(bg='red')
		try:
			self.get()
			func()
		except ValueError:
			self.l_progress.configure(text="Please input a valid number!",
					bg='yellow')

			self.master.after(1000, lambda : self.l_progress.configure(
					text="", bg="green"))

		except pag.FailSafeException:
			print("!!ABORTED!!")
		else:
			self.delete()
			self.l_progress.configure(text="", bg="green")
			print('\tTime = {} seconds\n'.format(ttime() - timer))

	# Daftar fungsi (function) yang bisa dijalankan
	def normal(self):
		"""Untuk hari-hari biasa."""
		self.meTindak(self.j_tindak)
		self.meRujuk(self.j_rujuk)
		self.meKocam(self.j_pasien)
	def senam(self):
		"""Untuk hari rabu saat ada senam."""
		self.meTindak(self.j_tindak)
		self.meRujuk(self.j_rujuk)
		self.meKocam(self.j_pasien)
	def sabtu(self):
		""" Untuk hari sabtu yang tanpa rujukan."""
		self.meTindak(self.j_tindak)
		self.meKocam(self.j_pasien)
	def dikit(self):
		"""Untuk hari biasa saat pasien sedikit."""
		self.meTindak(self.j_tindak)
		self.meRujuk(self.j_rujuk)
		self.meKocam(self.j_pasien)

# ------------------------END OF DEFINITIONS-------------------------- #

def main():
	root = tk.Tk()
	root.title("eKinerja")

	app = Frame(root)
	app.pack()

	root.mainloop()

if __name__ == "__main__":
	main()
