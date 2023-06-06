import pygame
import random

class Laberinto():
    def __init__(self, ancho, alto, interfaz, celda):
        self.ancho = ancho
        self.alto = alto
        self.interfaz = interfaz
        self.celda = celda

        # Colores
        self.blanco = (0, 0, 0)
        self.negro = (255, 255, 255)
        self.rojo = (255, 0, 0)
        self.amarillo = (0, 255, 255)

    def generar_laberinto(self):
        # Generar una matriz de celdas
        maze = [[1] * self.ancho for _ in range(self.alto)]

        # Punto de partida y apilarlo en la pila de celdas visitadas
        stack = [(0, 0)]
        visited = set()

        while stack:
            x, y = stack[-1]
            visited.add((x, y))
            maze[y][x] = 0

            # Obtener celdas vecinas no visitadas
            neighbors = []
            if x > 1 and (x - 2, y) not in visited:
                neighbors.append((x - 2, y))
            if x < self.ancho - 2 and (x + 2, y) not in visited:
                neighbors.append((x + 2, y))
            if y > 1 and (x, y - 2) not in visited:
                neighbors.append((x, y - 2))
            if y < self.alto - 2 and (x, y + 2) not in visited:
                neighbors.append((x, y + 2))

            if neighbors:
                # Elegir una celda vecina al azar
                nx, ny = random.choice(neighbors)

                # Eliminar el muro entre la celda actual y la vecina
                mx = (x + nx) // 2
                my = (y + ny) // 2
                maze[my][mx] = 0

                # Apilar la celda vecina y marcarla como visitada
                stack.append((nx, ny))
            else:
                # Si no hay celdas vecinas no visitadas, retroceder
                stack.pop()

        return maze
    
    def dibujar_punto_inicio(self, maze):
        # Calcular las coordenadas del punto de inicio
        x = self.celda // 2
        y = self.celda // 2

        # Dibujar el punto verde en el punto de inicio
        rectangulo = pygame.Rect(x - self.celda // 2, y - self.celda // 2, self.celda, self.celda)
        pygame.draw.rect(self.interfaz.pantalla, (0, 255, 0), rectangulo)
        pygame.display.update()

    def dibujar_jugador(self, maze):
        # Calcular las coordenadas del punto de inicio
        x = self.celda // 2
        y = self.celda // 2

        # Dibujar el punto verde en el punto de inicio
        pygame.draw.circle(self.interfaz.pantalla, (0, 0, 255), (x, y), self.celda // 2)
        pygame.display.update()
    
    def crear_punto_final(self, maze):
        celdas_blancas = []

        # Encontrar celdas blancas (posibles caminos) en el laberinto
        for y, fila in enumerate(maze):
            for x, celda in enumerate(fila):
                if celda == 0:
                    celdas_blancas.append((x, y))

        self.pos_fin = None
        posiciones_finales_validas = []

        # Encontrar posiciones válidas para el punto final (punto rojo)
        for pos in celdas_blancas:
            x, y = pos
            count = 0

            if x > 0 and maze[y][x - 1] == 1:
                count += 1
            if x < self.ancho - 1 and maze[y][x + 1] == 1:
                count += 1
            if y > 0 and maze[y - 1][x] == 1:
                count += 1
            if y < self.alto - 1 and maze[y + 1][x] == 1:
                count += 1

            if count == 3:
                posiciones_finales_validas.append(pos)

        # Elegir una posición aleatoria para el punto final
        if posiciones_finales_validas:
            self.pos_fin = random.choice(posiciones_finales_validas)
            # Dibujar el punto rojo en la posición seleccionada
            x = self.pos_fin[0] * self.celda
            y = self.pos_fin[1] * self.celda
            pygame.draw.rect(self.interfaz.pantalla, self.rojo, (x, y, self.celda, self.celda))

        pygame.display.update()

    
    def crear_puntos(self, maze):
        celdas_blancas = []

        # Encontrar las celdas blancas (posibles caminos) en el laberinto
        for y, fila in enumerate(maze):
            for x, celda in enumerate(fila):
                if celda == 0:
                    celdas_blancas.append((x, y))

        puntos_generados = 0
        max_puntos = 5  # Número máximo de puntos a generar

        while puntos_generados < max_puntos:
            pos_fin = random.choice(celdas_blancas)
            x, y = pos_fin
            count = 0

            # Verificar que haya exactamente una entrada (punto negro) y el resto sean paredes (puntos blancos) alrededor del punto rojo
            if x > 0 and maze[y][x - 1] == 1:
                count += 1
            if x < self.ancho - 1 and maze[y][x + 1] == 1:
                count += 1
            if y > 0 and maze[y - 1][x] == 1:
                count += 1
            if y < self.alto - 1 and maze[y + 1][x] == 1:
                count += 1

            if count == 1:
                # Dibujar el punto amarillo en la posición seleccionada
                x = pos_fin[0] * self.celda
                y = pos_fin[1] * self.celda
                pygame.draw.rect(self.interfaz.pantalla, self.amarillo, (x, y, self.celda, self.celda))
                puntos_generados += 1

        pygame.display.update()


class Interfaz():
    def __init__(self, nombre, pantalla, ancho_ventana, alto_ventana):
        self.nombre = nombre
        self.pantalla = pantalla
        self.alto_ventana = alto_ventana
        self.ancho_ventana = ancho_ventana

        # Colores
        self.blanco = (0, 0, 0)
        self.negro = (255, 255, 255)
        self.celda = 20

    def crear_interfaz(self):
        # Establecer el título del laberinto
        pygame.display.set_caption(self.nombre)
        # Crear una superficie de visualización para dibujar el juego
        self.pantalla = pygame.display.set_mode((self.alto_ventana, self.ancho_ventana))

    def dibujar_laberinto(self, maze):
        self.pantalla.fill(self.negro)

        for y, row in enumerate(maze):
            for x, cell in enumerate(row):
                rect = pygame.Rect(x * self.celda, y * self.celda, self.celda, self.celda)
                if cell == 1:
                    pygame.draw.rect(self.pantalla, self.blanco, rect)

        pygame.display.update()

    def dibujar_objeto(self):
        pass

class Jugador():
    def __init__(self, puntaje):
        self.puntaje = puntaje
    def mover_arriba(self):
        self.laberinto.dibujar_jugador(0, -1)
    def mover_abajo(self):
        self.laberinto.dibujar_jugador(0, 1)
    def mover_izquierda(self):
        self.laberinto.dibujar_jugador(-1, 0)
    def mover_derecha(self):
        self.laberinto.dibujar_jugador(1, 0)

class Singleplayer(Jugador):
    def __init__(self):
        pass
class Multiplayer(Jugador):    
    def __init__(self):
        pass
class Juego():
    def __init__(self):
        # Crear la ventana de la clase (nombre, pantalla, ancho_ventana, alto_ventana)
        self.interfaz = Interfaz("Laberinto", None, 800, 600)
        # Crear el laberinto( ancho, alto, interfaz, celda)
        self.laberinto = Laberinto(30, 30, self.interfaz, 20)
        self.jugador = Jugador(None)
        # Ejecutar el ciclo principal
        self.main()

    def iniciar(self):
        # Inicializar pygame
        pygame.init()
        # Llamar a la clase Ventana para crear la ventana
        self.interfaz.crear_interfaz()
        # Llamar a generar laberinto para que se dibuje el laberinto
        maze = self.laberinto.generar_laberinto()
        self.interfaz.dibujar_laberinto(maze)
        self.laberinto.dibujar_punto_inicio(maze)
        self.laberinto.dibujar_jugador(maze)
        self.laberinto.crear_punto_final(maze)  # Agregar esta línea
        self.laberinto.crear_puntos(maze)  # Agregar esta línea
        pygame.display.update()  # Actualizar la ventana

    def main(self):
        self.iniciar()
        # Mantener abierta la ventana
        ejecutar = True
        while ejecutar:
            for evento in pygame.event.get():
                if evento.type == pygame.QUIT:
                    ejecutar = False
            if evento.type == pygame.KEYDOWN:
                keys = pygame.key.get_pressed()
                if keys[pygame.K_LEFT]:
                    self.mover_izquierda(self.jugador)
                if keys[pygame.K_RIGHT]:
                    self.mover_derecha(self.jugador)
                if keys[pygame.K_UP]:
                    self.mover_arriba(self.jugador)
                if keys[pygame.K_DOWN]:
                    self.mover_abajo(self.jugador)
                if keys[pygame.K_a]:
                    self.mover_izquierda(self.jugador2)
                if keys[pygame.K_d]:
                    self.mover_derecha(self.jugador2)
                if keys[pygame.K_w]:
                    self.mover_arriba(self.jugador2)
                if keys[pygame.K_s]:
                    self.mover_abajo(self.jugador2)

                if self.win1_flag or self.win2_flag:
                    self.display_win()
                    self.initialize()
                    self.win1_flag = self.win2_flag = False

                self.draw_screen()
        # Salir de pygame
        pygame.quit()

Juego()
