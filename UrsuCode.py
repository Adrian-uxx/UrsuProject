import sys
from datetime import datetime

import pyodbc
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QLineEdit, QPushButton, QTabWidget, QTableWidget,
    QTableWidgetItem, QMessageBox, QHeaderView, QComboBox, QDateEdit,
    QDoubleSpinBox, QSpinBox, QTextEdit
)
from PyQt5.QtCore import Qt, QDate
from PyQt5.QtGui import QFont, QColor

# ===== CONEXIUNE SQL SERVER =========================================
CONN_STR = (
    "Driver={SQL Server};"
    "Server=desktop-1bq40ct;"
    "Database=MoldelectricaFinanciar;"
    "Trusted_Connection=yes;"
)

def get_connection():
    return pyodbc.connect(CONN_STR)

def exec_query(query, params=(), fetch=False):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(query, params)
    rows = cur.fetchall() if fetch else None
    conn.commit()
    cur.close()
    conn.close()
    return rows

# ===== STIL GENERAL =================================================
STYLE = """
QMainWindow {
    background-color: #1e1e1e;
}

QTabWidget::pane {
    border: 1px solid #b71c1c;
    background-color: #2c2c2c;
    border-radius: 10px;
}

QTabBar::tab {
    background: #b71c1c;
    color: white;
    padding: 12px 30px;
    margin: 3px;
    border-top-left-radius: 12px;
    border-top-right-radius: 12px;
    font-weight: bold;
    font-size: 13px;
}

QTabBar::tab:selected {
    background: #e63946;
    color: #ffffff;
}

QPushButton {
    background-color: #e63946;
    color: white;
    border: none;
    padding: 10px 20px;
    border-radius: 6px;
    font-weight: bold;
    font-size: 13px;
}

QPushButton:hover {
    background-color: #b71c1c;
    color: white;
}

QLineEdit, QComboBox, QDoubleSpinBox,
QSpinBox, QDateEdit {
    padding: 8px;
    border: 2px solid #b71c1c;
    border-radius: 6px;
    background-color: #f5f5f5;
    color: black;
    font-size: 13px;
}

QTableWidget {
    background-color: #ffffff;
    alternate-background-color: #f7f7f7;
    selection-background-color: #e63946;
    color: black;
}

QHeaderView::section {
    background-color: #b71c1c;
    color: white;
    padding: 8px;
    font-weight: bold;
    font-size: 12px;
    border: none;
}

QLabel {
    color: #f5f5f5;
    font-size: 13px;
}
"""

