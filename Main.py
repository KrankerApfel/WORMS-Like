from Application.Core.GameLogic import  *
if __name__ == '__main__':
    g = Game()
    g.splash_screen()
    while g.running:
       g.run()
    g.quit()
