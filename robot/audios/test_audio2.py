import pygame

pygame.mixer.init()
sound = pygame.mixer.Sound('/home/dadou/deploy/audios/gig.wav')
playing = sound.play()
while playing.get_busy():
    pygame.time.delay(100)