# ===== FEREASTRA PRINCIPALA =========================================
class MoldelectricaApp(QMainWindow):
    def __init__(self, user_info):
        super().__init__()
        self.user_info = user_info
        self.is_admin = (self.user_info["tip_cont"].lower() == "admin")

        self.setWindowTitle("Moldelectrica - Repartizare venituri și cheltuieli")
        self.setMinimumSize(1200, 720)
        self.setStyleSheet(STYLE)

        title = QLabel("Moldelectrica – Subsistem informatic financiar")
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet(
            "background-color: #b71c1c;"
            "color: white;"
            "font-size: 18px;"
            "font-weight: bold;"
            "padding: 12px;"
            "border-bottom: 2px solid #e63946;"
        )
        
        def apply_permissions(self):
            if not self.is_admin:
                admin_buttons = [
                    getattr(self, 'btn_add_tranzactie', None),
                    getattr(self, 'btn_add_regula', None),
                    getattr(self, 'btn_save_buget', None),
                    getattr(self, 'btn_repartizeaza', None),
                    getattr(self, 'btn_gen_export', None),
                    getattr(self, 'btn_add_angajat', None),
                    getattr(self, 'btn_calc_salariu', None),
                    getattr(self, 'btn_add_programare', None),
                ]

                for btn in admin_buttons:
                    if btn is not None:
                        btn.hide()

                # ascundem tab-urile clientului
                self.tabs.setTabVisible(self.tabs.indexOf(self.tab_reguli), False)
                self.tabs.setTabVisible(self.tabs.indexOf(self.tab_repartizare), False)
                self.tabs.setTabVisible(self.tabs.indexOf(self.tab_export), False)
                self.tabs.setTabVisible(self.tabs.indexOf(self.tab_angajati), False)
                self.tabs.setTabVisible(self.tabs.indexOf(self.tab_programari), False)

            else:
                # Adminul vede tot
                self.tabs.setTabVisible(self.tabs.indexOf(self.tab_reguli), True)
                self.tabs.setTabVisible(self.tabs.indexOf(self.tab_repartizare), True)
                self.tabs.setTabVisible(self.tabs.indexOf(self.tab_export), True)
                self.tabs.setTabVisible(self.tabs.indexOf(self.tab_angajati), True)
                self.tabs.setTabVisible(self.tabs.indexOf(self.tab_programari), True)


        central = QWidget()
        v = QVBoxLayout()
        v.addWidget(title)

        self.tabs = QTabWidget()
        v.addWidget(self.tabs)
        central.setLayout(v)
        self.setCentralWidget(central)

        # taburi
        self.tab_tranzactii = QWidget()
        self.tab_reguli = QWidget()
        self.tab_bugete = QWidget()
        self.tab_repartizare = QWidget()
        self.tab_export = QWidget()
        self.tab_angajati = QWidget()
        self.tab_programari = QWidget()
        self.tab_rapoarte = QWidget()
        self.tab_audit = QWidget()

        self.tabs.addTab(self.tab_tranzactii, "Tranzacții")
        self.tabs.addTab(self.tab_reguli, "Reguli")
        self.tabs.addTab(self.tab_bugete, "Bugete")
        self.tabs.addTab(self.tab_repartizare, "Repartizare")
        self.tabs.addTab(self.tab_export, "Export")
        self.tabs.addTab(self.tab_angajati, "Angajați/Salarii")
        self.tabs.addTab(self.tab_programari, "Programări")
        self.tabs.addTab(self.tab_rapoarte, "Rapoarte")
        self.tabs.addTab(self.tab_audit, "Audit")

        # construim fiecare tab
        self.build_tab_tranzactii()
        self.build_tab_reguli()
        self.build_tab_bugete()
        self.build_tab_repartizare()
        self.build_tab_export()
        self.build_tab_angajati()
        self.build_tab_programari()
        self.build_tab_rapoarte()
        self.build_tab_audit()

        self.apply_permissions()

        self.statusBar().showMessage(
            f"Autentificat ca: {user_info['login']} ({user_info['tip_cont']})"
        )

    # ===== PERMISIUNI (admin vs client) ==============================
        # ===== PERMISIUNI (admin vs client) ==============================
    def apply_permissions(self):
        """
        Se rulează după logare.
        Clientul vede doar tab-urile de vizualizare.
        Adminul vede toate tab-urile + butoanele de operare.
        """

        # -------------- CLIENT (utilizator simplu) --------------------
        if not self.is_admin:

            # Lista butoanelor administrative — se ascund complet
            admin_buttons = [
                getattr(self, 'btn_add_tranzactie', None),
                getattr(self, 'btn_add_regula', None),
                getattr(self, 'btn_save_buget', None),
                getattr(self, 'btn_repartizeaza', None),
                getattr(self, 'btn_gen_export', None),
                getattr(self, 'btn_add_angajat', None),
                getattr(self, 'btn_calc_salariu', None),
                getattr(self, 'btn_add_programare', None),
            ]

            for btn in admin_buttons:
                if btn is not None:
                    btn.hide()

            # Ascundem tab-urile administrative
            self.tabs.setTabVisible(self.tabs.indexOf(self.tab_reguli), False)
            self.tabs.setTabVisible(self.tabs.indexOf(self.tab_repartizare), False)
            self.tabs.setTabVisible(self.tabs.indexOf(self.tab_export), False)
            self.tabs.setTabVisible(self.tabs.indexOf(self.tab_angajati), False)
            self.tabs.setTabVisible(self.tabs.indexOf(self.tab_programari), False)

            # Clientul vede doar: tranzacții, bugete, rapoarte, audit
            self.tabs.setTabVisible(self.tabs.indexOf(self.tab_tranzactii), True)
            self.tabs.setTabVisible(self.tabs.indexOf(self.tab_bugete), True)
            self.tabs.setTabVisible(self.tabs.indexOf(self.tab_rapoarte), True)
            self.tabs.setTabVisible(self.tabs.indexOf(self.tab_audit), True)

        # -------------- ADMIN ----------------------------------------
        else:
            # Adminul vede tot
            self.tabs.setTabVisible(self.tabs.indexOf(self.tab_tranzactii), True)
            self.tabs.setTabVisible(self.tabs.indexOf(self.tab_reguli), True)
            self.tabs.setTabVisible(self.tabs.indexOf(self.tab_bugete), True)
            self.tabs.setTabVisible(self.tabs.indexOf(self.tab_repartizare), True)
            self.tabs.setTabVisible(self.tabs.indexOf(self.tab_export), True)
            self.tabs.setTabVisible(self.tabs.indexOf(self.tab_angajati), True)
            self.tabs.setTabVisible(self.tabs.indexOf(self.tab_programari), True)
            self.tabs.setTabVisible(self.tabs.indexOf(self.tab_rapoarte), True)
            self.tabs.setTabVisible(self.tabs.indexOf(self.tab_audit), True)


    # ===== AUDIT UTIL ================================================
    def log_actiune(self, tip_actiune, descriere):
        id_log = ("LG" + datetime.now().strftime("%Y%m%d%H%M%S"))[-13:]
        try:
            exec_query(
                """
                INSERT INTO LogAudit
                (ID_Log, ID_Utilizator, Tip_Actiune, Data_Ora, Descriere)
                VALUES (?,?,?,?,?)
                """,
                (id_log, self.user_info["id"], tip_actiune, datetime.now(), descriere),
                fetch=False
            )
        except Exception:
            pass  # nu blocam aplicatia daca log-ul esueaza

    # ===== TAB TRANZACTII ============================================
    def build_tab_tranzactii(self):
        layout = QVBoxLayout()
        form = QHBoxLayout()
        left = QVBoxLayout()
        right = QVBoxLayout()

        self.tr_tip = QComboBox()
        self.tr_tip.addItems(["Venit", "Cheltuiala"])
        self.tr_suma = QDoubleSpinBox()
        self.tr_suma.setRange(0, 10_000_000)
        self.tr_suma.setDecimals(2)
        self.tr_data = QDateEdit()
        self.tr_data.setCalendarPopup(True)
        self.tr_data.setDate(QDate.currentDate())
        self.tr_descriere = QLineEdit()
        self.tr_centru = QLineEdit()

        def add_row(lbl, widget):
            left.addWidget(QLabel(lbl))
            left.addWidget(widget)

        add_row("Tip operațiune:", self.tr_tip)
        add_row("Sumă:", self.tr_suma)
        add_row("Data operațiunii:", self.tr_data)
        add_row("Descriere:", self.tr_descriere)
        add_row("ID centru responsabil:", self.tr_centru)

        self.btn_add_tranzactie = QPushButton("Adaugă tranzacție")
        self.btn_add_tranzactie.clicked.connect(self.adauga_tranzactie)
        btn_reload = QPushButton("Reîncarcă tranzacții")
        btn_reload.clicked.connect(self.incarca_tranzactii)

        right.addWidget(self.btn_add_tranzactie)
        right.addWidget(btn_reload)
        right.addStretch()

        form.addLayout(left, 3)
        form.addLayout(right, 1)

        self.table_tranzactii = QTableWidget()
        self.table_tranzactii.setAlternatingRowColors(True)
        self.table_tranzactii.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

        layout.addLayout(form)
        layout.addWidget(QLabel("Lista tranzacțiilor:"))
        layout.addWidget(self.table_tranzactii)

        self.tab_tranzactii.setLayout(layout)
        self.incarca_tranzactii()

    def adauga_tranzactie(self):
        tip = self.tr_tip.currentText()
        suma = self.tr_suma.value()
        data = self.tr_data.date().toString("yyyy-MM-dd")
        desc = self.tr_descriere.text().strip()
        centru = self.tr_centru.text().strip() or None

        if suma <= 0:
            QMessageBox.warning(self, "Eroare", "Suma trebuie să fie > 0.")
            return

        now_str = datetime.now().strftime("%Y%m%d%H%M%S")
        id_tr = f"TR{now_str}"[-13:]

        try:
            exec_query(
                """
                INSERT INTO Tranzactii
                (ID_Transactie, Tip_Operatiune, Suma, Data_Operatiune,
                 Descriere, ID_CentruResponsabil)
                VALUES (?,?,?,?,?,?)
                """,
                (id_tr, tip, suma, data, desc, centru),
                fetch=False
            )
            self.log_actiune("Adaugare", f"Tranzacție {id_tr} adăugată")
        except Exception as e:
            QMessageBox.critical(self, "Eroare SQL", str(e))
            return

        QMessageBox.information(self, "OK", "Tranzacție adăugată.")
        self.incarca_tranzactii()

    def incarca_tranzactii(self):
        try:
            rows = exec_query(
                """
                SELECT ID_Transactie, Tip_Operatiune, Suma,
                       Data_Operatiune, Descriere, ID_CentruResponsabil
                FROM Tranzactii
                ORDER BY Data_Operatiune DESC
                """,
                fetch=True
            ) or []
        except Exception as e:
            QMessageBox.critical(self, "Eroare SQL", str(e))
            return

        header = ["ID", "Tip", "Sumă", "Data", "Descriere", "Centru"]
        self.table_tranzactii.setRowCount(len(rows))
        self.table_tranzactii.setColumnCount(len(header))
        self.table_tranzactii.setHorizontalHeaderLabels(header)

        for r, row in enumerate(rows):
            for c, val in enumerate(row):
                self.table_tranzactii.setItem(
                    r, c, QTableWidgetItem("" if val is None else str(val))
                )

    # ===== TAB REGULI ================================================
    def build_tab_reguli(self):
        layout = QVBoxLayout()
        form = QHBoxLayout()
        left = QVBoxLayout()
        right = QVBoxLayout()

        self.reg_descriere = QLineEdit()
        self.reg_tip_criteriu = QLineEdit()
        self.reg_valoare = QLineEdit()
        self.reg_procent = QDoubleSpinBox()
        self.reg_procent.setRange(0, 100)
        self.reg_procent.setDecimals(2)

        def add_row(lbl, w):
            left.addWidget(QLabel(lbl))
            left.addWidget(w)

        add_row("Descriere regulă:", self.reg_descriere)
        add_row("Tip criteriu:", self.reg_tip_criteriu)
        add_row("Valoare criteriu:", self.reg_valoare)
        add_row("Procent repartizare:", self.reg_procent)

        self.btn_add_regula = QPushButton("Adaugă regulă")
        self.btn_add_regula.clicked.connect(self.adauga_regula)
        btn_reload = QPushButton("Reîncarcă reguli")
        btn_reload.clicked.connect(self.incarca_reguli)

        right.addWidget(self.btn_add_regula)
        right.addWidget(btn_reload)
        right.addStretch()

        form.addLayout(left, 3)
        form.addLayout(right, 1)

        self.table_reguli = QTableWidget()
        self.table_reguli.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

        layout.addLayout(form)
        layout.addWidget(QLabel("Reguli definite:"))
        layout.addWidget(self.table_reguli)

        self.tab_reguli.setLayout(layout)
        self.incarca_reguli()

    def adauga_regula(self):
        descr = self.reg_descriere.text().strip()
        tipc = self.reg_tip_criteriu.text().strip()
        valc = self.reg_valoare.text().strip()
        proc = self.reg_procent.value()

        if not descr or not tipc:
            QMessageBox.warning(self, "Eroare", "Descriere și tip criteriu sunt obligatorii.")
            return

        id_reg = ("RG" + datetime.now().strftime("%Y%m%d%H%M%S"))[-13:]

        try:
            exec_query(
                """
                INSERT INTO ReguliRepartizare
                (ID_Regula, Descriere_Regula, Tip_Criteriu, Valoare_Criteriu, Procent_Repartizare)
                VALUES (?,?,?,?,?)
                """,
                (id_reg, descr, tipc, valc or None, proc),
                fetch=False
            )
            self.log_actiune("Adaugare", f"Regulă {id_reg} adăugată")
        except Exception as e:
            QMessageBox.critical(self, "Eroare SQL", str(e))
            return

        QMessageBox.information(self, "OK", "Regulă adăugată.")
        self.incarca_reguli()

    def incarca_reguli(self):
        try:
            rows = exec_query(
                """
                SELECT ID_Regula, Descriere_Regula, Tip_Criteriu,
                       Valoare_Criteriu, Procent_Repartizare
                FROM ReguliRepartizare
                """,
                fetch=True
            ) or []
        except Exception as e:
            QMessageBox.critical(self, "Eroare SQL", str(e))
            return

        header = ["ID", "Descriere", "Tip criteriu", "Valoare", "Procent"]
        self.table_reguli.setRowCount(len(rows))
        self.table_reguli.setColumnCount(len(header))
        self.table_reguli.setHorizontalHeaderLabels(header)
        for r, row in enumerate(rows):
            for c, val in enumerate(row):
                self.table_reguli.setItem(
                    r, c, QTableWidgetItem("" if val is None else str(val))
                )

    # ===== TAB BUGETE ================================================
    def build_tab_bugete(self):
        layout = QVBoxLayout()
        form = QHBoxLayout()
        left = QVBoxLayout()
        right = QVBoxLayout()

        self.buget_centru = QLineEdit()
        self.buget_an = QLineEdit()
        self.buget_suma_aloc = QDoubleSpinBox()
        self.buget_suma_aloc.setRange(0, 1_000_000_000)
        self.buget_suma_aloc.setDecimals(2)
        self.buget_suma_eff = QDoubleSpinBox()
        self.buget_suma_eff.setRange(0, 1_000_000_000)
        self.buget_suma_eff.setDecimals(2)

        def add_row(lbl, w):
            left.addWidget(QLabel(lbl))
            left.addWidget(w)

        add_row("ID centru responsabil:", self.buget_centru)
        add_row("An buget:", self.buget_an)
        add_row("Sumă alocată:", self.buget_suma_aloc)
        add_row("Sumă efectiv cheltuită:", self.buget_suma_eff)

        self.btn_save_buget = QPushButton("Salvează buget")
        self.btn_save_buget.clicked.connect(self.salveaza_buget)
        btn_reload = QPushButton("Reîncarcă bugete")
        btn_reload.clicked.connect(self.incarca_bugete)

        right.addWidget(self.btn_save_buget)
        right.addWidget(btn_reload)
        right.addStretch()

        form.addLayout(left, 3)
        form.addLayout(right, 1)

        self.table_bugete = QTableWidget()
        self.table_bugete.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

        layout.addLayout(form)
        layout.addWidget(QLabel("Situație bugete:"))
        layout.addWidget(self.table_bugete)

        self.tab_bugete.setLayout(layout)
        self.incarca_bugete()

    def salveaza_buget(self):
        centru = self.buget_centru.text().strip()
        an = self.buget_an.text().strip()
        suma_aloc = self.buget_suma_aloc.value()
        suma_eff = self.buget_suma_eff.value()

        if not centru or not an:
            QMessageBox.warning(self, "Eroare", "Centru și an sunt obligatorii.")
            return

        status = "In limita"
        if suma_eff > suma_aloc:
            status = "Depasit"
        elif suma_eff < suma_aloc * 0.5:
            status = "Subutilizat"

        id_b = ("BG" + datetime.now().strftime("%Y%m%d%H%M%S"))[-13:]

        try:
            exec_query(
                """
                INSERT INTO Bugete
                (ID_Buget, ID_CentruResponsabil, An_Buget,
                 Suma_Alocata, Suma_EfectivaCheltuita, Status_Executie)
                VALUES (?,?,?,?,?,?)
                """,
                (id_b, centru, an, suma_aloc, suma_eff, status),
                fetch=False
            )
            self.log_actiune("Adaugare", f"Buget {id_b} adăugat")
        except Exception as e:
            QMessageBox.critical(self, "Eroare SQL", str(e))
            return

        QMessageBox.information(self, "OK", "Buget salvat.")
        self.incarca_bugete()

    def incarca_bugete(self):
        try:
            rows = exec_query(
                """
                SELECT ID_Buget, ID_CentruResponsabil, An_Buget,
                       Suma_Alocata, Suma_EfectivaCheltuita, Status_Executie
                FROM Bugete
                """,
                fetch=True
            ) or []
        except Exception as e:
            QMessageBox.critical(self, "Eroare SQL", str(e))
            return

        header = ["ID", "Centru", "An", "Alocată", "Efectiv", "Status"]
        self.table_bugete.setRowCount(len(rows))
        self.table_bugete.setColumnCount(len(header))
        self.table_bugete.setHorizontalHeaderLabels(header)

        for r, row in enumerate(rows):
            for c, val in enumerate(row):
                item = QTableWidgetItem("" if val is None else str(val))
                if c == 5:
                    if val == "Depasit":
                        item.setBackground(QColor(255, 182, 193))
                    elif val == "Subutilizat":
                        item.setBackground(QColor(255, 255, 141))
                self.table_bugete.setItem(r, c, item)

    # ===== TAB REPARTIZARE AUTOMATA ==================================
    def build_tab_repartizare(self):
        layout = QVBoxLayout()
        top = QHBoxLayout()

        self.btn_repartizeaza = QPushButton("Repartizează toate tranzacțiile")
        self.btn_repartizeaza.clicked.connect(self.ruleaza_repartizare)
        btn_reload = QPushButton("Reîncarcă repartizări")
        btn_reload.clicked.connect(self.incarca_repartizari)

        top.addWidget(self.btn_repartizeaza)
        top.addWidget(btn_reload)
        top.addStretch()

        self.table_repartizari = QTableWidget()
        self.table_repartizari.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

        layout.addLayout(top)
        layout.addWidget(QLabel("Repartizări generate (ID tranzacție -> centre):"))
        layout.addWidget(self.table_repartizari)

        self.tab_repartizare.setLayout(layout)
        self.incarca_repartizari()

    def ruleaza_repartizare(self):
        """
        Algoritm simplificat:
         - pentru fiecare tranzactie,
         - cautam reguli care se potrivesc
           Tip_Criteriu = 'Tip_Operatiune'  si Valoare_Criteriu = Tip_Operatiune
           sau
           Tip_Criteriu = 'Centru'          si Valoare_Criteriu = ID_CentruResponsabil
         - pentru fiecare regula potrivita inseram in Repartizari
        """
        try:
            tranzactii = exec_query(
                "SELECT ID_Transactie, Tip_Operatiune, ID_CentruResponsabil FROM Tranzactii",
                fetch=True
            ) or []
            reguli = exec_query(
                "SELECT ID_Regula, Descriere_Regula, Tip_Criteriu, Valoare_Criteriu, Procent_Repartizare FROM ReguliRepartizare",
                fetch=True
            ) or []
        except Exception as e:
            QMessageBox.critical(self, "Eroare SQL", str(e))
            return

        cnt = 0
        for tr in tranzactii:
            id_tr, tip_op, centru_tr = tr
            for reg in reguli:
                _, _, tip_c, val_c, procent = reg
                aplica = False
                if tip_c == "Tip_Operatiune" and val_c == tip_op:
                    aplica = True
                elif tip_c == "Centru" and centru_tr is not None and val_c == centru_tr:
                    aplica = True

                if aplica:
                    id_rep = ("RP" + datetime.now().strftime("%Y%m%d%H%M%S") + f"{cnt:02d}")[-13:]
                    try:
                        exec_query(
                            """
                            INSERT INTO Repartizari
                            (ID_Repartizare, ID_Transactie, ID_CentruResponsabil,
                             Procent_Repartizare, Coeficient)
                            VALUES (?,?,?,?,?)
                            """,
                            (id_rep, id_tr, centru_tr or "CR001", procent, 1.00),
                            fetch=False
                        )
                        cnt += 1
                    except Exception:
                        # daca exista deja o repartizare similara, ignoram
                        pass

        self.log_actiune("Repartizare", f"Repartizare automată rulată; {cnt} înregistrări.")
        QMessageBox.information(self, "OK", f"Repartizare finalizată. Înregistrări noi: {cnt}")
        self.incarca_repartizari()

    def incarca_repartizari(self):
        try:
            rows = exec_query(
                """
                SELECT R.ID_Repartizare, R.ID_Transactie, R.ID_CentruResponsabil,
                       R.Procent_Repartizare, R.Coeficient
                FROM Repartizari R
                ORDER BY R.ID_Transactie
                """,
                fetch=True
            ) or []
        except Exception as e:
            QMessageBox.critical(self, "Eroare SQL", str(e))
            return

        header = ["ID Repartizare", "ID Tranzacție", "Centru", "Procent", "Coeficient"]
        self.table_repartizari.setRowCount(len(rows))
        self.table_repartizari.setColumnCount(len(header))
        self.table_repartizari.setHorizontalHeaderLabels(header)

        for r, row in enumerate(rows):
            for c, val in enumerate(row):
                self.table_repartizari.setItem(
                    r, c, QTableWidgetItem("" if val is None else str(val))
                )

    # ===== TAB EXPORT =================================================
    def build_tab_export(self):
        layout = QVBoxLayout()
        top = QHBoxLayout()

        self.export_sistem = QComboBox()
        self.export_sistem.addItems(["1C Contabilitate", "SAP Financials", "M-EnergoSoft"])

        self.btn_gen_export = QPushButton("Generează export pentru toate tranzacțiile")
        self.btn_gen_export.clicked.connect(self.genereaza_export)

        top.addWidget(QLabel("Sistem contabil:"))
        top.addWidget(self.export_sistem)
        top.addWidget(self.btn_gen_export)
        top.addStretch()

        self.table_export = QTableWidget()
        self.table_export.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

        layout.addLayout(top)
        layout.addWidget(QLabel("Istoric exporturi:"))
        layout.addWidget(self.table_export)

        self.tab_export.setLayout(layout)
        self.incarca_exporturi()

    def genereaza_export(self):
        sistem = self.export_sistem.currentText()
        today = datetime.now().strftime("%Y-%m-%d")

        try:
            tranzactii = exec_query(
                "SELECT ID_Transactie, Suma FROM Tranzactii",
                fetch=True
            ) or []
        except Exception as e:
            QMessageBox.critical(self, "Eroare SQL", str(e))
            return

        cnt = 0
        for tr in tranzactii:
            id_tr, suma = tr
            id_ex = ("EX" + datetime.now().strftime("%Y%m%d%H%M%S") + f"{cnt:02d}")[-13:]
            try:
                exec_query(
                    """
                    INSERT INTO Exporturi
                    (ID_Export, ID_Transactie, Sistem_Export, Data_Exportata, Suma_Exportata)
                    VALUES (?,?,?,?,?)
                    """,
                    (id_ex, id_tr, sistem, today, suma),
                    fetch=False
                )
                cnt += 1
            except Exception:
                pass

        self.log_actiune("Export", f"Export {sistem} generat; {cnt} înregistrări.")
        QMessageBox.information(self, "OK", f"Export generat ({cnt} rânduri).")
        self.incarca_exporturi()

    def incarca_exporturi(self):
        try:
            rows = exec_query(
                """
                SELECT ID_Export, ID_Transactie, Sistem_Export, Data_Exportata, Suma_Exportata
                FROM Exporturi
                ORDER BY Data_Exportata DESC
                """,
                fetch=True
            ) or []
        except Exception as e:
            QMessageBox.critical(self, "Eroare SQL", str(e))
            return

        header = ["ID Export", "ID Tranzacție", "Sistem", "Data", "Sumă"]
        self.table_export.setRowCount(len(rows))
        self.table_export.setColumnCount(len(header))
        self.table_export.setHorizontalHeaderLabels(header)

        for r, row in enumerate(rows):
            for c, val in enumerate(row):
                self.table_export.setItem(
                    r, c, QTableWidgetItem("" if val is None else str(val))
                )

    # ===== TAB ANGAJATI & SALARII ====================================
    def build_tab_angajati(self):
        layout = QVBoxLayout()
        form = QHBoxLayout()
        left = QVBoxLayout()
        right = QVBoxLayout()

        self.ang_idnp = QLineEdit()
        self.ang_nume = QLineEdit()
        self.ang_prenume = QLineEdit()
        self.ang_email = QLineEdit()
        self.ang_tel = QLineEdit()
        self.ang_functie = QLineEdit()
        self.ang_data = QDateEdit()
        self.ang_data.setCalendarPopup(True)
        self.ang_data.setDate(QDate.currentDate())
        self.ang_salariu = QDoubleSpinBox()
        self.ang_salariu.setRange(0, 1_000_000)
        self.ang_salariu.setDecimals(2)

        def add_row(lbl, w):
            left.addWidget(QLabel(lbl))
            left.addWidget(w)

        add_row("IDNP:", self.ang_idnp)
        add_row("Nume:", self.ang_nume)
        add_row("Prenume:", self.ang_prenume)
        add_row("Email:", self.ang_email)
        add_row("Telefon:", self.ang_tel)
        add_row("Funcție:", self.ang_functie)
        add_row("Data angajării:", self.ang_data)
        add_row("Salariu bază:", self.ang_salariu)

        self.btn_add_angajat = QPushButton("Adaugă angajat")
        self.btn_add_angajat.clicked.connect(self.adauga_angajat)

        # zona calcul salar
        self.calc_idnp = QLineEdit()
        self.calc_luna = QLineEdit()
        self.calc_luna.setPlaceholderText("ex: 2025-01")
        self.calc_ore = QSpinBox()
        self.calc_ore.setRange(0, 300)
        self.btn_calc_salariu = QPushButton("Calculează salariu")
        self.btn_calc_salariu.clicked.connect(self.calculeaza_salariu)

        right.addWidget(self.btn_add_angajat)
        right.addSpacing(15)
        right.addWidget(QLabel("Calcul salariu:"))
        right.addWidget(QLabel("IDNP angajat:"))
        right.addWidget(self.calc_idnp)
        right.addWidget(QLabel("Lună (YYYY-MM):"))
        right.addWidget(self.calc_luna)
        right.addWidget(QLabel("Nr. ore lucrate:"))
        right.addWidget(self.calc_ore)
        right.addWidget(self.btn_calc_salariu)
        right.addStretch()

        form.addLayout(left, 3)
        form.addLayout(right, 2)

        self.table_angajati = QTableWidget()
        self.table_angajati.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

        layout.addLayout(form)
        layout.addWidget(QLabel("Lista angajaților:"))
        layout.addWidget(self.table_angajati)

        self.tab_angajati.setLayout(layout)
        self.incarca_angajati()

    def adauga_angajat(self):
        idnp = self.ang_idnp.text().strip()
        nume = self.ang_nume.text().strip()
        pren = self.ang_prenume.text().strip()
        email = self.ang_email.text().strip()
        tel = self.ang_tel.text().strip()
        functie = self.ang_functie.text().strip()
        data_ang = self.ang_data.date().toString("yyyy-MM-dd")
        salariu = self.ang_salariu.value()

        if not idnp or not nume or not pren or not functie:
            QMessageBox.warning(self, "Eroare", "IDNP, nume, prenume și funcție sunt obligatorii.")
            return

        try:
            exec_query(
                """
                INSERT INTO Angajati
                (IDNP, Nume, Prenume, Email, Telefon, Functie, Data_Angajarii, Salariu_Baza)
                VALUES (?,?,?,?,?,?,?,?)
                """,
                (idnp, nume, pren, email, tel, functie, data_ang, salariu),
                fetch=False
            )
            self.log_actiune("Adaugare", f"Angajat {idnp} adăugat")
        except Exception as e:
            QMessageBox.critical(self, "Eroare SQL", str(e))
            return

        QMessageBox.information(self, "OK", "Angajat adăugat.")
        self.incarca_angajati()

    def incarca_angajati(self):
        try:
            rows = exec_query(
                "SELECT IDNP, Nume, Prenume, Functie, Data_Angajarii, Salariu_Baza FROM Angajati",
                fetch=True
            ) or []
        except Exception as e:
            QMessageBox.critical(self, "Eroare SQL", str(e))
            return

        header = ["IDNP", "Nume", "Prenume", "Funcție", "Data angajării", "Salariu bază"]
        self.table_angajati.setRowCount(len(rows))
        self.table_angajati.setColumnCount(len(header))
        self.table_angajati.setHorizontalHeaderLabels(header)

        for r, row in enumerate(rows):
            for c, val in enumerate(row):
                self.table_angajati.setItem(
                    r, c, QTableWidgetItem("" if val is None else str(val))
                )

    def calculeaza_salariu(self):
        idnp = self.calc_idnp.text().strip()
        luna = self.calc_luna.text().strip()
        ore = self.calc_ore.value()

        if not idnp or not luna:
            QMessageBox.warning(self, "Eroare", "IDNP și luna sunt obligatorii.")
            return

        try:
            rows = exec_query(
                "SELECT Salariu_Baza FROM Angajati WHERE IDNP = ?",
                (idnp,),
                fetch=True
            ) or []
        except Exception as e:
            QMessageBox.critical(self, "Eroare SQL", str(e))
            return

        if not rows:
            QMessageBox.warning(self, "Eroare", "Angajatul nu există.")
            return

        salariu_baza = rows[0][0] or 0
        # calcul simplu: salariu_baza / 168 * ore_lucrate
        salariu_calc = round(float(salariu_baza) / 168 * ore, 2)

        id_calc = ("CS" + datetime.now().strftime("%Y%m%d%H%M%S"))[-13:]
        try:
            exec_query(
                """
                INSERT INTO CalculSalarii
                (ID_Calcul, IDNP, Luna, Nr_Ore_Lucrate, Salariu_Calculat)
                VALUES (?,?,?,?,?)
                """,
                (id_calc, idnp, luna, ore, salariu_calc),
                fetch=False
            )
            self.log_actiune("Calcul", f"Salariu calculat pentru {idnp}, {luna}")
        except Exception as e:
            QMessageBox.critical(self, "Eroare SQL", str(e))
            return

        QMessageBox.information(
            self,
            "Salariu calculat",
            f"Salariu calculat pentru {idnp} în {luna}: {salariu_calc:.2f} MDL"
        )

    # ===== TAB PROGRAMARI ============================================
    def build_tab_programari(self):
        layout = QVBoxLayout()
        form = QHBoxLayout()
        left = QVBoxLayout()
        right = QVBoxLayout()

        self.prog_idclient = QLineEdit()
        self.prog_data = QDateEdit()
        self.prog_data.setCalendarPopup(True)
        self.prog_data.setDate(QDate.currentDate())
        self.prog_ora = QLineEdit()
        self.prog_ora.setPlaceholderText("HH:MM")
        self.prog_serviciu = QLineEdit()
        self.prog_resp = QLineEdit()

        def add_row(lbl, w):
            left.addWidget(QLabel(lbl))
            left.addWidget(w)

        add_row("ID client:", self.prog_idclient)
        add_row("Data programării:", self.prog_data)
        add_row("Ora programării:", self.prog_ora)
        add_row("Serviciu:", self.prog_serviciu)
        add_row("Responsabil:", self.prog_resp)

        self.btn_add_programare = QPushButton("Adaugă programare")
        self.btn_add_programare.clicked.connect(self.adauga_programare)

        right.addWidget(self.btn_add_programare)
        right.addStretch()

        form.addLayout(left, 3)
        form.addLayout(right, 1)

        self.table_programari = QTableWidget()
        self.table_programari.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

        layout.addLayout(form)
        layout.addWidget(QLabel("Lista programărilor:"))
        layout.addWidget(self.table_programari)

        self.tab_programari.setLayout(layout)
        self.incarca_programari()

    def adauga_programare(self):
        id_client = self.prog_idclient.text().strip()
        data = self.prog_data.date().toString("yyyy-MM-dd")
        ora = self.prog_ora.text().strip()
        serviciu = self.prog_serviciu.text().strip()
        resp = self.prog_resp.text().strip()

        if not id_client or not ora or not serviciu or not resp:
            QMessageBox.warning(self, "Eroare", "Toate câmpurile sunt obligatorii.")
            return

        id_prog = ("PG" + datetime.now().strftime("%Y%m%d%H%M%S"))[-13:]

        try:
            exec_query(
                """
                INSERT INTO Programari
                (ID_Programare, ID_Client, Data_Programarii, Ora_Programarii, Serviciu, Responsabil)
                VALUES (?,?,?,?,?,?)
                """,
                (id_prog, id_client, data, ora, serviciu, resp),
                fetch=False
            )
            self.log_actiune("Adaugare", f"Programare {id_prog} adăugată")
        except Exception as e:
            QMessageBox.critical(self, "Eroare SQL", str(e))
            return

        QMessageBox.information(self, "OK", "Programare adăugată.")
        self.incarca_programari()

    def incarca_programari(self):
        try:
            rows = exec_query(
                """
                SELECT ID_Programare, ID_Client, Data_Programarii,
                       Ora_Programarii, Serviciu, Responsabil
                FROM Programari
                ORDER BY Data_Programarii DESC
                """,
                fetch=True
            ) or []
        except Exception as e:
            QMessageBox.critical(self, "Eroare SQL", str(e))
            return

        header = ["ID Programare", "ID Client", "Data", "Ora", "Serviciu", "Responsabil"]
        self.table_programari.setRowCount(len(rows))
        self.table_programari.setColumnCount(len(header))
        self.table_programari.setHorizontalHeaderLabels(header)

        for r, row in enumerate(rows):
            for c, val in enumerate(row):
                self.table_programari.setItem(
                    r, c, QTableWidgetItem("" if val is None else str(val))
                )

    # ===== TAB RAPOARTE ==============================================
    def build_tab_rapoarte(self):
        layout = QVBoxLayout()
        top = QHBoxLayout()

        self.rap_tip = QComboBox()
        self.rap_tip.addItems([
            "Venituri/Cheltuieli pe perioadă",
            "Bugete pe centre",
        ])
        self.rap_perioada = QLineEdit()
        self.rap_perioada.setPlaceholderText("ex: 2025-01 sau 2025")

        btn_gen = QPushButton("Generează raport")
        btn_gen.clicked.connect(self.genereaza_raport)

        top.addWidget(QLabel("Tip raport:"))
        top.addWidget(self.rap_tip)
        top.addWidget(QLabel("Perioadă:"))
        top.addWidget(self.rap_perioada)
        top.addWidget(btn_gen)
        top.addStretch()

        self.rap_view = QTextEdit()
        self.rap_view.setReadOnly(True)

        layout.addLayout(top)
        layout.addWidget(self.rap_view)
        self.tab_rapoarte.setLayout(layout)

    def genereaza_raport(self):
        tip = self.rap_tip.currentText()
        perioada = self.rap_perioada.text().strip()

        if "Venituri/Cheltuieli" in tip:
            cond = ""
            params = ()
            if len(perioada) == 4:
                cond = "WHERE YEAR(Data_Operatiune) = ?"
                params = (int(perioada),)
            elif len(perioada) == 7 and "-" in perioada:
                an, luna = perioada.split("-")
                cond = "WHERE YEAR(Data_Operatiune)=? AND MONTH(Data_Operatiune)=?"
                params = (int(an), int(luna))

            query = f"""
                SELECT Tip_Operatiune, SUM(Suma)
                FROM Tranzactii
                {cond}
                GROUP BY Tip_Operatiune
            """
            try:
                rows = exec_query(query, params, fetch=True) or []
            except Exception as e:
                QMessageBox.critical(self, "Eroare SQL", str(e))
                return
            lines = [f"{r[0]}: {r[1]:.2f} MDL" for r in rows]
            if not lines:
                lines = ["Nu există tranzacții pentru perioada selectată."]
            self.rap_view.setPlainText("\n".join(lines))

        elif "Bugete" in tip:
            try:
                rows = exec_query(
                    "SELECT ID_CentruResponsabil, An_Buget, Suma_Alocata, Suma_EfectivaCheltuita, Status_Executie FROM Bugete",
                    fetch=True
                ) or []
            except Exception as e:
                QMessageBox.critical(self, "Eroare SQL", str(e))
                return
            lines = []
            for r in rows:
                lines.append(
                    f"Centru {r[0]} | An {r[1]} | Alocat {r[2]:.2f} | Efectiv {r[3]:.2f} | Status {r[4]}"
                )
            if not lines:
                lines = ["Nu există bugete introduse."]
            self.rap_view.setPlainText("\n".join(lines))

    # ===== TAB AUDIT =================================================
    def build_tab_audit(self):
        layout = QVBoxLayout()
        self.audit_table = QTableWidget()
        self.audit_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

        btn_reload = QPushButton("Reîncarcă jurnal")
        btn_reload.clicked.connect(self.incarca_audit)

        layout.addWidget(btn_reload)
        layout.addWidget(self.audit_table)
        self.tab_audit.setLayout(layout)
        self.incarca_audit()

    def incarca_audit(self):
        try:
            rows = exec_query(
                """
                SELECT TOP 200 ID_Log, ID_Utilizator, Tip_Actiune, Data_Ora, Descriere
                FROM LogAudit
                ORDER BY Data_Ora DESC
                """,
                fetch=True
            ) or []
        except Exception as e:
            QMessageBox.critical(self, "Eroare SQL", str(e))
            return

        header = ["ID Log", "Utilizator", "Acțiune", "Data/Ora", "Descriere"]
        self.audit_table.setRowCount(len(rows))
        self.audit_table.setColumnCount(len(header))
        self.audit_table.setHorizontalHeaderLabels(header)

        for r, row in enumerate(rows):
            for c, val in enumerate(row):
                self.audit_table.setItem(
                    r, c, QTableWidgetItem("" if val is None else str(val))
                )

