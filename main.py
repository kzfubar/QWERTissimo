import pygame
from note_constants import NoteEnum

# Initialize pygame
pygame.init()
pygame.mixer.set_num_channels(32)

# Set up the display
screen = pygame.display.set_mode((400, 200))
pygame.display.set_caption("Note Player")

# Set up font for rendering text
font = pygame.font.Font(None, 36)

# Define a list of keys corresponding to the keyboard keys
keyboard_keys = [
    pygame.K_y, pygame.K_u, pygame.K_i, pygame.K_o, pygame.K_p, pygame.K_LEFTBRACKET,
    pygame.K_h, pygame.K_j, pygame.K_k, pygame.K_l, pygame.K_SEMICOLON, pygame.K_QUOTE,
    pygame.K_n, pygame.K_m, pygame.K_COMMA, pygame.K_PERIOD, pygame.K_SLASH, pygame.K_RSHIFT
]


def generate_chromatic_scale(start_note, start_key):
    """Generate a chromatic scale starting from the specified note and key."""
    all_notes = list(NoteEnum)
    start_index = all_notes.index(start_note)
    scale = [None] * len(keyboard_keys)

    # Find the index of the starting key in the keyboard_keys list
    start_key_index = keyboard_keys.index(start_key)

    # Map notes forwards from the starting key
    for i in range(start_key_index, len(keyboard_keys)):
        scale[i] = all_notes[(start_index + (i - start_key_index)) % len(all_notes)]

    # Map notes backwards from the starting key
    for i in range(start_key_index - 1, -1, -1):
        scale[i] = all_notes[(start_index - (start_key_index - i)) % len(all_notes)]

    return scale


def generate_scale(start_note, start_key, intervals):
    """Generate a major scale starting from the specified note and key, repeating as needed."""
    all_notes = list(NoteEnum)
    start_index = all_notes.index(start_note)
    scale = [None] * len(keyboard_keys)

    # Find the index of the starting key in the keyboard_keys list
    start_key_index = keyboard_keys.index(start_key)

    # Map notes forwards from the starting key
    current_note_index = start_index
    scale[start_key_index] = all_notes[current_note_index]

    for i in range(1, len(keyboard_keys) - start_key_index):
        interval = intervals[(i - 1) % len(intervals)]
        current_note_index = (current_note_index + interval) % len(all_notes)
        scale[start_key_index + i] = all_notes[current_note_index]

    # Map notes backwards from the starting key
    current_note_index = start_index
    for i in range(1, start_key_index + 1):
        interval = intervals[-i % len(intervals)]
        current_note_index = (current_note_index - interval) % len(all_notes)
        scale[start_key_index - i] = all_notes[current_note_index]

    return scale


def map_sounds_to_keys(scale_type, start_key):
    major_intervals = [2, 2, 1, 2, 2, 2, 1]
    minor_intervals = [2, 1, 2, 2, 1, 2, 2]

    """Map the keys to sounds based on the selected scale type and starting key."""
    if scale_type == 0:
        scale = generate_chromatic_scale(starting_note, start_key)
    elif scale_type == 1:
        scale = generate_scale(starting_note, start_key, major_intervals)
    elif scale_type == 2:
        scale = generate_scale(starting_note, start_key, minor_intervals)
    else:
        raise ValueError("Invalid scale type. Use 0 for chromatic, 1 for major, 2 for minor.")

    sounds = {keyboard_keys[i]: pygame.mixer.Sound(scale[i].value) for i in range(len(scale))}
    note_names = {keyboard_keys[i]: scale[i].name for i in range(len(scale))}

    return sounds, note_names


# Define the starting note and starting key
starting_note = NoteEnum.C3  # Change this to set the starting note programmatically
starting_key = pygame.K_j  # Specify the key in keyboard_keys to start with

# Initialize the sounds and note names with the chromatic scale (default)
sounds, note_names = map_sounds_to_keys(0, starting_key)

# Define a dictionary to map keys to chords (list of notes)
key_to_chord = {
    pygame.K_z: [NoteEnum.C3, NoteEnum.E3, NoteEnum.G3],  # C major chord
    pygame.K_x: [NoteEnum.D3, NoteEnum.F3, NoteEnum.A3],  # D minor chord
    pygame.K_c: [NoteEnum.E3, NoteEnum.G3, NoteEnum.B3],  # E minor chord
    pygame.K_v: [NoteEnum.F3, NoteEnum.A3, NoteEnum.C3],  # F major chord
}

# Load the sound files for chords
chord_sounds = {key: [pygame.mixer.Sound(note.value) for note in chord] for key, chord in key_to_chord.items()}


# Function to display text on the screen
def display_note_name(note_name):
    screen.fill((0, 0, 0))  # Clear the screen with black
    text_surface = font.render(note_name, True, (255, 255, 255))  # Render the note name in white
    text_rect = text_surface.get_rect(center=(screen.get_width() // 2, screen.get_height() // 2))
    screen.blit(text_surface, text_rect)  # Draw the text on the screen
    pygame.display.flip()  # Update the screen


# Main loop
running = True
current_scale_type = 0  # Start with chromatic scale by default
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_1:  # Press '1' to switch to chromatic scale
                current_scale_type = 0
                sounds, note_names = map_sounds_to_keys(current_scale_type, starting_key)
            elif event.key == pygame.K_2:  # Press '2' to switch to major scale
                current_scale_type = 1
                sounds, note_names = map_sounds_to_keys(current_scale_type, starting_key)
            elif event.key == pygame.K_3:  # Press '3' to switch to minor scale
                current_scale_type = 2
                sounds, note_names = map_sounds_to_keys(current_scale_type, starting_key)
            elif event.key in sounds:
                note_name = note_names[event.key]
                display_note_name(note_name)
                sounds[event.key].play()
            elif event.key in chord_sounds:
                for sound in chord_sounds[event.key]:
                    sound.play()
                display_note_name("Chord Played")  # You can modify this to show specific chord names

pygame.quit()
