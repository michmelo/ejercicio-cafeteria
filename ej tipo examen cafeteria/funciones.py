import json
import csv
import random
import math

URL_EMPLEADOS = 'empleado.json'
URL_CARGOS = 'cargos.json'
URL_VENTAS = 'ventas.json'
URL_PRODUCTOS = 'productos.csv'

# Funciones para cargar archivos al código
def cargarDatosJson(url):
    try:
        with open(url, 'r', encoding='utf-8') as archivo:
            return json.load(archivo) #en json se usa .load para cargar
    except:
        [] #retorna lista vacía porque json trabaja con listas
    
def cargarDatosCSV(url):
    try:
        with open(url, 'r', encoding='utf-8') as archivo:
            return list(csv.DictReader(archivo)) #en csv se usa .DictReader para cargar, debo ponerle un list antes del tipo de archivo para convertirlo a una lista usando list
    except:
        return[] #retorna lista vacía porque lo convertí en una lista
    
#funciones para el menú

def guardarVenta(ventas):
    with open(URL_VENTAS, 'w', encoding='utf-8') as archivo:
        json.dump(ventas, archivo, indent=4)

def precargarVenta(ventas, empleados, productos):
    if not empleados: #si no hay empleados
        print('No hay empleados cargados en el sistema.')
        return
    if not productos: #si no hay productos
        print('No hay productos cargados en el sistema.')
        return
    #ventas si puede estar vacía ya que si no hay ventas cargadas podemos precargarla nosotros
    for i in range(80): # 80 porque el ejercicio pide cargar 80 ventas aleatorias
        venta = {
            'id_venta': f'v{len(ventas)} + 101',
            'empleado': random.choice(empleados)['id_empleado'], #uso la libreria random para escoger datos aleatoriamente
            'fecha': '2024-08-07',
            'totalVenta': 0,
            'productos': [],
            'propina': 0
        }
        numProductos = random.randit(1,5) #randit sirve para escoger una cantidad aleatoriamente
        for j in range(numProductos):
            productoSeleccionado = random.choice(productos)
            cantidad = random.randit(1,10)
            subtotal = int(productoSeleccionado['precio']) * cantidad
            venta['productos'].append({
                'id_producto': productoSeleccionado['id_producto'],
                'cantidad': cantidad,
                'precioUnitario': int(productoSeleccionado['precio']),
                'subtotal': subtotal
            })
            venta['totalVenta'] = venta['totalVenta'] + subtotal
        ventas.append(venta)
    guardarVenta(ventas)
    print('\n80 ventas aleatorias precargadas.')

def crearVenta(ventas, empleados, productos):
    while True:
        empleado_id = input('Ingrese el ID del empleado que realiza la venta (O "cancelar" para salir): ')
        #si ingresa cancelar
        if empleado_id.lower == 'cancelar':
            print('Operación cancelada.')
            return
        #si ingresa el id del empleado verifico
        flag = False
        for e in empleados:
            if e['id_empleado'] == empleado_id:
                break
        if flag == True:
            break
        else:
            print('Empleado no encontrado. Intente nuevamente.')
    
    venta = {
        'id_venta': f'v{len(ventas)} + 101',
            'empleado': empleado_id,
            'fecha': '2024-08-07',
            'totalVenta': 0,
            'productos': [],
            'propina': 0
    }
    while True:
        producto_id = input('Ingrese el ID del producto (O "fin" para terminar): ')
        if producto_id.lower() == 'fin':
            break
        producto = None
        for p in productos:
            if p['id_producto'] == producto_id:
                producto = p
                break
        if producto is not None:
            cantidad = int(input('Ingrese la cantidad: '))
            subtotal = int(producto['precio']) * cantidad
            venta['productos'].append({
                'id_producto': producto_id,
                'cantidad': cantidad,
                'precioUnitario': int(producto['precio']),
                'subtotal': int(subtotal)
            })
            venta['total_venta'] = int(venta['total_venta']) + subtotal
        else:
            print('Producto no encontrado.')
    #calculo propina
    venta['propina'] = venta['total_venta'] * 0.1
    ventas.append(venta)
    guardarVenta(ventas)
    print(f'\nVenta creada y guardada exitosamente.')

