class Yahtzee:

    @staticmethod
    def chance(d1, d2, d3, d4, d5):
        score = 0
        score += d1
        score += d2
        score += d3
        score += d4
        score += d5
        return score

    @staticmethod
    def yahtzee(dice):
        counts = [0]*(len(dice)+1)
        for die in dice:
            counts[die-1] += 1
        for i in range(len(counts)):
            if counts[i] == 5:
                return 50
        return 0

    @staticmethod
    def ones(d1, d2, d3, d4, d5):
        score = 0
        if (d1 == 1):
            score += 1
        if (d2 == 1):
            score += 1
        if (d3 == 1):
            score += 1
        if (d4 == 1):
            score += 1
        if (d5 == 1): 
            score += 1

        return score

    @staticmethod
    def twos(d1, d2, d3, d4, d5):
        score = 0
        if (d1 == 2):
             score += 2
        if (d2 == 2):
             score += 2
        if (d3 == 2):
             score += 2
        if (d4 == 2):
             score += 2
        if (d5 == 2):
             score += 2
        return score

    @staticmethod
    def threes(d1, d2, d3, d4, d5):
        score = 0
        if (d1 == 3):
             score += 3
        if (d2 == 3):
             score += 3
        if (d3 == 3):
             score += 3
        if (d4 == 3):
             score += 3
        if (d5 == 3):
             score += 3
        return score

    def __init__(self, d1, d2, d3, d4, d5):
        self.dice = [0]*5
        self.dice[0] = d1
        self.dice[1] = d2
        self.dice[2] = d3
        self.dice[3] = d4
        self.dice[4] = d5

    def fours(self):
        score = 0
        for i in range(5):
            if (self.dice[i] == 4):
                score += 4
        return score

    def fives(self):
        score = 0
        i = 0
        for i in range(len(self.dice)):
            if (self.dice[i] == 5):
                score = score + 5
        return score

    def sixes(self):
        score = 0
        for i in range(len(self.dice)):
            if (self.dice[i] == 6):
                score = score + 6
        return score

    @staticmethod
    def score_pair(d1, d2, d3, d4, d5):
        counts = [0]*6
        counts[d1-1] += 1
        counts[d2-1] += 1
        counts[d3-1] += 1
        counts[d4-1] += 1
        counts[d5-1] += 1
        i = 0
        for i in range(6):
            if (counts[6-i-1] == 2):
                return (6-i) * 2
        return 0

    @staticmethod
    def two_pair(d1, d2, d3, d4, d5):
        counts = [0]*6
        counts[d1-1] += 1
        counts[d2-1] += 1
        counts[d3-1] += 1
        counts[d4-1] += 1
        counts[d5-1] += 1
        pair_count = 0
        score = 0
        for i in range(6):
            if (counts[6-i-1] == 2):
                pair_count = pair_count + 1
                score += (6-i)

        if (pair_count == 2):
            return score * 2
        else:
            return 0

    @staticmethod
    def four_of_a_kind( d1, d2, d3, d4, d5):
        tallies = [0]*6
        tallies[d1-1] += 1
        tallies[d2-1] += 1
        tallies[d3-1] += 1
        tallies[d4-1] += 1
        tallies[d5-1] += 1
        for i in range(6):
            if (tallies[i] == 4):
                return (i+1) * 4
        return 0

    @staticmethod
    def three_of_a_kind(d1, d2, d3, d4, d5):
        tallies = [0]*6
        tallies[d1-1] += 1
        tallies[d2-1] += 1
        tallies[d3-1] += 1
        tallies[d4-1] += 1
        tallies[d5-1] += 1
        for i in range(6):
            if (tallies[i] == 3):
                return (i+1) * 3
        return 0

    @staticmethod
    def small_straight(d1, d2, d3, d4, d5):
        tallies = [0]*6
        tallies[d1-1] += 1
        tallies[d2-1] += 1
        tallies[d3-1] += 1
        tallies[d4-1] += 1
        tallies[d5-1] += 1
        if (tallies[0] == 1 and
            tallies[1] == 1 and
            tallies[2] == 1 and
            tallies[3] == 1 and
            tallies[4] == 1):
            return 15
        return 0

    @staticmethod
    def large_straight(d1, d2, d3, d4, d5):
        tallies = [0]*6
        tallies[d1-1] += 1
        tallies[d2-1] += 1
        tallies[d3-1] += 1
        tallies[d4-1] += 1
        tallies[d5-1] += 1
        if (tallies[1] == 1 and
            tallies[2] == 1 and
            tallies[3] == 1 and
            tallies[4] == 1
            and tallies[5] == 1):
            return 20
        return 0

    @staticmethod
    def full_house(d1, d2, d3, d4, d5):
        tallies = []
        has_pair = False
        
        pair_value = 0
        has_three = False
        three_value = 0
        i = 0

        tallies = [0]*6
        tallies[d1-1] += 1
        tallies[d2-1] += 1
        tallies[d3-1] += 1
        tallies[d4-1] += 1
        tallies[d5-1] += 1

        for i in range(6):
            if (tallies[i] == 2): 
                has_pair = True
                pair_value = i+1

        for i in range(6):
            if (tallies[i] == 3):
                has_three = True
                three_value = i+1

        if (has_pair and has_three):
            return pair_value * 2 + three_value * 3
        else:
            return 0
