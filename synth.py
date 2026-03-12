import numpy as np
import pygame

starting_note = 'D4'  # Change this to set the starting note programmatically
scale = 1  # 0: Chromatic, 1: Major, 2: Minor
chord_volume = 0.2  # Set the chord volume

# Define a list of keys corresponding to the keyboard keys
keyboard_keys = [
    pygame.K_n, pygame.K_m, pygame.K_COMMA, pygame.K_PERIOD, pygame.K_SLASH, pygame.K_RSHIFT,
    pygame.K_h, pygame.K_j, pygame.K_k, pygame.K_l, pygame.K_SEMICOLON, pygame.K_QUOTE,
    pygame.K_y, pygame.K_u, pygame.K_i, pygame.K_o, pygame.K_p, pygame.K_LEFTBRACKET,
]

# Mapping of note names to their frequencies
note_frequencies = {
    'C0': 16.35, 'C#0': 17.32, 'D0': 18.35, 'D#0': 19.45, 'E0': 20.60, 'F0': 21.83,
    'F#0': 23.12, 'G0': 24.50, 'G#0': 25.96, 'A0': 27.50, 'A#0': 29.14, 'B0': 30.87,

    'C1': 32.70, 'C#1': 34.65, 'D1': 36.71, 'D#1': 38.89, 'E1': 41.20, 'F1': 43.65,
    'F#1': 46.25, 'G1': 49.00, 'G#1': 51.91, 'A1': 55.00, 'A#1': 58.27, 'B1': 61.74,

    'C2': 65.41, 'C#2': 69.30, 'D2': 73.42, 'D#2': 77.78, 'E2': 82.41, 'F2': 87.31,
    'F#2': 92.50, 'G2': 98.00, 'G#2': 103.83, 'A2': 110.00, 'A#2': 116.54, 'B2': 123.47,

    'C3': 130.81, 'C#3': 138.59, 'D3': 146.83, 'D#3': 155.56, 'E3': 164.81, 'F3': 174.61,
    'F#3': 185.00, 'G3': 196.00, 'G#3': 207.65, 'A3': 220.00, 'A#3': 233.08, 'B3': 246.94,

    'C4': 261.63, 'C#4': 277.18, 'D4': 293.66, 'D#4': 311.13, 'E4': 329.63, 'F4': 349.23,
    'F#4': 369.99, 'G4': 392.00, 'G#4': 415.30, 'A4': 440.00, 'A#4': 466.16, 'B4': 493.88,

    'C5': 523.25, 'C#5': 554.37, 'D5': 587.33, 'D#5': 622.25, 'E5': 659.25, 'F5': 698.46,
    'F#5': 739.99, 'G5': 783.99, 'G#5': 830.61, 'A5': 880.00, 'A#5': 932.33, 'B5': 987.77,

    'C6': 1046.50, 'C#6': 1108.73, 'D6': 1174.66, 'D#6': 1244.51, 'E6': 1318.51, 'F6': 1396.91,
    'F#6': 1479.98, 'G6': 1567.98, 'G#6': 1661.22, 'A6': 1760.00, 'A#6': 1864.66, 'B6': 1975.53,
}


def generate_drum_hit_sound(duration=0.1, sample_rate=44100, amplitude=2048):
    # Generate white noise
    noise = np.random.uniform(-1, 1, int(sample_rate * duration)) * amplitude

    # Generate a low-frequency thump
    freq = 50  # Adjust this for a deeper or lighter thump
    t = np.linspace(0, duration, int(sample_rate * duration), endpoint=False)
    thump = amplitude * np.sin(2 * np.pi * freq * t)

    # Combine the noise and thump
    hit_sound = noise + thump

    # Apply an exponential decay to simulate the sharp attack and quick fade-out
    envelope = np.exp(-np.linspace(0, 5, int(sample_rate * duration)))
    hit_sound = hit_sound * envelope

    # Convert to an appropriate format for pygame
    hit_sound = hit_sound.astype(np.int16)

    return pygame.sndarray.make_sound(hit_sound)


def generate_kick_sound(duration=0.3, sample_rate=44100, amplitude=2048, start_freq=150, end_freq=50):
    # Generate a time array
    t = np.linspace(0, duration, int(sample_rate * duration), endpoint=False)

    # Generate a frequency array that drops from start_freq to end_freq
    freq = np.linspace(start_freq, end_freq, int(sample_rate * duration))

    # Generate the kick sound by combining the frequency and time arrays
    kick_sound = amplitude * np.sin(2 * np.pi * freq * t)

    # Apply an exponential decay to simulate the quick fade-out of a kick drum
    envelope = np.exp(-np.linspace(0, 5, int(sample_rate * duration)))
    kick_sound = kick_sound * envelope

    # Convert to an appropriate format for pygame
    kick_sound = kick_sound.astype(np.int16)

    return pygame.sndarray.make_sound(kick_sound)


def generate_snare_sound(duration=0.2, sample_rate=44100, amplitude=2048):
    # Generate white noise
    noise = np.random.uniform(-1, 1, int(sample_rate * duration)) * amplitude

    # Apply an exponential decay to simulate the sharp attack of a snare drum
    envelope = np.exp(-np.linspace(0, 5, int(sample_rate * duration)))

    # Apply the envelope to the noise
    snare_sound = noise * envelope

    # Convert to an appropriate format for pygame
    snare_sound = snare_sound.astype(np.int16)

    sound = pygame.sndarray.make_sound(snare_sound)
    sound.set_volume(.8)  # Set volume
    return sound


