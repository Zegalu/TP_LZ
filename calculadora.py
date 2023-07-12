from PyQt6.QtWidgets import (QApplication, QWidget, QLabel, QPushButton, QDateEdit, QFileDialog,
                             QLineEdit, QComboBox, QFormLayout, QHBoxLayout, QMessageBox)
from PyQt6.QtGui import QFont
from PyQt6.QtCore import Qt, QDate, QStandardPaths
import sys


class Calculadora(QWidget):

    def __init__(self, tabla):
        super().__init__()
        self.lista_a_guardar = None
        self.file = None
        self.valor_entrada = None
        self.mes_entrada = None
        self.anio_entrada = None
        self.mes_salida = None
        self.anio_salida = None
        self.tabla_ipc = tabla
        self.lista_mes = ["01", "02", "03", "04", "05", "06", "07", "08", "09", "10", "11", "12"]
        self.lista_anio = [x[0] for x in self.tabla_ipc]
        self.inicializar_ui()

    def inicializar_ui(self):
        self.setGeometry(400, 400, 350, 200)
        self.setWindowTitle("Calculadora")
        self.crear_formulario()

    def crear_formulario(self):
        titulo = QLabel("Calculadora de valores por inflación:")
        titulo.setFont(QFont("Helvetica", 14))
        titulo.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.valor_entrada = QLineEdit()

        self.mes_entrada = QComboBox()
        self.mes_entrada.addItems(self.lista_mes)
        self.anio_entrada = QComboBox()
        self.anio_entrada.addItems(self.lista_anio)

        self.mes_salida = QComboBox()
        self.mes_salida.addItems(self.lista_mes)
        self.anio_salida = QComboBox()
        self.anio_salida.addItems(self.lista_anio)

        boton_calcular = QPushButton("Calcular")
        boton_calcular.clicked.connect(self.calcular_inflacion)
        boton_calcular.setFixedHeight(40)

        boton_exportar = QPushButton("Exportar periodo")
        boton_exportar.clicked.connect(self.exportar_periodo)
        boton_exportar.setFixedHeight(40)

        caja_fecha_entrada = QHBoxLayout()
        caja_fecha_entrada.addWidget(self.mes_entrada)
        caja_fecha_entrada.addWidget(self.anio_entrada)

        caja_fecha_salida = QHBoxLayout()
        caja_fecha_salida.addWidget(self.mes_salida)
        caja_fecha_salida.addWidget(self.anio_salida)

        caja_principal = QFormLayout()
        caja_principal.addRow(titulo)
        caja_principal.addRow("Valor inicial:  $", self.valor_entrada)
        caja_principal.addRow("Fecha inicial:  ", caja_fecha_entrada)
        caja_principal.addRow("Fecha final:  ", caja_fecha_salida)
        caja_principal.addRow(boton_calcular)
        caja_principal.addRow(boton_exportar)
        caja_principal.setSpacing(15)

        self.setLayout(caja_principal)

    def calcular_inflacion(self):
        try:
            valor_entrada = float(self.valor_entrada.text())
            anio_entrada = self.lista_anio.index(self.anio_entrada.currentText())
            mes_entrada = int(self.mes_entrada.currentText())

            anio_salida = self.lista_anio.index(self.anio_salida.currentText())
            mes_salida = int(self.mes_salida.currentText())

            lista_periodo = []
            inflacion_total = 1

            if anio_entrada == anio_salida:
                if mes_entrada != mes_salida:
                    if mes_entrada < mes_salida:
                        for i in range(mes_entrada, mes_salida):
                            inflacion_total *= (float(self.tabla_ipc[anio_entrada][i].replace(',', '.')) / 100 + 1)
                    else:
                        for i in range(mes_salida, mes_entrada):
                            inflacion_total *= (float(self.tabla_ipc[anio_entrada][i].replace(',', '.')) / 100 + 1)
                        inflacion_total = 1 / inflacion_total

            else:
                if anio_entrada < anio_salida:
                    a, b = anio_entrada, anio_salida
                else:
                    a, b = anio_salida, anio_entrada

                for i in range(a, b + 1):
                    if i == a:
                        lista_periodo.extend(self.tabla_ipc[i][mes_entrada:])
                    elif i != b:
                        lista_periodo.extend(self.tabla_ipc[i][1:])
                    else:
                        lista_periodo.extend(self.tabla_ipc[i][1:mes_salida])

                for i in lista_periodo:
                    inflacion_total *= (float(i.replace(',', '.')) / 100 + 1)

                if anio_entrada > anio_salida:
                    inflacion_total = 1 / inflacion_total

            resultado = valor_entrada * inflacion_total

            QMessageBox.information(self, "Resultado",
                                    f"El valor ${valor_entrada} a la fecha {mes_entrada:02}/"
                                    f"{self.lista_anio[anio_entrada]}\nserian ${resultado:.2f} en la fecha "
                                    f"{mes_salida:02}/{self.lista_anio[anio_salida]}",
                                    QMessageBox.StandardButton.Ok, QMessageBox.StandardButton.Ok)
        except ValueError:
            QMessageBox.information(self, "Error",
                                    "Error. No se ingreso ningún valor,\no se ingreso un dato no valido.",
                                    QMessageBox.StandardButton.Ok, QMessageBox.StandardButton.Ok)

    def exportar_periodo(self):

        anio_entrada = self.lista_anio.index(self.anio_entrada.currentText())
        mes_entrada = int(self.mes_entrada.currentText())

        anio_salida = self.lista_anio.index(self.anio_salida.currentText())
        mes_salida = int(self.mes_salida.currentText())

        lista_a_exportar = []

        if anio_entrada == anio_salida:
            if mes_entrada != mes_salida:
                if mes_entrada < mes_salida:
                    a, b = mes_entrada, mes_salida
                else:
                    a, b = mes_salida, mes_entrada
                for i in range(a, b+1):
                    lista_a_exportar.append([f"{self.lista_anio[anio_entrada]}",
                                             f"{i: 02}",
                                             self.tabla_ipc[anio_entrada][i]])
            else:
                lista_a_exportar.append([f"{self.lista_anio[anio_entrada]}",
                                         f"{mes_entrada:02}",
                                         self.tabla_ipc[anio_entrada][mes_entrada]])

        else:
            if anio_entrada < anio_salida:
                a, b = anio_entrada, anio_salida
            else:
                a, b = anio_salida, anio_entrada

            for i in range(a, b + 1):
                if i == a:
                    for m in range(mes_entrada, len(self.lista_anio[i])+1):
                        lista_a_exportar.append([f"{self.lista_anio[i]}",
                                                 f"{m:02}",
                                                 self.tabla_ipc[i][m]])
                elif i != b:
                    for m in range(1, 13):
                        lista_a_exportar.append([f"{self.lista_anio[i]}",
                                                 f"{m:02}",
                                                 self.tabla_ipc[i][m]])
                else:
                    """lista_periodo.extend(self.tabla_ipc[i][1:mes_salida])"""
                    for m in range(1, mes_salida+1):
                        lista_a_exportar.append([f"{self.lista_anio[i]}",
                                                 f"{m:02}",
                                                 self.tabla_ipc[i][m]])

        self.lista_a_guardar = lista_a_exportar[:]
        self.lista_a_guardar.sort(key=lambda x: x[0]+x[1])

        self.guardar_archivo()

    def guardar_archivo(self):
        carpeta_inicial = QStandardPaths.writableLocation(QStandardPaths.StandardLocation.DocumentsLocation)
        tipos_archivo = "Csv Files (*.csv);;Text Files (*.txt);;All Files (*)"
        self.file, _ = QFileDialog.getSaveFileName(self, "Guardar Archivo", carpeta_inicial, tipos_archivo)

        try:
            with open(self.file, "w") as archivo:
                registro = ""
                for fila in self.lista_a_guardar:
                    registro += f"{fila[0]};{fila[1]};{fila[2]}\n"
                archivo.write(registro)

            QMessageBox.information(self, "Exportación completa",
                                    f"Se ha exportado el IPC de los periodos,\ndesde la fecha"
                                    f" {mes_entrada:02}/{self.lista_anio[anio_entrada]}\nhasta la fecha "
                                    f" {mes_salida:02}/{self.lista_anio[anio_salida]}",
                                    QMessageBox.StandardButton.Ok, QMessageBox.StandardButton.Ok)
        except OSError:
            QMessageBox.information(self, "Error al guardar",
                                    "<Error al guardar el archivo.\nSe cancelo la guardar del archivo.>",
                                    QMessageBox.StandardButton.Ok, QMessageBox.StandardButton.Ok)
