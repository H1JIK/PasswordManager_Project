import sqlite3
import sys

from loginw_ui import Ui_login_w
from PasswordManager_main import Ui_PasswordManager
from add_acc_site_ui import Ui_Add_Acc_Ui
from add_new_user_ui import Ui_Add_user
from PyQt5.QtWidgets import QApplication, QMainWindow, QTableWidgetItem, QWidget, QMessageBox
from PyQt5 import QtGui
from test_generate_password import Generate
from check_password import Check_password


class Password_Manager_Main(QMainWindow, Ui_PasswordManager):
    def __init__(self, parent=None):
        global user_id, acc_lst, cur
        super().__init__(parent)
        self.setWindowIcon(QtGui.QIcon('logo.png'))
        self.setupUi(self)
        self.con = sqlite3.connect('Pass_Manager.db')
        self.cur = self.con.cursor()
        cur = self.con.cursor()
        user_id = self.cur.execute(f'''SELECT id from users
                                WHERE user_name = "{user.currentText()}"''').fetchall()[0][0]
        acc_lst = self.account_list
        self.run_table()
        self.find_account.clicked.connect(self.search_acc)
        self.add_pass.clicked.connect(self.open_add_pass_window)
        self.return_to_lst.clicked.connect(self.run_table)
        self.delete_acc.clicked.connect(self.delete_account)
        self.change_user.clicked.connect(self.change_usr)

    def change_usr(self):
        self.close()
        self.back_login = Login(self)
        self.back_login.show()

    def run_table(self):
        acc_lst.clear()
        self.result = cur.execute(f"""
                        SELECT site_name, link, login, password
                        FROM accounts
                        WHERE id_user = {user_id}""").fetchall()
        acc_lst.setRowCount(len(self.result))
        acc_lst.setColumnCount(4)
        acc_lst.setHorizontalHeaderLabels(
            ['Site name', 'Link', 'Login', 'Password'])
        for i, elem in enumerate(self.result):
            for j, val in enumerate(elem):
                acc_lst.setItem(i, j, QTableWidgetItem(str(val)))

    def open_add_pass_window(self):
        self.add_pass_acc1 = Add_account_Site(self)
        self.add_pass_acc1.show()

    def search_acc(self):
        if self.request.text():
            self.result = self.cur.execute(
                f"""SELECT site_name, link, login, password
                    FROM accounts
                    WHERE site_name LIKE '{self.request.text()}' AND id_user = {user_id}"""
            ).fetchall()
        self.account_list.setRowCount(len(self.result))
        self.account_list.setColumnCount(4)
        self.account_list.setHorizontalHeaderLabels(
            ['Site name', 'Link', 'Login', 'Password'])
        for i, elem in enumerate(self.result):
            for j, val in enumerate(elem):
                self.account_list.setItem(i, j, QTableWidgetItem(str(val)))

    def delete_account(self):
        rows = list(set([i.row() for i in self.account_list.selectedItems()]))
        name_s = [self.account_list.item(i, 0).text() for i in rows]
        if self.account_list.selectedItems() != []:
            valid = QMessageBox.question(
                self, 'Подтверждение удаления', "Действительно удалить аккаунт от " + ",".join(name_s),
                QMessageBox.Yes, QMessageBox.No)
            if valid == QMessageBox.Yes:
                self.cur.execute(f'DELETE FROM accounts WHERE site_name LIKE "{name_s[0]}" AND id_user = "{user_id}"')
                self.con.commit()
                cur_row = self.account_list.currentRow()
                self.account_list.removeRow(cur_row)
                self.con.commit()


