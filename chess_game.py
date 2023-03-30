from boards import *
from render_engines import *
from rule_engines import *
import pygame
import matplotlib.pyplot as plt

if __name__ == "__main__":
    pygame.init()
    renderer = DummyRenderEngine()

    renderer.test_ais(['minmax_sib-8', 'minmax_lib-8'], 100, 50, True)
    renderer.test_ais(['minmax_lib-8', 'minmax_sib-8'], 100, 50, True)
    renderer.test_ais(['minmax_sib-8', 'minmax_sib_smart-8'], 100, 50, True)
    renderer.test_ais(['minmax_sib_smart-8', 'minmax_sib-8'], 100, 50, True)

    plt.show()
