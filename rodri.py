# Test
import socket
import time
import numpy as np

# ESTE NO LO USAMOS, EL QUE USAMOS ESTA EN cobot/cobot_connector.py


#La siguiente función transforma de radianes a grados para poder insertar las coordenadas indicadas en el teach pendant directamente en las
#funciones de move
def rads_to_degrees_string(degree_array: list[float]) -> str :
    rads_array = np.deg2rad(degree_array)
    rads_list = list(map(str, rads_array))
    return f"[{', '.join(rads_list)}]"

#Conexiones IP
HOST = "192.168.0.16" # IP del robot
PORT = 30001 # port: 30001, 30002 o 30003, en ambos extremos
print("Conectando a IP: ", HOST)

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
print("conectando...")
s.connect((HOST, PORT))
time.sleep(0.5)

# Punto generico Y1
s.send (b"movej(" + rads_to_degrees_string([-5.39, -59.17, 34.62, 10.34, 87.98, 1.38]).encode('utf-8') + ", a=0.5, v=0.25)\n".encode('utf-8'))
time.sleep(5)

# Letra Y
s.send (b"movej(" + rads_to_degrees_string([-8.64, -48.46, 13.09, 29.53, 75.28, -3.93]).encode('utf-8') + ", a=0.5, v=0.25)\n".encode('utf-8'))
time.sleep(2)
s.send (b"movej(" + rads_to_degrees_string([-9.75, -48.83, 13.05, 25.97, 75.32, -3.95]).encode('utf-8') + ", a=0.5, v=0.25)\n".encode('utf-8'))
time.sleep(2)
s.send (b"movej(" + rads_to_degrees_string([-8.64, -48.46, 13.09, 29.53, 75.28, -3.93]).encode('utf-8') + ", a=0.5, v=0.25)\n".encode('utf-8'))
time.sleep(2)
s.send (b"movej(" + rads_to_degrees_string([-9.71, -48.49, 13.04, 24.18, 68.15, -3.95]).encode('utf-8') + ", a=0.5, v=0.25)\n".encode('utf-8'))
time.sleep(2)
s.send (b"movej(" + rads_to_degrees_string([-8.64, -48.46, 13.09, 29.53, 75.28, -3.93]).encode('utf-8') + ", a=0.5, v=0.25)\n".encode('utf-8'))
time.sleep(2)
s.send (b"movej(" + rads_to_degrees_string([-10.5, -47.68, 13.14, 31.97, 70.54, -4.93]).encode('utf-8') + ", a=0.5, v=0.25)\n".encode('utf-8'))
time.sleep(2)

# Punto generico Y2
s.send (b"movej(" + rads_to_degrees_string([-4.30, -57.68, 34.27, 16.29, 88.02, 1.38]).encode('utf-8') + ", a=0.5, v=0.25)\n".encode('utf-8'))
time.sleep(5)

# Punto generico P1
s.send (b"movej(" + rads_to_degrees_string([-12.35, -63.19, 45.51, 8.92, 72.91, -3.18]).encode('utf-8') + ", a=0.5, v=0.25)\n".encode('utf-8'))
time.sleep(5)

# Letra P
s.send (b"movej(" + rads_to_degrees_string([-12.39, -59.80, 45.51, -0.95, 70.74, -3.18]).encode('utf-8') + ", a=0.5, v=0.25)\n".encode('utf-8'))
time.sleep(2)
s.send (b"movej(" + rads_to_degrees_string([-12.38, -59.53, 44.60, -8.67, 71.32, 0.39]).encode('utf-8') + ", a=0.5, v=0.25)\n".encode('utf-8'))
time.sleep(2)
s.send (b"movej(" + rads_to_degrees_string([-13.19, -59.48, 44.62, -8.27, 76.08, 0.38]).encode('utf-8') + ", a=0.5, v=0.25)\n".encode('utf-8'))
time.sleep(2)
s.send (b"movej(" + rads_to_degrees_string([-13.18, -59.48, 44.66, -4.50, 76.10, 0.38]).encode('utf-8') + ", a=0.5, v=0.25)\n".encode('utf-8'))
time.sleep(2)
s.send (b"movej(" + rads_to_degrees_string([-10.72, -59.48, 44.65, -4.51, 76.07, 0.38]).encode('utf-8') + ", a=0.5, v=0.25)\n".encode('utf-8'))
time.sleep(2)

# Punto generico P1
s.send (b"movej(" + rads_to_degrees_string([-11.77, -63.11, 42.62, 10.14, 75.47, -3.18]).encode('utf-8') + ", a=0.5, v=0.25)\n".encode('utf-8'))
time.sleep(5)

# Punto generico F1
s.send (b"movej(" + rads_to_degrees_string([-15.84, -62.38, 42.55, 13.67, 73.35, -7.90]).encode('utf-8') + ", a=0.5, v=0.25)\n".encode('utf-8'))
time.sleep(5)

# Letra F
s.send (b"movej(" + rads_to_degrees_string([-15.53, -59.11, 42.55, 3.62, 71.72, 1.14]).encode('utf-8') + ", a=0.5, v=0.25)\n".encode('utf-8'))
time.sleep(2)
s.send (b"movej(" + rads_to_degrees_string([-15.82, -59.06, 41.96, -4.13, 71.12, 1.36]).encode('utf-8') + ", a=0.5, v=0.25)\n".encode('utf-8'))
time.sleep(2)
s.send (b"movej(" + rads_to_degrees_string([-18.04, -58.85, 41.95, -4.69, 70.97, 1.36]).encode('utf-8') + ", a=0.5, v=0.25)\n".encode('utf-8'))
time.sleep(2)
s.send (b"movej(" + rads_to_degrees_string([-15.82, -59.06, 41.96, -4.13, 71.12, 1.36]).encode('utf-8') + ", a=0.5, v=0.25)\n".encode('utf-8'))
time.sleep(2)
s.send (b"movej(" + rads_to_degrees_string([-16.57, -58.85, 41.97, -0.93, 68.96, 1.36]).encode('utf-8') + ", a=0.5, v=0.25)\n".encode('utf-8'))
time.sleep(2)
s.send (b"movej(" + rads_to_degrees_string([-18.52, -58.85, 41.97, -0.94, 69.00, 1.36]).encode('utf-8') + ", a=0.5, v=0.25)\n".encode('utf-8'))
time.sleep(2)

# Punto generico F2
s.send (b"movej(" + rads_to_degrees_string([-19.52, -62.71, 41.96, 11.9, 68.95, 1.37]).encode('utf-8') + ", a=0.5, v=0.25)\n".encode('utf-8'))
time.sleep(5)

s.close()
