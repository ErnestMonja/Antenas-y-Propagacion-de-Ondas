import numpy as np
import matplotlib.pyplot as plt

# Evitar advertencias por divisiones por cero o valores no validos
np.seterr(divide='ignore', invalid='ignore')


# Esta función calcula el Factor de Forma |F(theta)| del dipolo.
# Se suma un valor ínfimo (epsilon) a theta para evitar la división por cero en los polos (ya que cuando theta = 0, pi el sin(theta) = 0).
def calcular_factor_forma(theta, L_lambda):
    epsilon = 1e-10
    theta_seguro = np.where((theta == 0) | (theta == np.pi), theta + epsilon, theta)
    
    numerador = np.cos(np.pi * L_lambda * np.cos(theta_seguro)) - np.cos(np.pi * L_lambda)
    denominador = np.sin(theta_seguro)
    
    F = np.abs(numerador / denominador)
    return F

# Lista de relaciones L/lambda según tu imagen
lambdas = [
    (1/8, 'λ/8'),
    (1/4, 'λ/4'),
    (1/2, 'λ/2'),
    (3/4, '3λ/4'),
    (1, 'λ'),
    (5/4, '5λ/4'),
    (3/2, '3λ/2'),
    (7/4, '7λ/4'),
    (2, '2λ'),
    (9/4,'9λ/4')
]

# Recorremos cada valor de la lista para generar su gráfica
for L_val, label in lambdas:
    fig = plt.figure(figsize=(15, 5))
    fig.suptitle(f'Diagrama de Radiación para L = {label}', fontsize=16, fontweight='bold')

    # -------------------------------------------------------------
    # 1. Gráfica 2D - Corte en Azimut (Plano XY, theta = pi/2)
    # -------------------------------------------------------------
    ax_az = fig.add_subplot(131, projection='polar')
    phi_az = np.linspace(0, 2 * np.pi, 360)
    # En el plano acimutal el dipolo es omnidireccional, F(theta=pi/2) es constante
    r_az = np.ones_like(phi_az) * calcular_factor_forma(np.pi/2, L_val)
    
    ax_az.plot(phi_az, r_az, color='blue', linewidth=2)
    ax_az.set_title('Plano Azimutal (Elevación = 90°)', pad=15)
    ax_az.set_rticks([]) # Ocultamos anillos radiales para mayor claridad

    # -------------------------------------------------------------
    # 2. Gráfica 2D - Corte en Elevación (Plano XZ o YZ)
    # -------------------------------------------------------------
    ax_el = fig.add_subplot(132, projection='polar')
    # Para el corte polar, barremos theta de 0 a 2*pi para ver el lóbulo completo
    theta_el = np.linspace(0, 2 * np.pi, 360)
    r_el = calcular_factor_forma(theta_el, L_val)
    
    ax_el.plot(theta_el, r_el, color='red', linewidth=2)
    ax_el.set_theta_zero_location('N') # Que el grado 0 (eje Z) apunte hacia arriba
    ax_el.set_title('Plano de Elevación (Corte transversal)', pad=15)
    ax_el.set_rticks([]) 

    # -------------------------------------------------------------
    # 3. Gráfica 3D - Patrón de Radiación Espacial
    # -------------------------------------------------------------
    ax_3d = fig.add_subplot(133, projection='3d')
    
    # Mallas para theta (0 a pi) y phi (0 a 2pi)
    theta_3d, phi_3d = np.mgrid[0:np.pi:100j, 0:2*np.pi:100j]
    r_3d = calcular_factor_forma(theta_3d, L_val)
    
    # Conversión de coordenadas esféricas a cartesianas para graficar en 3D
    x = r_3d * np.sin(theta_3d) * np.cos(phi_3d)
    y = r_3d * np.sin(theta_3d) * np.sin(phi_3d)
    z = r_3d * np.cos(theta_3d)
    
    # Graficar la superficie
    ax_3d.plot_surface(x, y, z, cmap='viridis', edgecolor='none', alpha=0.9)
    
    # Ajustar proporciones de los ejes para que no se deforme el lóbulo
    max_range = np.array([x.max()-x.min(), y.max()-y.min(), z.max()-z.min()]).max() / 2.0
    mid_x = (x.max()+x.min()) * 0.5
    mid_y = (y.max()+y.min()) * 0.5
    mid_z = (z.max()+z.min()) * 0.5
    
    ax_3d.set_xlim(mid_x - max_range, mid_x + max_range)
    ax_3d.set_ylim(mid_y - max_range, mid_y + max_range)
    ax_3d.set_zlim(mid_z - max_range, mid_z + max_range)
    
    ax_3d.set_title('Patrón de Radiación 3D', pad=15)
    
    # Mostrar la figura
    plt.tight_layout()
    plt.show()