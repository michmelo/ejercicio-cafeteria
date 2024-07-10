import funciones as fn

URL_EMPLEADOS = 'empleado.json'
URL_CARGOS = 'cargos.json'
URL_VENTAS = 'ventas.json'
URL_PRODUCTOS = 'productos.csv'

#menu

while True:
    #defino variables dentro del while para llamar funciones de los datos cargados
    ventas = fn.cargarDatosJson(URL_VENTAS)
    empleados = fn.cargarDatosJson(URL_EMPLEADOS)
    productos = fn.cargarDatosCSV(URL_PRODUCTOS)
    print('1. Precargar venta.')
    print('2. Crear venta.')
    print('3. Reporte de sueldos.')
    print('4. Ver estadísticas')
    print('5. Salir.')
    
    op = input('Seleccione opción: ')
    if op == '1':
        fn.precargarVenta(ventas, empleados, productos)
    elif op == '2':
        fn.crearVenta(ventas, empleados, productos)
    elif op == '3':
        fn.reporteSueldos(empleados, ventas)
    elif op == '4':
        fn.estadisticas(ventas)
    elif op == '5':
        print('Saliendo...')
        break
    else:
        print('Opción no válida.')