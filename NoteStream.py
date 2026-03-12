class NoteStream:
    def __init__(self, screen_width, font):
        self.notes = []
        self.screen_width = screen_width
        self.font = font

    def add_note(self, note):
        # Each note starts at the right side of the screen with full opacity
        self.notes.append({'text': note, 'x': self.screen_width, 'opacity': 255})

    def update_notes(self):
        # Update the position and opacity of each note
        for note in self.notes:
            note['x'] -= 2  # Move the note leftward
            note['opacity'] -= 1  # Gradually reduce opacity

        # Remove notes that have moved off the screen or faded out
        self.notes = [note for note in self.notes if note['x'] > -50 and note['opacity'] > 0]

    def draw_notes(self, screen):
        for note in self.notes:
            text_surface = self.font.render(note['text'], True, (255, 255, 255))
            text_surface.set_alpha(note['opacity'])
            screen.blit(text_surface, (note['x'], screen.get_height() - 50))  # Draw near the bottom


