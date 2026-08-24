import os
import random
import time

width, height = 60, 20
embers = [[random.randint(0, width - 1), random.randint(0, height - 1)] for _ in range(15)]

def render_terminal():
    while True:
        os.system('cls' if os.name == 'nt' else 'clear')
        screen = [[" " for _ in range(width)] for _ in range(height)]
        
        for e in embers:
            e[1] -= 1  # Move up
            if e[1] < 0:
                e[1] = height - 1
                e[0] = random.randint(0, width - 1)
            screen[e[1]][e[0]] = "•"
            
        output = []
        for row in screen:
            output.append("".join(row))
        
        print("\033[31;1m" + "\n".join(output) + "\033[0m")
        print("\033[36m[SLITH3RRAINBOW TERMINAL ACTIVE - PRESS CTRL+C TO EXIT]\033[0m")
        time.sleep(0.1)

if __name__ == "__main__":
    try:
        render_terminal()
    except KeyboardInterrupt:
        print("\nExiting terminal interface...")
