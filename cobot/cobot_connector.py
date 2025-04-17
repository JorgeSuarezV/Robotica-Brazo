import socket
import time
import numpy as np

# --- Configuración global ---
FIXED_VELOCITY = 0.04              # Velocidad fija (unidades/s)
ARBITRARY_ACCELERATION = 0.025     # Aceleración (unidades/s²)
DRAWING_Z = 0.062                  # Altura de dibujo en el eje Z
LIFT_Z = 0.1                       # Altura al levantar el brazo

ROBOT_IP = "192.168.0.18"
ROBOT_PORT = 30001


# --- Funciones auxiliares ---
def calculate_distance(x1, y1, x2, y2):
    return np.hypot(x2 - x1, y2 - y1)


def calculate_time(distance, velocity):
    return max(distance / velocity, 0.6)


# --- Conexión al robot ---
def init_connection():
    print(f"Conectando a IP: {ROBOT_IP}...")
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((ROBOT_IP, ROBOT_PORT))
    time.sleep(0.5)
    return s


# --- Enviar comandos ---
def send_command(s, x, y, z, t=None):
    if t is None:
        command = (
            f"movel(p[{x:.2f}, {y:.2f}, {z:.2f}, 2.5, -1.9, 0], "
            f"a={ARBITRARY_ACCELERATION:.2f}, v={FIXED_VELOCITY:.2f})\n"
        )
    else:
        command = (
            f"movel(p[{x:.2f}, {y:.2f}, {z:.2f}, 2.5, -1.9, 0], "
            f"a={ARBITRARY_ACCELERATION:.2f}, v={FIXED_VELOCITY:.2f}, t={t:.2f})\n"
        )
    s.send(command.encode('utf-8'))
    print(f"Command sent: {command.strip()}")


# --- Dibujar trayectoria ---
def draw(x_coords, y_coords):
    s = init_connection()

    # Mover a la posición inicial levantado
    send_command(s, x_coords[0], y_coords[0], LIFT_Z, 3)
    time.sleep(3)

    for i in range(len(x_coords)):
        x1, y1 = x_coords[i], y_coords[i]

        if i < len(x_coords) - 1:
            x2, y2 = x_coords[i + 1], y_coords[i + 1]
            distance = calculate_distance(x1, y1, x2, y2)
            t_travel = calculate_time(distance, FIXED_VELOCITY)
        else:
            t_travel = 0.6  # Último punto

        send_command(s, x1, y1, DRAWING_Z, t_travel)
        time.sleep(t_travel)

    # Levantar el brazo al finalizar
    send_command(s, x_coords[-1], y_coords[-1], LIFT_Z, 3)
    time.sleep(3)

    s.close()


# --- Dibujar con altura variable ---
def draw_x_y_z(x_coords, y_coords, z_coords):
    s = init_connection()

    for i in range(len(x_coords) - 1):
        x = x_coords[i]
        y = y_coords[i]
        z = z_coords[i]

        send_command(s, x, y, z, 5)
        time.sleep(5)

    s.close()
