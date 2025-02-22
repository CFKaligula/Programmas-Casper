﻿from abc import ABC, abstractmethod
import globals
from random import choice


def get_counts_in_list(list):
    count_dict = {}
    for elem in list:
        if elem == 'worm':
            if elem in count_dict:
                count_dict[elem] += 5
            else:
                count_dict[elem] = 5

        else:
            if elem in count_dict:
                count_dict[elem] += elem
            else:
                count_dict[elem] = elem
    return count_dict

def get_scores_in_dice_roll(dice_roll, dice_in_hand):
    #for the dice option you take, remove the average value of a dice 
    # this way taking three 3s is not better than 2 5s
    # and also remove a number valueing the opportunity you lost by taking that option
    # (if you take a 5 now, you lose the chance to ever take 5 again that turn)
    count_dict = {}
    sum_dict = {}
    remaining_dice_dict = {}
    choosable_dice_options = (set(globals._DICE_OPTIONS) - {"worm"}) - (set(dice_in_hand))
    
    average_die_val = sum(set(choosable_dice_options)) / len(set(choosable_dice_options))
    #average_die_val = 3
    
    for elem in dice_roll:  
        if elem == 'worm':
            if elem in count_dict:
                sum_dict[elem] += 5 - average_die_val
                count_dict[elem] += 1
                remaining_dice_dict[elem] -= 1
            else:
                sum_dict[elem] = 5 - average_die_val
                count_dict[elem] = 1
                remaining_dice_dict[elem] = globals._NUMBER_OF_DICE - len(dice_in_hand) -1

        else:
            if elem in count_dict:
                sum_dict[elem] += elem - average_die_val
                count_dict[elem] += 1
                remaining_dice_dict[elem] -= 1
            else:
                sum_dict[elem] = elem - average_die_val
                count_dict[elem] = 1
                remaining_dice_dict[elem] = globals._NUMBER_OF_DICE - len(dice_in_hand) -1

    for elem in sum_dict:
        sum_dict[elem] = sum_dict[elem] - (remaining_dice_dict[elem]* elem/6)
    if globals.verbose:
        print(sum_dict)
        print(count_dict)
        print(remaining_dice_dict)
    return sum_dict
    
class abstract_player(ABC):

    def __init__(self, player_name):
        self.player_name = player_name
        self.dice_in_hand = []
        if globals.verbose:
            print("initialized ab player", self.player_name)
        pass

    @abstractmethod
    def decide_roll_or_stop(self):
        print("not implemented!")

    @abstractmethod
    def decide_dice(self, dice_roll):
        print("not implemented!")

    def duplicate_chance(self):
        unique_dice_in_hand = list(set(self.dice_in_hand))
        return len(unique_dice_in_hand)/6

    def dice_sum(self):
        sum = 0
        for die in self.dice_in_hand:
            if die == "worm":
                sum += 5
            else:
                sum += die
        return sum

    def check_valid_hand_to_pick_tile(self):
        stealable_tiles = list(globals.get_stealable_tiles_dict(self.player_name).keys())
        if globals.verbose:
            print("stealable tiles", stealable_tiles)
        dice_sum = self.dice_sum()
        return ((dice_sum >= globals.active_tiles[0]) or dice_sum in stealable_tiles) and ("worm" in self.dice_in_hand)


class human_player(abstract_player):
    def __init__(self, *args):
        if globals.verbose:
            print("initialized simple player")
        super().__init__(*args)

    def decide_roll_or_stop(self):
        user_input = input("Do you want to roll or stop? (r/s)")
        if user_input.startswith("r"):
            result = "roll"
        else:
            result = "stop"

        return result

    def decide_dice(self, dice_roll):
        dice_roll_options = list(filter(lambda x: x not in self.dice_in_hand, dice_roll))
        user_input = input(f"What dice do you want to pick? {list(set(dice_roll_options))}")
        if user_input.startswith("w"):
            user_input = "worm"
        if user_input.isnumeric():
            user_input = int(user_input)
        while user_input not in dice_roll_options:
            user_input = input(f"NOT A VALID OPTION!!\nWhat dice do you want to pick? {list(set(dice_roll_options))}")
            if user_input != "worm":
                user_input = int(user_input)

        return user_input


