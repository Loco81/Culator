from PyQt5 import QtCore, QtGui, QtWidgets
from win32com.client import Dispatch
import sys, time, os, ctypes, winshell, sqlite3

myappid = 'mycompany.myproduct.subproduct.version' # arbitrary string
ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)

    
_files = sys._MEIPASS+'\\Culator_Files'
#_files = r'D:\Backups\Others\Us\Me\_-_Develope_-_\~My Programs\Apps\Python\Culator\Code\Culator_Files'
_data = 'C:\\Windows'
#_data = 'C:\\Users\\LoCo\\Documents\\Visual Studio 2022\\Projects\\Python-04\\_main'

class Marker(QtWidgets.QMainWindow):
    def __init__(self):
        QtWidgets.QMainWindow.__init__(self)

        self.setWindowFlags(QtCore.Qt.Widget | QtCore.Qt.FramelessWindowHint);
        self.setAttribute(QtCore.Qt.WA_NoSystemBackground, True);
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground, True);
        self.clicked = False
        self.resize(350, 250)

    def mousePressEvent(self, event):
        self.old_pos = event.screenPos()

    def mouseMoveEvent(self, event):
        if self.clicked:
            dx = int(self.old_pos.x() - event.screenPos().x())
            dy = int(self.old_pos.y() - event.screenPos().y())
            self.move(self.pos().x() - dx, self.pos().y() - dy)
        self.old_pos = event.screenPos()
        self.clicked = True

        return QtWidgets.QMainWindow.mouseMoveEvent(self, event)


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        def createShortcut(path, target='', wDir='', icon=''):    
            ext = path[-3:]
            if ext == 'url':
                shortcut = open(path, 'w')
                shortcut.write('[InternetShortcut]\n')
                shortcut.write('URL=%s' % target)
                shortcut.close()
            else:
                shell = Dispatch('WScript.Shell')
                shortcut = shell.CreateShortCut(path)
                shortcut.Targetpath = target
                shortcut.WorkingDirectory = wDir
                if icon != '':
                    shortcut.IconLocation = icon
                shortcut.save()

        global i_db, n_db, i_c, n_c
        i_db = sqlite3.connect(_data+'\\Culator_items.dll')
        i_c = i_db.cursor()
        i_c.execute('''
                    CREATE TABLE IF NOT EXISTS items
                    ([item] TEXT)
                    ''')
        i_db.commit()
        n_db = sqlite3.connect(_data+'\\Culator_notes.dll')
        n_c = n_db.cursor()
        n_c.execute('''
                    CREATE TABLE IF NOT EXISTS notes
                    ([note] TEXT)
                    ''')
        n_db.commit()
        if not os.path.exists(_data+'\\Culator_BP.ini'):
            file = open(_data+'\\Culator_BP.ini', 'w')
            file.write('D:\\Backups\\\nTrue')
            file.close()
        if not os.path.exists(_data+'\\Culator_Files\\icon.ico'):
            from shutil import copytree, rmtree
            try: rmtree(_data+'\\Culator_Files')
            except: pass
            copytree(_files, _data+'\\Culator_Files')

        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(351, 600)
        MainWindow.setWindowFlag(QtCore.Qt.FramelessWindowHint)
        MainWindow.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        MainWindow.setFixedSize(369, 609)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        MainWindow.setWindowOpacity(.96)
        self.frame2 = QtWidgets.QFrame(self.centralwidget)
        self.frame2.setGeometry(QtCore.QRect(0, 0, 351, 573))
        self.frame2.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame2.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame2.setObjectName("frame2")
        self.listWidget = QtWidgets.QListWidget(self.frame2)
        self.listWidget.setGeometry(QtCore.QRect(10, 40, 331, 458))
        self.listWidget.setObjectName("listWidget")
        self.listWidget.setStyleSheet("background-color: rgb(228, 228, 228);\n"
"border-width: 0px;\n"
"color: rgb(70, 70, 70);")
        self.listWidget.setDragDropMode(QtWidgets.QAbstractItemView.InternalMove)
        self.listWidget.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        font = QtGui.QFont()
        font.setFamily("SimSun-ExtB")
        font.setPointSize(12)
        def lc():
            i_c.execute('DROP TABLE IF EXISTS items')
            i_c.execute('''
                      CREATE TABLE IF NOT EXISTS items
                      ([item] TEXT)
                      ''')
            n = '''
                INSERT INTO items (item)

                    VALUES
                    '''
            for i in range(self.listWidget.count()):
                n += "('"+self.listWidget.item(i).text()+"'),\n"
            n+=','
            n = n.replace('),\n,', ')')
            i_c.execute(n)
            i_db.commit()
            
        self.listWidget.model().rowsMoved.connect(lambda: lc())

        if os.path.exists(_data+'\\Culator_items.dll'):
            db = sqlite3.connect(_data+'\\Culator_items.dll')
            c = db.cursor()
            c.execute('SELECT * FROM items')  
            lines = []
            for i in c.fetchall():
                lines.append(i[0])
            db.close()
            if len(lines) == 1 and lines[0] == '':
                pass
            else:
                for i in lines:
                    try: x=int(i.split(' ')[0])
                    except:
                        item = QtWidgets.QListWidgetItem(i.strip('\n'))
                        item.setBackground(QtGui.QColor('#FFFFFF'))
                        self.listWidget.addItem(item)
                    else:
                        if x < 1000001:
                            if x>0 and x<50001:
                                colorr = '#67C800'
                            elif x>50000 and x<100001:
                                colorr = '#A7C800'
                            elif x>100000 and x<150001:
                                colorr = '#C8BE00'
                            elif x>150000 and x<200001:
                                colorr = '#C8A700'
                            elif x>200000 and x<350001:
                                colorr = '#C88F00'
                            elif x>350000 and x<500001:
                                colorr = '#C87B00'
                            elif x>500000 and x<600001:
                                colorr = '#C86700'
                            elif x>600000 and x<700001:
                                colorr = '#C85700'
                            elif x>700000 and x<800001:
                                colorr = '#C84300'
                            elif x>800000 and x<900001:
                                colorr = '#C83200'
                            elif x>900000 and x<1000001:
                                colorr = '#C82500'
                        else:
                            colorr = '#C80000'
                        item = QtWidgets.QListWidgetItem(i.strip('\n'))
                        item.setForeground(QtGui.QColor(colorr))
                        self.listWidget.addItem(item)
        self.listWidget.setAutoScroll(True)

        self.close1 = QtWidgets.QPushButton(self.frame2)
        self.close1.setGeometry(QtCore.QRect(176, 7, 21, 21))
        self.close1.setText("")
        self.close1.setObjectName("close1")
        self.min1 = QtWidgets.QPushButton(self.frame2)
        self.min1.setGeometry(QtCore.QRect(153, 7, 21, 21))
        self.min1.setText("")
        self.min1.setObjectName("min1")
        self.switch_btn = QtWidgets.QPushButton(self.frame2)
        self.switch_btn.setGeometry(QtCore.QRect(320, 6, 21, 30))
        self.add1 = QtWidgets.QPushButton(self.frame2)
        self.add1.setGeometry(QtCore.QRect(269, 504, 35, 27))
        font = QtGui.QFont()
        font.setFamily("Marlett")
        font.setPointSize(22)
        self.add1.setFont(font)
        self.add1.setObjectName("add1")

        def del1_func():
            row = self.listWidget.currentRow()
            i_c.execute(f"DELETE FROM items WHERE item='{self.listWidget.item(row).text()}'")
            i_db.commit()
            self.listWidget.takeItem(row)
            calculate()

        self.del1 = QtWidgets.QPushButton(self.frame2)
        self.del1.setGeometry(QtCore.QRect(305, 504, 35, 27))
        font = QtGui.QFont()
        font.setFamily("Marlett")
        font.setPointSize(18)
        self.del1.setFont(font)
        self.del1.setObjectName("del1")
        self.del1.clicked.connect(del1_func)

        def le1():
            if self.lineEdit.text() != '':
                try: x=int(self.lineEdit.text())
                except: self.lineEdit.setText('')
                else:
                    if x>0:
                        self.lineEdit_2.setFocus()
                    else:
                        self.lineEdit.setText('')
        self.lineEdit = QtWidgets.QLineEdit(self.frame2)
        self.lineEdit.setGeometry(QtCore.QRect(12, 505, 114, 27))
        font = QtGui.QFont()
        font.setFamily("Comic Sans MS")
        font.setPointSize(18)
        font.setBold(False)
        font.setWeight(50)
        self.lineEdit.setFont(font)
        self.lineEdit.setMaxLength(8)
        self.lineEdit.setAlignment(QtCore.Qt.AlignCenter)
        self.lineEdit.setObjectName("lineEdit")
        self.lineEdit.returnPressed.connect(le1)
        self.lineEdit.setFocus()

        def le2():
            if "'" in self.lineEdit_2.text():
                return
            if self.lineEdit.text() != '':
                try: x=int(self.lineEdit.text())
                except: 
                    self.lineEdit.setText('')
                    self.lineEdit.setFocus()
                else:
                    if x>0:
                        if x < 1000001:
                            if x>0 and x<50001:
                                colorr = '#67C800'
                            elif x>50000 and x<100001:
                                colorr = '#A7C800'
                            elif x>100000 and x<150001:
                                colorr = '#C8BE00'
                            elif x>150000 and x<200001:
                                colorr = '#C8A700'
                            elif x>200000 and x<350001:
                                colorr = '#C88F00'
                            elif x>350000 and x<500001:
                                colorr = '#C87B00'
                            elif x>500000 and x<600001:
                                colorr = '#C86700'
                            elif x>600000 and x<700001:
                                colorr = '#C85700'
                            elif x>700000 and x<800001:
                                colorr = '#C84300'
                            elif x>800000 and x<900001:
                                colorr = '#C83200'
                            elif x>900000 and x<1000001:
                                colorr = '#C82500'
                        else:
                            colorr = '#C80000'

                        toadd = self.lineEdit.text()+' '*(16-len(self.lineEdit.text()))+self.lineEdit_2.text()
                        item = QtWidgets.QListWidgetItem(toadd)
                        item.setForeground(QtGui.QColor(colorr))
                        self.listWidget.addItem(item)
                        i_c.execute(f"INSERT INTO items (item) values ('{toadd}')")
                        i_db.commit()
                        calculate()
                        self.listWidget.scrollToBottom()
                        self.lineEdit.setText('')
                        self.lineEdit_2.setText('')
                        self.lineEdit.setFocus()
                    else: 
                        self.lineEdit.setText('')
                        self.lineEdit.setFocus()

        self.lineEdit_2 = QtWidgets.QLineEdit(self.frame2)
        self.lineEdit_2.setGeometry(QtCore.QRect(128, 505, 137, 27))
        font = QtGui.QFont()
        font.setFamily("Comic Sans MS")
        font.setPointSize(15)
        self.lineEdit_2.setFont(font)
        self.lineEdit_2.setAlignment(QtCore.Qt.AlignCenter)
        self.lineEdit_2.setObjectName("lineEdit_2")
        self.lineEdit_2.returnPressed.connect(le2)
        self.add1.clicked.connect(le2)

        global color
        color = '(115, 115, 115)'
        def calculate():
            global color
            def styler():
                global color
                self.frame2.setStyleSheet("background-color: rgb(255, 255, 255);\n"
"border-radius: 16px;\n"
"border: 1px solid;\n"
"border-color: rgb"+color+";")
                self.close1.setStyleSheet("QPushButton{\n"
"    background-color: rgb"+color+";\n"
"    border-radius: 6px;\n"
"    border-width: 0px;\n"
"}\n"
"QPushButton::hover{\n"
"    background-color: rgb(115, 0, 0);\n"
"}")
                self.min1.setStyleSheet("QPushButton{\n"
"    background-color: rgb"+color+";\n"
"    border-radius: 6px;\n"
"    border-width: 0px;\n"
"}\n"
"QPushButton::hover{\n"
"    background-color: rgba"+color[:-1]+", 115);\n"
"}")
                self.add1.setStyleSheet("QPushButton{\n"
"    background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:0, stop:0 rgba"+color[:-1]+", 255), stop:1 rgba"+color[:-1]+", 115));\n"
"    border-radius: 6px;\n"
"    border-width: 0px;\n"
"}\n"
"QPushButton::hover{\n"
"    background-color: rgba"+color[:-1]+", 115);\n"
"}")
                self.del1.setStyleSheet("QPushButton{\n"
"    \n"
"    background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:0, stop:0 rgba"+color[:-1]+", 115), stop:1 rgba"+color[:-1]+", 255));\n"
"    border-radius: 6px;\n"
"    border-width: 0px;\n"
"}\n"
"QPushButton::hover{\n"
"    background-color:rgba"+color[:-1]+", 115);\n"
"}")
                self.lineEdit.setStyleSheet("border: 1px solid;\n"
"border-radius: 8px;\n"
"border-color: rgb"+color+";")
                self.lineEdit_2.setStyleSheet("border: 1px solid;\n"
"border-radius: 8px;\n"
"border-color: rgb"+color+";")
                self.backup.setStyleSheet("QPushButton{\n"
"    background-color: rgb"+color+";\n"
"    border-radius: 6px;\n"
"    border-width: 0px;\n"
"}\n"
"QPushButton::hover{\n"
"    background-color: rgb(90, 194, 90);\n"
"}")
                self.separator.setStyleSheet("QPushButton{\n"
"    background-color: rgb"+color+";\n"
"    border-radius: 6px;\n"
"    border-width: 0px;\n"
"}\n"
"QPushButton::hover{\n"
"    background-color: rgba"+color[:-1]+", 165);\n"
"}")

            x = 0
            n = 0
            for i in range(self.listWidget.count()):
                try: x += int(self.listWidget.item(i).text().split(' ')[0])
                except: pass
            file = open(_data+'\\Culator_BP.ini', 'r')
            flag = file.read().split('\n')[1].strip('\n')
            file.close()
            if x == 0:
                self.label.setStyleSheet("color: rgb(255, 255, 255);\nborder-width: 0px;")
                color = '(115, 115, 115)'
                MainWindow.setWindowIcon(QtGui.QIcon(_files+"\\icon.ico"))
                if flag == 'True':
                    createShortcut(path=winshell.desktop()+"\Culator.lnk", target=sys.argv[0], icon=_data+"\\Culator_Files\\icon.ico")
            elif x > 0:
                self.label.setStyleSheet("color: rgb(100, 100, 100);\nborder-width: 0px;")
                if x < 3000001:
                    if x>0 and x<1000001:
                        color = '(' + str(int(x/5000)) + ', 200, 0)'
                    elif x>1000000 and x<3000001:
                        color = '(200, ' + str(-(int(x-3000000)/10000)) + ', 0)'

                    if x>0 and x<125001:
                        MainWindow.setWindowIcon(QtGui.QIcon(_files+"\\icon01.ico"))
                        if flag == 'True':
                            createShortcut(path=winshell.desktop()+"\Culator.lnk", target=sys.argv[0], icon=_data+"\\Culator_Files\\icon01.ico") 
                    elif x>125000 and x<250001:
                        MainWindow.setWindowIcon(QtGui.QIcon(_files+"\\icon02.ico"))
                        if flag == 'True':
                            createShortcut(path=winshell.desktop()+"\Culator.lnk", target=sys.argv[0], icon=_data+"\\Culator_Files\\icon02.ico")
                    elif x>250000 and x<375001:
                        MainWindow.setWindowIcon(QtGui.QIcon(_files+"\\icon03.ico"))
                        if flag == 'True':
                            createShortcut(path=winshell.desktop()+"\Culator.lnk", target=sys.argv[0], icon=_data+"\\Culator_Files\\icon03.ico")
                    elif x>375000 and x<500001:
                        MainWindow.setWindowIcon(QtGui.QIcon(_files+"\\icon04.ico"))
                        if flag == 'True':
                            createShortcut(path=winshell.desktop()+"\Culator.lnk", target=sys.argv[0], icon=_data+"\\Culator_Files\\icon04.ico")
                    elif x>500000 and x<625001:
                        MainWindow.setWindowIcon(QtGui.QIcon(_files+"\\icon05.ico"))
                        if flag == 'True':
                            createShortcut(path=winshell.desktop()+"\Culator.lnk", target=sys.argv[0], icon=_data+"\\Culator_Files\\icon05.ico")
                    elif x>625000 and x<750001:
                        MainWindow.setWindowIcon(QtGui.QIcon(_files+"\\icon06.ico"))
                        if flag == 'True':
                            createShortcut(path=winshell.desktop()+"\Culator.lnk", target=sys.argv[0], icon=_data+"\\Culator_Files\\icon06.ico")
                    elif x>750000 and x<875001:
                        MainWindow.setWindowIcon(QtGui.QIcon(_files+"\\icon07.ico"))
                        if flag == 'True':
                            createShortcut(path=winshell.desktop()+"\Culator.lnk", target=sys.argv[0], icon=_data+"\\Culator_Files\\icon07.ico")
                    elif x>875000 and x<1000001:
                        MainWindow.setWindowIcon(QtGui.QIcon(_files+"\\icon08.ico"))
                        if flag == 'True':
                            createShortcut(path=winshell.desktop()+"\Culator.lnk", target=sys.argv[0], icon=_data+"\\Culator_Files\\icon08.ico")
                    elif x>1000000 and x<1285001:
                        MainWindow.setWindowIcon(QtGui.QIcon(_files+"\\icon09.ico"))
                        if flag == 'True':
                            createShortcut(path=winshell.desktop()+"\Culator.lnk", target=sys.argv[0], icon=_data+"\\Culator_Files\\icon09.ico")
                    elif x>1285000 and x<1570001:
                        MainWindow.setWindowIcon(QtGui.QIcon(_files+"\\icon10.ico"))
                        if flag == 'True':
                            createShortcut(path=winshell.desktop()+"\Culator.lnk", target=sys.argv[0], icon=_data+"\\Culator_Files\\icon10.ico")
                    elif x>1570000 and x<1855001:
                        MainWindow.setWindowIcon(QtGui.QIcon(_files+"\\icon11.ico"))
                        if flag == 'True':
                            createShortcut(path=winshell.desktop()+"\Culator.lnk", target=sys.argv[0], icon=_data+"\\Culator_Files\\icon11.ico")
                    elif x>1855000 and x<2140001:
                        MainWindow.setWindowIcon(QtGui.QIcon(_files+"\\icon12.ico"))
                        if flag == 'True':
                            createShortcut(path=winshell.desktop()+"\Culator.lnk", target=sys.argv[0], icon=_data+"\\Culator_Files\\icon12.ico")
                    elif x>2140000 and x<2425001:
                        MainWindow.setWindowIcon(QtGui.QIcon(_files+"\\icon13.ico"))
                        if flag == 'True':
                            createShortcut(path=winshell.desktop()+"\Culator.lnk", target=sys.argv[0], icon=_data+"\\Culator_Files\\icon13.ico")
                    elif x>2425000 and x<2750001:
                        MainWindow.setWindowIcon(QtGui.QIcon(_files+"\\icon14.ico"))
                        if flag == 'True':
                            createShortcut(path=winshell.desktop()+"\Culator.lnk", target=sys.argv[0], icon=_data+"\\Culator_Files\\icon14.ico")
                    elif x>2750000 and x<3000001:
                        MainWindow.setWindowIcon(QtGui.QIcon(_files+"\\icon15.ico"))
                        if flag == 'True':
                            createShortcut(path=winshell.desktop()+"\Culator.lnk", target=sys.argv[0], icon=_data+"\\Culator_Files\\icon15.ico") 
                else:
                    color = '(200, 0, 0)'
                    MainWindow.setWindowIcon(QtGui.QIcon(_files+"\\icon16.ico"))
                    if flag == 'True':
                        createShortcut(path=winshell.desktop()+"\Culator.lnk", target=sys.argv[0], icon=_data+"\\Culator_Files\\icon16.ico")
            styler()
            x = str(x)[::-1]
            for i in range(len(x)):
                if i%3 == 0 and i!=0:
                    x = x[:i+n]+' '+x[i+n:]
                    n+=1
            x = x[::-1]
            self.label.setText(x)

        self.label = QtWidgets.QLabel(self.frame2)
        self.label.setGeometry(QtCore.QRect(45, 539, 260, 27))
        font = QtGui.QFont()
        font.setFamily("Comic Sans MS")
        font.setPointSize(20)
        self.label.setFont(font)
        self.label.setStyleSheet("color: rgb(255, 255, 255);\nborder-width: 0px;")
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.label.setObjectName("label")

        def backup_func():
            global color
            from shutil import copy
            file = open(_data+'\\Culator_BP.ini', 'r')
            path = file.read().split('\n')[0].strip('\n')
            file.close()
            try: copy(_data+'\\Culator_items.dll', path)
            except: 
                self.backup.setStyleSheet("QPushButton{\n"
"    background-color: rgb(213, 0, 0);\n"
"    border-radius: 6px;\n"
"    border-width: 0px;\n"
"}\n"
"QPushButton::hover{\n"
"    background-color: rgb(213, 0, 0);\n"
"}")
                QtWidgets.QApplication.processEvents()
                time.sleep(0.3)
                self.backup.setStyleSheet("QPushButton{\n"
"    background-color: rgb"+color+";\n"
"    border-radius: 6px;\n"
"    border-width: 0px;\n"
"}\n"
"QPushButton::hover{\n"
"    background-color: rgb(90, 194, 90);\n"
"}")
                QtWidgets.QApplication.processEvents()
            else:
                try: copy(_data+'\\Culator_notes.dll', path)
                except: pass
                self.backup.setStyleSheet("QPushButton{\n"
"    background-color: rgb(0, 213, 0);\n"
"    border-radius: 6px;\n"
"    border-width: 0px;\n"
"}\n"
"QPushButton::hover{\n"
"    background-color: rgb(0, 213, 0);\n"
"}")
                QtWidgets.QApplication.processEvents()
                time.sleep(0.3)
                self.backup.setStyleSheet("QPushButton{\n"
"    background-color: rgb"+color+";\n"
"    border-radius: 6px;\n"
"    border-width: 0px;\n"
"}\n"
"QPushButton::hover{\n"
"    background-color: rgb(90, 194, 90);\n"
"}")
                QtWidgets.QApplication.processEvents()
            
        def separator_func():
            if self.lineEdit_2.text() != '':
                toadd = '[ '+self.lineEdit_2.text().strip(' ')+' ]'
                item = QtWidgets.QListWidgetItem(toadd)
                item.setBackground(QtGui.QColor('#FFFFFF'))
                self.listWidget.addItem(item)
            else:
                toadd = ' '
                item = QtWidgets.QListWidgetItem(toadd)
                item.setBackground(QtGui.QColor('#FFFFFF'))
                self.listWidget.addItem(item)
            i_c.execute(f"INSERT INTO items (item) values ('{toadd}')")
            i_db.commit()
            calculate()
            self.lineEdit.setText('')
            self.lineEdit_2.setText('')
            self.lineEdit.setFocus()

        self.backup = QtWidgets.QPushButton(self.frame2)
        self.backup.setGeometry(QtCore.QRect(12, 538, 45, 25))
        self.backup.setText("Backup")
        self.backup.setObjectName("Backup")
        self.backup.clicked.connect(backup_func)
        self.separator = QtWidgets.QPushButton(self.frame2)
        self.separator.setGeometry(QtCore.QRect(288, 538, 52, 25))
        self.separator.setText("Separator")
        self.separator.setObjectName("Separator")
        self.separator.clicked.connect(separator_func)
        calculate()
        self.frame = QtWidgets.QFrame(self.centralwidget)
        self.frame.setGeometry(QtCore.QRect(0, 0, 351, 0))
        self.frame.setMaximumHeight(573)
        self.frame.setMinimumHeight(0)
        self.frame.setStyleSheet("background-color: rgb(255, 255, 255);\n"
"border-radius: 16px;\n"
"border: 1px solid;\n"
"border-color: rgb(53, 100, 107);")
        self.frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame.setObjectName("frame")
        
        global win_state
        win_state = "closed"
        def switch_func():
            global win_state
            if win_state == 'closed':
                self.frame.setStyleSheet("background-color: rgb(255, 255, 255);\n"
"border-radius: 16px;\n"
"border: 1px solid;\n"
"border-width: 1px 1px 0px 1px;\n"
"border-color: rgb(53, 100, 107);")
                self.lineEdit_3.setFocus()
                for i in range(0,581,10):
                    self.frame.setGeometry(QtCore.QRect(0, 0, 351, i))
                    time.sleep(0.01)
                    QtWidgets.QApplication.processEvents()
                self.frame.setStyleSheet("background-color: rgb(255, 255, 255);\n"
"border-radius: 16px;\n"
"border: 1px solid;\n"
"border-color: rgb(53, 100, 107);")
                win_state = "opened"
            else:
                self.frame.setStyleSheet("background-color: rgb(255, 255, 255);\n"
"border-radius: 16px;\n"
"border: 1px solid;\n"
"border-width: 1px 1px 0px 1px;\n"
"border-color: rgb(53, 100, 107);")
                self.lineEdit.setFocus()
                for i in reversed(range(0,581,10)):
                    self.frame.setGeometry(QtCore.QRect(0, 0, 351, i))
                    time.sleep(0.01)
                    QtWidgets.QApplication.processEvents()
                self.frame.setStyleSheet("background-color: rgb(255, 255, 255);\n"
"border-radius: 16px;\n"
"border: 1px solid;\n"
"border-color: rgb(53, 100, 107);")
                win_state = "closed"

        font = QtGui.QFont()
        font.setFamily("Symbol")
        font.setPointSize(14)
        font.setBold(True)
        font.setWeight(75)
        self.switch_btn.setFont(font)
        self.switch_btn.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.switch_btn.setStyleSheet("color: rgb(52, 52, 52);\nborder-width: 0px;")
        self.switch_btn.setObjectName("switch_btn")
        self.switch_btn.clicked.connect(switch_func)

        self.listWidget_2 = QtWidgets.QListWidget(self.frame)
        self.listWidget_2.setGeometry(QtCore.QRect(10, 40, 331, 492))
        self.listWidget_2.setStyleSheet("background-color: qlineargradient(spread:pad, x1:0.488636, y1:0, x2:0.505682, y2:1, stop:0 rgba(53, 100, 107, 255), stop:1 rgba(53, 100, 107, 10));\nborder-width: 0px;\n")
        self.listWidget_2.setObjectName("listWidget_2")
        self.listWidget_2.setDragDropMode(QtWidgets.QAbstractItemView.InternalMove)
        self.listWidget_2.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        def lc2():
            n_c.execute('DROP TABLE IF EXISTS notes')
            n_c.execute('''
                      CREATE TABLE IF NOT EXISTS notes
                      ([note] TEXT)
                      ''')
            n = '''
                INSERT INTO notes (note)

                    VALUES
                    '''
            for i in range(self.listWidget_2.count()):
                n += "('"+self.listWidget_2.item(i).text()+"'),\n"
            n+=','
            n = n.replace('),\n,', ')')
            n_c.execute(n)
            n_db.commit()
        self.listWidget_2.model().rowsMoved.connect(lambda: lc2())

        if os.path.exists(_data+'\\Culator_notes.dll'):
            db = sqlite3.connect(_data+'\\Culator_notes.dll')
            c = db.cursor()
            c.execute('SELECT * FROM notes')  
            lines = []
            for i in c.fetchall():
                lines.append(i[0])
            db.close()
            if len(lines) == 1 and lines[0] == '':
                pass
            else:
                for i in lines:
                    self.listWidget_2.addItem(i.strip('\n'))
        self.listWidget_2.setAutoScroll(True)

        self.close2 = QtWidgets.QPushButton(self.frame)
        self.close2.setGeometry(QtCore.QRect(176, 7, 21, 21))
        self.close2.setStyleSheet("QPushButton{\n"
"    background-color:rgb(53, 100, 107);\n"
"    border-radius: 6px;\n"
"    border-width: 0px;\n"
"}\n"
"QPushButton::hover{\n"
"    background-color: rgb(194, 31, 34);\n"
"}")
        self.close2.setText("")
        self.close2.setObjectName("close2")
        self.close2.clicked.connect(switch_func)
        self.min2 = QtWidgets.QPushButton(self.frame)
        self.min2.setGeometry(QtCore.QRect(153, 7, 21, 21))
        self.min2.setStyleSheet("QPushButton{\n"
"    background-color:rgb(53, 100, 107);\n"
"    border-radius: 6px;\n"
"    border-width: 0px;\n"
"}\n"
"QPushButton::hover{\n"
"    background-color: rgba(53, 100, 107, 110);\n"
"}")
        self.min2.setText("")
        self.min2.setObjectName("min2")

        def le3():
            toadd = self.lineEdit_3.text()
            if "'" in toadd:
                return
            if toadd != '':
                self.listWidget_2.addItem(toadd)
                n_c.execute(f"INSERT INTO notes (note) values ('{toadd}')")
                n_db.commit()
                self.listWidget_2.scrollToBottom()
                self.lineEdit_3.setText('')
                self.lineEdit_3.setFocus()

        self.add2 = QtWidgets.QPushButton(self.frame)
        self.add2.setGeometry(QtCore.QRect(269, 538, 35, 27))
        font = QtGui.QFont()
        font.setFamily("Marlett")
        font.setPointSize(22)
        self.add2.setFont(font)
        self.add2.setStyleSheet("QPushButton{\n"
"    \n"
"    background-color: qlineargradient(spread:pad, x1:0, y1:0.551, x2:1, y2:0.523, stop:0 rgba(53, 100, 107, 255), stop:1 rgba(53, 100, 107, 110));\n"
"    border-radius: 6px;\n"
"    border-width: 0px;\n"
"}\n"
"QPushButton::hover{\n"
"    background-color:rgba(53, 100, 107, 110);\n"
"}")
        self.add2.setObjectName("add2")
        self.add2.clicked.connect(le3)

        def del2_func():
            row = self.listWidget_2.currentRow()
            n_c.execute(f"DELETE FROM notes WHERE note='{self.listWidget_2.item(row).text()}'")
            n_db.commit()
            self.listWidget_2.takeItem(row)

        self.del2 = QtWidgets.QPushButton(self.frame)
        self.del2.setGeometry(QtCore.QRect(305, 538, 35, 27))
        font = QtGui.QFont()
        font.setFamily("Marlett")
        font.setPointSize(18)
        self.del2.setFont(font)
        self.del2.setStyleSheet("QPushButton{\n"
"    \n"
"    \n"
"    background-color: qlineargradient(spread:pad, x1:0, y1:0.551, x2:1, y2:0.523, stop:0 rgba(53, 100, 107, 110), stop:1 rgba(53, 100, 107, 255));\n"
"    border-radius: 6px;\n"
"    border-width: 0px;\n"
"}\n"
"QPushButton::hover{\n"
"    background-color:rgba(53, 100, 107, 110);\n"
"}")
        self.del2.setObjectName("del2")
        self.del2.clicked.connect(del2_func)
        self.lineEdit_3 = QtWidgets.QLineEdit(self.frame)
        self.lineEdit_3.setGeometry(QtCore.QRect(12, 539, 253, 27))
        font = QtGui.QFont()
        font.setFamily("Comic Sans MS")
        font.setPointSize(18)
        font.setBold(False)
        font.setWeight(50)
        self.lineEdit_3.setFont(font)
        self.lineEdit_3.setStyleSheet("border: 1px solid;\n"
"border-radius: 8px;\n"
"border-color:rgb(53, 100, 107);")
        self.lineEdit_3.setAlignment(QtCore.Qt.AlignCenter)
        self.lineEdit_3.setObjectName("lineEdit_3")
        self.lineEdit_3.returnPressed.connect(le3)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 369, 18))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)

        self.retranslateUi(MainWindow)
        self.close1.clicked.connect(lambda: i_db.close() or n_db.close() or sys.exit()) # type: ignore
        self.min1.clicked.connect(MainWindow.showMinimized) # type: ignore
        self.min2.clicked.connect(MainWindow.showMinimized) # type: ignore
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Culator"))
        self.switch_btn.setText(_translate("MainWindow", "z"))
        self.add1.setText(_translate("MainWindow", "a"))
        self.del1.setText(_translate("MainWindow", "X"))
        self.lineEdit.setPlaceholderText(_translate("MainWindow", "Cash"))
        self.lineEdit_2.setPlaceholderText(_translate("MainWindow", "For?"))
        self.add2.setText(_translate("MainWindow", "a"))
        self.del2.setText(_translate("MainWindow", "X"))
        self.lineEdit_3.setPlaceholderText(_translate("MainWindow", "Note"))


if __name__ == "__main__":
    QtWidgets.QApplication.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling, True)   # enable highdpi scaling
    QtWidgets.QApplication.setAttribute(QtCore.Qt.AA_UseHighDpiPixmaps, True)   # use highdpi icons
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = Marker()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
