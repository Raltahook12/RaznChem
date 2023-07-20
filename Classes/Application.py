from PySide6.QtWidgets import QApplication

class App(QApplication):

    def __init__(self,*args):
        super().__init__(*args)

    def getScreensize(self):
        self.mainScreen = self.screens()[0]
        return self.mainScreen.size()
