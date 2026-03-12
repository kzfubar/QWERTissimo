import pygame
import numpy as np

pygame.mixer.pre_init(44100, -16, 1, 512)
pygame.init()

# Frequency and sample rate
freq = 440
sample_rate = 44100

# Generate sound
arr = np.array([4096 * np.sin(2.0 * np.pi * freq * x / sample_rate) for x in range(0, sample_rate)]).astype(np.int16)
sound = pygame.sndarray.make_sound(arr)

# Play sound
sound.play(-1)  # -1 means loop indefinitely

pygame.time.delay(1000)  # play for 1 second
pygame.quit()