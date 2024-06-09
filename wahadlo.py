import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from matplotlib.animation import FuncAnimation

# Stałe
L = 1.0  # długość wahadła (m)
g = 9.81  # przyspieszenie ziemskie (m/s^2)
omega_p = np.sqrt(g / L)  # częstość własna wahadła (rad/s)
Omega = 2 * np.pi / (24 * 3600) * 1000  # zwiększona prędkość kątowa Ziemi (rad/s)
latitude = np.pi / 4  # szerokość geograficzna (45 stopni)
sin_theta = np.sin(latitude)

# Parametry symulacji
dt = 0.01  # krok czasowy (s)
T = 20  # całkowity czas symulacji (s)
N = int(T / dt)  # liczba kroków

# Początkowy kąt wychylenia (w stopniach)
initial_angle_degrees = 30
initial_angle_radians = np.radians(initial_angle_degrees)

# Obliczenie początkowych współrzędnych x i y na podstawie kąta wychylenia
x_initial = L * np.sin(initial_angle_radians)
y_initial = -L * np.cos(initial_angle_radians)

# Inicjalizacja tablic
x = np.zeros(N)
y = np.zeros(N)
vx = np.zeros(N)
vy = np.zeros(N)
t = np.linspace(0, T, N)

# Warunki początkowe
x[0] = x_initial  # początkowe współrzędne x
y[0] = y_initial  # początkowe współrzędne y
vx[0] = 0.0  # początkowa prędkość (m/s)
vy[0] = 0.0  # początkowa prędkość (m/s)

# Inicjalizacja tablicy z
z = np.zeros(N)

# Symulacja
for i in range(1, N):
    ax = -omega_p**2 * x[i-1] + 2 * vy[i-1] * Omega * sin_theta
    ay = -omega_p**2 * y[i-1] - 2 * vx[i-1] * Omega * sin_theta
    vx[i] = vx[i-1] + ax * dt
    vy[i] = vy[i-1] + ay * dt
    x[i] = x[i-1] + vx[i] * dt
    y[i] = y[i-1] + vy[i] * dt

    # Sprawdzenie czy wyrażenie pod pierwiastkiem jest nieujemne
    if L**2 - x[i]**2 - y[i]**2 >= 0:
        z[i] = -np.sqrt(L**2 - x[i]**2 - y[i]**2)
    else:
        z[i] = np.nan

# Rysowanie
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
ax.set_xlim([-L, L])
ax.set_ylim([-L, L])
ax.set_zlim([-L, 0])
ax.set_xlabel('X')
ax.set_ylabel('Y')
ax.set_zlabel('Z')

line, = ax.plot([], [], [], 'b-', label='Trajektoria wahadła Foucaulta')
point, = ax.plot([], [], [], 'ro')
ax.legend()

# Dodanie sznurka przyczepionego do piłki
line_sznurek, = ax.plot([], [], [], color='gray')

# Funkcja inicjalizująca
def init():
    line.set_data([], [])
    line.set_3d_properties([])
    point.set_data([], [])
    point.set_3d_properties([])
    line_sznurek.set_data([], [])
    line_sznurek.set_3d_properties([])
    return line, point, line_sznurek

# Funkcja aktualizująca
def update(num):
    line.set_data(x[:num], y[:num])
    line.set_3d_properties(z[:num])
    point.set_data([x[num]], [y[num]])  # zmieniono na sekwencję
    point.set_3d_properties([z[num]])  # zmieniono na sekwencję
    line_sznurek.set_data([0, x[num]], [0, y[num]])  # aktualizacja sznurka
    line_sznurek.set_3d_properties([0, z[num]])  # aktualizacja sznurka
    return line, point, line_sznurek

# Tworzenie animacji
ani = FuncAnimation(fig, update, frames=N, init_func=init, blit=True, interval=20)

plt.show()