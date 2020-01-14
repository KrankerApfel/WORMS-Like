from Application.Core.GameLogic import  *
if __name__ == '__main__':
    g = Game()
    g.menu()
    while g.running:
       g.run()
    g.quit()
