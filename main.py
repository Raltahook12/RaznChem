import sys
from Classes.Application import App
from Classes.Window import Window

if __name__ == '__main__':
    app = App(sys.argv)
    screensize = app.getScreensize()
    main = Window(screensize)
    main.show()

    sys.exit(app.exec())