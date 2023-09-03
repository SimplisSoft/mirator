import sys
import os
import subprocess  # Import subprocess module
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import Qt, QUrl, QTimer
from PyQt5.QtMultimedia import QMediaPlayer, QMediaContent
from tinytag import TinyTag


import pytube

font_style = ("Arial", 14)

# Ventana para agregar canción de YouTube
class VentanaYouTube(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Agregar Canción de YouTube")
        self.setGeometry(300, 300, 400, 100)

        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        self.label = QLabel("Introduce la URL de YouTube:")
        self.layout.addWidget(self.label)

        self.url_input = QLineEdit()
        self.layout.addWidget(self.url_input)

        self.agregar_button = QPushButton("Agregar")
        self.agregar_button.clicked.connect(self.agregar_cancion_youtube)
        self.layout.addWidget(self.agregar_button)

    # Agregar canción de YouTube a la playlist
    def agregar_cancion_youtube(self):
        url = self.url_input.text()
        if url:
            self.parent().agregar_cancion_de_youtube(url)
            self.accept()


# Ventana principal
class ReproductorDeMusica(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("MIRATOR")
        self.setWindowIcon(QIcon("iconos/icon.png"))
        self.setGeometry(200, 200, 400, 300)
        self.player = QMediaPlayer()

        # Lista de reproducción
        self.lista_reproduccion = []

        # Reproducción aleatoria
        self.reproduccion_aleatoria = False

        # Variable para el tema oscuro
        self.tema_oscuro = False

        # Widget central
        self.widget_central = QWidget(self)
        self.setCentralWidget(self.widget_central)

        # Diseño principal
        self.layout_principal = QVBoxLayout()
        self.widget_central.setLayout(self.layout_principal)

        # Lista de reproducción
        self.lista_widget = QListWidget()
        self.lista_widget.itemDoubleClicked.connect(self.reproducir_cancion_seleccionada)
        self.layout_principal.addWidget(self.lista_widget)
        self.lista_widget.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)  # Mostrar el scrollbar vertical si es necesario
        self.lista_widget.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)  # Ocultar el scrollbar horizontal


        # Botones de control
        self.layout_botones = QHBoxLayout()
        self.barra_progreso = QSlider(Qt.Horizontal)
        self.barra_progreso.setMinimum(0)
        self.barra_progreso.setMaximum(100)
        self.layout_principal.addWidget(self.barra_progreso)
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.actualizar_posicion_barra_progreso)
        self.timer.start(1000)  # Actualizar cada segundo

        # Crear el botón con el ícono y el texto
        btn_agregar_canciones = QPushButton(QIcon('iconos/exp.png'), "AÑADIR CANCIÓN")
        btn_agregar_canciones.clicked.connect(self.agregar_canciones)
        self.layout_principal.addWidget(btn_agregar_canciones)



        btn_retroceder = QPushButton(QIcon("iconos/icons8-saltar-a-inicio-96.png"), "")
        btn_retroceder.clicked.connect(self.retroceder_cancion)
        self.layout_botones.addWidget(btn_retroceder)

        btn_pausar = QPushButton(QIcon("iconos/icons8-pausa-96.png"), "")
        btn_pausar.clicked.connect(self.pausar)
        self.layout_botones.addWidget(btn_pausar)

        btn_reproducir = QPushButton(QIcon("iconos/icons8-play-96.png"), "")
        btn_reproducir.clicked.connect(self.reproducir)
        self.layout_botones.addWidget(btn_reproducir)

        btn_detener = QPushButton(QIcon("iconos/icons8-detener-96.png"), "")
        btn_detener.clicked.connect(self.detener)
        self.layout_botones.addWidget(btn_detener)

        btn_siguiente = QPushButton(QIcon("iconos/icons8-fin-96.png"), "")
        btn_siguiente.clicked.connect(self.siguiente_cancion)
        self.layout_botones.addWidget(btn_siguiente)

        self.layout_principal.addLayout(self.layout_botones)

        # Etiqueta de información de la canción
        self.etiqueta_cancion = QLabel()
        self.layout_principal.addWidget(self.etiqueta_cancion)

        # Conectar señales de reproducción del reproductor
        self.player.mediaStatusChanged.connect(self.media_status_changed)
        self.player.stateChanged.connect(self.player_state_changed)

        # Estilo inicial
        self.aplicar_estilo()


        # Menú
        self.barra_menu = self.menuBar()

        menu_archivo = self.barra_menu.addMenu("Archivo")
        menu_ver = self.barra_menu.addMenu("Ver")
        menu_ayuda = self.barra_menu.addMenu("Ayuda")

        # Mover el menú a la barra de título
        self.setMenuBar(self.barra_menu)

        # Acciones del menú Archivo
        accion_agregar_canciones = QAction("Agregar canciones", self)
        accion_agregar_canciones.triggered.connect(self.agregar_canciones)
        menu_archivo.addAction(accion_agregar_canciones)

        # Acción del menú Ver para agregar canciones de YouTube
        accion_agregar_youtube = QAction("Agregar canción de YouTube", self)
        accion_agregar_youtube.triggered.connect(self.abrir_ventana_youtube)
        menu_ver.addAction(accion_agregar_youtube)


        # Acciones del menú Ver
        accion_tema_oscuro = QAction("Tema Oscuro", self)
        accion_tema_oscuro.setCheckable(True)
        accion_tema_oscuro.triggered.connect(self.cambiar_tema_oscuro)
        menu_ver.addAction(accion_tema_oscuro)

        accion_transparencia = QAction("Transparencia", self)
        accion_transparencia.setCheckable(True)
        accion_transparencia.triggered.connect(self.activar_transparencia)
        menu_ver.addAction(accion_transparencia)

        accion_reproduccion_aleatoria = QAction("Reproducción Aleatoria", self)
        accion_reproduccion_aleatoria.setCheckable(True)
        accion_reproduccion_aleatoria.setChecked(self.reproduccion_aleatoria)
        accion_reproduccion_aleatoria.triggered.connect(self.toggle_reproduccion_aleatoria)
        menu_ver.addAction(accion_reproduccion_aleatoria)


        # Acciones del menú Ayuda
        accion_informacion_canciones = QAction("Información sobre la canción", self)
        accion_informacion_canciones.triggered.connect(self.mostrar_informacion_canciones)
        menu_ayuda.addAction(accion_informacion_canciones)

        accion_informacion_creador = QAction("Sobre la Versión", self)
        accion_informacion_creador.triggered.connect(self.mostrar_informacion_creador)
        menu_ayuda.addAction(accion_informacion_creador)

        # Aplicar estilo inicial
        self.aplicar_estilo()

    # Obtener la lista de canciones en un directorio específico
    def obtener_canciones(self):
        canciones, _ = QFileDialog.getOpenFileNames(self, "Agregar canciones", "", "Archivos de música (*.mp3)")
        return canciones

    def actualizar_posicion_barra_progreso(self):
        # Obtener la posición actual en segundos
        posicion_actual = self.player.position() // 1000
        self.barra_progreso.setValue(posicion_actual)

    # Reproducir una canción
    def reproducir_cancion(self, cancion):
        self.player.setMedia(QMediaContent(QUrl.fromLocalFile(cancion)))
        self.player.play()

    # Pausar la reproducción
    def pausar_reproduccion(self):
        self.player.pause()

    def reproducir(self):
        self.player.play()  # Reanudar la reproducción

    # Reanudar la reproducción
    def reanudar_reproduccion(self):
        self.player.play()

    def detener(self):
        self.player.stop()  # Detener la reproducción

    # Detener la reproducción
    def detener_reproduccion(self):
        self.player.stop()

    def pausar(self):
        self.player.pause()  # Pausar la reproducción

    # Agregar canciones a la lista de reproducción
    def agregar_canciones(self):
        canciones = self.obtener_canciones()
        if canciones:
            self.lista_reproduccion.extend(canciones)
            self.actualizar_lista_reproduccion()



    # Actualizar la lista de reproducción en el widget
    def actualizar_lista_reproduccion(self):
        self.lista_widget.clear()
        for cancion in self.lista_reproduccion:
            self.lista_widget.addItem(os.path.splitext(os.path.basename(cancion))[0])

    # Reproducir la canción seleccionada
    def reproducir_cancion_seleccionada(self, item):
        index = self.lista_widget.row(item)
        if index >= 0:
            cancion_seleccionada = self.lista_reproduccion[index]
            self.reproducir_cancion(cancion_seleccionada)
            self.etiqueta_cancion.setText(os.path.basename(cancion_seleccionada))
            self.setWindowTitle(f"{os.path.basename(cancion_seleccionada)}")
            self.barra_progreso.setValue(0)
            tag = TinyTag.get(cancion_seleccionada)
            self.barra_progreso.setMaximum(int(tag.duration))

    # Retroceder a la canción anterior
    def retroceder_cancion(self):
        if self.lista_reproduccion:
            self.player.stop()
            index_actual = self.lista_widget.currentRow()
            if index_actual == 0:
                cancion_anterior = self.lista_reproduccion[-1]
            else:
                cancion_anterior = self.lista_reproduccion[index_actual - 1]
            self.lista_widget.setCurrentRow(self.lista_reproduccion.index(cancion_anterior))
            self.reproducir_cancion(cancion_anterior)
            self.etiqueta_cancion.setText(os.path.basename(cancion_anterior))
            self.setWindowTitle(f" {os.path.basename(cancion_anterior)}")

    # Reproducir la siguiente canción
    def siguiente_cancion(self):
        if self.lista_reproduccion:
            self.player.stop()
            index_actual = self.lista_widget.currentRow()
            if index_actual == len(self.lista_reproduccion) - 1:
                cancion_siguiente = self.lista_reproduccion[0]
            else:
                cancion_siguiente = self.lista_reproduccion[index_actual + 1]
            self.lista_widget.setCurrentRow(self.lista_reproduccion.index(cancion_siguiente))
            self.reproducir_cancion(cancion_siguiente)
            self.etiqueta_cancion.setText(os.path.basename(cancion_siguiente))
            self.setWindowTitle(f" {os.path.basename(cancion_siguiente)}")

    # Cambiar al tema oscuro
    def cambiar_tema_oscuro(self):
        self.tema_oscuro = self.sender().isChecked()
        self.aplicar_estilo()

    # Activar transparencia
    def activar_transparencia(self):
        if self.sender().isChecked():
            self.setWindowOpacity(0.8)
        else:
            self.setWindowOpacity(1.0)

    # Alternar reproducción aleatoria
    def toggle_reproduccion_aleatoria(self):
        self.reproduccion_aleatoria = not self.reproduccion_aleatoria

    # Mostrar información de las canciones
    def mostrar_informacion_canciones(self):
        index = self.lista_widget.currentRow()
        if index >= 0:
            cancion_seleccionada = self.lista_reproduccion[index]
            self.mostrar_informacion_cancion(cancion_seleccionada)

    def mostrar_informacion_creador(self):
        mensaje = (
            "MIRATOR - Reproductor de Música<br>"
            "Versión: 1.0<br>"
            "Desarrollado por: SimplisSoft<br>"
            "Año: 2023<br>"
            "Derechos de Autor © 2023<br><br>"
            "MIRATOR es un reproductor de música simple y elegante que te permite reproducir "
            "tus canciones favoritas. Ofrece características como agregar canciones de YouTube, "
            "lista de reproducción, control de reproducción y más. Este proyecto fue desarrollado "
            "como parte de un proyecto de desarrollo de software.<br><br>"
            "Página web: <a href='https://simplissoft.github.io/'>SimplisSoft</a><br>"
            "Correo electrónico: carlosavelinocorrea@gmail.com<br><br>"
            "<a href='https://www.facebook.com/'><img src='iconos/facebook.png'></a>"
            "<a href='https://www.twitter.com/'><img src='iconos/twitter.png'></a>"
            "<a href='https://www.instagram.com/'><img src='iconos/instagram.png'></a>"
            "<a href='https://www.instagram.com/'><img src='iconos/github.png'></a>"
        )
        ventana_emergente = QMessageBox()
        ventana_emergente.setWindowTitle("Sobre MIRATOR")
        ventana_emergente.setTextFormat(Qt.RichText)
        ventana_emergente.setText(mensaje)
        ventana_emergente.setIcon(QMessageBox.Information)

        if self.tema_oscuro:
            qss_file = 'sobre\messagebox_styles_dark.qss'
        else:
            qss_file = 'sobre\messagebox_styles_light.qss'

        with open(qss_file, 'r') as f:
            styles = f.read()
            ventana_emergente.setStyleSheet(styles)

        ventana_emergente.exec_()

    # Mostrar información detallada de la canción
    def mostrar_informacion_cancion(self, ruta_cancion):
        tag = TinyTag.get(ruta_cancion)
        titulo = tag.title
        artista = tag.artist
        album = tag.album
        genero = tag.genre
        year = tag.year
        duracion = self.obtener_duracion_cancion(ruta_cancion)

        mensaje = f"Información de la canción:\n\n"
        mensaje += f"Título: {titulo}\n"
        mensaje += f"Artista: {artista}\n"
        mensaje += f"Álbum: {album}\n"
        mensaje += f"Género: {genero}\n"
        mensaje += f"Año: {year}\n"
        mensaje += f"Duración: {duracion}\n"

        ventana_emergente = QMessageBox()
        ventana_emergente.setWindowTitle("Información de la Canción")
        ventana_emergente.setText(mensaje)
        ventana_emergente.setIcon(QMessageBox.Information)
        ventana_emergente.exec_()

    # Obtener la duración de la canción en formato de tiempo (minutos:segundos)
    def obtener_duracion_cancion(self, ruta_cancion):
        tag = TinyTag.get(ruta_cancion)
        duracion = int(tag.duration)
        minutos = duracion // 60
        segundos = duracion % 60
        return f"{minutos}:{segundos:02d}"

    # Actualizar la etiqueta de la canción en la barra de estado
    def actualizar_etiqueta_cancion(self, cancion):
        self.etiqueta_cancion.setText(cancion)
        self.setWindowTitle(cancion)

    # Manejar los cambios de estado de reproducción del reproductor
    def media_status_changed(self, status):
        if status == QMediaPlayer.EndOfMedia:
            self.siguiente_cancion()

    # Manejar los cambios de estado del reproductor
    def player_state_changed(self, state):
        if state == QMediaPlayer.PlayingState:
            self.barra_progreso.setEnabled(True)
        elif state == QMediaPlayer.PausedState:
            self.barra_progreso.setEnabled(True)
        elif state == QMediaPlayer.StoppedState:
            self.barra_progreso.setEnabled(False)
            self.barra_progreso.setValue(0)

    def aplicar_estilo(self):
            estilo = QStyleFactory.create('Fusion')
            paleta = estilo.standardPalette()

            if self.tema_oscuro:
                with open('styles_dark.qss', 'r') as f:
                    styles = f.read()
            else:
                with open('styles_light.qss', 'r') as f:
                    styles = f.read()
            self.setStyleSheet(styles)


    # Abrir ventana para agregar canción de YouTube
    def abrir_ventana_youtube(self):
            ventana_youtube = VentanaYouTube(self)
            ventana_youtube.exec_()

    # Agregar canción de YouTube a la playlist
    def agregar_cancion_de_youtube(self, url):
        video = pytube.YouTube(url)
        audio_stream = video.streams.filter(only_audio=True).first()

        # Construct a meaningful filename
        filename = f"{video.title}.{audio_stream.subtype}"
        audio_stream.download(filename=filename)

        audio_file = os.path.join(os.getcwd(), filename)
        self.lista_reproduccion.append(audio_file)

        self.actualizar_lista_reproduccion()



if __name__ == "__main__":
    app = QApplication(sys.argv)
    ventana = ReproductorDeMusica()
    ventana.show()
    sys.exit(app.exec_())
