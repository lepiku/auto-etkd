# kinerja Linux
#-----------------------------------------------------------------------

# import all required packages
import pyautogui as pag
from time import sleep as tsleep

# setting variables and delays, sometimes different for every OS
realPause = 0
testPause = 0.2
testVar = False
waitDelay = 0.001

scrollValue = 20 # scroll value
scrollDelay = 0.24 # delay after scolling

#   coodinates for every 'laporkan' button that should be 1 pixel above
# the border between the bottom line of the button and the background
button1x = 1831
button1y = [246, 394, 542, 690, 837]

# coordinates for 'Aktivitas umum' and 'Tambah Laporan' in there
tabButtonx = 1400
tabButtony = 600
button2x = 1800
button2y = 920

# calibration settings
image_prefix = '/home/dimas/Dropbox/Python/auto-etkd/images/'
windowNamePath = image_prefix + 'ekinerjaWindow.png'
laporkanButtonPath = image_prefix + 'laporkanButton.png'
clockButtonPath = image_prefix + 'clockButton.png'
aktivitasUmumPath = image_prefix + 'aktivitasUmum.png'
aktivitasUtamaPath = image_prefix + 'aktivitasUtama.png'
tambahLaporanPath = image_prefix + 'tambahLaporan.png'

windowLocation = (1315, 13, 115, 5)
lapOffsetx = -9
lapOffsety = 10
clockOffsetx = 90
clockOffsety = -11
aktUmumOffsetx = 27
aktUmumOffsety = 6
tamLapOffsetx = 26
tamLapOffsety = 10

blueEdgex = 1375
blueEdgey = 683

# i3 settings
button1x   = 1806
button1y   = [293, 441, 589, 737, 884] # [293, 441, 589, 737, 884]
blueEdgex  = 1343
blueEdgey  = 697
tabButtonx = 1368
tabButtony = 647 # 639
button2x   = 1790
button2y   = 934

# failsafe and settings
pag.PAUSE = 0
pag.FAILSAFE = True
j_masuk = ""
j_tindak = 0
j_rujuk = 0
j_pasien = 0

def tempYChange():
    global button1y, tabButtony

    button1y = [293, 441, 589, 737, 884]
    tabButtony = 639

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
        return False
    elif button1x == butLoc[0] + lapOffsetx \
            and button1y[0] == butLoc[1] + lapOffsety:
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
    return True

def calibrate2():
    '''Calibrates the coordinate for waitClockInput button.'''
    global blueEdgex, blueEdgey

    # preparation
    button1Check()
    pag.click(button1x, button1y[3])
    checkPixel(button1x, button1y[3], (26, 28))

    clockLoc = pag.locateOnScreen(clockButtonPath)

    if clockLoc == None:
        print('Calibration UNSUCCESSFUL: Clock button not found.')
    elif blueEdgex == clockLoc[0] + clockOffsetx \
            and blueEdgey == clockLoc[1] + clockOffsety:
        print('Calibration Successful: Clock button is already correct!')
    else:
        print('OLD =', blueEdgex, blueEdgey)

        blueEdgex = clockLoc[0] + clockOffsetx
        blueEdgey = clockLoc[1] + clockOffsety

        print('NEW =', blueEdgex, blueEdgey)
        print('Calibration Successful! Clock button is calibrated!')

    waitClockInput(3)
    pag.typewrite('\t\t\t\t\t\n', interval=0.005)
    waitSubmit()
    pag.scroll(20)

