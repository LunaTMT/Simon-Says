from gpiozero import RGBLED, LEDBoard, Button
from time import sleep
from signal import pause


class Player
    def __init__(self, rgb:RGBLED, health_bar:LEDBoard, button:Button):
        self.rgb = rgb
        self.health_bar = health_bar
        self.button = button
        self.lives = 4
        
        self.name = 1
        self.button.when_pressed = self.buttonClicked


    def showLives(self):
        self.health_bar.value = (0 if self.lives < i else 1 for i in range(self.lives))

    def buttonClicked(self):
        print(f"player {self.name} clicked button")

    
    def testComponents(self):
        for i in range(2):
            self.rgb.on()
            sleep(0.1)
            self.rgb.off()
            for led in self.health_bar:
                led.on()
                sleep(0.1)
                led.off()
        self.rgb.on()
        

p1 = Player(RGBLED(21, 20, 16), LEDBoard( 5, 6, 13, 19), Button(26))
p2 = Player(RGBLED(23, 18, 15), LEDBoard(2, 3, 4, 17), Button(14))
players = [p1, p2]

for player in players:
    player.testComponents()

pause()

