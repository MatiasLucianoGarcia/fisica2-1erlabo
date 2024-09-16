import numpy as np
import matplotlib.pyplot as plt

# Constante de Coulomb (1/4πε0)(N·m²/C²)
k = 8.99e9  

# Función para pedir al usuario el número de cargas, debe ser >= 3
def pedir_numero_cargas():
    while True:
        n = int(input("¿Cuántas cargas quieres usar? (Debe ser 3 o mayor): "))
        if n >= 3:
            return n
        else:
            print("El número de cargas debe ser 3 o mayor.")

# Pedir al usuario el número de cargas
n_cargas = pedir_numero_cargas()

# Inicializar listas para almacenar las cargas y posiciones
cargas = []
posiciones = []

# Pedir al usuario la magnitud y posición de cada carga
for i in range(n_cargas):
    q = float(input(f"Introduce la magnitud de la carga {i+1} (en Coulombs): "))
    xq = float(input(f"Introduce la posición x de la carga {i+1}: "))
    yq = float(input(f"Introduce la posición y de la carga {i+1}: "))
    cargas.append(q)
    posiciones.append((xq, yq))

# Crear una cuadrícula de puntos donde calcular el campo eléctrico y el potencial
x = np.linspace(-10, 10, 200) #va de -10 a 10 con 200 puntos a lo largo del eje
y = np.linspace(-10, 10, 200)
X, Y = np.meshgrid(x, y)  # 40,000 puntos en la cuadrícula dado por el 200x200

# Inicializar los componentes del campo eléctrico y el potencial
Ex_total = np.zeros(X.shape)
Ey_total = np.zeros(X.shape)
V_total = np.zeros(X.shape)

# Calcular el campo eléctrico y el potencial para cada carga
for i, carga in enumerate(cargas):
    xq, yq = posiciones[i]
    
    # Distancias desde la carga a cada punto de la cuadrícula
    Rx = X - xq
    Ry = Y - yq
    R = np.sqrt(Rx**2 + Ry**2) #raiz(x^2 + y^2)
    
    # Evitar división por cero cuando un punto de la cuadrícula coincide con la posición de una carga
    # se reemplaza R = 0 por un valor muy pequeño (1e-12), lo cual evita errores sin afectar los resultados.
    R[R == 0] = 1e-12
    
    # Campo eléctrico debido a la carga puntual
    Ex = k * carga * Rx / R**3 # lo que es igual a 1/4πε0 * q * (R - R')/|R-R'|^3
    Ey = k * carga * Ry / R**3
    
    # Potencial eléctrico debido a la carga puntual
    V = k * carga / R
    
    # Superposición de los campos y potenciales
    Ex_total += Ex
    Ey_total += Ey
    V_total += V

# Calcular la magnitud del campo eléctrico
E_magnitud = np.sqrt(Ex_total**2 + Ey_total**2)

# Función para manejar eventos de clic
def onclick(event):
    if event.inaxes:  # Solo si el clic está dentro de los ejes
        # Obtener las coordenadas del clic
        x_click = event.xdata
        y_click = event.ydata
        
        # Calcular la distancia desde el clic a cada punto de la cuadrícula
        Rx_click = X - x_click
        Ry_click = Y - y_click
        R_click = np.sqrt(Rx_click**2 + Ry_click**2)
        
        # Encontrar el índice del punto más cercano al clic
        idx = np.unravel_index(np.argmin(R_click, axis=None), R_click.shape)
        
        # Obtener el valor del campo y potencial en ese punto
        E_valor = E_magnitud[idx]
        V_valor = V_total[idx]
        
        # Mostrar los valores en la consola
        print(f"Campo eléctrico en ({x_click:.2f}, {y_click:.2f}): {E_valor:.2e} N/C")
        print(f"Potencial eléctrico en ({x_click:.2f}, {y_click:.2f}): {V_valor:.2e} V")

# Generar el gráfico combinado
fig, ax = plt.subplots(figsize=(10, 10))

# Graficar las líneas de campo eléctrico
strm = ax.streamplot(X, Y, Ex_total, Ey_total, color=E_magnitud, linewidth=1, cmap='cool', density=2)

# Graficar las líneas equipotenciales del potencial eléctrico
contour = ax.contour(X, Y, V_total, levels=50, cmap='inferno')

# Dibujar las cargas: rojo para positivas y azul para negativas
for i, carga in enumerate(cargas):
    color = 'red' if carga > 0 else 'blue'
    ax.scatter(posiciones[i][0], posiciones[i][1], color=color, s=100, marker='o')

# Etiquetas y detalles del gráfico
ax.set_title('Campo Eléctrico y Potencial Eléctrico')
fig.colorbar(strm.lines, label='Intensidad del Campo Eléctrico / Potencial Eléctrico')
ax.set_xlabel('x')
ax.set_ylabel('y')
ax.grid(True)

# Conectar el evento de clic
cid = fig.canvas.mpl_connect('button_press_event', onclick)

# Mostrar la gráfica
plt.show()