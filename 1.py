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
        self.win = 0
        self.loss = 0
        self.draw = 0
        self.points = win + draw * 0.5
class Chesser:
    def __init__(self, name, org, id, records, skills):
        self.name = name
        self.org = org
        self.id = id
        self.records = records
        self.skills = skills
    def __str__(self):
        return f"{self.name} : {self.records.points}"

def roundrobin(players):
    pairings = []
    for i in range(len(players) - 1):
        for j in range(len(players) // 2):
            player1 = players[j]["id"]
            player2 = players[len(players) - 1 - j]["id"]
