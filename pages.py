
from PyQt5 import QtCore, QtWidgets
from MyPyQt5 import MyCustomContextMenu,QObject,pyqtSignal,MyQTreeWidget,MyMessageBox
import typing,pyperclip
from styles import Styles
from datetime import datetime

class Page1(QObject):
    StopSignal = pyqtSignal(bool)
    msg = MyMessageBox()

    def __init__(self, parent:typing.Optional[QtWidgets.QWidget]):
        self.Name = ""
        self.parent = parent
        self.verticalLayout = QtWidgets.QVBoxLayout(parent)
        self.FirstFrame = QtWidgets.QFrame(parent)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout(self.FirstFrame)
        self.LimitLabel = QtWidgets.QLabel(self.FirstFrame)
        self.LimitLabel.setText("Limit")
        self.LimitLabel.setStyleSheet("font:18px bold ;color :black;")
        self.LimitLabel.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.horizontalLayout_2.addWidget(self.LimitLabel)
        self.spinBox = QtWidgets.QSpinBox(self.FirstFrame)
        self.spinBox.setStyleSheet(Styles.SPINBOX)
        self.spinBox.setMaximum(10000)
        self.spinBox.setMinimum(1)
        self.horizontalLayout_2.addWidget(self.spinBox)
        self.horizontalLayout_2.setStretch(0, 5)
        self.horizontalLayout_2.setStretch(1, 1)
        self.verticalLayout.addWidget(self.FirstFrame)
        self.ButtonsFrame = QtWidgets.QFrame(parent)
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.ButtonsFrame)
        self.StartButton = QtWidgets.QPushButton(self.ButtonsFrame)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Preferred)
        self.StartButton.setSizePolicy(sizePolicy)
        self.StartButton.setStyleSheet(Styles.BUTTON_RUN)
        self.StartButton.setText("Start")
        self.StartButton.setShortcut("Return")
        self.StartButton.setFlat(True)
        self.horizontalLayout.addWidget(self.StartButton)
        self.StopButton = QtWidgets.QPushButton(self.ButtonsFrame)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Preferred)
        self.StopButton.setSizePolicy(sizePolicy)
        self.StopButton.setStyleSheet(Styles.BUTTON_RUN)
        self.StopButton.setShortcut("space")
        self.StopButton.setText("Stop")
        self.StopButton.setFlat(True)
        self.horizontalLayout.addWidget(self.StopButton)
        self.verticalLayout.addWidget(self.ButtonsFrame)
        self.treeWidget = MyQTreeWidget(parent)
        self.treeWidget.setColumns(["Phone","Last Message"])
        self.treeWidget.onLengthChanged.connect(lambda: self.counter(self.treeWidget._ROW_INDEX,self.spinBox.value()))
        self.treeWidget.setColumnWidth(0,300)
        self.treeWidget.setStyleSheet("background-color:white;color:black;font:16px bold;")
        self.treeWidget.setContextMenuPolicy(QtCore.Qt.ContextMenuPolicy.CustomContextMenu)
        self.treeWidget.customContextMenuRequested.connect(self.menu)
        self.verticalLayout.addWidget(self.treeWidget)
        self.CounterLabel = QtWidgets.QLabel(parent)
        self.CounterLabel.setText("Count : 0")
        self.CounterLabel.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.verticalLayout.addWidget(self.CounterLabel)
        self.verticalLayout.setStretch(1, 1)
        self.verticalLayout.setStretch(2, 4)
        self.verticalLayout.setStretch(3,0)
        super().__init__()

    def counter(self,count:int,max:typing.Optional[int]=None):
        self.CounterLabel.setText(f"Count : {count} Max : {max}")
        if max != None and count >= max :
            self.StopSignal.emit(False)


    def menu(self):
        
        menu = MyCustomContextMenu([
        "Copy Phone", # 0    
        "Copy LastMessage", # 1
        "Delete Row" , # 3
        "Export All To Excel", # 4
        "Copy Phone List", # 5
        "Copy LastMessage List", # 6
        "Copy Phones and LastMessage", # 8
        "Copy All", # 9
        "Clear Results", # 10
        ])
        # menu.connectShortcut(3,QKeySequence("Ctrl+e"))
        menu.multiConnect(functions=[
            lambda : self.copy(0), # 0
            lambda : self.copy(1), # 1
            self.delete , # 3
            lambda: self.export(self.Name) , # 4
            lambda : pyperclip.copy(self.treeWidget.extract_data_to_string(0)) if self.treeWidget._ROW_INDEX != 0 else self.msg.showWarning(text="No Data In Column !") , # 5
            lambda : pyperclip.copy(self.treeWidget.extract_data_to_string(1)) if self.treeWidget._ROW_INDEX != 0 else self.msg.showWarning(text="No Data In Column !"),  # 6
            lambda: pyperclip.copy(self.treeWidget.extract_data_to_DataFrame(range_of=range(0,2)).to_string(index=False)) if self.treeWidget._ROW_INDEX != 0 else self.msg.showWarning(text="No Data Found !") , # 8
            lambda: pyperclip.copy(self.treeWidget.extract_data_to_DataFrame().to_string(index=False)) if self.treeWidget._ROW_INDEX != 0 else self.msg.showWarning(text="No Data Found !") , # 9
            self.treeWidget.clear , # 10
        ])
        
        menu.show()

    def copy(self , index:int):
        try :
            pyperclip.copy(self.treeWidget.currentItem().text(index))
        except :
            self.msg.showWarning(text="No Item Selected please Select one !")

    def delete(self):
        try:
            self.treeWidget.takeTopLevelItem(self.treeWidget.indexOfTopLevelItem(self.treeWidget.currentItem()))
        except:
            self.msg.showWarning(text="No Item Selected please Select one !")

    def export(self,name:typing.Optional[str]):
        if self.treeWidget._ROW_INDEX > 0 :
            time = datetime.now()
            self.treeWidget.extract_data_to_DataFrame().to_excel(f"Data/Exports/{name}({time.date()})({time.hour}-{time.minute}-{time.second}).xlsx",index=False)
            self.msg.showInfo(text=f"Exported Succecfully to 'Data/Exports/{name}({time.date()})({time.hour}-{time.minute}-{time.second}).xlsx'")
        else :
            self.msg.showWarning(text="No Data In App Please Try Again Later")