# ===== FEREASTRA LOGIN ==============================================
class LoginWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Moldelectrica – Login")
        self.setFixedSize(450, 320)
        self.setStyleSheet("background-color: #1e1e1e;")

        card = QWidget()
        card.setStyleSheet("""
            background-color: #ffffff;
            border-radius: 15px;
        """)
        card_layout = QVBoxLayout()
        card.setLayout(card_layout)

        title = QLabel("⚡ Moldelectrica Login")
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet("""
            color: #e63946;
            font-size: 22px;
            font-weight: bold;
            margin-bottom: 15px;
        """)

        lbl_user = QLabel("Username:")
        lbl_user.setStyleSheet("color: #333;")
        self.ed_login = QLineEdit()
        self.ed_login.setStyleSheet("""
            border: 2px solid #e63946;
            padding: 6px;
            border-radius: 8px;
        """)

        lbl_pass = QLabel("Password:")
        lbl_pass.setStyleSheet("color: #333;")
        self.ed_pass = QLineEdit()
        self.ed_pass.setEchoMode(QLineEdit.Password)
        self.ed_pass.setStyleSheet("""
            border: 2px solid #e63946;
            padding: 6px;
            border-radius: 8px;
        """)

        btn = QPushButton("LOGIN")
        btn.setStyleSheet("""
            background-color: #e63946;
            padding: 10px;
            border-radius: 8px;
            font-size: 15px;
            font-weight: bold;
        """)
        btn.clicked.connect(self.do_login)

        card_layout.addWidget(title)
        card_layout.addWidget(lbl_user)
        card_layout.addWidget(self.ed_login)
        card_layout.addWidget(lbl_pass)
        card_layout.addWidget(self.ed_pass)
        card_layout.addWidget(btn)
        card_layout.addStretch()

        main_layout = QVBoxLayout()
        main_layout.addStretch()
        main_layout.addWidget(card)
        main_layout.addStretch()
        self.setLayout(main_layout)

    def do_login(self):
        login = self.ed_login.text().strip()
        pw = self.ed_pass.text().strip()

        if not login or not pw:
            QMessageBox.warning(self, "Eroare", "Completează login și parola.")
            return

        try:
            rows = exec_query(
                """
                SELECT ID_Utilizator, Login, Tip_Cont
                FROM Utilizatori
                WHERE Login = ? AND Parola = ?
                """,
                (login, pw),
                fetch=True
            ) or []
        except Exception as e:
            QMessageBox.critical(self, "Eroare SQL", str(e))
            return

        if not rows:
            QMessageBox.warning(self, "Eroare", "Login sau parolă incorectă.")
            return

        r = rows[0]
        user_info = {
            "id": r[0],
            "login": r[1],
            "tip_cont": r[2],
        }

        # logam login-ul
        id_log = ("LG" + datetime.now().strftime("%Y%m%d%H%M%S"))[-13:]
        try:
            exec_query(
                """
                INSERT INTO LogAudit
                (ID_Log, ID_Utilizator, Tip_Actiune, Data_Ora, Descriere)
                VALUES (?,?,?,?,?)
                """,
                (id_log, user_info["id"], "Login", datetime.now(), "Autentificare reușită"),
                fetch=False
            )
        except Exception:
            pass

        self.main = MoldelectricaApp(user_info)
        self.main.show()
        self.close()

# ===== MAIN =========================================================
def main():
    app = QApplication(sys.argv)
    app.setFont(QFont("Segoe UI", 10))
    win = LoginWindow()
    win.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
