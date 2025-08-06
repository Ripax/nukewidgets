import sys
# sys.path.append("/home/ripan/dev/")


from PySide2.QtCore import Qt, QPoint
from PySide2.QtWidgets import QWidget, QApplication
# from nukeUI.ui.nukewidgets import Ui_Form
from nukewidgets import Ui_Form
import inspect
import random


class Nukewidget(Ui_Form, QWidget):
    def __init__(self):
        super(Nukewidget, self).__init__()
        self.setupUi(self)
        self.setWindowTitle("Nuke widgets for node.")
        self.setWindowFlags(self.windowFlags() | Qt.WindowStaysOnTopHint)
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.setAttribute(Qt.WA_TranslucentBackground)

        self.pushButton.clicked.connect(self.read_from_write)
        self.pushButton_5.clicked.connect(self.searchnode)
        self.pushButton_RandomColor.clicked.connect(self.randomcolor)
        self.pushButton_Write_fromRead.clicked.connect(self.writefromread)
        self.pushButton_allnodes.clicked.connect(self.allnodes)
        self.pushButton_selected_nodes.clicked.connect(self.selectednodes)

        self.listWidget.itemClicked.connect(self.item_clicked)

    def mousePressEvent(self, event):
        self.oldPosition = event.globalPos()


    def mouseMoveEvent(self, event):
        delta = QPoint(event.globalPos() - self.oldPosition)
        self.move(self.x() + delta.x(), self.y() + delta.y())
        self.oldPosition = event.globalPos()

    def allnodes(self):
        self.listWidget.clear()
        self.comboBox.clear()
        print(f"Message from {inspect.currentframe().f_code.co_name}")
        allnodes = nuke.allNodes()

        for node in allnodes:
            nodename = node.name()
            self.listWidget.addItem(nodename)
            self.comboBox.addItem(nodename)

    def selectednodes(self):
        print(f"Message from {inspect.currentframe().f_code.co_name}")

    def randomcolor(self):
        selected = nuke.selectedNode()
        print(f"Message from {inspect.currentframe().f_code.co_name}")
        color = self.color_gen()
        selected['tile_color'].setValue(color)

    def writefromread(self):
        print(f"Message from {inspect.currentframe().f_code.co_name}")

    def read_from_write(self):
        print(f"Message from {inspect.currentframe().f_code.co_name}")

    def searchnode(self):
        nukescripts.clear_selection_recursive()
        print(f"Message from {inspect.currentframe().f_code.co_name}")
        selected_name = self.comboBox.currentText()
        if not selected_name:
            print("No node selected in comboBox.")
            return
        node = nuke.toNode(selected_name)
        if node:
            node.setSelected(True)
            nuke.zoomToFitSelected()
        else:
            print(f"Node '{selected_name}' not found in node graph.")

    @staticmethod
    def item_clicked(item):
        nukescripts.clear_selection_recursive()
        node_name = item.text()
        node = nuke.toNode(node_name)

        if node:
            node.setSelected(True)
            nuke.zoomToFitSelected()
        else:
            print(f"Node '{node_name}' not found.")


    def color_gen(self):
        r = (float(random.randint(20, 40))) / 100
        g = (float(random.randint(15, 50))) / 100
        b = (float(random.randint(10, 60))) / 100
        r_int = int(r * 255)
        g_int = int(g * 255)
        b_int = int(b * 255)
        a_int = 255  # full opacity

        hex_color = int(f'{r_int:02x}{g_int:02x}{b_int:02x}{a_int:02x}', 16)
        return hex_color

# For widgets
if __name__ == '__main__':
    widgets = Nukewidget()
    widgets.show()
