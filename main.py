import csv
import sys

from PyQt6.QtCore import Qt, QStandardPaths
from PyQt6.QtGui import QFont
from PyQt6.QtWidgets import (QApplication, QWidget, QLabel, QVBoxLayout, QPushButton, QFileDialog, QMessageBox,
                             QTextEdit, QComboBox, QLineEdit, QHBoxLayout, QFormLayout)
from prettytable import PrettyTable

from calculadora import Calculadora


class VentanaPrincipal(QWidget):
    def __init__(self):
        # ATRIBUTOS
        self.ventana_secundaria = None
        self.ventana_calculadora = None
        self.ventana_actualizar = None
        self.tabla_a_mostrar = None
        self.file = None
        self.titulo_tabla = ['Año', 'Enero', 'Febrero', 'Marzo', 'Abril', 'Mayo', 'Junio',
                             'Julio', 'Agosto', 'Septiembre', 'Octubre', 'Noviembre', 'Diciembre']
        self.tabla_ipc = []

        super().__init__()
        self.generar_formulario()

    # METODOS
    def generar_formulario(self):
        self.setGeometry(700, 300, 360, 250)
        self.setWindowTitle("TP - Luis Zegarra")
        self.generar_menu()
        self.show()

    def generar_menu(self):
        fuente = "Helvetica"
        titulo = QLabel("CALCULADORA DE LA INFLACIÓN")
        titulo.setFont(QFont(fuente, 12))
        titulo.setAlignment(Qt.AlignmentFlag.AlignCenter)

        subtitulo = QLabel("Por favor, seleccione una de las siguientes opciones:")
        subtitulo.setFont(QFont(fuente, 11))

        titulo_menu = QLabel("MENU PRINCIPAL:")
        titulo_menu.setFont(QFont(fuente, 11))
        titulo_menu.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # BOTONES DEL MENU
        boton_calculadora = QPushButton("Ir a la calculadora de valores")
        boton_calculadora.clicked.connect(self.mostrar_calculadora)
        boton_calculadora.setFixedHeight(40)

        boton_cargar = QPushButton("Cargar tabla del IPC")
        boton_cargar.clicked.connect(self.cargar_tabla)
        boton_cargar.setFixedHeight(40)

        boton_mostrar_tabla = QPushButton("Mostrar tabla del IPC")
        boton_mostrar_tabla.clicked.connect(self.abrir_ventana_mostrar)
        boton_mostrar_tabla.setFixedHeight(40)

        boton_actualizar = QPushButton("Actualizar periodos del IPC")
        boton_actualizar.clicked.connect(self.actualizar_tabla)
        boton_actualizar.setFixedHeight(40)

        boton_salir = QPushButton("Salir del programa")
        boton_salir.clicked.connect(self.salir)
        boton_salir.setFixedHeight(40)

        # ARMADO DEL MENU
        cuerpo_menu = QVBoxLayout()
        cuerpo_menu.addWidget(titulo)
        cuerpo_menu.addWidget(subtitulo)
        cuerpo_menu.addWidget(titulo_menu)

        cuerpo_menu.addWidget(boton_calculadora)
        cuerpo_menu.addWidget(boton_cargar)
        cuerpo_menu.addWidget(boton_mostrar_tabla)
        cuerpo_menu.addWidget(boton_actualizar)
        cuerpo_menu.addWidget(boton_salir)

        cuerpo_menu.setSpacing(15)

        self.setLayout(cuerpo_menu)

    def abrir_ventana_mostrar(self):
        self.tabla_a_mostrar = self.mostrar_tabla()
        self.ventana_secundaria = VentanaSecundaria(self.tabla_a_mostrar)
        if self.tabla_a_mostrar:
            self.ventana_secundaria.show()

    def mostrar_calculadora(self):
        self.ventana_calculadora = Calculadora(self.tabla_ipc)
        if self.tabla_ipc:
            self.ventana_calculadora.show()
        else:
            QMessageBox.information(self, "Tabla Vacia",
                                    "<No hay una tabla cargada.\nNo se puede usar el programa.>",
                                    QMessageBox.StandardButton.Ok, QMessageBox.StandardButton.Ok)

    def cargar_tabla(self):
        carpeta_inicial = QStandardPaths.writableLocation(QStandardPaths.StandardLocation.DocumentsLocation)
        tipos_archivo = "Csv Files (*.csv);;Text Files (*.txt);;All Files (*)"

        self.file, _ = QFileDialog.getOpenFileName(self, "Abrir Archivo", carpeta_inicial, tipos_archivo, )
        try:
            with open(self.file, "r") as archivo:
                tabla_csv = csv.reader(archivo, delimiter=',', quotechar='"')
                self.tabla_ipc = []
                for fila in tabla_csv:
                    self.tabla_ipc.append(fila)
        except OSError:
            QMessageBox.information(self, "Error de carga",
                                    "<Error al cargar el archivo.\nSe cancelo la cargar del archivo.>",
                                    QMessageBox.StandardButton.Ok, QMessageBox.StandardButton.Ok)

    def mostrar_tabla(self):
        tabla = PrettyTable()
        tabla.field_names = self.titulo_tabla
        try:
            for fila in self.tabla_ipc:
                tabla.add_row(fila)
            return str(tabla)

        except ValueError:
            QMessageBox.information(self, "Error al cargar tabla",
                                    "<Error al cargar la tabla.\nArchivo no compatible a la tabla.>",
                                    QMessageBox.StandardButton.Ok, QMessageBox.StandardButton.Ok)

    def actualizar_tabla(self):
        self.ventana_actualizar = Actualizador(self.tabla_ipc)
        self.ventana_actualizar.show()

    def salir(self):
        self.close()