def calibrate3():
    '''Calibrates the coordinate for AktivitasUmum button.'''
    global tabButtonx, tabButtony

    # preparation
    button1Check()
    pag.scroll(scrollValue // 2)
    tsleep(scrollDelay)

    buttonLoc = pag.locateOnScreen(aktivitasUmumPath)

    if buttonLoc == None:
        print('Calibration UNSUCCESSFUL: tab button not found.')
    elif tabButtonx == buttonLoc[0] + aktUmumOffsetx \
            and tabButtony == buttonLoc[1] + aktUmumOffsety:
        print('Calibration Successful: Tab button is already correct!')
    else:
        print('OLD =', tabButtonx, tabButtony)

        tabButtonx = buttonLoc[0] + aktUmumOffsetx
        tabButtony = buttonLoc[1] + aktUmumOffsety

        print('NEW =', tabButtonx, tabButtony)
        print('Calibration Successful! Tab button is calibrated!')

    pag.scroll(20)
    tsleep(scrollDelay)

def calibrate4():
    '''Calibrates the coordinate for tambahLaporan button.'''
    global button2x, button2y

    # preparation
    button1Check()
    pag.scroll(scrollValue // 2)
    tsleep(scrollDelay)
    pag.click(tabButtonx, tabButtony)
    checkPixel(tabButtonx, tabButtony, 220)

    buttonLoc = pag.locateOnScreen(tambahLaporanPath)

    if buttonLoc == None:
        print('Calibration UNSUCCESSFUL: tambah laporan  button not found.')
    elif button2x == buttonLoc[0] + tamLapOffsetx \
            and button2y == buttonLoc[1] + tamLapOffsety:
        print('Calibration Successful: Tambah Laporan button is already correct!')
    else:
        print('OLD =', button2x, button2y)

        button2x = buttonLoc[0] + tamLapOffsetx
        button2y = buttonLoc[1] + tamLapOffsety

        print('NEW =', button2x, button2y)
        print('Calibration Successful! Tambah Laporan button is calibrated!')

    pag.click(tabButtonx - 130, tabButtony + 240)
    checkPixel(tabButtonx - 130, tabButtony + 240, 220)
    pag.scroll(20)
    tsleep(scrollDelay)

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

        # calibrate after 5 ScrollPrep
        if counter == 5:
            tempYChange()

        if counter == 10:
            calibrate1()
            calibrate3()

        counter += 1
        scrollPrep()

def waitClockInput(button):
    '''Wait until we can click on 'Jam Mulai'.'''
    checkPixel(button1x, button1y[button], (26, 28))

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
    '''Check the pixel color of x and y until the red color is different.'''
    if type(color) in (tuple, list):
        while pag.screenshot(region=(x, y, 1, 1)).getpixel((0, 0))[0] in color:
            tsleep(waitDelay)
    elif type(color) == int:
        while pag.screenshot(region=(x, y, 1, 1)).getpixel((0, 0))[0] == color:
            tsleep(waitDelay)
    else:
        print("WRONG color")

def checkNotPixel(x, y, color):
    '''Check the pixel color of x and y until the red color is the same.'''
    while pag.screenshot(region=(x, y, 1, 1)).getpixel((0, 0))[0] != color:
        tsleep(waitDelay)

def isiUmum(search, timeStart, timeEnd, info):
    '''Input an activity in 'Aktivitas Umum.'''
    # click 'Aktivitas Umum'
    button1Check()
    pag.scroll(scrollValue // 2)
    tsleep(scrollDelay)
    pag.click(tabButtonx, tabButtony)
    checkPixel(tabButtonx, tabButtony, 220)

    # click 'Tambahkan Laporan'
    pag.click(button2x, button2y)
    checkPixel(button2x, button2y, (26, 28))

    # check until the data can be inputed
    checkNotPixel(button2x - 280, button2y + 50, 246)
    pag.click(button2x - 280, button2y + 50)
    pag.typewrite(search + "\n\t" + timeStart + "\t" + timeEnd + "\t\t" + info
            + submit())

    # check until can go back to 'Aktivitas Utama'
    checkPixel(tabButtonx - 60, tabButtony + 440, (26, 28))
    if not testVar: # check the first green icon on the right
        for _ in range(0, 10):
            if pag.screenshot(region=(button2x, button2y + 41, 1, 1)).getpixel((0, 0))[0] == 26:
                break
            tsleep(waitDelay)

    # set the location of 'Aktivitas Utama' button
    tombolUtama = (tabButtonx - 130,)
    if testVar:
        tombolUtama += (tabButtony + 240,)
    else:
        tombolUtama += (tabButtony + 195,)

    # go back to 'Aktivitas Utama'
    if pag.screenshot(region=(tombolUtama[0], tombolUtama[1], 1, 1)).getpixel((0, 0))[0] == 220:
        pag.click(tombolUtama[0], tombolUtama[1])

    checkPixel(tombolUtama[0], tombolUtama[1], 220)

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

def formatClock(clock):
    clock = clock.replace(":", "")
    return clock[0:2] + ":" + clock[2:4]

# Saved 'isiUmum' preset
def isiSenam():
    '''Input 'senam' activity in 'Aktifitas Umum'.'''
    isiUmum("mengikuti senam", "07:00", "08:00", "Senam pagi karyawan RSUD Jagakarsa")

def isiApel():
    '''Input 'Menjadi petugas Apel' activity in 'Aktifitas Umum'.'''
    isiUmum("apel -", "07:30", "08:00", "Mengikuti apel pagi RSUD Jagakarsa")

# Saved 'tindakan' preset
def meTindak():
    '''Normal 'tindakan'.'''
    tOpt = ['07:30', '09:00', '10:30', '12:00']
    if j_masuk:
        tOpt[0] = formatClock(j_masuk)
    tindak(j_tindak, tOpt)
def seTindak():
    '''Senam 'tindakan'.'''
    tindak(j_tindak, ['08:00', '09:00', '10:30', '12:00'])
def diTindak():
    '''Only a few 'tindakan'.'''
    tindak(j_tindak, ['07:30', '09:00', '10:30'])
def apTindak():
    '''When there's a ceremony.'''
    tindak(j_tindak, ['08:00', '09:00', '10:30', '12:00'])

# Saved 'rujukan' preset
def meRujuk():
    '''Normal 'rujukan'.'''
    rujuk(j_rujuk, ['12:00', '12:30'])
def diRujuk():
    '''Only a few 'rujukan'.'''
    rujuk(j_rujuk, ['10:30', '11:00'])

# Saved 'konsultasi dan catatan medik' preset
def meKocam():
    '''Normal 'konsultasi dan catatan medik'.'''
    kocam(j_pasien, ['12:30', '13:30', '14:00'])
def saKocam():
    '''Saturday 'konsultasi dan catatan medik'.'''
    kocam(j_pasien, ['12:00', '12:30', '13:00'])
def diKocam():
    '''Only a few 'konsultasi dan catatan medik'.'''
    kocam(j_pasien, ['11:00', '11:30', '12:00'])

# Daftar fungsi-fungsi yang bisa dijalankan
def normal():
    '''Untuk hari-hari biasa.'''
    meTindak()
    meRujuk()
    meKocam()
def senam():
    '''Untuk hari rabu saat ada senam.'''
    seTindak()
    meRujuk()
    meKocam()
    # isiSenam()
def sabtu():
    ''' Untuk hari sabtu yang tanpa rujukan.'''
    meTindak()
    meKocam()
def dikit():
    '''Untuk hari biasa saat pasien sedikit.'''
    meTindak()
    meRujuk()
    meKocam()
def senin():
    # isiApel()
    apTindak()
    meRujuk()
    meKocam()

if __name__ == '__main__':
    # check until etkd website is opened
    while not checkKinerja():
        tsleep(1)
