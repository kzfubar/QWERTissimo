import asyncio
import pygame
import synth
from NoteStream import NoteStream

starting_note = 'C5'
scale = 1
chord_volume = 0.2
fadeout = 880
chord_fadeout = 440 * 3

roman_numerals_major = {
    0: "I",   # Tonic
    1: "ii",  # Supertonic
    2: "iii", # Mediant
    3: "IV",  # Subdominant
    4: "V",   # Dominant
    5: "vi",  # Submediant
    6: "vii°" # Leading tone
}

roman_numerals_minor = {
    0: "i",   # Tonic
    1: "ii°", # Supertonic diminished
    2: "III", # Mediant
    3: "iv",  # Subdominant
    4: "v",   # Dominant
    5: "VI",  # Submediant
    6: "VII"  # Subtonic
}

async def play_percussion_sequence(sequence, sound_map, rest_durations, stop_event, chord_sounds, chord_sequence):
    chord_index = 0
    active_chord_sounds = []

    while not stop_event.is_set():
        i = 0
        while i < len(sequence):
            if stop_event.is_set():
                break
            char = sequence[i]
            if char in sound_map:
                simultaneous_sounds = [char]
                i += 1
                while i < len(sequence) and sequence[i] in sound_map:
                    simultaneous_sounds.append(sequence[i])
                    i += 1
                for sound_char in simultaneous_sounds:
                    sound_map[sound_char].play()
            elif char in rest_durations:
                await asyncio.sleep(rest_durations[char])
                i += 1
            else:
                print(f"Unknown character '{char}' in sequence.")
                i += 1

        # Stop the currently playing chord before starting the next one
        for sound in active_chord_sounds:
            sound.fadeout(440)  # Apply a fadeout before stopping the chord sound

        # Play the next chord after the loop
        chord_number = chord_sequence[chord_index]
        chord_key = list(chord_sounds.keys())[chord_number - 1]  # Chord numbers are 1-based
        active_chord_sounds = [sound for sound in chord_sounds[chord_key]]
        for sound in active_chord_sounds:
            sound.set_volume(chord_volume)
            sound.play(-1)

        # Move to the next chord in the sequence
        chord_index = (chord_index + 1) % len(chord_sequence)



def load_chord_sequence(file_name):
    with open(file_name, 'r') as file:
        sequence = [int(line.strip()) for line in file.readlines() if line.strip().isdigit()]
    return sequence

def display_note_name(screen, font, note_name, roman_numeral):
    screen.fill((0, 0, 0))  # Clear the screen with black

    # Render the Roman numeral above the note name
    roman_surface = font.render(roman_numeral, True, (255, 255, 255))  # Render the Roman numeral in white
    roman_rect = roman_surface.get_rect(center=(screen.get_width() // 2, screen.get_height() // 3))
    screen.blit(roman_surface, roman_rect)  # Draw the Roman numeral on the screen

    # Render the note name below the Roman numeral
    text_surface = font.render(note_name, True, (255, 255, 255))  # Render the note name in white
    text_rect = text_surface.get_rect(center=(screen.get_width() // 2, screen.get_height() // 2))
    screen.blit(text_surface, text_rect)  # Draw the text on the screen

    pygame.display.flip()  # Update the screen


async def handle_events(screen, font, sounds, note_names, chord_sounds, key_to_chord, stop_event, chord_sequence):
    active_sounds = {}
    active_chord_sounds = {}
    note_stream = NoteStream(screen.get_width(), font)  # Initialize the NoteStream

    snare = synth.generate_snare_sound()
    kick = synth.generate_kick_sound()
    drum_hit = synth.generate_drum_hit_sound()
    sound_map = {
        'K': kick,
        'S': snare,
        'H': drum_hit,
    }

    rest_durations = {
        '.': 0.25,
        '-': 0.4,
        '_': 1,
    }

    sequence = synth.load_percussion_sequence('percussion.txt')
    roman_numeral = "consul"
    note_name = "hello"
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                stop_event.set()
                return
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    if not stop_event.is_set():
                        stop_event.set()
                    else:
                        stop_event.clear()
                        asyncio.create_task(
                            play_percussion_sequence(sequence, sound_map, rest_durations, stop_event, chord_sounds,
                                                     chord_sequence))
                elif event.key in sounds:
                    note_name = note_names[event.key]
                    # Get the index of the key and wrap it around using modulo
                    index = list(note_names.keys()).index(event.key) % 7
                    # Determine the Roman numeral based on the key and scale
                    if scale == 2:
                        roman_numeral = roman_numerals_minor[index]
                    else:
                        roman_numeral = roman_numerals_major[index]

                    # Add the Roman numeral to the streaming list
                    note_stream.add_note(roman_numeral)

                    active_sounds[event.key] = sounds[event.key]
                    active_sounds[event.key].play(-1)
                elif event.key in chord_sounds:
                    if event.key in active_chord_sounds:
                        for sound in active_chord_sounds[event.key]:
                            sound.stop()
                        del active_chord_sounds[event.key]
                    index = list(chord_sounds.keys()).index(event.key) % 7
                    if scale == 2:
                        roman_numeral = roman_numerals_minor[index]
                    else:
                        roman_numeral = roman_numerals_major[index]

                    # Add the Roman numeral to the streaming list
                    note_stream.add_note(roman_numeral)

                    display_note_name(screen, font, ", ".join(key_to_chord[event.key]), roman_numeral)
                    active_chord_sounds[event.key] = []
                    for sound in chord_sounds[event.key]:
                        sound.set_volume(chord_volume)
                        sound.play(-1)
                        active_chord_sounds[event.key].append(sound)
            elif event.type == pygame.KEYUP:
                if event.key in active_sounds:
                    active_sounds[event.key].fadeout(fadeout)
                    del active_sounds[event.key]
                elif event.key in active_chord_sounds:
                    for sound in active_chord_sounds[event.key]:
                        sound.fadeout(chord_fadeout)
                    del active_chord_sounds[event.key]


        display_note_name(screen, font, note_name, roman_numeral)
        # Update and draw the streaming notes
        note_stream.update_notes()
        note_stream.draw_notes(screen)
        pygame.display.flip()

        await asyncio.sleep(0.01)  # Small sleep to avoid high CPU usage


async def main():
    pygame.mixer.pre_init(44100, -16, 1, 512)
    pygame.init()
    pygame.mixer.set_num_channels(32)

    sounds, note_names = synth.map_sounds_to_keys(starting_note, scale, pygame.K_j)

    screen = pygame.display.set_mode((400, 200))
    pygame.display.set_caption("Async Note Player")
    font = pygame.font.Font(None, 36)

    key_to_chord = synth.generate_chord_mapping(synth.transpose_note(starting_note, -1), scale)

    chord_sounds = {
        key: [synth.generate_note_sound(synth.note_frequencies[note]) for note in chord]
        for key, chord in key_to_chord.items()
    }

    chord_sequence = load_chord_sequence('chords.txt')

    stop_event = asyncio.Event()
    stop_event.set()
    # Start handling events
    await handle_events(screen, font, sounds, note_names, chord_sounds, key_to_chord, stop_event, chord_sequence)


if __name__ == "__main__":
    asyncio.run(main())