def calcularSueldo(empleado, ventas):
    sueldoBase = empleado['sueldo_base']
    propinas = 0
    for venta in ventas:
        if venta['empleado'] == empleado['id_empleado']:
            propinas = propinas + venta['propina']
    total_ventas = 0
    for venta in ventas:
        if venta['empleado'] == empleado['id_empleado']:
            total_ventas = total_ventas + venta['total_venta']
    salud = sueldoBase * 0.07
    afp = sueldoBase * 0.12
    bono = 0
    if total_ventas > 2000000:
        bono = total_ventas * 0.05
    elif total_ventas > 1000000:
        bono = total_ventas * 0.02
    elif total_ventas > 500000:
        bono = total_ventas * 0.01
    sueldoLiquido = (sueldoBase - salud - afp) + propinas + bono

    return{
        'sueldo_base': sueldoBase,
        'propinas': propinas,
        'salud': salud,
        'AFP': afp,
        'bono': bono,
        'sueldo_liquido': sueldoLiquido
    }

def reporteSueldos(empleados, ventas):
    #cabecera de la tabla
    print(f'{'empleado' :>14} | {'Sueldo bruto' :>12} | {'Propinas' :>8} | {'Bono' :>5} | {'Descuento AFP' :>12} | {'Sueldo Liquido' :>14}')
    print('-' * 103)

    for empleado in empleados:
        sueldo = calcularSueldo(empleado, ventas)
        print(f'{empleado['nombre'] :>14} | {sueldo['sueldo_base'] : >12} | {sueldo['propinas'] :>8} | {sueldo['bono'] :>5} | {sueldo['salud'] :>13} | {sueldo['sueldo_liquido'] :>14}')

def estadisticas(ventas):
    if not ventas:
        print('No hay ventas para mostrar estadísticas')
        return
    ventas_ordenadas = ventas[:] #los dos puntos copia la lista
    
    for i in range(len(ventas_ordenadas)):
        for j in range(i + 1, len(ventas_ordenadas)):
            if ventas_ordenadas[i]['total_venta'] < ventas_ordenadas[j]['total_venta']:
                ventas_ordenadas[i] = ventas_ordenadas[j]
                ventas_ordenadas[j] = ventas_ordenadas[i]
    
    print(' 5 ventas más altas: ')
    for venta in ventas_ordenadas[:5]:
        print(f'ID venta: {venta['id_venta']}, Total: {venta['total_venta']}, Empleado: {venta['empleado']}')

    print(' 5 ventas más bajas: ')
    ventas_ordenadas_alreves = ventas_ordenadas[::-1] #con [::-1] se ordena al reves una lista
    for venta in ventas_ordenadas_alreves[:5]:
        print(f'ID venta: {venta['id_venta']}, Total: {venta['total_venta']}, Empleado: {venta['empleado']}')

    #calcular media geometrica
    '''venta_valores = []
    for venta in ventas:
        venta_valores.append(venta['total_venta'])

    multipl_ventas = 1
    for valor in venta_valores:
        multipl_ventas = multipl_ventas * valor

    media_geometrica = multipl_ventas **(1/len(venta_valores))
    print(f'Media geométrica de las ventas: {round(media_geometrica)}')'''
    #solución con librería math
    venta_valores = []
    for venta in ventas:
        venta_valores.append(venta['total_venta'])

    #comprobar si hay valores
    if len(venta_valores) == 0:
        media_geometrica = None
    else:
        #calcular la suma de los logaritmos de los valore
        log_sum = 0
        for valor in venta_valores:
            log_sum = log_sum + math.log(valor)
        
        #calcular la media geometrica en la escala logaritmica
        media_geometrica_log = log_sum / len(venta_valores)

        #convertir la media geometrica a la escala original
        media_geometrica = math.exp(media_geometrica_log)
        print('\nMedia geometrica de las ventas: ', round(media_geometrica))