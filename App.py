from PyQt5 import  QtWidgets 
from MyPyQt5 import  QSideMenuNewStyle ,MyThread,pyqtSignal , MyQMainWindow
from pages import Page1 
from styles import Styles
import requests
from mainclass import Whatsapp




class MainWindow(MyQMainWindow):

    def SetupUi(self):
        self.setAppIcon("Data\Icons\data-mining.png")
        self.resize(800,600)
        self.setFrameLess()
        self.centralwidget = QtWidgets.QWidget()
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
        self.Leaved.connect(lambda: self.Menu.MainLabel.setText("رايح فين يا ابو الصحاب"))
        self.Entered.connect(lambda: self.Menu.MainLabel.setText("ايوه ركز معايا هنا "))
        self.FirstPage = self.Menu.GetPage(0)
        self.FirstPage.setStyleSheet("background-color:#C1C1C1;")
        self.Button = self.Menu.GetButton(0)
        self.Button.setText("DashBoard")
        self.Button.setStyleSheet(Styles.BUTTON)
        self.Page1 = Page1(self.FirstPage)
        self.Menu.DarkModetoggle.stateChanged.connect(self.darkmode)
        
        try : 
            requests.get("https://www.google.com")
            self.InterNetConnection = True
        except Exception as e :
            self.InterNetConnection = False 

        if not self.InterNetConnection :
            self.MessageBox.showCritical(text="No InterNetConnection here امشى اطلع بره" ) 
        elif self.InterNetConnection :
            self.MessageBox.showInfo(text="كله under control")

        # Thread Part 
        self.thread = Thread()
        self.thread.mesg.connect(self.MessageBox.showInfo)
        self.thread.statues.connect(self.Menu.MainLabel.setText)
        self.thread.LeadSignal.connect(self.Page1.treeWidget.appendData)
        self.Page1.StartButton.clicked.connect(self.thread.start)
        self.Page1.StopButton.clicked.connect(self.thread.kill)
        return super().SetupUi(self.centralwidget)

    

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
            
        self.Whatsapp = Whatsapp(ui.Menu.Hidetoggle.isChecked(),ui.Menu.DarkModetoggle.isChecked())
        self.Whatsapp.LeadSignal.connect(self.LeadSignal.emit)
        self.Whatsapp.scrape_Archive(ui.Page1.spinBox.value())
        self.Whatsapp.exit()
        self.statues.emit("حلو اوى كده بالصلاه على النبى")
        self.mesg.emit("حلو اوى كده بالصلاه على النبى")


if __name__ == "__main__":
    import sys
    ui = MainWindow()
    ui.SetupUi()
