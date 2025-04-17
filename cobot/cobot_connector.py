import socket
import time
import numpy as np

# Velocidad fija predeterminada (en unidades por segundo)
FIXED_VELOCITY = 0.04  # Ajusta esta velocidad según sea necesario
# Aceleración arbitraria (en unidades por segundo cuadrado)
ARBITRARY_ACCELERATION = 0.025  # Ajusta esta aceleración según sea necesario

# z = 0.075
z = 0.062


# Calcula la distancia entre dos puntos
def calculate_distance(x1, y1, x2, y2):
    return np.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)


# Calcula el tiempo necesario para moverse entre dos puntos dado una velocidad fija
def calculate_time(distance, velocity):
    return distance / velocity


# Punto generico Y1
def draw(x_coords, y_coords):
    s = init()
    send_command(s, x_coords[0], y_coords[0], 0.1, 3)
    time.sleep(3)

    for i in range(0, len(x_coords)):
        if i < len(x_coords) - 1:
            x1 = x_coords[i]
            y1 = y_coords[i]
            x2 = x_coords[i + 1]
            y2 = y_coords[i + 1]
            distance = calculate_distance(x1, y1, x2, y2)
            time_to_travel = calculate_time(distance, FIXED_VELOCITY)
            time_to_travel = time_to_travel if time_to_travel > 0.6 else 0.6
        else:
            x1 = x_coords[i]
            y1 = y_coords[i]
            time_to_travel = 0.6

        send_command(s, x1, y1, z, time_to_travel)
        time.sleep(time_to_travel)

    send_command(s, x_coords[len(x_coords) - 1], y_coords[len(y_coords) - 1], 0.1, 3)
    time.sleep(3)
    s.close()


def init():
    # Conexiones IP
    HOST = "192.168.0.18"  # IP del robot
    PORT = 30001  # port: 30001, 30002 o 30003, en ambos extremos
    print("Conectando a IP: ", HOST)
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    print("conectando...")
    s.connect((HOST, PORT))
    time.sleep(0.5)
    return s


def draw_x_y_z(x_coords, y_coords, z_coords):
    s = init()
    for i in range(0, len(x_coords) - 1):
        x1 = x_coords[i]
        y1 = y_coords[i]
        y2 = y_coords[i + 1]
        x2 = x_coords[i + 1]
        z_local = z_coords[i]
        #
        # distance = calculate_distance(x1, y1, x2, y2)
        # time_to_travel = calculate_time(distance, FIXED_VELOCITY)
        # time_to_travel = time_to_travel if time_to_travel > 0.6 else 0.6
        send_command(s, x1, y1, z_local, 5)
        time.sleep(5)


def send_command(s, x, y, z, t=None):
    if t is None:
        # Enviar comando con velocidad fija y aceleración arbitraria
        command = f"movel(p[{x:.2f}, {y:.2f}, {z:.2f}, 2.5, -1.9, 0], a={ARBITRARY_ACCELERATION:.2f}, v={FIXED_VELOCITY:.2f})\n"
    else:
        # Enviar comando con velocidad fija y aceleración arbitraria
        command = f"movel(p[{x:.2f}, {y:.2f}, {z:.2f}, 2.5, -1.9, 0], a={ARBITRARY_ACCELERATION:.2f}, v={FIXED_VELOCITY:.2f}, t={t:.2f})\n"
    s.send(command.encode('utf-8'))
    print(f"Command sent: {command}")