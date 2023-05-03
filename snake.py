import pygame
import sys 
import random
import datetime, time

pygame.init()

SW, SH = 800, 800
score=0
crtime=0

BLOCK_SIZE = 50
FONT = pygame.font.SysFont("arial", BLOCK_SIZE*2)

screen = pygame.display.set_mode((800, 800))
pygame.display.set_caption("Snake!")
clock = pygame.time.Clock()

class Snake:
    def __init__(self):
        self.x, self.y = BLOCK_SIZE, BLOCK_SIZE
        self.xdir = 1
        self.ydir = 0
        self.head = pygame.Rect(self.x, self.y, BLOCK_SIZE, BLOCK_SIZE)
        self.body = [pygame.Rect(self.x-BLOCK_SIZE, self.y, BLOCK_SIZE, BLOCK_SIZE)]
        self.dead = False
    
    def update(self):
        global apple
        global score
        for square in self.body:
            if self.head.x == square.x and self.head.y == square.y:
                self.dead = True
                
            if self.head.x not in range(0, SW) or self.head.y not in range(0, SH):
                self.dead = True
                
        if self.dead:
            time.sleep(1)
            self.x, self.y = BLOCK_SIZE, BLOCK_SIZE
            self.head = pygame.Rect(self.x, self.y, BLOCK_SIZE, BLOCK_SIZE)
            self.body = [pygame.Rect(self.x-BLOCK_SIZE, self.y, BLOCK_SIZE, BLOCK_SIZE)]
            self.xdir = 1
            self.ydir = 0
            self.dead = False
            score=0
            apple=Apple()
        
        self.body.append(self.head)
        for i in range(len(self.body)-1):
            self.body[i].x, self.body[i].y = self.body[i+1].x, self.body[i+1].y
        self.head.x += self.xdir * BLOCK_SIZE
        self.head.y += self.ydir * BLOCK_SIZE
        self.body.remove(self.head)

class Apple:
    def __init__(self):
        
        self.x = int(random.randint(0, SW)/BLOCK_SIZE) * BLOCK_SIZE
        self.y = int(random.randint(0, SH)/BLOCK_SIZE) * BLOCK_SIZE
        self.rect = pygame.Rect(self.x, self.y, BLOCK_SIZE, BLOCK_SIZE)

    def update(self):
        pygame.draw.rect(screen, "red", self.rect)


class Mandarin:
    def __init__(self):
        self.x = int(random.randint(0, SW)/BLOCK_SIZE) * BLOCK_SIZE
        self.y = int(random.randint(0, SH)/BLOCK_SIZE) * BLOCK_SIZE
        self.rect = pygame.Rect(self.x, self.y, BLOCK_SIZE, BLOCK_SIZE)
    
    def update(self):
        pygame.draw.rect(screen, "orange", self.rect)


def drawGrid():
    for x in range(0, SW, BLOCK_SIZE):
        for y in range(0, SH, BLOCK_SIZE):
            rect = pygame.Rect(x, y, BLOCK_SIZE, BLOCK_SIZE)
            pygame.draw.rect(screen, "#3c3c3b", rect, 1)

scoref = FONT.render(str(score), False, (255, 255,255))
score_rect = scoref.get_rect(center=(SW/2, SH/20))

drawGrid()

snake = Snake()

apple = Apple()

apple_timer=time.time()

mandarin=Mandarin()

while True:
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_DOWN:
                if snake.ydir!=-1:
                    snake.ydir = 1
                    snake.xdir = 0
            elif event.key == pygame.K_UP:
                if snake.ydir!=1:
                    snake.ydir = -1
                    snake.xdir = 0
            elif event.key == pygame.K_RIGHT:
                if snake.xdir!=-1:
                    snake.ydir = 0
                    snake.xdir = 1
            elif event.key == pygame.K_LEFT:
                if snake.xdir!=1:
                    snake.ydir = 0
                    snake.xdir = -1
            

    snake.update()
    
    screen.fill('black')
    drawGrid()

    scoref = FONT.render(str(score), True, "white")
    
    pygame.draw.rect(screen, "green", snake.head)

    for square in snake.body:
        pygame.draw.rect(screen, "green", square)

    screen.blit(scoref, score_rect)
    
    if score>=3 and score<=10:
        mandarin.update()
        if snake.head.x == mandarin.x and snake.head.y == mandarin.y:
            snake.body.append(pygame.Rect(square.x, square.y, BLOCK_SIZE, BLOCK_SIZE))
            mandarin = Mandarin()
            score+=3
    else:  
        apple.update()
        if snake.head.x == apple.x and snake.head.y == apple.y:
            snake.body.append(pygame.Rect(square.x, square.y, BLOCK_SIZE, BLOCK_SIZE))
            apple = Apple()
            score+=1
    if score>10: 

        if time.time() - apple_timer > 8:
            apple=Apple()
            apple_timer=time.time()
            
        else:
            if snake.head.x == apple.x and snake.head.y == apple.y:
                snake.body.append(pygame.Rect(square.x, square.y, BLOCK_SIZE, BLOCK_SIZE))
                score+=5
                apple.update()
                apple_timer = time.time()
     
    pygame.display.update()
    clock.tick(5)