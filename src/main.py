''' module: main
    function: create App class,
              combine functions from submodules
'''
from direct.showbase.ShowBase import ShowBase


class App(ShowBase):

    def __init__(self):

        ShowBase.__init__(self)

if __name__ == '__main__':
    app = App()
    app.run()