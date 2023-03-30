'''
Copyright 2023 Sam A. Haygood

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
'''

from boards import *
from rule_engines import *
from render_engines import AbstractRenderEngine
import matplotlib.pyplot as plt
from matplotlib.patches import Patch
from concurrent.futures import ThreadPoolExecutor
import concurrent
import numpy as np

class DummyRenderEngine(AbstractRenderEngine):
    def __init__(self, board: AbstractBoard = None, rule_engine: AbstractRenderEngine = None):
        if board == None:
            self.board = StandardBoard()
        else:
            self.board = board
        if rule_engine == None:
            self.rule_engine = StandardRuleEngine()
        else:
            self.rule_engine = rule_engine

    def copy(self):
        copy_engine = DummyRenderEngine(self.board.copy(), self.rule_engine.copy())
        return copy_engine
    
    def draw_board(self):
        pass

    def draw_pieces(self):
        pass

    def initialize(self, ai_teams):
        self.ai_teams = ai_teams
        return self.main_loop()
    
    def main_loop(self):
        turn = 1
        while True:
            if (not self.rule_engine.all_legal_moves(self.board.current_team, self.board) and len(self.rule_engine.teams) > 2) or \
            self.board.current_team not in [self.board.get_tile(tile).piece.team.name for tile in self.board.royal_tiles if self.board.get_tile(tile).piece != None]:
                current_team = self.board.current_team
                next_index = self.rule_engine.turn_order.index(self.board.current_team) + 1
                if next_index in range(len(self.rule_engine.turn_order)):
                    self.board.current_team = self.rule_engine.turn_order[next_index]
                else:
                    self.board.current_team = self.rule_engine.turn_order[0]
                try:
                    self.rule_engine.turn_order.remove(current_team)
                    if len(self.rule_engine.turn_order) == 1:
                        break
                except:
                    pass

            if self.board.current_team in self.ai_teams and len(self.rule_engine.turn_order) > 1:
                if self.board.current_team == self.rule_engine.turn_order[-1]:
                    turn += 1
                self.board = self.rule_engine.ai_play(self.board, False, self.ai_teams[self.board.current_team])
        
        return self.rule_engine.turn_order[0], turn
    
    def run_games(self, ai_teams, i, games):
        wins = {ai: 0 for ai in ai_teams.values()}
        avg_turns = {ai: 0 for ai in ai_teams.values()}
        for j in range(games):
            dummy_render_engine = self.copy()
            winner, turns = dummy_render_engine.initialize(ai_teams)
            self.completed_games += 1
            print(f'finished game {self.completed_games} out of {self.total_games}: {ai_teams[winner]} won in {turns} turns')
            wins[ai_teams[winner]] += 1
            avg_turns[ai_teams[winner]] += turns
        return wins, avg_turns

    def test_ais(self, ai_list, samples, games, save=False):
        win_percent_dist = {ai: [] for ai in ai_list}
        avg_turn_dist = {ai: [] for ai in ai_list}
        relative_elo_rating = {ai: 0 for ai in ai_list}
        ai_teams = dict(zip(self.rule_engine.turn_order, ai_list))

        self.total_games = samples*games
        self.completed_games = 0

        plt.figure(figsize=(15, 5))

        with ThreadPoolExecutor() as executor:
            # for i in range(samples):
            future_to_results = {executor.submit(self.run_games, ai_teams, i, games): i for i in range(samples)}
            for future in concurrent.futures.as_completed(future_to_results):
                i = future_to_results[future]
                wins, avg_turns = future.result()

                avg_turns = {ai: avg_turns[ai] / games for ai in avg_turns}
                win_percent = {ai: wins[ai] / games for ai in wins}
                relative_elo_rating = {ai: relative_elo_rating[ai] + 32*(wins[ai] - sum(wins[enemy] for enemy in wins if enemy != ai)) for ai in relative_elo_rating}
                for ai in win_percent:
                    win_percent_dist[ai].append(win_percent[ai])

                for ai in avg_turns:
                    avg_turn_dist[ai].append(avg_turns[ai])

            plt.clf()
            # Create the win percent distribution subplot (1 row, 2 columns, 1st plot)
            plt.subplot(1, 2, 1)
            for team, win_rate in win_percent_dist.items():
                n, bins, patches = plt.hist(win_rate, bins=20, alpha=0.75, label=team)
                mean_win_percent = np.mean(win_rate)
                std_win_percent = np.std(win_rate)
                bar_color = patches[0].get_facecolor()
                plt.axvline(mean_win_percent, linestyle='dashed', linewidth=1, color=bar_color)
                plt.text(mean_win_percent, plt.gca().get_ylim()[1] * 0.01, f'{mean_win_percent:.2f}', color=bar_color)
            plt.xlabel('Win %')
            plt.ylabel('Frequency')
            plt.legend(loc='upper right')
            plt.grid(True)

            # Create the average number of turns distribution subplot (1 row, 2 columns, 2nd plot)
            plt.subplot(1, 2, 2)
            for team, turns in avg_turn_dist.items():
                n, bins, patches = plt.hist(turns, bins=20, alpha=0.75, label=team)
                mean_turns = np.mean(turns)
                std_turns = np.std(turns)
                bar_color = patches[0].get_facecolor()
                plt.axvline(mean_turns, linestyle='dashed', linewidth=1, color=bar_color)
                plt.text(mean_turns, plt.gca().get_ylim()[1] * 0.01, f'{mean_turns:.1f}', color=bar_color)
            plt.xlabel('Average Number of Turns')
            plt.ylabel('Frequency')
            plt.legend(loc='upper right')
            plt.grid(True)

            plt.draw()
            plt.pause(0.1)

        # Display both subplots at the same time
        if save:
            plt.savefig(f"algorithm_stats/{' vs '.join(ai_list)}.png")
        return win_percent_dist, avg_turn_dist