import numpy as np
import simpleaudio as sa
import sounddevice as sd
from PyQt5 import QtCore, QtGui, QtWidgets
from gui import Ui_MainWindow
import sys

# get tsteps for each sample, T is note duration in seconds
sample_rate = 44100
T = 0.5
t = np.linspace(0, T, int(T * sample_rate), False)

# calculate note frequencies
notes_range = np.arange(-9, 3)
A_freq = 440

notes_freq = np.zeros(12)
notes_sound= [0]*12
#generate from C4 notes(middle c) to B4
for i in range(len(notes_range)):
    notes_freq[i] = A_freq * 2 ** (notes_range[i] / 12)
# print(notes_freq)
class ApplicationWindow(QtWidgets.QMainWindow):

    def __init__(self):
        super(ApplicationWindow, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.ui.piano.clicked.connect(self.piano)
        self.ui.guitar.clicked.connect(self.guitar)

        self.pFlag =0
        self.buttonslist=[self.ui.c_note,self.ui.csharp,self.ui.d_note,
                          self.ui.eflat,self.ui.e_note,self.ui.f_note,
                          self.ui.fsharp,self.ui.g_note,self.ui.aflat,
                          self.ui.a_note, self.ui.bflat,self.ui.b_note]
        self.playnotes=[lambda: self.playEachNote(0),lambda:self.playEachNote(1),lambda:self.playEachNote(2),
                        lambda:self.playEachNote(3),lambda:self.playEachNote(4),lambda:self.playEachNote(5),
                        lambda:self.playEachNote(6),lambda:self.playEachNote(7),lambda:self.playEachNote(8),
                        lambda:self.playEachNote(9),lambda:self.playEachNote(10),lambda: self.playEachNote(11)]
    def piano(self):
        self.pFlag = 1
        for i in range(12):
            notes_sound[i] = 0.6 * np.sin(2 * np.pi * notes_freq[i] * t) * np.exp(-0.0015 * np.pi * notes_freq[i] * t)
            notes_sound[i] += 0.4 * np.sin(2 * np.pi * notes_freq[i] * t) * np.exp(-0.0015 * np.pi * notes_freq[i] * t)
            # for saturated sound
            notes_sound[i] += notes_sound[i] * notes_sound[i] * notes_sound[i]
            notes_sound[i] *= 1 + 16 * t * np.exp(-6 * t)
            # normalize to 16-bit range
            notes_sound[i] *= 32767 / np.max(np.abs(notes_sound[i]))
            # convert to 16-bit data
            notes_sound[i] = notes_sound[i].astype(np.int16)

            self.buttonslist[i].clicked.connect(self.playnotes[i])
    
    def playEachNote(self, i):
        if self.pFlag == 1:
            play_obj = sa.play_buffer(notes_sound[i], 1, 2, sample_rate)
            # play_obj.wait_done()

    def karplusStrong(self, wavetable, n_samples):
        samples = []
        current_sample = 0
        previous_value = 0
        while len(samples) < n_samples:
            wavetable[current_sample] = 0.5 * (wavetable[current_sample] + previous_value)
            samples.append(wavetable[current_sample])
            previous_value = samples[-1]
            current_sample += 1
            current_sample = current_sample % wavetable.size
        return np.array(samples)
    def guitar(self,freq):
        wavetable_size = sample_rate // int(freq)
        wavetable = (2 * np.random.randint(0, 2, wavetable_size) - 1).astype(np.float)
        sample = self.karplus_strong(wavetable, 1 * sample_rate)
        sd.play(sample, sample_rate)

def main():
    app = QtWidgets.QApplication(sys.argv)
    application = ApplicationWindow()
    application.show()
    app.exec_()


if __name__ == "__main__":
    main()