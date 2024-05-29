import pygame
import numpy as np
from math import *

# Definition der Farben
WHITE = (0, 0, 0)
RED = (255, 0, 0)
BLACK = (255, 255, 255)

# Fenstergröße festlegen
WIDTH, HEIGHT = 1920, 1080
pygame.display.set_caption("3D projection in pygame!")
screen = pygame.display.set_mode((WIDTH, HEIGHT))

# Skalierung für die 3D-Projektion
scale = 100

# Startposition des Würfels
circle_pos = [WIDTH//2, HEIGHT//2]

# Initialisierung des Winkels für die Rotation
angle = 0

# Liste zur Speicherung der 3D-Punkte des Würfels
points = []

# Definition der Würfel-Eckpunkte im 3D-Raum
points.append(np.array([-1, -1, 1])) # X Y Z Ordnung
points.append(np.array([1, -1, 1]))
points.append(np.array([1, 1, 1]))
points.append(np.array([-1, 1, 1]))
points.append(np.array([-1, -1, -1]))
points.append(np.array([1, -1, -1]))
points.append(np.array([1, 1, -1]))
points.append(np.array([-1, 1, -1]))

# Definition der Projektionsmatrix für die 3D->2D Projektion
projection_matrix = np.array([
    [1, 0, 0], # bedeutet, dass die X-Koordinate des 3D-Punkts unverändert bleibt.
    [0, 1, 0]  # bedeutet, dass die Y-Koordinate des 3D-Punkts ebenfalls unverändert bleibt
]) 

# Liste zur Speicherung der projizierten 2D-Punkte des Würfels
projected_points = [
    [n, n] for n in range(len(points))
]

# Funktion zum Verbinden der Punkte mit Linien
def connect_points(i, j, points):
    pygame.draw.line(
        screen, BLACK, (points[i][0], points[i][1]), (points[j][0], points[j][1]))

# Hauptprogrammschleife
clock = pygame.time.Clock()
while True:
    clock.tick(60)  # Begrenzt die Bildwiederholrate auf 60 FPS

    for event in pygame.event.get():  # Eventschleife für die Behandlung von Schließ-Events
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        elif event.type == pygame.KEYDOWN:  # Schließe das Fenster, wenn ESC gedrückt wird
            if event.key == pygame.K_ESCAPE:
                pygame.quit()
                exit()

    # Würfelrotation um die X-, Y- und Z-Achse
    rotation_z = np.array([
        [cos(angle), -sin(angle), 0],
        [sin(angle), cos(angle), 0],
        [0, 0, 1],
    ])

    rotation_y = np.array([
        [cos(angle), 0, sin(angle)],
        [0, 1, 0],
        [-sin(angle), 0, cos(angle)],
    ])

    rotation_x = np.array([
        [1, 0, 0],
        [0, cos(angle), -sin(angle)],
        [0, sin(angle), cos(angle)],
    ])

    angle += 0.01  # Inkrementiere den Rotationswinkel

    # Lösche den Bildschirm
    screen.fill(WHITE)

    # Projiziere die 3D-Punkte auf den 2D-Bildschirm und zeichne sie
    for i, point in enumerate(points):
        rotated2d = np.dot(rotation_z, point.reshape((3, 1)))
        rotated2d = np.dot(rotation_y, rotated2d)
        rotated2d = np.dot(rotation_x, rotated2d)

        projected2d = np.dot(projection_matrix, rotated2d)

        x = int(projected2d[0][0] * scale) + circle_pos[0]
        y = int(projected2d[1][0] * scale) + circle_pos[1]

        projected_points[i] = [x, y]
        pygame.draw.circle(screen, RED, (x, y), 5)

    # Verbinde die Punkte, um die Kanten des Würfels zu zeichnen
    for p in range(4):
        connect_points(p, (p+1) % 4, projected_points)
        connect_points(p+4, ((p+1) % 4) + 4, projected_points)
        connect_points(p, (p+4), projected_points)

    # Bildschirm aktualisieren
    pygame.display.update()