from boards.standard_board import StandardBoard
from boards.poly_board import PolyBoard
from render_engines.timetravel_render_engine import TimeTravelRenderEngine
from render_engines.square_render_engine import SquareRenderEngine
from render_engines.dummy_render_engine import DummyRenderEngine
from render_engines.hex_render_engine import HexRenderEngine
from rule_set import RuleSet
from rule_engines.standard_rule_engine import StandardRuleEngine
from piece import Piece
from variants import Variants
from tile import Tile
from teams.team import Team, TeamPresets as tp
import pygame
import random
import matplotlib.pyplot as plt

if __name__ == "__main__":
    pygame.init()
    renderer = DummyRenderEngine()

    renderer.test_ais(['minmax_sib-8', 'minmax_lib-8'], 50, 50)



    # win_loss_dist = []
    # win_loss_white_dist = []
    # win_loss_black_dist = []
    # avg_turn_dist = {'minmax_sib-8': [], 'minmax_lib-8': []}
    
    # # Create a new figure
    # plt.figure(figsize=(15, 5))

    # for i in range(50):
    #     wins = {'minmax_sib-8': 0, 'minmax_lib-8': 0}
    #     wins_white = {'minmax_sib-8': 0, 'minmax_lib-8': 0}
    #     wins_black = {'minmax_sib-8': 0, 'minmax_lib-8': 0}
    #     average_turns = {'minmax_sib-8': 0, 'minmax_lib-8': 0}
    #     ai_list = ['minmax_sib-8', 'minmax_lib-8']
    #     for j in range(50):
    #         random.shuffle(ai_list)
    #         ais = dict(zip(['white', 'black'], ai_list))
    #         new_game = renderer.copy()
    #         winner, turns = new_game.initialize((800, 600), ais, 1)
    #         print(f'sample {i+1} game {j+1}: {ais[winner]} won in {turns} turns')
    #         wins[ais[winner]] += 1
    #         if ais['white'] == 'minmax_sib-8':
    #             wins_white[ais[winner]] += 1
    #         else:
    #             wins_black[ais[winner]] += 1
    #         average_turns[ais[winner]] += turns
    #     for team in average_turns:
    #         average_turns[team] /= 50.0
    #     win_loss = wins['minmax_sib-8']/(wins['minmax_lib-8'])
    #     win_loss_dist.append(win_loss)
    #     win_loss_white = wins_white['minmax_sib-8']/(wins_white['minmax_lib-8'])
    #     win_loss_white_dist.append(win_loss_white)
    #     win_loss_black = wins_black['minmax_sib-8']/(wins_black['minmax_lib-8'])
    #     win_loss_black_dist.append(win_loss_black)
    #     for team in avg_turn_dist:
    #         avg_turn_dist[team].append(average_turns[team])
    #     print(f'wins-loss: {win_loss}\navg turns: {average_turns}')

    #     plt.clf()
    #     # Create the win-loss distribution subplot (1 row, 2 columns, 1st plot)
    #     plt.subplot(1, 2, 1)
    #     plt.hist(win_loss_dist, bins=20, alpha=0.75, label=['total'])
    #     plt.hist(win_loss_white_dist, bins=20, alpha=0.75, label=['white'])
    #     plt.hist(win_loss_black_dist, bins=20, alpha=0.75, label=['black'])
    #     plt.xlabel('Win-Loss Ratio (minmax_sib-8)')
    #     plt.ylabel('Frequency')
    #     plt.title('Win-Loss Distribution')
    #     plt.legend(loc='upper right')
    #     plt.grid(True)

    #     # Create the average number of turns distribution subplot (1 row, 2 columns, 2nd plot)
    #     plt.subplot(1, 2, 2)
    #     for team, turns in avg_turn_dist.items():
    #         plt.hist(turns, bins=20, alpha=0.75, label=team)
    #     plt.xlabel('Average Number of Turns')
    #     plt.ylabel('Frequency')
    #     plt.title('Average Number of Turns Distribution')
    #     plt.legend(loc='upper right')
    #     plt.grid(True)

    #     plt.draw()
    #     plt.pause(0.1)

    # # Display both subplots at the same time
    # plt.show()

