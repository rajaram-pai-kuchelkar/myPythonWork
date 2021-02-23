import sys
import os
import sqlite3
from sqlite3 import Error
from PyQt5.QtWidgets import QApplication, QInputDialog, QLabel, QMessageBox, QWidget, QPushButton, QTableWidget, QTableWidgetItem,  QLineEdit
from PyQt5.QtGui import QIcon, QValidator, QIntValidator
from PyQt5.QtCore import pyqtSlot
from os import listdir
from os.path import isfile, isdir, join

PATH = '/Users/rpkDocuments/db/todoDb.db'

class App(QWidget):

    def __init__(self):
        super().__init__()
        self.title = 'Add Title to Design Checklist'
        self.left = 10
        self.top = 10
        self.width = 400
        self.height = 400
        #if self.getText() == 'abc' :
        #    self.initUI()
        self.initUI()
        
    def initUI(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)     
        
        lbSno=QLabel('Sno',self)
        lbSno.setStyleSheet("color : blue" )
        lbSno.move(50,30)
        self.txtSno = QLineEdit(self)
        self.txtSno.move(100,30)
        self.txtSno.resize(50,30)
        #self.txtSno.setText('abc')
        v = QIntValidator(1,10000,None)
        self.txtSno.setValidator(v)
        
        
        self.txtSno.textEdited.connect(self.txtSno_Validate)
        #self.txtSno.econnect(self.txtSno_Validate)
        lbTit=QLabel('Title',self)
        lbTit.move(50,70)
        
        self.txtTit = QLineEdit(self)
        self.txtTit.move(100,70)
        self.txtTit.resize(200,30)
         
        #self.txtSno.setText('abc')
        
        self.btSave = QPushButton('Save', self)
        #btSave.setToolTip('This is an example button')c
        self.btSave.move(100,110)
        self.btSave.setEnabled(False)
        self.btSave.clicked.connect(self.on_click)
        

        self.table1=QTableWidget(self)
        #self.table1.setRowCount(1)
      
        self.table1.setColumnCount(2)
        self.table1.verticalHeader().setVisible(False)
        headerLabels = ["SrNo","Description"]
        self.table1.setHorizontalHeaderLabels(headerLabels)
        self.table1.move(100,140)
        #self.table1.setItem(0,0,QTableWidgetItem('gekki'))
        self.fill_table()
        
        self.table1.resizeColumnToContents(0)
        self.table1.setColumnWidth(1,200)
        self.table1.scrollToBottom()
        #print(self.txt.text())
        self.show()

    @pyqtSlot()
    def txtSno_Validate(self):
        txt=self.txtSno.displayText()
        if txt=="":
            txt="0"
        if (int(txt) > 0) :           
            #print("Enabled ")
            self.btSave.setEnabled(True)
            return 1
        else :
            #print("Disabled ")
            self.btSave.setEnabled(False)
            return 0
    

    
            
    @pyqtSlot()    
    def on_click(self):
            
            if (self.txtSno.displayText()!= "" and self.txtSno_Validate()) :
                database = PATH
                # create a database connection
                conn = self.create_connection(database)
                x=self.txtSno.displayText()
                x=int(x)
                y=self.txtTit.displayText()
                title=(x,y)  
                print(title)
                if ( x!=0 and y!="") :
                    id = self.create_title(conn,title)  
                    print(id)
                else:
                    print('input is nothing')
            else :
                print('nothing to save')
   
     
        
    def create_connection(self,db_file):
        """ create a database connection to the SQLite database
            specified by the db_file
        :param db_file: database file
        :return: Connection object or None
        """
        try:
            conn = sqlite3.connect(db_file)
            return conn
        except Error as e:
            print(e)
     
        return None    
        
    def create_title(self,conn, title):
        """
        Create a new project into the projects table
        :param conn:
        :param project:
        :return: project id
        """
        try :
            sql = ''' INSERT INTO t_title (msn,title) VALUES (?,?) '''
            cur = conn.cursor()
            cur.execute(sql,title)
            conn.commit()
            j=self.table1.rowCount()
            self.table1.insertRow(j)
            self.table1.setItem(j,0,QTableWidgetItem(str(title[0])))
            self.table1.setItem(j,1,QTableWidgetItem(title[1]))
            self.table1.scrollToBottom()
            return cur.lastrowid
            
        except Error as e:
            title="Error Message"
            QMessageBox.warning(self, title , str(e))            
        return 0
  
    
    def fill_table(self):
            database = PATH
            # create a database connection
            conn = self.create_connection(database)
            sql = ''' select msn,title from t_title  '''
            cur = conn.cursor()
            
            
            cur.execute(sql)
            i=0
            for rw in cur :
                self.table1.insertRow(i)
                self.table1.setItem(i,0,QTableWidgetItem(str(rw[0])))
                self.table1.setItem(i,1,QTableWidgetItem(rw[1]))
                
                i=i+1
           
            conn.close()

    def getText(self):
        text, okPressed = QInputDialog.getText(self, "Get text","Your name:", QLineEdit.Password, "")
        if okPressed and text != '':
            print(text)
        return text           
            
if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()
    app.exec_()