def generate_note_sound(frequency, duration=1, sample_rate=44100, amplitude=2048):
    # Generate a looping sound for a given frequency that starts and ends at zero amplitude.
    num_cycles = int(frequency * duration)
    actual_duration = num_cycles / frequency
    t = np.linspace(0, actual_duration, int(sample_rate * actual_duration), endpoint=False)
    arr = amplitude * np.sin(2.0 * np.pi * frequency * t)
    arr = np.convolve(arr, np.ones(5) / 5, mode='same')
    arr = arr.astype(np.int16)
    sound = pygame.sndarray.make_sound(arr)
    sound.set_volume(1.0)  # Set volume to maximum
    return sound


def generate_chromatic_scale(start_note, start_key):
    all_notes = list(note_frequencies.keys())
    start_index = all_notes.index(start_note)
    scale = [None] * len(keyboard_keys)
    start_key_index = keyboard_keys.index(start_key)
    for i in range(start_key_index, len(keyboard_keys)):
        scale[i] = all_notes[(start_index + (i - start_key_index)) % len(all_notes)]
    for i in range(start_key_index - 1, -1, -1):
        scale[i] = all_notes[(start_index - (start_key_index - i)) % len(all_notes)]
    return scale


def generate_scale(start_note, start_key, intervals):
    all_notes = list(note_frequencies.keys())
    start_index = all_notes.index(start_note)
    scale = [None] * len(keyboard_keys)
    start_key_index = keyboard_keys.index(start_key)
    current_note_index = start_index
    scale[start_key_index] = all_notes[current_note_index]
    for i in range(1, len(keyboard_keys) - start_key_index):
        interval = intervals[(i - 1) % len(intervals)]
        current_note_index = (current_note_index + interval) % len(all_notes)
        scale[start_key_index + i] = all_notes[current_note_index]
    current_note_index = start_index
    for i in range(1, start_key_index + 1):
        interval = intervals[-i % len(intervals)]
        current_note_index = (current_note_index - interval) % len(all_notes)
        scale[start_key_index - i] = all_notes[current_note_index]
    return scale


def map_sounds_to_keys(starting_note, scale_type, start_key):
    major_intervals = [2, 2, 1, 2, 2, 2, 1]
    minor_intervals = [2, 1, 2, 2, 1, 2, 2]
    if scale_type == 0:
        scale = generate_chromatic_scale(starting_note, start_key)
    elif scale_type == 1:
        scale = generate_scale(starting_note, start_key, major_intervals)
    elif scale_type == 2:
        scale = generate_scale(starting_note, start_key, minor_intervals)
    else:
        raise ValueError("Invalid scale type. Use 0 for chromatic, 1 for major, 2 for minor.")
    sounds = {keyboard_keys[i]: generate_note_sound(note_frequencies[scale[i]]) for i in range(len(scale))}
    note_names = {keyboard_keys[i]: scale[i] for i in range(len(scale))}
    return sounds, note_names


def transpose_note(note, octave_shift):
    note_base = note[:-1]
    octave = int(note[-1])
    new_octave = octave + octave_shift
    return f"{note_base}{new_octave}"


def generate_chord(note, chord_type):
    major_chord = [0, 4, 7, 11]
    minor_chord = [0, 3, 7, 10]
    diminished_chord = [0, 3, 6, 9]

    all_notes = list(note_frequencies.keys())
    root_index = all_notes.index(note)

    if chord_type == 'major':
        chord = [all_notes[(root_index + interval) % len(all_notes)] for interval in major_chord]
    elif chord_type == 'minor':
        chord = [all_notes[(root_index + interval) % len(all_notes)] for interval in minor_chord]
    elif chord_type == 'diminished':
        chord = [all_notes[(root_index + interval) % len(all_notes)] for interval in diminished_chord]
    else:
        raise ValueError("Invalid chord type")
    return chord


def generate_chord_mapping(start_note, scale_type):
    all_notes = list(note_frequencies.keys())
    start_index = all_notes.index(start_note)
    if scale_type == 1 or scale_type == 0:  # Major scale
        chord_types = ['major', 'minor', 'minor', 'major', 'major', 'minor', 'diminished']
        scale_intervals = [0, 2, 4, 5, 7, 9, 11]
    elif scale_type == 2:  # Minor scale
        chord_types = ['minor', 'diminished', 'major', 'minor', 'minor', 'major', 'major']
        scale_intervals = [0, 2, 3, 5, 7, 8, 10]
    else:
        raise ValueError("Invalid scale type")
    scale_chords = []
    for i, interval in enumerate(scale_intervals):
        root_note = all_notes[(start_index + interval) % len(all_notes)]
        scale_chords.append(generate_chord(root_note, chord_types[i]))
    return {
        pygame.K_a: scale_chords[0],
        pygame.K_s: scale_chords[1],
        pygame.K_d: scale_chords[2],
        pygame.K_f: scale_chords[3],
        pygame.K_z: scale_chords[4],
        pygame.K_x: scale_chords[5],
        pygame.K_c: scale_chords[6],
        pygame.K_v: [transpose_note(note, 1) for note in scale_chords[0]],  # First chord one octave up
    }


def load_percussion_sequence(file_name):
    with open(file_name, 'r') as file:
        sequence = file.read().strip()
    return sequence
