from gpiozero import RGBLED, LEDBoard, Button
import time
from signal import pause
from typing import List

round = 0
won = False

class Player:
    count = 1
    def __init__(self, rgb:RGBLED, health_bar:LEDBoard, button:Button):
        self.rgb = rgb
        self.health_bar = health_bar
        self.button = button
        self.lives = 4
        
        self.name = Player.count
        Player.count += 1

        self.button.when_pressed = self.buttonClicked

        self.turn = False
        self.simon = False

        self.start_time = None
        self.times = [0]


    def setEnemy(self, enemy) -> None:
        self.enemy = enemy

    def showLives(self) -> None:
        self.health_bar.value = (0 if i > self.lives else 1 for i in range(4, 0, -1))
        if self.simon:
            self.rgb.color = (0.1, 0.3, 0.9)
        else:
            pass

    def toggleTurn(self) -> None:
        self.turn = not self.turn
        if self.turn:
            self.rgb.color = (0.1, 0.3, 0.9)
        else:
            self.rgb.off()
    def toggleSimon(self) -> bool:
        self.simon = not self.simon
        if self.simon:
            self.rgb.color = (0.1, 0.3, 0.9)
    
    def resetTimes(self) -> None:
        self.start_time = None
        self.times = [0]
    
    def hasSpoken(self) -> bool:
        if self.start_time:
            return time.time() - self.start_time >= 2
        else:
            return False
    def hasRepliedCorrectly(self):
        simon = self.enemy

        #The user has pressed too many or to few times
        if len(simon.times) != len(self.times):
            return False

        #There time between clicks must match simon's within 0.5+-
        for p_t, s_t in zip(simon.times, self.times):
            if not (s_t - 0.5 <= p_t <= s_t + 0.5):
                return False
        return True

    def buttonClicked(self) -> None:
        if self.turn:
            if not self.start_time:
                self.start_time = time.time()
            else:
                elapsed_time = time.time() - self.start_time
                self.start_time = time.time()
                self.times.append(elapsed_time)

    def flash(self, colour=(0.1, 0.3, 0.9)):
        time.sleep(0.5)
        for _ in range(3):
            self.rgb.off()
            time.sleep(0.1)
            self.rgb.color = colour
            time.sleep(0.1)
        self.rgb.off()
        time.sleep(0.5)
    def winningDance(self):
        for _ in range(2):
            self.health_bar.off()
            time.sleep(0.5)
            self.health_bar.on()
            time.sleep(0.5)
        
        for _ in range(4):
            self.health_bar.value = (1, 0, 0, 0)
            time.sleep(0.1)
            self.health_bar.value = (0, 1, 0, 0)
            time.sleep(0.1)
            self.health_bar.value = (0, 0, 1, 0)
            time.sleep(0.1)
            self.health_bar.value = (0, 0, 0, 1)
            time.sleep(0.1)
            self.health_bar.value = (0, 0, 1, 0)
            time.sleep(0.1)
            self.health_bar.value = (0, 1, 0, 0)
            time.sleep(0.1)
            
        
        self.health_bar.on()
        self.flash((0, 1, 0))
        self.rgb.color = (0, 1, 0)



class Game:
    def __init__(self, players : List[Player]):
        self.players = players
        self.curr = players[0]
        self.curr.turn = True
        self.curr.simon = True

    def toggleSimon(self):
        for player in self.players:
            player.toggleSimon()
            player.resetTimes()

            if player.simon:
                self.curr = player

    def toggleTurn(self):
        for player in self.players:
            player.toggleTurn()

    def showPlayerLives(self):
        for player in self.players:
            player.showLives()

    def play(self):
        while True:
            self.showPlayerLives()
            
            while self.curr.turn:
                if self.curr.simon and self.curr.hasSpoken():
                    break
                else:
                    pass

            self.toggleTurn()
    
            enemy = self.curr.enemy

            while not enemy.hasSpoken():
                pass
                    
            if enemy.hasRepliedCorrectly():
                enemy.flash((0, 1, 0))
            else:
                enemy.flash((1, 0, 0))
                self.curr.enemy.lives -= 1
                if enemy.lives == 0:
                    enemy.showLives()
                    self.curr.winningDance()
                    break

            self.toggleSimon()


p1 = Player(RGBLED(21, 20, 16), LEDBoard( 5, 6, 13, 19), Button(26))
p2 = Player(RGBLED(23, 18, 15), LEDBoard(17, 4, 3, 2), Button(14))
p1.setEnemy(p2)
p2.setEnemy(p1)

print("Please note, that if you do not press the button for 2 seconds after your first initial click your turn will be over")
game = Game([p1, p2])
game.play()
pause()

