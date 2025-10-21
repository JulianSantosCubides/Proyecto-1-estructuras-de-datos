ChatGPT dijo:

Manual de usuario
Sistema de gestión de producción

Introducción
El sistema de gestión de producción permite simular y administrar órdenes de fabricación en una planta industrial. A través de una interfaz gráfica, el usuario puede crear pedidos, asignarlos a máquinas, seguir su progreso y consultar el historial de órdenes completadas. El programa fue desarrollado en Python con el objetivo de representar de forma sencilla los procesos de producción y control de pedidos.

Requisitos del sistema

Python 3.10 o superior

Librería customtkinter instalada

Sistema operativo Windows, macOS o Linux

Instalación

Descargar el proyecto completo en una carpeta local.

Abrir la carpeta del proyecto en un entorno de desarrollo (por ejemplo Visual Studio o Visual Studio Code).

Instalar la librería necesaria ejecutando en la terminal:
pip install customtkinter

Ejecutar el programa desde el archivo principal main.py.

Inicio del programa
Al ejecutar el archivo principal, se abre una ventana llamada “Sistema de gestión de producción”. Desde esta ventana principal se pueden registrar nuevas órdenes, ver las máquinas disponibles y acceder al historial de pedidos terminados.

Funciones principales

1. Creación de órdenes de producción
El usuario puede registrar una nueva orden seleccionando el producto, la cantidad y sus características. El sistema calcula automáticamente el costo total. Cada orden recibe una prioridad que determina el orden en el que será procesada por las máquinas disponibles.

2. Gestión de máquinas
El sistema cuenta con varias máquinas virtuales. Cada una tiene su propia cola de trabajo que representa las órdenes pendientes. Las órdenes se asignan automáticamente según la disponibilidad de cada máquina, y el usuario puede ver su estado en la interfaz.

3. Historial de órdenes completadas
Las órdenes finalizadas se almacenan en un historial. El usuario puede abrir la ventana del historial desde la interfaz principal para consultar pedidos terminados con su información básica: producto, cantidad, máquina utilizada y costo total. La ventana del historial se puede cerrar sin afectar el funcionamiento del programa principal.

4. Cierre del programa
Para cerrar el sistema se debe presionar el botón de salida o cerrar la ventana principal. El programa cierra todas las ventanas activas y finaliza su ejecución de forma segura.

Recomendaciones de uso

No cerrar el programa directamente desde el entorno de desarrollo mientras se estén procesando órdenes.

Evitar abrir varias ventanas de historial al mismo tiempo.

Si la interfaz no responde, cerrar la ventana y volver a ejecutar el archivo principal.

Problemas comunes

El programa no inicia: verificar que Python esté instalado y la librería customtkinter configurada.
No se muestran las ventanas: ejecutar el archivo main.py desde la carpeta principal.
La ventana del historial no se puede cerrar: asegurarse de usar la versión actual del programa.

Créditos
Proyecto académico desarrollado en Python para la asignatura de Estructuras de Datos.
Autores: Equipo de desarrollo del proyecto Sistema de gestión de producción.
