import os
from enum import Enum

# Define the path to the directory containing the music note files
directory = 'sounds/'

# Define the notes and octaves
notes = ["A", "A#", "B", "C", "C#", "D", "D#", "E", "F", "F#", "G", "G#"]

# Generate the note names dynamically and map them to file paths
note_paths = {}
for octave in range(0, 9):  # From octave 0 to 8
    for note in notes:
        note_name = f"{note}{octave}"
        note_path = f"{directory}/{note_name}.wav"
        note_paths[note_name] = note_path
        if len(note_paths) == 64:  # Stop once we have the first 64 notes
            break
    if len(note_paths) == 64:
        break

# Write the Enum class to a file
with open('note_constants.py', 'w') as f:
    f.write("from enum import Enum\n\n")
    f.write("class NoteEnum(Enum):\n")
    for note_name, note_path in note_paths.items():
        # Replace sharp (#) with "S" to make it a valid identifier
        enum_name = note_name.replace("#", "S")
        f.write(f"    {enum_name} = \"{note_path}\"\n")

print("Enum class 'NoteEnum' has been generated in 'note_constants.py'.")
