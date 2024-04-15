import pygame
import math


# pygame setup
pygame.init()

SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

pygame.display.set_caption("Test")




#Paddle Class For Player and Opponent
#Includes a Move and Draw Methods
class Paddle():
    #Static Properies of the Paddle
    width = 28
    height = 140

    speed = 6

    color = (58, 123, 170)

    def __init__(self, x, y):

        self.x = x
        self.y = y

        self.vx = 0
        self.vy = 0




    def move(self):
        #Apply Velocity to Position
        self.y += self.vy*Paddle.speed


    def draw(self):
        pygame.draw.rect(screen, Paddle.color, pygame.Rect(self.x, self.y, Paddle.width, Paddle.height))


# Ball Class for Game Ball
#Includes Move and Draw Methods
class Ball():
    #Static Properies of the Ball
    radius = 12

    speed = 8

    color = (255, 209, 89)

    def __init__(self, x, y):

        self.x = x
        self.y = y

        self.vx = -1
        self.vy = 0




    def move(self, player, opponent):
        #Check to See if Collided With Player
        if ((player.x+25 <= self.x <= (player.x+Paddle.width)) and (player.y <= self.y <= (player.y+ Paddle.height))):
            #Bounce off Player
            self.vx *= -1
            #Find Where the Ball Hit the Player
            if (player.y <= self.y <= ((player.y+ (Paddle.height)/3))):
                self.vy = -0.25
                #print("On the top")
            elif ((player.y+ (Paddle.height)/3) <= self.y <= (player.y+ 2*((Paddle.height)/3))):
                self.vy = self.vy
                #print("In the middle")
            elif (player.y+ 2*((Paddle.height)/3)) <= self.y <= (player.y+ Paddle.height):
                    self.vy = 0.25
                    #print("On the bottom")

            #Increase Speed
            self.speed += 0.5
        #Check to See if Collided With Opponent
        elif ((opponent.x-25 <= self.x <= (opponent.x+Paddle.width)) and (opponent.y <= self.y <= (opponent.y+ Paddle.height))):
            #Bounce off Opponent
            self.vx *= -1
            #Find Where the Ball Hit the Opponent
            if (opponent.y <= self.y <= ((opponent.y+ (Paddle.height)/3))):
                self.vy = -0.25
                #print("On the top")
            elif ((opponent.y+ (opponent.height)/3) <= self.y <= (opponent.y+ 2*((Paddle.height)/3))):
                self.vy = self.vy
                #print("In the middle")
            elif (opponent.y+ 2*((opponent.height)/3)) <= self.y <= (opponent.y+ Paddle.height):
                    self.vy = 0.25
                    #print("On the bottom")

            #Increase Speed
            self.speed += 0.5

        # Normalize Velocity
        self.vx = self.vx/(math.sqrt((math.pow(self.vx,2)+math.pow(self.vy,2))))
        self.vy = self.vy/(math.sqrt((math.pow(self.vx,2)+math.pow(self.vy,2))))


        # Bounce off Screen
        if not(10 < self.y < SCREEN_HEIGHT-10):
            self.vy *= -1

        #Apply Velocity to Position
        self.x += self.vx*Ball.speed
        self.y += self.vy*Ball.speed


    def draw(self):
        pygame.draw.circle(screen, Ball.color, (self.x , self.y), Ball.radius)


def main():
    # On Ready Set Up
    running = True
    clock = pygame.time.Clock()

    #Instance Classes
    player = Paddle(20, 300)
    opponent = Paddle(SCREEN_WIDTH-Paddle.width-20, 300)
    ball = Ball(SCREEN_WIDTH/2, SCREEN_HEIGHT/2)

    #Start the Game Loop
    while running:
        #Set Tick rate
        clock.tick(60)

        #Fill Screen
        screen.fill((1, 32, 54))


        #Check for Player Input
        key = pygame.key.get_pressed()
        #If 'W' Move Up
        if key[pygame.K_w] == True:
            #Check for Bounds
            if player.y - 10 < 0:
                player.position = 0
            else:
                player.vy = -1
                player.move()
        #If 'S' Move Down
        elif key[pygame.K_s] == True:
            #Check for Bounds
            if player.y+Paddle.height + 10 > SCREEN_HEIGHT:
                player.position = SCREEN_HEIGHT
            else:
                player.vy = 1
                player.move()
        player.draw()

        #Opponent Actions
        #Find the Ball and Move to it

        #Under the Ball
        if ball.y < opponent.y + Paddle.height/2:
            #Check for Bounds
            if opponent.y - 10 < 0:
                opponent.position = 0
            else:
                opponent.vy =-1
            opponent.move()
        #At the Ball
        elif opponent.y-4 < ball.y < opponent.y + Paddle.height+4:
            opponent.vy = 0

        #Over the Ball
        elif ball.y > opponent.y + Paddle.height/2:
            #Check for Bounds
            if opponent.y+Paddle.height + 10 > SCREEN_HEIGHT:
                opponent.position = SCREEN_HEIGHT
            else:
                opponent.vy =1
            opponent.move()
        opponent.draw()

        #Move the ball
        ball.move(player, opponent)
        ball.draw()


        #Check for Quit
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        #Update Screen
        pygame.display.update()

    pygame.quit()


#Initiate the Game
if __name__ == "__main__":
    main()
