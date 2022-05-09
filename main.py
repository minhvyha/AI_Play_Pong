# https://neat-python.readthedocs.io/en/latest/xor_example.html
from pong import Game
import pygame
import neat
import os
import time
import pickle


FONT = pygame.font.SysFont('comicsans', 50)
FONT_start = pygame.font.SysFont('comicsans', 37)
FONT_start_small = pygame.font.SysFont('comicsans', 20)

BLUE = (10,174,255)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED_d = (217,11,32)

class PongGame:
    def __init__(self, window, width, height):
        self.game = Game(window, width, height)
        self.ball = self.game.ball
        self.left_paddle = self.game.left_paddle
        self.right_paddle = self.game.right_paddle

    def test_ai(self, best, hard, medium, easy):
        clock = pygame.time.Clock()
        run = True
        started = False
        end = False
        r = False

        while run:
            if started:
                game_info = self.game.loop()
            clock.tick(80)
            keys = pygame.key.get_pressed()
            if keys[pygame.K_1] and not started:
                net = easy
                started = True
            if keys[pygame.K_2] and not started:
                net = medium
                started = True
            if keys[pygame.K_3] and not started:
                net = hard
                started = True
            if keys[pygame.K_4] and not started:
                net = best
                started = True
            if keys[pygame.K_r] and end == True:
                end = False
                self.game.reset()

            if not started and end == False:
                self.game.draw_start()

            if started:
                self.game.draw(draw_score=True)

            if end:
                self.game.draw_end(t)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
                    break
            if keys[pygame.K_w] and started:
                self.game.move_paddle(left=True, up=True)
            if keys[pygame.K_s] and started:
                self.game.move_paddle(left=True, up=False)

            if self.game.left_score >= 10:
                t = FONT_start.render('Player WIN!!!', 1, WHITE)
                end = True
                started = False

            if self.game.right_score >= 10:
                t = FONT_start.render('AI WIN!!!', 1, WHITE)
                end = True
                started = False
            if started:
                output = net.activate((self.right_paddle.y, abs(
                    self.right_paddle.x - self.ball.x), self.ball.y))
                decision = output.index(max(output))

                if decision == 1 and started:  # AI moves up
                    self.game.move_paddle(left=False, up=True)
                elif decision == 2 and started:  # AI moves down
                    self.game.move_paddle(left=False, up=False)

            pygame.display.update()

    def train_ai(self, genome1, genome2, config, draw=False):
        run = True
        start_time = time.time()

        net1 = neat.nn.FeedForwardNetwork.create(genome1, config)
        net2 = neat.nn.FeedForwardNetwork.create(genome2, config)
        self.genome1 = genome1
        self.genome2 = genome2

        max_hits = 50

        while run:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return True

            game_info = self.game.loop()

            self.move_ai_paddles(net1, net2)

            if draw:
                self.game.draw(draw_score=False, draw_hits=True)
                pygame.display.update()


            duration = time.time() - start_time
            if game_info.left_score == 1 or game_info.right_score == 1 or game_info.left_hits >= max_hits:
                self.calculate_fitness(game_info, duration)
                break

        return False

    def move_ai_paddles(self, net1, net2):
        players = [(self.genome1, net1, self.left_paddle, True), (self.genome2, net2, self.right_paddle, False)]
        for (genome, net, paddle, left) in players:
            output = net.activate(
                (paddle.y, abs(paddle.x - self.ball.x), self.ball.y))
            decision = output.index(max(output))

            valid = True
            if decision == 0:  # Don't move
                genome.fitness -= 0.01  # we want to discourage this
            elif decision == 1:  # Move up
                valid = self.game.move_paddle(left=left, up=True)
            else:  # Move down
                valid = self.game.move_paddle(left=left, up=False)

            if not valid:  # If the movement makes the paddle go off the screen punish the AI
                genome.fitness -= 1

    def calculate_fitness(self, game_info, duration):
        self.genome1.fitness += game_info.left_hits + duration
        self.genome2.fitness += game_info.right_hits + duration


def eval_genomes(genomes, config):
    width, height = 700, 500
    win = pygame.display.set_mode((width, height))
    pygame.display.set_caption("Pong")

    for i, (genome_id1, genome1) in enumerate(genomes):
        print(round(i/len(genomes) * 100), end=" ")
        genome1.fitness = 0
        for genome_id2, genome2 in genomes[min(i+1, len(genomes) - 1):]:
            genome2.fitness = 0 if genome2.fitness == None else genome2.fitness
            pong = PongGame(win, width, height)

            force_quit = pong.train_ai(genome1, genome2, config, draw=False)
            if force_quit:
                quit()


def run_neat(config):
    #p = neat.Checkpointer.restore_checkpoint('neat-checkpoint-30')
    p = neat.Population(config)
    p.add_reporter(neat.StdOutReporter(True))
    stats = neat.StatisticsReporter()
    p.add_reporter(stats)
    p.add_reporter(neat.Checkpointer(1))

    winner = p.run(eval_genomes, 50)
    with open("easy.pickle", "wb") as f:
        pickle.dump(winner, f)


def test_best_network(config):
    with open("impossible.pickle", "rb") as f:
        bestie = pickle.load(f)
    best = neat.nn.FeedForwardNetwork.create(bestie, config)
    with open("easy.pickle", "rb") as f:
        ease = pickle.load(f)
    easy = neat.nn.FeedForwardNetwork.create(ease, config)
    with open("medium.pickle", "rb") as f:
        med = pickle.load(f)
    medium = neat.nn.FeedForwardNetwork.create(med, config)
    with open("hard.pickle", "rb") as f:
        ha = pickle.load(f)
    hard = neat.nn.FeedForwardNetwork.create(ha, config)


    width, height = 700, 500
    win = pygame.display.set_mode((width, height))
    pygame.display.set_caption("Pong")
    pong = PongGame(win, width, height)
    pong.test_ai(best, hard, medium, easy)

if __name__ == '__main__':
    local_dir = os.path.dirname(__file__)
    config_path = os.path.join(local_dir, 'config.txt')

    config = neat.Config(neat.DefaultGenome, neat.DefaultReproduction,
                         neat.DefaultSpeciesSet, neat.DefaultStagnation,
                         config_path)

    #run_neat(config)
    test_best_network(config)
