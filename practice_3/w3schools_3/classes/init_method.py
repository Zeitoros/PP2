class Player:
    def __init__(self, nickname, game, hours):
        self.nickname = nickname
        self.game = game
        self.hours = hours
    
plr_1 = Player("Zeitoros", "Terraria", 500)
print(plr_1.nickname)
print(plr_1.game)