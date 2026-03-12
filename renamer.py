import os

# Define the path to the directory containing the music note files
directory = 'sounds/'

# Get a sorted list of the filenames in the directory
filenames = sorted([f for f in os.listdir(directory) if f.endswith('.wav')])

# Define the notes and octaves
notes = ["A", "A#", "B", "C", "C#", "D", "D#", "E", "F", "F#", "G", "G#"]

# Generate the note names dynamically
note_names = []
for octave in range(0, 9):  # From octave 0 to 8
    for note in notes:
        note_name = f"{note}{octave}"
        note_names.append(note_name)
        if len(note_names) == len(filenames):
            break
    if len(note_names) == len(filenames):
        break

# Ensure the number of note names matches the number of files
if len(note_names) != len(filenames):
    raise ValueError("Number of filenames does not match the number of note names.")

# Rename each file
for i, filename in enumerate(filenames):
    old_path = os.path.join(directory, filename)
    new_name = f"{note_names[i]}.wav"
    new_path = os.path.join(directory, new_name)
    os.rename(old_path, new_path)
    print(f"Renamed {filename} to {new_name}")