class Add_account_Site(QMainWindow, Ui_Add_Acc_Ui):
    def __init__(self, parent=None):
        global cur
        super().__init__(parent)
        self.setWindowIcon(QtGui.QIcon('logo.png'))
        self.con = sqlite3.connect('Pass_Manager.db')
        cur = self.con.cursor()
        self.setupUi(self)
        self.add_site_btn.clicked.connect(self.add_site_acc)
        self.generate_passw_btn.clicked.connect(self.generate_strong_password)
        self.check_passw_button.clicked.connect(self.check_passw)
        self.sites_names_lst = cur.execute('''SELECT site_name from accounts''').fetchall()

    def add_site_acc(self):
        dump = (
            user_id, self.line_namesite.text(), self.line_link.text(), self.line_passw.text(),
            self.line_login.text())
        line_txt = self.line_namesite.text()
        flag_new_acc_error = False
        for acc_name in self.sites_names_lst:
            if acc_name[0] == line_txt:
                flag_new_acc_error = True
        self.add_new_acc_error1.setStyleSheet("color: red"), self.add_new_acc_error2.setStyleSheet("color: red")
        if line_txt == '':
            self.add_new_acc_error1.setText('Название сайта/приложения не должно быть пустым')
        elif flag_new_acc_error:
            self.add_new_acc_error1.setText('Название сайта/приложения не должно совпадать с ранее добавленным')
        elif self.line_passw.text() == '':
            self.add_new_acc_error2.setText('Пароль не может быть пустым')
        else:
            cur.execute("INSERT INTO accounts VALUES(?, ?, ?, ?, ?);", dump)
            self.con.commit()
            Password_Manager_Main.run_table(self)
            self.close()

    def check_passw(self):
        pass_txt = self.line_passw.text()
        if pass_txt == '':
            self.add_new_acc_error2.setStyleSheet(f"color: red")
            self.add_new_acc_error2.setText('Строка ввода пароля пуста')
        elif pass_txt == self.line_login.text():
            self.add_new_acc_error2.setStyleSheet(f"color: red; background-color: black")
            self.add_new_acc_error2.setText('Уровень надёжности пароля: ужсано (пароль совпадает с логином)')
        else:
            check_p = Check_password()
            verdict_password = check_p.check(pass_txt)
            self.add_new_acc_error2.setStyleSheet(f"color: {verdict_password[1]}; background-color: black")
            self.add_new_acc_error2.setText(f'Уровень надёжности пароля: {verdict_password[0]}')

    def generate_strong_password(self):
        g = Generate()
        self.line_passw.setText(g.generate_password())


class Login(QMainWindow, Ui_login_w):
    def __init__(self, parent=None):
        global user
        super().__init__(parent)
        self.setWindowIcon(QtGui.QIcon('logo.png'))
        self.setupUi(self)
        self.con = sqlite3.connect('Pass_Manager.db')
        self.cur = self.con.cursor()
        user = self.view_user
        self.load_roll_users()
        self.okb_user.clicked.connect(self.open_pass_manager)
        self.add_user.clicked.connect(self.add_new_user_def)
        self.delete_user_button.clicked.connect(self.delete_user)

    def load_roll_users(self):
        user.clear()
        user.addItems(
            [item[0] for item in self.cur.execute("SELECT user_name FROM users").fetchall()])

    def open_pass_manager(self):
        if user.currentText() == '':
            self.error_login.setStyleSheet("color: red")
            self.error_login.setText('Выберите или создайте пользователя')
        else:
            self.close()
            self.passmanager = Password_Manager_Main(self)
            self.passmanager.show()

    def add_new_user_def(self):
        self.close()
        self.add_new_user = Add_new_user()
        self.add_new_user.show()

    def delete_user(self):
        if user.currentText() == '':
            self.error_login.setStyleSheet("color: red")
            self.error_login.setText('Пользователь не выбран')
        else:
            valid = QMessageBox.question(
                self, 'Подтверждение удаления', "Действительно удалить пользователя " + user.currentText(),
                QMessageBox.Yes, QMessageBox.No)
            if valid == QMessageBox.Yes:
                cur_usr_id = self.cur.execute(f'''SELECT id from users
                                        WHERE user_name = "{user.currentText()}"''').fetchall()[0][0]
                self.cur.execute(f'DELETE FROM users WHERE id = "{cur_usr_id}"')
                self.cur.execute(f'DELETE FROM accounts WHERE id_user = "{cur_usr_id}"')
                self.con.commit()
                Login.load_roll_users(self)


class Add_new_user(QWidget, Ui_Add_user):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.setWindowIcon(QtGui.QIcon('logo.png'))
        self.con = sqlite3.connect('Pass_Manager.db')
        self.cur = self.con.cursor()
        self.users_lst = self.cur.execute('''SELECT user_name from users''').fetchall()
        self.add_btn_new_user.clicked.connect(self.add_new_user_sql)
        self.back_but_log.clicked.connect(self.back_to_login_window)

    def add_new_user_sql(self):
        res_text = self.input_new_user.text()
        flag_new_user_error = False
        for usr_name in self.users_lst:
            if usr_name[0] == res_text:
                flag_new_user_error = True
        self.add_new_user_error.setStyleSheet("color: red")
        if res_text == '':
            self.add_new_user_error.setText('Имя пользователя не должно быть пустым')
        elif flag_new_user_error:
            self.add_new_user_error.setText('Имя пользователя не должно совпадать с ранее созданным')
        else:
            self.cur.execute(f'''INSERT INTO users (user_name) VALUES('{res_text}')''')
            self.con.commit()
            self.close()
            self.back_lg = Login(self)
            self.back_lg.show()

    def back_to_login_window(self):
        self.close()
        self.back_lg = Login(self)
        self.back_lg.show()


def except_hook(cls, exception, traceback):
    sys.__excepthook__(cls, exception, traceback)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setStyle('Fusion')
    ex = Login()
    ex.show()
    sys.excepthook = except_hook
    sys.exit(app.exec_())
