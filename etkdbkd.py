# autoKinerja etkdbkd GUI
# imports required modules
import tkinter as tk
import pyautogui as pag
from time import time as ttime, sleep as tsleep
import etkdLinux as etkd

class Frame(tk.Frame):
	'''GUI for the program.'''
	def __init__(self, master):
		super().__init__(master)
		self.master = master
		self.fonts = [('Arial', 14)]

		# variables
		self.getMouse = False

		# check if the website is opened
		for x in range(10):
			if etkd.checkKinerja():
				break
			tsleep(1)

		# create widgets
		self.widgets()

	def widgets(self):
		'''Create the widgets.'''
		# labels
		l_tindak = tk.Label(self, text='Tindakan :', anchor='e', pady=5,
				font=self.fonts[0])
		l_rujuk = tk.Label(self, text='Rujukan :', anchor='e', pady=5,
				font=self.fonts[0])
		l_pasien = tk.Label(self, text='Pasien :', anchor='e', pady=5,
				font=self.fonts[0])

		l_tindak.grid(row=0, column=0, sticky='we')
		l_rujuk.grid(row=1, column=0, sticky='we')
		l_pasien.grid(row=2, column=0, sticky='we')

		# entries
		self.e_tindak = tk.Entry(self, font=self.fonts[0])
		self.e_rujuk = tk.Entry(self, font=self.fonts[0])
		self.e_pasien = tk.Entry(self, font=self.fonts[0])

		self.e_tindak.grid(row=0, column=1, columns=2)
		self.e_rujuk.grid(row=1, column=1, columns=2)
		self.e_pasien.grid(row=2, column=1, columns=2)

		# buttons
		b_normal = tk.Button(self, text='Normal', font=self.fonts[0], bg='yellow',
				command=lambda : self.wrapper(self.get, etkd.normal))
		b_senam = tk.Button(self, text='Senam', font=self.fonts[0], bg='yellow',
				command=lambda : self.wrapper(self.get, etkd.senam))
		b_sabtu = tk.Button(self, text='Sabtu', font=self.fonts[0], bg='yellow',
				command=lambda : self.wrapper(self.get, etkd.sabtu))

		b_normal.grid(row=3, column=0, sticky='we')
		b_senam.grid(row=3, column=1, sticky='we')
		b_sabtu.grid(row=3, column=2, sticky='we')

		# progress bar
		self.l_progress = tk.Label(self, font=self.fonts[0], bg='green')
		self.l_progress.grid(row=4, column=0, columnspan=4, sticky='we')

		# other buttons
		b_mouse = tk.Checkbutton(self, text='Cek Mouse', font=self.fonts[0],
				anchor='w', command=self.checkMouse)
		b_mengetes = tk.Checkbutton(self, text='Mengetes', font=self.fonts[0],
				anchor='w', command=etkd.mengetes)
		b_calib = tk.Button(self, text='Calibrate', font=self.fonts[0],
				anchor='w', command=self.calibrate)
		b_settings  = tk.Button(self, text='Settings', font=self.fonts[0],
				anchor='w', command=self.settings)

		b_mouse.grid(row=0, column=3, sticky='we')
		b_mengetes.grid(row=1, column=3, sticky='we')
		b_calib.grid(row=2, column=3, sticky='we')
		b_settings.grid(row=3, column=3, sticky='we')

	def delete(self):
		'''Delete all entries.'''
		self.e_tindak.delete(0, 'end')
		self.e_rujuk.delete(0, 'end')
		self.e_pasien.delete(0, 'end')

	def checkMouse(self):
		'''Change the status of get mouse command.'''
		self.getMouse = not self.getMouse
		if self.getMouse:
			self.gM()

	def gM(self):
		'''Get mouse location and the color on the mouse coordinate
		for every quarter of a second.'''
		if self.getMouse:
			mpos = pag.position()
			pcolor = pag.screenshot(region=(mpos[0], mpos[1], 1, 1))
			pcolor = pcolor.getpixel((0, 0))
			xcolor = ''.join('{:02x}'.format(i) for i in pcolor)
			pcolor = list(map(str, pcolor))
			print('X: {:<5}Y: {:<5}Color: {:11} #{}'.format(mpos[0], mpos[1],
					','.join(pcolor), xcolor))

			self.master.after(250, self.gM)

	def calibrate(self):
		'''Make new window for calibration options.'''
		calib = tk.Tk()

		but1 = tk.Button(calib, text='Calibrate\nLaporkan Button',
				command=lambda: self.dest(calib, etkd.calibrate1))
		but2 = tk.Button(calib, text='Calibrate\nClock Button',
				command=lambda: self.dest(calib, etkd.calibrate2))

		but1.pack(side='left')
		but2.pack(side='right')

		calib.mainloop()

	def settings(self):
		sett = tk.Tk()

		tin0 = tk.Button(sett, text='Normal tindakan',
				command=lambda: self.wrapper(self.get1, etkd.meTindak))
		tin1 = tk.Button(sett, text='Senam tindakan',
				command=lambda: self.wrapper(self.get1, etkd.seTindak))
		tin2 = tk.Button(sett, text='Dikit tindakan',
				command=lambda: self.wrapper(self.get1, etkd.diTindak))

		tin0.grid(row=0, column=0, sticky='we')
		tin1.grid(row=1, column=0, sticky='we')
		tin2.grid(row=2, column=0, sticky='we')

		ruj0 = tk.Button(sett, text='Normal rujukan',
				command=lambda: self.wrapper(self.get1, etkd.meRujuk))
		ruj1 = tk.Button(sett, text='Senam rujukan',
				command=lambda: self.wrapper(self.get1, etkd.diRujuk))

		ruj0.grid(row=0, column=1, sticky='we')
		ruj1.grid(row=1, column=1, sticky='we')

		koc0 = tk.Button(sett, text='Normal kocam',
				command=lambda: self.wrapper(self.get1, etkd.meKocam))
		koc1 = tk.Button(sett, text='Sabtu kocam',
				command=lambda: self.wrapper(self.get1, etkd.saKocam))
		koc2 = tk.Button(sett, text='Dikit kocam',
				command=lambda: self.wrapper(self.get1, etkd.diKocam))

		koc0.grid(row=0, column=2, sticky='we')
		koc1.grid(row=1, column=2, sticky='we')
		koc2.grid(row=2, column=2, sticky='we')

		sett.mainloop()

	def dest(self, window, func):
		'''Destroy the window after running the function.'''
		func()
		window.destroy()

	# wraps commands with get function and a timer
	def wrapper(self, get_func, func):
		'''Wraps the function with a timer and showing the progress.'''
		timer = ttime()
		self.l_progress.configure(text='', bg='red')
		self.l_progress.update()
		print()
		try:
			get_func(func)
			func()
		# if the entries input aren't numbers
		except ValueError:
			self.l_progress.configure(text='The numbers are invalid!',
					bg='yellow')

			self.master.after(1000, lambda : self.l_progress.configure(
					text='', bg='green'))

			self.delete()
		# if you move the mouse to coordinate 0,0
		except pag.FailSafeException:
			print('!!ABORTED!!')
			self.l_progress.configure(text='!!ABORTED!!', bg='yellow')
		# if no error exist
		else:
			self.l_progress.configure(text='', bg='green')
			print('\tTime = {} seconds'.format(ttime() - timer))
			self.delete()

	def get(self, func):
		'''Get from all entries.'''
		etkd.j_tindak = int(self.e_tindak.get())
		etkd.j_pasien = int(self.e_pasien.get())

		# if on saturday, dont check rujukan
		if func == etkd.sabtu:
			etkd.j_rujuk = 0
		else:
			etkd.j_rujuk = int(self.e_rujuk.get())

		# if the numbers is too big
		if etkd.j_tindak + etkd.j_rujuk + etkd.j_pasien > 100:
			raise ValueError

	def get1(self, func):
		if func in [etkd.meTindak, etkd.seTindak, etkd.diTindak]:
			etkd.j_tindak = int(self.e_tindak.get())

		elif func in [etkd.meRujuk, etkd.diRujuk]:
			etkd.j_rujuk = int(self.e_rujuk.get())

		elif func in [etkd.meKocam, etkd.saKocam, etkd.diKocam]:
			etkd.j_pasien = int(self.e_pasien.get())

def main():
	'''Running the GUI.'''
	root = tk.Tk()
	root.title('autoKinerja')

	app = Frame(root)
	app.pack()

	root.mainloop()

if __name__ == '__main__':
	main()
