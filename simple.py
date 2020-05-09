import numpy as np
import simpleaudio as sa

# get tsteps for each sample, T is note duration in seconds
sample_rate = 44100
T = 0.5
t = np.linspace(0, T, int(T*sample_rate), False)

# calculate note frequencies
notes_range = np.arange(-9,3)
A_freq = 440
notes_freq=np.zeros(12)
for i in range(len(notes_range)):
    notes_freq[i] = A_freq*2**(notes_range[i]/12)
print(notes_freq)

Csh_freq = A_freq * 2 ** (4 / 12)
E_freq = A_freq * 2 ** (7 / 12)
audio =np.zeros(12)
# generate sine wave notes
notes_sound= [0]*12
for i in range(12):
    # notes_sound[i] = np.sin(2*np.pi*notes_freq[i]*t)*np.exp(-0.0004*np.pi*notes_freq[i]*t)
    # notes_sound[i] += 0.5*np.sin(2*2*np.pi*notes_freq[i]*t)*np.exp(-0.0004*np.pi*notes_freq[i]*t)
    # notes_sound[i] += 0.25 * np.sin(3*2 * np.pi * notes_freq[i] * t) * np.exp(-0.0004 * np.pi * notes_freq[i] * t)
    # notes_sound[i] += 0.125 * np.sin(4*2 * np.pi * notes_freq[i] * t) * np.exp(-0.0004 * np.pi * notes_freq[i] * t)
    # notes_sound[i] += 0.0625 * np.sin(5*2 * np.pi * notes_freq[i] * t) * np.exp(-0.0004 * np.pi * notes_freq[i] * t)
    # notes_sound[i] += 0.03125 * np.sin(6*2 * np.pi * notes_freq[i] * t) * np.exp(-0.0004 * np.pi * notes_freq[i] * t)
    notes_sound[i] = 0.6 * np.sin(2 * np.pi * notes_freq[i] * t) * np.exp(-0.0015 * np.pi * notes_freq[i] * t)
    notes_sound[i] += 0.4 * np.sin(2 * np.pi * notes_freq[i] * t) * np.exp(-0.0015 * np.pi * notes_freq[i] * t)
    #for saturated sound
    notes_sound[i] += notes_sound[i]*notes_sound[i]*notes_sound[i]
    # notes_sound[i] *= 1 +16*t*np.exp(-6*t)
    # concatenate notes
for i in range(12):
    # normalize to 16-bit range
    notes_sound[i] *= 32767 / np.max(np.abs(notes_sound[i]))
    # convert to 16-bit data
    notes_sound[i] = notes_sound[i].astype(np.int16)

# start playback
play_obj = sa.play_buffer(notes_sound[0], 1, 2, sample_rate)
play_obj.wait_done()

play_obj = sa.play_buffer(notes_sound[2], 1, 2, sample_rate)
play_obj.wait_done()

play_obj = sa.play_buffer(notes_sound[4], 1, 2, sample_rate)

# wait for playback to finish before exiting
play_obj.wait_done()

# Csh_note = 0.6*np.sin(2*np.pi*Csh_freq*t)*np.exp(-0.0015*np.pi*Csh_freq*t)
# Csh_note += 0.4*np.sin(2*np.pi*Csh_freq*t)*np.exp(-0.0015*np.pi*Csh_freq*t)
# Csh_note += Csh_note*Csh_note*Csh_note
# Csh_note *=1 +16*t*np.exp(-6*t)

# E_note = 0.6*np.sin(2*np.pi*E_freq*t)*np.exp(-0.0015*np.pi*E_freq*t)
# E_note += 0.4*np.sin(2*np.pi*E_freq*t)*np.exp(-0.0015*np.pi*E_freq*t)
# E_note += E_note*E_note*E_note
# E_note *=1 +16*t*np.exp(-6*t)
#
# audio = np.hstack((notes_sound[1],Csh_note, E_note))
# # normalize to 16-bit range
# audio *= 32767 / np.max(np.abs(audio))
# # convert to 16-bit data
# audio = audio.astype(np.int16)
#
# # start playback
# play_obj = sa.play_buffer(audio, 1, 2, sample_rate)
#
# # wait for playback to finish before exiting
# play_obj.wait_done()