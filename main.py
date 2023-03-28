import random
import argparse
import time


class Die:
    def __init__(self):
        self.value = 0

    def roll(self):
        self.value = random.randint(1, 6)
        return self.value


class Player:
    def __init__(self, name):
        self.name = name
        self.score = 0
        self.turn_score = 0

    def reset_turn_score(self):
        self.turn_score = 0

    def roll(self, current_player, next_player):
        roll = Die().roll()
        if roll == 1:
            print(f"Unfortunate! {current_player.name} rolled a 1. {next_player.name}'s turn.")
            self.reset_turn_score()
            return 0
        else:
            self.turn_score += roll
            print(f"{self.name} rolled a {roll} (This turns total: {self.turn_score}, Total Score: {self.score})")
            return self.turn_score

    def hold(self):
        self.score += self.turn_score
        print(f"{self.name} holds. (Turn Total: {self.turn_score}, Total Score: {self.score})")
        self.reset_turn_score()


class ComputerPlayer(Player):
    def __init__(self, name):
        super().__init__(name)

    def strategy(self):
        x = self.score
        if x < 75:
            return "r"
        elif x < 100 - 25:
            return "r"
        else:
            return "h"

    def roll(self, current_player, next_player):
        decision = self.strategy()
        if decision == "h":
            self.hold()
        else:
            super().roll(current_player, next_player)


class PlayerFactory:
    def __init__(self):
        pass

    def get_player(self, name, player_type):
        if player_type == "human":
            return Player(name)
        elif player_type == "computer":
            return ComputerPlayer(name)


class Game:
    def __init__(self, player1, player2):
        self.player1 = player1
        self.player2 = player2
        self.current_player = player1
        self.next_player = player2

    def switch_players(self):
        if self.current_player == self.player1:
            self.current_player = self.player2
            self.next_player = self.player1
        else:
            self.current_player = self.player1
            self.next_player = self.player2

    def play(self):
        self.start_time = time.time()
        while self.player1.score < 100 and self.player2.score < 100: #I dont have enough time to finish debugging this unfortunately...
            if time.time() - self.start_time > 60:
                self.determine_winner()
                return
            print(f"\n{self.current_player.name}'s turn.")
            decision = input("Enter 'r' to roll or 'h' to hold: ")
            while decision not in ['r', 'h']:
                print("Enter 'r' to roll and 'h' to hold: ")
                decision = input()

            if decision == 'r':
                self.current_player.roll(self.current_player, self.next_player)
            else:
                self.current_player.hold()
                self.switch_players()

        self.determine_winner()

    def determine_winner(self):
        if self.player1.score >= 100:
            print(f"\nGame over!\n{self.player1.name} wins with a score of {self.player1.score}!"
                  f"\n{self.player2.name} came in a close second with a score of {self.player2.score}!")
        elif self.player2.score >= 100:
            print(f"\nGame over!\n{self.player2.name} wins with a score of {self.player2.score}!"
                  f"\n{self.player1.name} came in a close second with a score of {self.player1.score}!")



class TimedGameProxy:
    def __init__(self, player1_type, player2_type):
        self.game = Game(player1_type, player2_type)
        self.start_time = time.time()

    def roll(self):
        if time.time() - self.start_time > 60:
            self.determine_winner()
            return


    def hold(self):
        if time.time() - self.start_time > 60:
            self.determine_winner()
            return


    def determine_winner(self):
        if self.game.player1.score >= 100:
            print(f"\nGame over! You ran out of time.\n{self.game.player1.name} wins with a score of {self.game.player1.score}!"
                  f"\n{self.game.player2.name} came in a close second with a score of {self.game.player2.score}!")
        elif self.game.player2.score >= 100:
            print(f"\nGame over! You ran out of time.\n{self.game.player2.name} wins with a score of {self.game.player2.score}!"
                  f"\n{self.game.player1.name} came in a close second with a score of {self.game.player1.score}!")
        else:
            print(f"\nGame over! Both players have scores under 100. "
                  f"{self.game.player1.name} scored {self.game.player1.score} and "
                  f"{self.game.player2.name} scored {self.game.player2.score}. It's a draw!")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--player1', choices=['human', 'computer'], default='human')
    parser.add_argument('--player2', choices=['human', 'computer'], default='human')
    parser.add_argument('--timed', action='store_true')
    args = parser.parse_args()

    if args.timed:
        game = TimedGameProxy(args.player1, args.player2)
    else:
        game = Game(args.player1, args.player2)

    game.play()


if __name__ == "__main__":
    main()