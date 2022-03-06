import random


class ShipOfFoolsGame:
    """
    Ship of Fools is a simple classic dice game. It is played with five 
    standard 6-faced dice by two or more players.  This is in charge alloting 
    randonly generated values between 1 and 6

    """
    def __init__(self):
        """
        set_gameing with a list of 5 cup objects and hardcoding Winninscore to 21.
        """
        self.__cup = DiceCup(5)
        self.__winning_score = 21

    def round(self, name, j):
        """
            The main logic of the ship game set_games here. The logic was the first
            item to hold for banked should be 6, then after 6 the value 5 dice 
            should be banked.For the third index dice the value 4 should be banked.
            If everything was banked correctly in the above order, then the remaining
            two dices resulted values are calculated as player score. 
            
        """
        flag = False
        flag2 = False
        flag3 = False
        self.__name = name
        self.load = 0
        self.l = [0] * self.__cup.n

        for _ in range(3):
            self.__cup.roll()
            for k in range(5):
                di = self.__cup._dice[k].get_value()
                self.l[k] = di
            print(self.l)

            if not flag and 6 in self.l:
                bolle = True
                while(bolle):
                    s = self.l.index(6)
                    self.__cup.bank(s)
                    bolle = False
                flag = True
                

            if flag and not flag2 and 5 in self.l:
                bolle = True
                while(bolle):
                    c = self.l.index(5)
                    self.__cup.bank(c)
                    bolle = False
                flag2 = True

            if flag2 and not flag3 and 4 in self.l:
                bolle = True
                while(bolle):
                    cr = self.l.index(4)
                    self.__cup.bank(cr)
                    bolle = False
                flag3 = True

            if flag and flag2 and flag3:
                for i in range(5):
                    if self.l[i] > 3:
                        self.__cup.bank(i)

        if flag and flag2 and flag3:
            self.load = sum(self.l) - 15
            print(
                f"The score which is scored {self.__name} in the Round {j} is: {self.load}"
                )
        else:
            print(
                f"""The score which is scored {self.__name} in the Round {j} is: 0"""
                )

        self.__cup.release_all()

    @property
    def winScore(self):
        return self.__winning_score


class DiceCup:
    """

    This DiceCup class works for returning present dice value, banking dice value,
    unbanking dice value and rolling unbanked dice.  it is the duty of this function to 
    store the desired value and roll the remaining.
    
    """
    def __init__(self, n):
        """
        The values from a given index are 
        stored in the dice list.
        """
        self._dice = []
        self.li = [False, False, False, False, False]
        self.n = n
        for _ in range(self.n):
            die = Die()
            self._dice.append(die)

    def value(self, index):
        """ eturns the current dice value by taking a position as a
            aurgment"""
        return self._dice[index].get_value()

    def bank(self, index):
        """
        it shall bank the dice by taking a position as aurgment.
        """
        self.li[index] = True

    def is_banked(self, index):
        """it is used to check dice is
            Banked or Not."""
        return self.li[index]

    def release(self, index):
        """it shall realse the dice by taking position as
            aurgment."""
        self.li[index] = False

    def release_all(self):
        """it shall release all the dices."""
        for i in range(len(self.li)):
            self.li[i] = False

    def roll(self):
        """it shall roll the unbanked dice """
        for d in range(self.n):
            if self.is_banked(d) is False:
                self._dice[d].roll()


class Die:
    """
    This is the main class for the entering the dice value
    """
    def __init__(self):
        """ The dice value is generated here."""
        self.__output = 1

    def get_value(self):
        """ This function returns the dice value to present state."""
        return self.__output

    def roll(self):
        """ This function shall roll the dice and let generate the dice value."""
        self.__output = random.randint(1, 6)


class PlayRoom:
    """This class is in charge of monitoring the player scores and ensure equal turns
    for each of the two players.
        """
    def __init__(self):
        self.__game = 0
        self.__players = []
        self.__A = 0
        self.__B = 0

    def set_game(self, game):
        """responsible for Setting the game by creating the object ShipOfFoolsGame
            class"""
        self.__game = game

    def add_player(self, player):
        """ This function shall add_player the players to the list."""
        self.__players.append(player)

    def reset_scores(self):
        """This function shall reset all player scores to 0."""
        for i in range(len(self.__players)):
            self.__players[i].__score = 0

    def play_round(self):
        """This Function shall call the player round function for
            playing the game."""
        self.__A += 1
        for i in range(len(self.__players)):
            self.__players[i].play_round(self.__game, self.__A)

    def game_finished(self):
        """ Checking the player score and winning score return true if
            score reaches the winning score else return false."""
        self.__lc = [0] * len(self.__players)
        for i in range(len(self.__players)):
            self.__lc[i] = self.__players[i].current_score()
        if max(self.__lc) >= self.__game.winScore:
            return True
        else:
            return False

    def print_scores(self):
        """This function shall print the scores of players."""
        for i in range(len(self.__players)):
            print(f"{self.__players[i].getter()} : ", end='')
            print(self.__players[i].current_score())

    def print_winner(self):
        """This function shall print the Winner name."""
        self.__maximum = max(self.__lc)
        self.__minimum = min(self.__lc)
        if self.__minimum == self.__maximum:
            print("The Game is on Tie Play the Game Again :-)")
        elif (
              self.__maximum >= self.__game.winScore and
              self.__minimum >= self.__game.winScore
              ):
            self.__A = self.__lc.index(max(self.__lc))
            self.__B = self.__players[self.__A].getter()
            print("The Winner is", self.__B)
            #print("All the Players are in Winning State.Play Again")
        else:
            self.__A = self.__lc.index(max(self.__lc))
            self.__B = self.__players[self.__A].getter()
            print("The Winner is", self.__B)


class Player:
    """Player class consists of player name,his score and has a function
    for playing the game taking game object as a parameter.
    The identifiers of the class are :
    name : name of the player
    score : score of the player
    """
    def __init__(self, name):
        """Intilazing the name of player by his name and the score to 0"""
        self.__name = name
        self.__score = 0

    def set_name(self, name):
        """
        This function shall takes name as input and assign it to class variable.
        """
        self.__name = name

    def getter(self):
        """This function shall return the name of player."""
        return self.__name

    def current_score(self):
        """This function shall return current score of player."""
        return self.__score

    def reset(self):
        """This function shall reset the player score."""
        self.__score = 0

    def play_round(self, game, j):
        """This function shall call the round function in Game class by
            its object as a parameter."""
        self.__g = game
        self.__A = j
        self.__g.round(self.__name, self.__A)
        self.__score += self.__g.load

if __name__ == "__main__":
    room = PlayRoom()
    room.set_game(ShipOfFoolsGame())
    room.add_player(Player("Ling"))
    room.add_player(Player("Chang"))
    room.reset_scores()
    while not room.game_finished():
        room.play_round()
        room.print_scores()
    room.print_winner()
