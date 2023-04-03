from boards import *
from render_engines import *
from rule_engines import *
import pygame
import matplotlib.pyplot as plt
import random

if __name__ == "__main__":
    pygame.init()

    renderer = Variants.load('square/dynamove')

    renderer.initialize((800, 600))
    plt.show()
