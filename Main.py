from Application.Core.GameLogic import  *
if __name__ == '__main__':
    g = Game()
    g.new()
    while g.running:
       g.run()
    g.quit()
