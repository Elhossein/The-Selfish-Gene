"""creature class module"""
import math
import random
import pygame
import genome


class Creature():
    """creature has different attributes based off its genes"""
    img1 = pygame.image.load('assets/creature.png')
    img2 = pygame.image.load('assets/mating_creature.png')

    def __init__(self, x, y, gene=0):
        self.gene = genome.Genome(gene)
        # self.gene.mutate()
        self.x_pos = x
        self.y_pos = y
        self.rad = 10
        self.aggro = self.gene.dna['aggro']
        self.speed = 2
        self.c_img = pygame.transform.scale(self.img1, (self.rad*2, self.rad*2))
        self.ac_img = pygame.transform.scale(self.img2, (self.rad*2, self.rad*2))
        self.closest_food = 0
        self.wander_dir = random.randrange(4)
        self.wander_count = 1000
        self.energy = 100
        self.vision = 100

    def move(self, all_ctr, all_food, hunted_food, time):
        """moves creature"""
        self.energy -= 0.4
        other_move = False
  

        # should rework that with good algorithm
        if not other_move:

            if self.closest_food not in all_food.keys():
                for apple in all_food.keys():
                    if self.distance((self.x_pos, self.y_pos), (apple.x_pos, apple.y_pos)) <= self.vision and len(all_food[apple]) <= 1:
                        self.closest_food = apple
                        all_food[apple].append(self)
                        break
            if self.closest_food != 0 and self.closest_food in all_food.keys():
                self.move_towards(self.closest_food.x_pos, self.closest_food.y_pos)
                if self.distance((self.x_pos, self.y_pos), (self.closest_food.x_pos, self.closest_food.y_pos)) < self.closest_food.rad * 2 :
                    try:
                        # sometimes is deleted twice?
                        if len(all_food[self.closest_food]) == 1:
                            self.eat()
                        else:
                            # print(len(all_food[self.closest_food]))
                            self.deal(*all_food[self.closest_food])

                        del all_food[self.closest_food]
                        # all_food.pop(all_food.index(self.closest_food))
                        self.closest_food = 0
                        other_move = True
                    except ValueError:
                        print('ValueError')
                

        # wandering movement
        if not other_move:
            if self.wander_count <= 0:
                self.wander_dir = random.randrange(4)
                self.wander_count = 100
            if self.wander_dir == 0:
                if self.x_pos + self.rad + self.speed > 700:
                    self.wander_dir = 1
                else:
                    self.x_pos += self.speed
                self.wander_count -= 1
            elif self.wander_dir == 1:
                if self.x_pos - self.rad - self.speed < 0:
                    self.wander_dir = 0
                else:
                    self.x_pos -= self.speed
                self.wander_count -= 1
            elif self.wander_dir == 2:
                if self.y_pos + self.rad + self.speed > 700:
                    self.wander_dir = 3
                else:
                    self.y_pos += self.speed
                self.wander_count -= 1
            elif self.wander_dir == 3:
                if self.y_pos - self.rad - self.speed < 0:
                    self.wander_dir = 2
                else:
                    self.y_pos -= self.speed
                self.wander_count -= 1

    def move_towards(self, x_pos, y_pos):
        """moves creature towards given pair of coordinates"""
        if self.x_pos < x_pos:
            self.x_pos += self.speed
        if self.x_pos > x_pos:
            self.x_pos -= self.speed
        if self.y_pos < y_pos:
            self.y_pos += self.speed
        if self.y_pos > y_pos:
            self.y_pos -= self.speed

    def eat(self):
        """increases satiation after eating"""
        self.energy += 200
        
    @classmethod
    def deal(cls, self1, other):
        if self1.aggro and other.aggro:
            self1.energy += 25
            other.energy += 25

        elif self1.aggro:
            self1.energy += 150
            other.energy += 50

        elif other.aggro:
            self1.energy += 50
            other.energy += 150

        else:
            self1.energy += 100
            other.energy += 100

    def die(self, all_ctr, all_food, time):
        """uses up satiation every 'hunger' seconds, dies if no satiation"""
        if self.energy <= 0:
            if self.closest_food in all_food.keys() :
                all_food[self.closest_food].remove(self)
            all_ctr.pop(all_ctr.index(self))

    def reproduce(self, x_pos, y_pos):
        """creates new child creature"""
        if self.energy >= 200:
            new_creature = Creature(x_pos, y_pos, self.aggro)
            return new_creature


    def distance(self, point1, point2):
        """distance formula function that takes two tuples"""
        return math.sqrt((point1[0] - point2[0])**2 + (point1[1] - point2[1])**2)

    def draw(self, win):
        """draws creature"""
        if self.aggro == 0:
            win.blit(self.c_img, (self.x_pos-self.rad,
                                   self.y_pos-self.rad))
        else:
            win.blit(self.ac_img, (self.x_pos-self.rad,
                                  self.y_pos-self.rad))
        # shows vision (for debug)
        # pygame.draw.circle(WIN, (255, 0, 0),
        #                   (round(self.x_pos), round(self.y_pos)), round(self.vision), 1)

    def another_day(self):
        self.energy += 100
