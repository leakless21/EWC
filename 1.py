import random
import pandas as pd
#Classes
class Skills:
    def __init__(self, intu, know, time, open, end, ment):
        self.intu = intu
        self.know = know
        self.time = time
        self.open = open
        self.end = end
        self.ment = ment
class Records:
    def __init__(self, win, loss, draw, points):
        self.win = win
        self.loss = loss
        self.draw = draw
    @property
    def points(self):
        return self.win + self.draw * 0.5
class Chesser:
    def __init__(self, name, org, id, records, skills):
        self.name = name
        self.org = org
        self.id = id
        self.records = records
        self.skills = skills
class Category:
    def __init__(self,name , weights, draw):
        self.name = name
        self.weights = weights
        self.draw = draw

#Functions
def roundrobin(players): #Generate match-up for each round, each pair play each other twice
    pairings = []
    for i in range(len(players) - 1):
        roundmatch = []
        for j in range(len(players) // 2):
            player1 = players[j]
            player2 = players[len(players) - 1 - j]
            roundmatch.append((player1.id, player2.id))
            roundmatch.append((player2.id, player1.id))
        pairings.append(roundmatch)
        players = [players[0]] + [players[-1]] + players[1:-1]
    return pairings
def loadplayers(path): #Get players from csv file
    df = pd.read_csv(path)
    players = []
    for _, row in df.iterrows():
        skills = Skills(
            intu=row["Intuition"],
            know=row["Knowledge"],
            time=row["Time Management"],
            open=row["Opening"],
            end=row["Endgame"],
            ment=row["Mental"]
        )
        player = Chesser(
            id=row["ID"],
            name=row["Name"],
            org=row["Org"],
            skills=skills,
            records=Records(0, 0, 0, 0)
        )
        players.append(player)
    return players
def matchupscore(player, variation):
    return sum(s * w for s, w in zip(vars(player.skills).values(), vars(variation.weights).values()))
def drawprob(player1, player2, variation):
    endf = variation.weights.end * ((player1.skills.end + player2.skills.end) / 200)
    mentf = variation.weights.ment * ((player1.skills.ment + player2.skills.ment) / 200)
    timef = variation.weights.time * ((player1.skills.time + player2.skills.time) / 200)
    return max(0.05, min(0.6, variation.draw + endf + mentf + timef))
def simulate(player1, player2, variation):
    score1 = matchupscore(player1, variation)
    score2 = matchupscore(player2, variation)
    prob1 = score1 / (score1 + score2)
    rand = random.random()
    if rand < prob1:
        return player1
    elif rand < prob1 + drawprob(player1, player2, variation):
        return "Draw"
    else:
        return player2
def updateresult(outcome, player1, player2):
    if outcome == player1:
        player1.records.win += 1
        player2.records.loss += 1
    elif outcome == player2:
        player2.records.win += 1
        player1.records.loss += 1
    elif "Draw" in outcome:
        player1.records.draw += 1
        player2.records.draw += 1
def displayresult(players, category):
    players.sort(key=lambda p: (p.records.points, p.records.win), reverse=True)
    print(f"\n{category.name} results:")
    for i, player in enumerate(players, start=1):
        print(f"{i}. {player.name} ({player.org}): {player.records.points} pts, {player.records.win}W, {player.records.loss}L, {player.records.draw}D")
def choosevariation():
    x = int(input("""Choose a variation:
    1. Classical
    2. Rapid
    3. Blitz
    4. Freestyle
    Your choice: """))
    if x == 1:
        return Classical
    elif x == 2:
        return Rapid
    elif x == 3:
        return Blitz
    elif x == 4:
        return Freestyle
    else:
        print("Invalid input")
        return None

#Categories
Classical = Category("Classical", weights=Skills(0.15, 0.25, 0.1, 0.2, 0.2, 0.1), draw=0.2)
Rapid = Category("Rapid", weights=Skills(0.2, 0.2, 0.2, 0.15, 0.15, 0.1), draw=0.15)
Blitz = Category("Blitz", weights=Skills(0.3, 0.15, 0.25, 0.15, 0.05, 0.1), draw=0.1)
Freestyle = Category("Freestyle", weights=Skills(0.25, 0.25, 0.15, 0.1, 0.15, 0.1), draw=0.15)

#Main loop
players = loadplayers("Players.csv")
pairings = roundrobin(players)
variation = choosevariation()

# Simulate each round
for round_matches in pairings:
    for match in round_matches:
        p1_id, p2_id = match
        player1 = next(p for p in players if p.id == p1_id)
        player2 = next(p for p in players if p.id == p2_id)
        outcome = simulate(player1, player2, variation)
        updateresult(outcome, player1, player2)

displayresult(players, variation)

