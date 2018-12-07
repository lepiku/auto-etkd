# autoKinerja etkdbkd GUI

import tkinter as tk
import pyautogui as pag
from time import time as ttime, sleep as tsleep
import etkdLinux as etkd
class Frame(tk.Frame):
	def __init__(self, master):
		super().__init__(master)
		self.master = master
		self.fonts = [("Arial", 14)]

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

		self.e_tindak.grid(row=0, column=1, columns=2)
		self.e_rujuk.grid(row=1, column=1, columns=2)
		self.e_pasien.grid(row=2, column=1, columns=2)

		b_normal = tk.Button(self, text="Normal", font=self.fonts[0],
				command=lambda : self.wrapper(etkd.normal))
		b_senam = tk.Button(self, text="Senam", font=self.fonts[0],
				command=lambda : self.wrapper(etkd.senam))
		b_sabtu = tk.Button(self, text="Sabtu", font=self.fonts[0],
				command=lambda : self.wrapper(etkd.sabtu))

		b_normal.grid(row=3, column=0)
		b_senam.grid(row=3, column=1)
		b_sabtu.grid(row=3, column=2)

		self.l_progress = tk.Label(self, font=self.fonts[0], bg='green')
		self.l_progress.grid(row=4, column=0, columnspan=4, sticky='we')

		# other options
		b_mouse = tk.Checkbutton(self, text="Cek Mouse", font=self.fonts[0],
				anchor='w', command=self.checkMouse)
		b_mengetes = tk.Checkbutton(self, text="Mengetes", font=self.fonts[0],
				anchor='w', command=etkd.mengetes)
		b_calib1 = tk.Button(self, text="Calibrate", font=self.fonts[0],
				anchor='w', command=self.calibrate)
		b_calib2  = tk.Button(self, text="Calib 2", font=self.fonts[0],
				anchor='w', command=etkd.calibrate2)

		b_mouse.grid(row=0, column=3, sticky='we')
		b_mengetes.grid(row=1, column=3, sticky='we')
		b_calib1.grid(row=2, column=3, sticky='we')
		b_calib2.grid(row=3, column=3, sticky='we')

	def get(self, func):
		"""Get entries."""
		etkd.j_tindak = int(self.e_tindak.get())
		etkd.j_pasien = int(self.e_pasien.get())

		# if on saturday, dont check rujukan
		if func == etkd.sabtu:
			etkd.j_rujuk = 0
		else:
			etkd.j_rujuk = int(self.e_rujuk.get())

		# it the numbers is too big
		if etkd.j_tindak + etkd.j_rujuk + etkd.j_pasien > 100:
			raise ValueError

	def delete(self):
		self.e_tindak.delete(0, 'end')
		self.e_rujuk.delete(0, 'end')
		self.e_pasien.delete(0, 'end')

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
			print('X: {:<5}Y: {:<5}Color: {:11} #{}'.format(mpos[0], mpos[1],
					','.join(pcolor), xcolor))

			self.master.after(250, self.gM)

	def calibrate(self):
		calib = tk.Tk()

		but1 = tk.Button(calib, text='Calibrate\nLaporkan Button',
				command=lambda: self.dest(calib, etkd.calibrate1))
		but2 = tk.Button(calib, text='Calibrate\nClock Button',
				command=lambda: self.dest(calib, etkd.calibrate2))

		but1.pack(side='left')
		but2.pack(side='right')

		calib.mainloop()

	def dest(self, window, func):
		"""Destroy the window after running the function."""
		func()
		window.destroy()

	# wraps commands with get function and a timer
	def wrapper(self, func):
		timer = ttime()
		self.l_progress.configure(text='', bg='red')
		self.l_progress.update()
		print()
		try:
			self.get(func)
			func()
		except ValueError:
			self.l_progress.configure(text="The numbers are invalid!",
					bg='yellow')

			self.master.after(1000, lambda : self.l_progress.configure(
					text="", bg="green"))

			self.delete()

		except pag.FailSafeException:
			print("!!ABORTED!!")
			self.l_progress.configure(text="!!ABORTED!!", bg="yellow")
		else:
			self.delete()
			self.l_progress.configure(text="", bg="green")
			print('\tTime = {} seconds'.format(ttime() - timer))

def main():
	root = tk.Tk()
	root.title("autoKinerja")

	app = Frame(root)
	app.pack()

	root.mainloop()

if __name__ == "__main__":
	main()
