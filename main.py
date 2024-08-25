import neat.nn.feed_forward
import pygame
import neat
from flappy import FlappyGame
from flappy import Bird
import os
import pickle

width, height = 600, 750
window = pygame.display.set_mode((width, height))
clock = pygame.time.Clock()
    
def train_ai(genomes, config):
    nets = []
    birds = []
    for i, (genome_id, genome) in enumerate(genomes):
        nets.append(neat.nn.FeedForwardNetwork.create(genome, config))
        birds.append(Bird(window, height // 10, width // 2))
    
    run = True
    game = FlappyGame(window, height, width, birds)
    while(run):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                print(game.score)
                quit()
        
        for i, net in enumerate(nets):
            if birds[i].game_over:
                continue
            
            next_pipe = None
            
            if game.pipe1.x < game.pipe2.x:
                if game.pipe1.passed:
                    next_pipe = game.pipe2
                else:
                    next_pipe = game.pipe1
            else:
                if game.pipe2.passed:
                    next_pipe = game.pipe1
                else:
                    next_pipe = game.pipe2
            
            output = net.activate((birds[i].y, birds[i].dy, next_pipe.x, next_pipe.y))
            decision = output.index(max(output))
            if decision == 0:
                birds[i].jump()
        
        game.loop()     
        game.draw()
        MAX = 150
        if game.game_over or game.score == MAX:
            for i, bird in enumerate(birds):
                if not bird.game_over:
                    genomes[i][1].fitness = MAX
                else:
                    genomes[i][1].fitness = bird.score
                
            break

        pygame.display.update()

def eval_genomes(genomes, config):
    train_ai(genomes, config)
    
def run_neat(config):
    # p = neat.Checkpointer.restore_checkpoint('neat-checkpoint-45 (config-1)')
    p = neat.Population(config)
    p.add_reporter(neat.StdOutReporter(True))
    stats = neat.StatisticsReporter()
    p.add_reporter(stats)
    p.add_reporter(neat.Checkpointer(1))

    winner = p.run(eval_genomes, 1)
    print(winner)
    with open("best.pickle", "wb") as f:
        pickle.dump(winner, f)
    
def test_ai(config):
    with open("best.pickle", "rb") as f:
        winner = pickle.load(f)
    net = neat.nn.FeedForwardNetwork.create(winner, config)
    
    bird = Bird(window, height // 10, width // 2)
    game = FlappyGame(window, height, width, [bird])
    
    run = True
    while(run):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                print(game.score)
                quit()
        
        next_pipe = None
            
        if game.pipe1.x < game.pipe2.x:
            if game.pipe1.passed:
                next_pipe = game.pipe2
            else:
                next_pipe = game.pipe1
        else:
            if game.pipe2.passed:
                next_pipe = game.pipe1
            else:
                next_pipe = game.pipe2
        
        output = net.activate((bird.y, bird.dy, next_pipe.x, next_pipe.y))
        decision = output.index(max(output))
        if decision == 0:
            bird.jump()
        game.loop()     
        game.draw()
        pygame.display.update()        
        

if __name__ == "__main__":
    local_dir = os.path.dirname(__file__)
    config_path = os.path.join(local_dir, "config.txt")

    config = neat.Config(neat.DefaultGenome, neat.DefaultReproduction,
                         neat.DefaultSpeciesSet, neat.DefaultStagnation,
                         config_path)
    # run_neat(config)
    test_ai(config)