class random_player(abstract_player):
    def __init__(self, *args):
        if globals.verbose:
            print("initialized simple player")
        super().__init__(*args)

    def decide_roll_or_stop(self):
        result = "roll"
        if len(self.dice_in_hand) == 0:
            result = "roll"
        # if we have enough dice to pick the lowest tile and atleast one worm, stop
        elif self.check_valid_hand_to_pick_tile():
            result = "stop"

        return result

    def decide_dice(self, dice_roll):
        dice_roll_numbers = list(filter(lambda x: x not in self.dice_in_hand, dice_roll))
        return choice(list(set(dice_roll_numbers)))


class simple_player(abstract_player):
    def __init__(self, *args):
        if globals.verbose:
            print("initialized simple player")
        super().__init__(*args)

    def decide_roll_or_stop(self):
        result = "roll"
        if len(self.dice_in_hand) == 0:
            result = "roll"
        # if we have enough dice to pick the lowest tile and atleast one worm, stop
        elif self.check_valid_hand_to_pick_tile():
            result = "stop"

        return result

    def decide_dice(self, dice_roll):
        result = 0
        # if we do not have a worm and a worm is in the dice roll, take it
        if "worm" in dice_roll and "worm" not in self.dice_in_hand:
            result = "worm"
        else:
            dice_roll_numbers = list(filter(lambda x: type(x) == int and x not in self.dice_in_hand, dice_roll))
            result = max(dice_roll_numbers)
            #result = choice(list(set(dice_roll_numbers)))

        return result
    
    
class score_player(abstract_player):
    def __init__(self, *args):
        if globals.verbose:
            print("initialized simple player")
        super().__init__(*args)

    def decide_roll_or_stop(self):
        result = "roll"
        if len(self.dice_in_hand) == 0:
            result = "roll"
        # if we have enough dice to pick the lowest tile and atleast one worm, stop
        elif self.check_valid_hand_to_pick_tile():
            result = "stop"

        return result

    def decide_dice(self, dice_roll):
        result = 0
        # if we do not have a worm and a worm is in the dice roll, take it
        if "worm" in dice_roll and "worm" not in self.dice_in_hand:
            result = "worm"
        else:
            dice_roll_numbers = list(filter(lambda x: type(x) == int and x not in self.dice_in_hand, dice_roll))
            score_dict = globals.sorted_dict(get_scores_in_dice_roll(dice_roll_numbers, self.dice_in_hand))
            if globals.verbose:
                print("scores", score_dict)
            result = globals.key_with_max_val(score_dict)
            #result = choice(list(set(dice_roll_numbers)))

        return result


class less_dumb_player(abstract_player):
    def __init__(self, *args):
        if globals.verbose:
            print("initlized smart player")
        super().__init__(*args)

    def decide_roll_or_stop(self):
        result = "roll"
        if len(self.dice_in_hand) == 0:
            result = "roll"
        # if we have enough dice to pick the lowest tile and atleast one worm, stop
        elif self.check_valid_hand_to_pick_tile() and (self.duplicate_chance() >= 0.5 or self.dice_sum() > 25):
            result = "stop"

        return result

    def decide_dice(self, dice_roll):
        dice_roll = list(filter(lambda x: x not in self.dice_in_hand, dice_roll))
        result = 0
        # if we do not have a worm and a worm is in the dice roll, take it
        worm_count = dice_roll.count("worm")
        # if there are only worms (wormcount == len dice roll), pick worm
        # otherwise pick worm for some other constraints
        if worm_count == len(dice_roll) or \
                ((worm_count > 2 or self.duplicate_chance() >= 0.3) and ("worm" not in self.dice_in_hand and "worm" in dice_roll)):
            result = "worm"
        else:
            dice_roll_numbers = list(filter(lambda x: type(x) == int and x not in self.dice_in_hand, dice_roll))
            count_dict = globals.sorted_dict(get_counts_in_list(dice_roll_numbers))
            result = globals.key_with_max_val(count_dict)

        return result


