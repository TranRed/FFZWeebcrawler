from PyQt5 import QtWidgets
import interface
import requests
import re

def create_naughtylist(app, ui):
    baseurl = ui.lineEdit.text() + '?c_page='
    ui.label_status.setText("running ...")
    app.processEvents()
    err404 = False
    page = 0
    channelTag = '<a href="/channel/'
    error = "<title>404"

    file = open("naughtylist.txt","a")

    while err404 == False:
        page += 1
        url = baseurl + str(page)
        r = requests.get(url)

        source = str(r.content)

        for match in re.finditer(error, source):
            err404 = True

        if err404 == False:
            for match in re.finditer(channelTag, source):
                notEnded = True
                i = match.end()
                channel = ''
                while notEnded == True:
                    if source[i] == '"':
                        notEnded = False
                    else:
                        channel = channel + source[i]
                        i += 1
                channel = channel + '\n'
                file.write(channel)

    file.close()
    ui.label_status.setText("finished!")


def connect_button(app, ui):
    ui.pushButton.clicked.connect(lambda: create_naughtylist(app, ui))

class MainWindow(QtWidgets.QMainWindow, interface.Ui_MainWindow):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        self.setupUi(self)

if __name__ == "__main__":
    import sys
    #create application object
    app = QtWidgets.QApplication(sys.argv)
    ui = MainWindow()
    connect_button(app, ui)
    ui.show()
    sys.exit(app.exec_())
