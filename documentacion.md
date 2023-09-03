Documentación del Código - Reproductor de Música MIRATOR
Introducción

Este documento proporciona una descripción general del código fuente del Reproductor de Música MIRATOR. El Reproductor de Música MIRATOR es una aplicación de reproductor de música simple y elegante desarrollada con PyQt5 y otras bibliotecas.
Estructura del Código

El código está estructurado en dos clases principales: VentanaYouTube y ReproductorDeMusica. A continuación, se describe cada clase y sus componentes clave.
VentanaYouTube

La clase VentanaYouTube representa la ventana para agregar canciones de YouTube al reproductor.

    __init__(self, parent=None): Constructor de la clase que crea la ventana y sus elementos, como la etiqueta, el campo de entrada de URL y el botón Agregar.

    agregar_cancion_youtube(self): Método para agregar una canción de YouTube a la lista de reproducción del reproductor.

ReproductorDeMusica

La clase ReproductorDeMusica representa la ventana principal de la aplicación del reproductor de música.

    __init__(self): Constructor de la clase que configura la ventana principal y sus componentes, incluyendo la lista de reproducción, los botones de control, la etiqueta de información de la canción y el menú.

    obtener_canciones(self): Método que abre un cuadro de diálogo para seleccionar archivos de música y devuelve la lista de rutas de archivos seleccionados.

    actualizar_posicion_barra_progreso(self): Método que actualiza la posición de la barra de progreso según la posición actual de la canción en reproducción.

    reproducir_cancion(self, cancion): Método para reproducir una canción específica.

    pausar_reproduccion(self): Método para pausar la reproducción de la canción actual.

    reanudar_reproduccion(self): Método para reanudar la reproducción de la canción pausada.

    detener_reproduccion(self): Método para detener la reproducción de la canción actual.

    agregar_canciones(self): Método para agregar canciones locales a la lista de reproducción.

    actualizar_lista_reproduccion(self): Método para actualizar la lista de reproducción en el widget.

    reproducir_cancion_seleccionada(self, item): Método para reproducir la canción seleccionada en la lista de reproducción.

    retroceder_cancion(self): Método para retroceder a la canción anterior en la lista de reproducción.

    siguiente_cancion(self): Método para reproducir la siguiente canción en la lista de reproducción.

    cambiar_tema_oscuro(self): Método para cambiar entre los temas claro y oscuro de la interfaz.

    activar_transparencia(self): Método para activar o desactivar la transparencia de la ventana.

    toggle_reproduccion_aleatoria(self): Método para alternar la reproducción aleatoria de canciones.

    mostrar_informacion_canciones(self): Método para mostrar información detallada sobre la canción seleccionada.

    mostrar_informacion_creador(self): Método para mostrar información sobre la versión y los desarrolladores de la aplicación.

    mostrar_informacion_cancion(self, ruta_cancion): Método para mostrar información detallada de una canción específica.

    obtener_duracion_cancion(self, ruta_cancion): Método para obtener la duración de una canción en formato de tiempo (minutos:segundos).

    actualizar_etiqueta_cancion(self, cancion): Método para actualizar la etiqueta de la canción en la barra de estado.

    media_status_changed(self, status): Método para manejar los cambios en el estado de reproducción de la canción.

    player_state_changed(self, state): Método para manejar los cambios en el estado del reproductor.

    aplicar_estilo(self): Método para aplicar el estilo de la interfaz de usuario (tema claro u oscuro).

    abrir_ventana_youtube(self): Método para abrir la ventana de agregación de canciones de YouTube.

    agregar_cancion_de_youtube(self, url): Método para agregar una canción de YouTube a la lista de reproducción.

Uso de la Aplicación

La aplicación Reproductor de Música MIRATOR permite al usuario:

    Agregar canciones locales a la lista de reproducción.
    Reproducir, pausar, detener, avanzar y retroceder canciones.
    Cambiar entre temas claro y oscuro.
    Activar la transparencia de la ventana.
    Alternar la reproducción aleatoria de canciones.
    Mostrar información detallada de las canciones.
    Agregar canciones de YouTube a la lista de reproducción.

Conclusión

El Reproductor de Música MIRATOR es una aplicación de reproductor de música versátil y fácil de usar que ofrece una variedad de funciones para mejorar la experiencia de escucha de música.