class Actualizador(QWidget):

    def __init__(self, tabla):
        self.file = None
        self.valor_entrada = None
        self.anio_entrada = None
        self.mes_entrada = None
        self.lista_mes = ["01", "02", "03", "04", "05", "06", "07", "08", "09", "10", "11", "12"]
        self.lista_anio = ['1970', '1971', '1972', '1973', '1974', '1975', '1976', '1977', '1978', '1979', '1980',
                           '1981', '1982', '1983', '1984', '1985', '1986', '1987', '1988', '1989', '1990', '1991',
                           '1992', '1993', '1994', '1995', '1996', '1997', '1998', '1999', '2000', '2001', '2002',
                           '2003', '2004', '2005', '2006', '2007', '2008', '2009', '2010', '2011', '2012', '2013',
                           '2014', '2015', '2016', '2017', '2018', '2019', '2020', '2021', '2022', '2023']
        self.tabla_ipc = tabla
        self.lista_anio_ipc = [x[0] for x in self.tabla_ipc]
        super().__init__()
        self.iniciar_ui()

    def iniciar_ui(self):
        self.setWindowTitle("Actualizar IPC")
        self.setGeometry(400, 400, 350, 200)
        self.crear_formulario()

    def crear_formulario(self):
        titulo = QLabel("Actualizar o Guardar IPC:")
        titulo.setFont(QFont("Arial", 14))
        titulo.setAlignment(Qt.AlignmentFlag.AlignCenter)

        intro = QLabel("Ingrese la fecha que quiere actualizar:")
        self.mes_entrada = QComboBox()
        self.mes_entrada.addItems(self.lista_mes)
        self.anio_entrada = QComboBox()
        self.anio_entrada.addItems(self.lista_anio)
        self.valor_entrada = QLineEdit()

        caja_fecha_entrada = QHBoxLayout()
        caja_fecha_entrada.addWidget(self.mes_entrada)
        caja_fecha_entrada.addWidget(self.anio_entrada)

        boton_actualizar = QPushButton("Actualizar mes")
        boton_actualizar.clicked.connect(self.actualizar_archivo)
        boton_actualizar.setFixedHeight(40)

        boton_guardar = QPushButton("Guardar Tabla")
        boton_guardar.clicked.connect(self.guardar_archivo)
        boton_guardar.setFixedHeight(40)

        caja_principal = QFormLayout()
        caja_principal.addRow(titulo)
        caja_principal.addRow(intro)
        caja_principal.addRow(caja_fecha_entrada)
        caja_principal.addRow("Ingrese el valor a actualizar:", self.valor_entrada)
        caja_principal.addRow(boton_actualizar)
        caja_principal.addRow(boton_guardar)
        caja_principal.setSpacing(15)

        self.setLayout(caja_principal)

    def actualizar_archivo(self):
        try:
            entrada = float(self.valor_entrada.text())
            anio_entrada = self.anio_entrada.currentText()
            mes_entrada = int(self.mes_entrada.currentText())
            try:
                ind = self.lista_anio_ipc.index(anio_entrada)
                self.tabla_ipc[ind][mes_entrada] = str(entrada)
                QMessageBox.information(self, "Actualización completa",
                                        f"Se ha actualizo exitosamente el IPC de la fecha"
                                        f" {mes_entrada:02}/{anio_entrada} a:\n {entrada}",
                                        QMessageBox.StandardButton.Ok, QMessageBox.StandardButton.Ok)

            except ValueError:
                self.tabla_ipc.append([anio_entrada, "", "", "", "", "", "", "", "", "", "", "", ""])
                self.tabla_ipc[-1][mes_entrada] = str(entrada)
                self.tabla_ipc.sort()
                self.lista_anio_ipc.append(anio_entrada)
                self.lista_anio_ipc.sort()

                QMessageBox.information(self, "Actualización completa",
                                        f"Se ha actualizo exitosamente el IPC de la fecha"
                                        f" {mes_entrada:02}/{anio_entrada} a:\n {entrada}",
                                        QMessageBox.StandardButton.Ok, QMessageBox.StandardButton.Ok)
        except ValueError:
            QMessageBox.information(self, "Error",
                                    "Error. No se ingreso ningún valor,\no se ingreso un dato no valido.",
                                    QMessageBox.StandardButton.Ok, QMessageBox.StandardButton.Ok)

    def guardar_archivo(self):
        carpeta_inicial = QStandardPaths.writableLocation(QStandardPaths.StandardLocation.DocumentsLocation)
        tipos_archivo = "Csv Files (*.csv);;Text Files (*.txt);;All Files (*)"
        self.file, _ = QFileDialog.getSaveFileName(self, "Guardar Archivo", carpeta_inicial, tipos_archivo)

        try:
            with open(self.file, "w") as archivo:
                registro = ""
                for fila in self.tabla_ipc:
                    for i in range(len(fila)):
                        registro += f"'{fila[i]}';"
                    registro = registro[:-1]
                    registro += "\n"
                archivo.write(registro)
        except OSError:
            QMessageBox.information(self, "Error al guardar",
                                    "<Error al guardar el archivo.\nSe cancelo la guardar del archivo.>",
                                    QMessageBox.StandardButton.Ok, QMessageBox.StandardButton.Ok)


class VentanaSecundaria(QWidget):

    def __init__(self, tabla):
        self.tabla_a_mostrar = tabla
        super().__init__()
        self.iniciar_ui()

    def iniciar_ui(self):
        self.setWindowTitle("Tabla del IPC")
        self.setGeometry(400, 400, 1130, 400)

        titulo = QLabel("Tabla del IPC mensual:")
        titulo.setFont(QFont("Arial", 14))
        titulo.setAlignment(Qt.AlignmentFlag.AlignCenter)

        pantalla = QTextEdit()
        pantalla.setFont(QFont("Lucida Console", 11))
        pantalla.setText(self.tabla_a_mostrar)

        boton_cerrar = QPushButton('Cerrar', self)
        boton_cerrar.setFixedHeight(40)
        boton_cerrar.clicked.connect(self.cerrar)

        cuerpo_vista = QVBoxLayout()
        cuerpo_vista.addWidget(titulo)
        cuerpo_vista.addWidget(pantalla)
        cuerpo_vista.addWidget(boton_cerrar)

        self.setLayout(cuerpo_vista)

    def cerrar(self):
        self.close()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ventana_principal = VentanaPrincipal()
    ventana_principal.show()
    sys.exit(app.exec())
