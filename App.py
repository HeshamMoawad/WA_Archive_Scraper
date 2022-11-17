from PyQt5 import QtCore , QtWidgets , QtGui
from MyPyQt5 import  QSideMenuNewStyle ,MyThread,pyqtSignal , MyMessageBox
from pages import Page1 
from styles import Styles
import sqlite3

from mainclass import Whatsapp

class MyMainWindow():
    def show(self):
        self.MainWindow.show()


    def Setup(self,MainWindow:QtWidgets.QMainWindow):
        self.message = MyMessageBox()

        self.MainWindow = MainWindow
        MainWindow.resize(800,600)
        MainWindow.setWindowFlag(QtCore.Qt.WindowType.FramelessWindowHint)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.Menu = QSideMenuNewStyle(
            self.centralwidget,
            ButtonsCount = 1 ,
            PagesCount = 1 ,
            ExitButtonIconPath = "Data/Icons/reject.png" ,
            DefultIconPath = "Data\Icons\list.png" , 
            ClickIconPath = "Data/Icons/arrowheads-of-thin-outline-to-the-left.png",
            ButtonsFrameFixedwidth = 150 ,
            MaxButtonIconPath = "Data\Icons\maximize.png",
            MiniButtonIconPath = "Data\Icons\delete.png",
            Mini_MaxButtonIconPath = "Data\Icons\minimize.png",
            ButtonsFixedHight=50
            )

        self.FirstPage = self.Menu.GetPage(0)
        self.FirstPage.setStyleSheet("background-color:#C1C1C1;")
        self.Button = self.Menu.GetButton(0)
        self.Button.setText("DashBoard")
        self.Button.setStyleSheet(Styles.BUTTON)
        self.Page1 = Page1(self.FirstPage)
        self.Menu.DarkModetoggle.stateChanged.connect(self.darkmode)
        
        # Thread Part 
        self.thread = Thread()
        self.thread.mesg.connect(self.message.showInfo)
        self.thread.statues.connect(self.Menu.MainLabel.setText)
        self.thread.LeadSignal.connect(self.Page1.treeWidget.appendData)
        self.Page1.StartButton.clicked.connect(self.thread.start)
        self.Page1.StopButton.clicked.connect(self.thread.kill)
        MainWindow.setCentralWidget(self.centralwidget)


    def darkmode(self):
        if self.Menu.DarkModetoggle.isChecked():
            self.FirstPage.setStyleSheet("background-color:black;color:white;")
            self.Menu.BottomFrame.setStyleSheet(Styles.APP_DARK)
            self.Menu.TopFrame.setStyleSheet(Styles.APP_DARK)
            self.Button.setStyleSheet(Styles.BUTTON_DARK)
            self.Menu.ExitButton.setStyleSheet(Styles.BUTTON_DARK)
            self.Menu.MaxButton.setStyleSheet(Styles.BUTTON_DARK)
            self.Menu.MiniButton.setStyleSheet(Styles.BUTTON_DARK)
            self.Page1.LimitLabel.setStyleSheet("font:18px bold ;color :white;")
            self.Page1.StartButton.setStyleSheet(Styles.BUTTON_RUN_DARK)
            self.Page1.StopButton.setStyleSheet(Styles.BUTTON_RUN_DARK)
            self.Page1.treeWidget.setStyleSheet("background-color:white;color:black;")
            self.Menu.MenuButton.setStyleSheet(Styles.BUTTON_DARK)
        else:
            self.Menu.BottomFrame.setStyleSheet(Styles.APP)
            self.Menu.TopFrame.setStyleSheet(Styles.APP)
            self.Menu.ExitButton.setStyleSheet(Styles.BUTTON)
            self.Menu.MaxButton.setStyleSheet(Styles.BUTTON)
            self.Menu.MiniButton.setStyleSheet(Styles.BUTTON)
            self.Page1.LimitLabel.setStyleSheet("font:18px bold ;color :black;")
            self.Page1.StartButton.setStyleSheet(Styles.BUTTON_RUN)
            self.Page1.StopButton.setStyleSheet(Styles.BUTTON_RUN)
            self.Page1.treeWidget.setStyleSheet("background-color:white;color:black;")
            self.FirstPage.setStyleSheet("background-color:#C1C1C1;")
            self.Button.setStyleSheet(Styles.BUTTON)
            self.Menu.MenuButton.setStyleSheet(Styles.BUTTON)





class Thread(MyThread):
    LeadSignal= pyqtSignal(list)
    mesg = pyqtSignal(str)

    def run(self) -> None:
        self.statues.emit("يلا اسعتنا على الشقا بالله ^_^ ")
        self.Whatsapp = Whatsapp(ui.Menu.Hidetoggle.isChecked())
        self.Whatsapp.LeadSignal.connect(self.LeadSignal.emit)
        ui.Page1.StopSignal.connect(self.Whatsapp.contenue)
        self.Whatsapp.scrape_Archive()
        self.Whatsapp.exit()
        self.statues.emit("حلو اوى كده بالصلاه على النبى")
        self.mesg.emit("حلو اوى كده بالصلاه على النبى")

if __name__ == "__main__":
    import sys,requests
    app = QtWidgets.QApplication(sys.argv)
    app_icon = QtGui.QIcon()
    app_icon.addFile('Data\Icons\Capture.PNG', QtCore.QSize(16,16))
    app_icon.addFile('Data\Icons\Capture.PNG', QtCore.QSize(24,24))
    app_icon.addFile('Data\Icons\Capture.PNG', QtCore.QSize(32,32))
    app_icon.addFile('Data\Icons\Capture.PNG', QtCore.QSize(48,48))
    app_icon.addFile('Data\Icons\Capture.PNG', QtCore.QSize(256,256))
    app.setWindowIcon(app_icon)

    MainWindow = QtWidgets.QMainWindow()
    ui = MyMainWindow()
    ui.Setup(MainWindow)
    ui.show()
    sys.exit(app.exec_())
