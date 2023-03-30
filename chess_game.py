from boards import *
from render_engines import *
from rule_engines import *
import pygame
import matplotlib.pyplot as plt

if __name__ == "__main__":
    pygame.init()

    renderer = Variants.load('square/glass_cannon')
    renderer.initialize((800, 600), {'black': 'minmax_sib_smart-8'})

    plt.show()