class simple_thief(abstract_player):
    def __init__(self, *args):
        if globals.verbose:
            print("initialized thief")
        super().__init__(*args)

    def decide_roll_or_stop(self):
        result = "roll"
        if len(self.dice_in_hand) == 0:
            result = "roll"
        # if we have enough dice to pick the lowest tile and atleast one worm, stop
        # elif self.check_valid_hand_to_pick_tile() and (self.duplicate_chance() > 0.5 or self.dice_sum() > 30):
        elif self.check_valid_hand_to_pick_tile():
            result = "stop"

        return result

    def decide_dice(self, dice_roll):
        result = 0
        # if we do not have a worm and a worm is in the dice roll, take it
        if "worm" in dice_roll and "worm" not in self.dice_in_hand:
            result = "worm"
        else:
            dice_roll_numbers = list(filter(lambda x: type(x) == int and x not in self.dice_in_hand, dice_roll))
            stealable_tiles = list(globals.get_stealable_tiles_dict(self.player_name).keys())
            count_dict = globals.sorted_dict(get_counts_in_list(dice_roll_numbers))

            # check for every option whether taking it results in stealing
            # since count_dict is sorted from highest, we also always steal the highest tile possible
            for die_option in count_dict:
                if (self.dice_sum() + count_dict[die_option]) in stealable_tiles:
                    result = die_option
                    if globals.verbose:
                        print("STEAL TIME", count_dict, stealable_tiles)
                    break

            else:
                # if we found no chance to steal, just take largest sum
                result = max(dice_roll_numbers)

        return result


class less_dumb_thief(abstract_player):
    def __init__(self, *args):
        if globals.verbose:
            print("initialized thief")
        super().__init__(*args)

    def decide_roll_or_stop(self):
        result = "roll"
        if len(self.dice_in_hand) == 0:
            result = "roll"
        # if we have enough dice to pick the lowest tile and atleast one worm, stop
        elif self.check_valid_hand_to_pick_tile() and (self.duplicate_chance() >= 0.5 or self.dice_sum() > 25):
            result = "stop"

        return result

    def decide_dice(self, dice_roll):
        result = 0
        # if we do not have a worm and a worm is in the dice roll, take it
        if "worm" in dice_roll and "worm" not in self.dice_in_hand:
            result = "worm"
        else:
            dice_roll_numbers = list(filter(lambda x: type(x) == int and x not in self.dice_in_hand, dice_roll))
            stealable_tiles = list(globals.get_stealable_tiles_dict(self.player_name).keys())
            count_dict = globals.sorted_dict(get_counts_in_list(dice_roll_numbers))

            # check for every option whether taking it results in stealing
            # since count_dict is sorted from highest, we also always steal the highest tile possible
            for die_option in count_dict:
                if (self.dice_sum() + count_dict[die_option]) in stealable_tiles:
                    result = die_option
                    if globals.verbose:
                        print("STEAL TIME", count_dict, stealable_tiles)
                    break

            else:
                # if we found no chance to steal, just take largest sum
                result = globals.key_with_max_val(count_dict)

        return result


class smart_player(abstract_player):
    def __init__(self, *args):
        if globals.verbose:
            print("initialized thief")
        super().__init__(*args)

    def decide_roll_or_stop(self):
        result = "roll"
        if len(self.dice_in_hand) == 0:
            result = "roll"
        # if we have enough dice to pick the lowest tile and atleast one worm, stop
        elif self.check_valid_hand_to_pick_tile():
        
        #elif self.check_valid_hand_to_pick_tile() and (self.duplicate_chance() >= 0.5 or self.dice_sum() > 25):
            result = "stop"

        return result

    def decide_dice(self, dice_roll):
        result = None
        if "worm" in dice_roll and "worm" not in self.dice_in_hand:
            result = "worm"
        else:
            dice_roll_numbers = list(filter(lambda x: x not in self.dice_in_hand, dice_roll))
            count_dict = globals.sorted_dict(get_counts_in_list(dice_roll_numbers))

            # check for every option whether taking it results in stealing
            # since count_dict is sorted from highest, we also always steal the highest tile possible
            for die_option in count_dict:
                point_value = count_dict[die_option]
                if die_option == 'worm':
                    num_of_dice = point_value / 5
                else:
                    num_of_dice = point_value / die_option

                if die_option == 'worm' or die_option > 3:
                    # always take worms, 5s or 4s if more than 1
                    if num_of_dice > 1:
                        result = die_option
                        break
            else:
                # if not more than 2 high dice, take the highest of the lows
                possible_lows = (list(filter(lambda x: x not in self.dice_in_hand and x in dice_roll_numbers, [1, 2, 3])))
                if len(possible_lows) > 0:
                    result = max(possible_lows)
                else:
                    # if there are no lows to take, take highest last possible
                    result = max(dice_roll_numbers)

        return result
