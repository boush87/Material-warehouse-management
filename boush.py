from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.uic import loadUiType

import mysql.connector as mdb
import sys
import datetime

MainUi, _ = loadUiType("data/main.ui")

class Main(QMainWindow, MainUi):
    def __init__(self, parent=None):
        super(Main, self).__init__(parent)
        QMainWindow.__init__(self)
        self.setupUi(self)
        self.DB_Connect()
        self.Ui_Changes()
        self.Handel_Buttons()




    def Ui_Changes(self):
        self.Open_All_Products()

        self.tabWidget.tabBar().setVisible(False)

        header = self.table.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.Stretch)
        header.setSectionResizeMode(1, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(2, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(3, QHeaderView.ResizeToContents)



        #  get data
        self.Get_Data()

    def Clear_Edit(self):
        self.name_edit.clear()
        self.quantity_edit.clear()
        self.unit_edit.clear()

        self.date_edit.clear()


    def Clear_Edite(self):
        self.name_edit_3.clear()
        self.quantity_edit_3.clear()
        self.unit_edit_3.clear()

        self.date_edit_3.clear()

    def Clear_Edit_2(self):
        self.id_label.setText("N°")
        self.name_edit_2.clear()
        self.quantity_edit_2.clear()
        self.unit_edit_2.clear()
        self.date_edit_2.clear()

    def Clear_exit_3(self):
       # self.id_label.setText("N°")
        self.name_edit_3.clear()
        self.quantity_edit_3.clear()
        self.unit_edit_3.clear()
        self.date_edit_3.clear()


    def DB_Connect(self):
        self.conn = mdb.connect(host="localhost", user="root", password="123456", database="bosh_mater")
        self.cur = self.conn.cursor()




    def Get_Data(self):
        cmd = """ USE bosh_mater  """
        self.cur.execute(cmd)
        cmd = """ SELECT   date_a , name  , enter_a, exit_a , nats_a   FROM products """
        self.cur.execute(cmd)

        result = self.cur.fetchall()

        self.table.setRowCount(0)

        for row_num, row_data in enumerate(result):
            self.table.insertRow(row_num)
            for column_num, data in enumerate(row_data):
                self.table.setItem(row_num, column_num, QTableWidgetItem(str(data)))

        self.cur.execute(""" SELECT name FROM products """)
        result = self.cur.fetchall()

        self.search_combo.clear()
        self.search_combo.addItem("---- Products ----")

        for r in result:
            self.search_combo.addItem(r[0])


    def Get_Datash(self):
        cmd = """ USE bosh_mater  """
        self.cur.execute(cmd)
        product_val = self.search_combo.currentText()
        cmd = """ SELECT   date_a , name  , enter_a, exit_a , nats_a   FROM products WHERE name = %s  """
        val = (product_val,)
        self.cur.execute(cmd, val)
        result = self.cur.fetchall()
        self.table_2.setRowCount(0)
        for row_num, row_data in enumerate(result):
            self.table_2.insertRow(row_num)
            for column_num, data in enumerate(row_data):
                self.table_2.setItem(row_num, column_num, QTableWidgetItem(str(data)))



        self.cur.execute(""" SELECT name FROM products """)
        result = self.cur.fetchall()

        self.search_combo.clear()
        self.search_combo.addItem("---- Products ----")

        for r in result:
            self.search_combo.addItem(r[0])





    def Add_Products(self):
        name_val = self.name_edit.text()
        enter_val = self.quantity_edit.text()
        nats_val = self.unit_edit.text()
        exit_val = 0
        date_vdl = self.date_edit.text()

        sql = """ INSERT INTO `products` (date_a , name, enter_a, exit_a , nats_a ) VALUES (%s, %s, %s , %s , %s )  """
        val = (date_vdl ,name_val, enter_val,exit_val , nats_val   )

        self.cur.execute(sql, val)
        self.conn.commit()

        self.Clear_Edit()
        self.Get_Data()


    def exit_Products(self):
        name_vale = self.name_edit_3.text()
        exit_vale = self.quantity_edit_3.text()
        notes_vale = self.unit_edit_3.text()
        date_vale = self.date_edit_3.text()
        enter_val = 0

        sql = """ INSERT INTO `products` (date_a , name, enter_a, exit_a , nats_a ) VALUES (%s, %s, %s , %s , %s )  """
        val = (date_vale , name_vale,enter_val, exit_vale, notes_vale )

        self.cur.execute(sql, val)
        self.conn.commit()

        self.Clear_exit_3()
        self.Get_Data()

    def Search_Products(self):
        try:
            product_val = self.search_combo.currentText()

            sql = """ SELECT product_id, name,sum(enter_a), sum(exit_a) FROM products WHERE name = %s  """
            val = (product_val,)

            self.cur.execute(sql, val)
            result = self.cur.fetchall()

           # r1 = result[0][0]
            r2 = result[0][1]
            r3 = result[0][2]
            r4 = result[0][3]

            #self.id_label.setText(str(r1))
            self.name_edit_2.setText(str(r2))
            self.quantity_edit_2.setText(str(r3))
            self.unit_edit_2.setText(str(r4))
        except:
            self.Clear_Edit_2()
            pass

    def Update_Product(self):
        id_val = self.id_label.text()
        name_val = self.name_edit_2.text()
        enter_val = self.quantity_edit_2.text()
        exit_val = self.unit_edit_2.text()

        sql = """ UPDATE products SET name_a=%s, enter_a=%s, exit_a=%s WHERE product_id=%s """
        row = (name_val, enter_val, exit_val, id_val)

        self.cur.execute(sql, row)

        # save the changes with the commit() function
        self.conn.commit()

        self.Clear_Edit_2()
        self.Get_Data()





    def Delete_Product(self):

        id_val = str(self.id_label.text())
        cmd = """ DELETE FROM products WHERE product_id=%s """
        self.cur.execute(cmd, (id_val,))
        self.conn.commit()

        self.Clear_Edit_2()
        self.Get_Data()

    def Handel_Buttons(self):
        self.btn_all.clicked.connect(self.Open_All_Products)
        self.btn_add.clicked.connect(self.Open_Add_Products)
        self.btn_add_product_3.clicked.connect(self.exit_Products)
        self.btn_edit.clicked.connect(self.Open_Edit_Products)
        self.btn_settings.clicked.connect(self.Open_Settings)
        self.btn_apply.clicked.connect(self.Change_Theme)
        self.btn_refresh.clicked.connect(self.Get_Data)

        self.btn_update.clicked.connect(self.Get_Datash)

        self.btn_add_product.clicked.connect(self.Add_Products)
        self.btn_search.clicked.connect(self.Search_Products)
        #self.btn_delete.clicked.connect(self.Delete_Product)
        #self.btn_update.clicked.connect(self.Update_Product)

        self.btn_edit_2.clicked.connect(self.Open_Exeti_Products)

    def Change_Theme(self):
        combotext = str(self.themes_combo.currentText())

        if not "---- Themes ----" == combotext:
            if "orange dark" in combotext.lower():
                self.Dark_Orange_Theme()
            elif "blue dark" in combotext.lower():
                self.Dark_Blue_Theme()
            elif "q dark" in combotext.lower():
                self.QDark_Theme()
            elif "gray dark" in combotext.lower():
                self.Dark_Gray_Theme()
            else:
                pass



    def Open_All_Products(self):
        self.tabWidget.setCurrentIndex(0)

    def Open_Add_Products(self):
        self.tabWidget.setCurrentIndex(1)


    def Open_Exeti_Products(self):
        self.tabWidget.setCurrentIndex(2)




    def Open_Edit_Products(self):
        self.tabWidget.setCurrentIndex(3)

    def Open_Settings(self):
        self.tabWidget.setCurrentIndex(4)




    def Dark_Blue_Theme(self):
        style = open("data/themes/darkblue.css", "r")
        style = style.read()
        self.setStyleSheet(style)

    def Dark_Gray_Theme(self):
        style = open("data/themes/darkgray.css", "r")
        style = style.read()
        self.setStyleSheet(style)

    def Dark_Orange_Theme(self):
        style = open("data/themes/darkorange.css", "r")
        style = style.read()
        self.setStyleSheet(style)

    def QDark_Theme(self):
        style = open("data/themes/qdark.css", "r")
        style = style.read()
        self.setStyleSheet(style)




def main():
    app = QApplication(sys.argv)
    window = Main()
    window.show()
    app.exec_()


if __name__ == "__main__":
    main()
