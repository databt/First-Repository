import pygame
file = r'F:\艺术签名生成器\aa.mp3'
file1 = r'F:\艺术签名生成器\bb.mp3'
file2 = r'F:\艺术签名生成器\cc.mp3'
pygame.mixer.init()
track = pygame.mixer.music.load(file)
pygame.mixer.music.play()
