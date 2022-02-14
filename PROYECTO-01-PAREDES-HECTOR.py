from lifestore_file import lifestore_products, lifestore_sales, lifestore_searches

mensaje_bienvenida = 'Bienvenido al sistema de Lifestore, accede con tus datos de usuario.'
print(mensaje_bienvenida)
print("")

intentos=3
UsuarioAccedio=False
while not UsuarioAccedio:
  #Ingresa credenciales
  usuario=input("Usuario: ")
  contrasena=input("Contrasena: ")
  if usuario == "hectorpcas" and contrasena == "emtech2022":
    UsuarioAccedio=True
  else:
    if usuario== "hectorpcas":
      intentos -=1
      print (f"Contrasena errónea, tiene {intentos} intentos restantes")
      print("")
    else:
      intentos -=1
      print(f"El usuario '{usuario}' no existe, tiene {intentos} intentos restantes")
      print("")
  if intentos == 0:
    print("Límite de intentos excedido. Acceso denegado.")
    exit()
print("")
print(f"Bienvenido, {usuario}")
print("")

# Se contabilizan las unidades vendidas por producto que no fuero devueltas
id_ventas = []
for prod in lifestore_products:
    id_prod = prod[0]
    sub = [id_prod, 0]
    id_ventas.append(sub)

# Se obtiene Id y unidades vendidas
for sale in lifestore_sales:
    id_prod = sale[1]
    indice = id_prod - 1
    if sale[-1] == 1:
        continue
    id_ventas[indice][1] += 1
  
# Unicamente reune los valores de unidades vendidas por id
id_ventas_d = []
for uds in id_ventas:
  id_ventas_d.append(uds[1])

# Se repite proceso de contabilizar unidades vendidas. Se consideran tambien las unidades devueltas. Esto se usa para promediar reseñas de productos devueltos.
id_ventas_todas = []
for prod in lifestore_products:
    id_prod = prod[0]
    sub = [id_prod, 0]
    id_ventas_todas.append(sub)

for sale in lifestore_sales:
    id_prod = sale[1]
    indice = id_prod - 1
    id_ventas_todas[indice][1] += 1
  
id_ventas_todas_d = []
for uds in id_ventas_todas:
  id_ventas_todas_d.append(uds[1])

# Suma de ventas de producto no devuelto por el cliente
id_suma_ventas=[]

# Arreglo que recolecta precios de producto por ID
lifestore_prices = []
for price in lifestore_products:
  lifestore_prices.append(price[2])
  
# Contador de posicion del id del producto
id_pos=0
# se multiplican unidades no devueltas de cada producto por su precio. El resultado se agrega a lista de suma de ventas,
for prod in id_ventas_d:
  venta_total_id = id_ventas_d[id_pos]*lifestore_prices[id_pos]
  id_suma_ventas.append(venta_total_id)
  id_pos+=1

# Recolecta reseñas de las ventas
id_resena = []
for prod in lifestore_products:
    id_prod = prod[0]
    sub = [id_prod, 0]
    id_resena.append(sub)

# Suma de las reseñas totales por producto
for sale in lifestore_sales:
    id_prod = sale[1]
    indice = id_prod - 1
    id_resena[indice][1] += sale[2]

# Recoge unicamente valores de las sumas de reseñas
id_resena_suma = []
for uds in id_resena:
  id_resena_suma.append(uds[1])

# Calcula reseñas promedio de cada producto con arreglo de sumas de reseña y de unidades vendidas considerando devoluciones
id_resena_promedio=[]

id_pos=0
for prod in id_ventas_todas_d:
  # si el total de ventas del producto considerando devoluciones es mayor a 0 se divide el valor de la suma de reseñas entre las ventas, ya que si no hay ventas no es posible dividir entre 0 y se detendra el programa 
  if id_ventas_todas_d[id_pos] > 0:
    res_avg = id_resena_suma[id_pos]/id_ventas_todas_d[id_pos]
    id_resena_promedio.append(round(res_avg, 2))
  # si el total de ventas del producto considerando devoluciones es igual a 0 su reseña promedio es 0
  else:
    id_resena_promedio.append(0)
  id_pos+=1

#Conteo de busquedas por producto"
id_busquedas = []
for prod in lifestore_products:
    id_prod = prod[0]
    sub = [id_prod, 0]
    id_busquedas.append(sub)

for sale in lifestore_searches:
    id_prod = sale[1]
    indice = id_prod - 1
    id_busquedas[indice][1] += 1

#Recoge solo valores de total de busquedas por id
id_busquedas_d = []
for uds in id_busquedas:
  id_busquedas_d.append(uds[1])

#Arreglo que recoge los datos solicitados de cada producto, recogiendo los datos de los arreglos anteiores
id_datos = []
id_pos = 0
for prod in lifestore_products:
  name = prod[1]
  cat = prod[3]
  #[0:ID, 1:nombre, 2:categoria, 3: unidades vendidas (excepto rembolsos), 4: ventas en $, 5: resena promedio y 6: busquedas]
  id_datos.append([prod[0], name, cat, id_ventas_d[id_pos], id_suma_ventas[id_pos], id_resena_promedio[id_pos], id_busquedas_d[id_pos]])
  id_pos+=1

#Productos con mas ventas en unidades
#Encabezados de tabla
print('Productos con mas ventas (unidades)')
print('  ID  Nombre                           Cantidad')

#Ordenar por unidads vendidas
id_datos.sort(key= lambda x :x[3], reverse=True)

#conteo de productos para acumular solo los primeros 5
pos = 0
for prod in id_datos:
  #se condiciona la adicion de productos a la lista hasta reunir 5
  while pos < 5:
    #Funciones para recortar el nombre del producto
    name = id_datos[pos][1]
    name = name[:30]
    print(f'{pos+1} {id_datos[pos][0]}  {name}   ({id_datos[pos][3]} uds)')
    pos+=1
print("")

#Productos con mas ventas en $

#Encabezados de tabla
print('Productos con mas ventas ($)')
print(' ID  Nombre                           Cantidad')

#Ordenar productos por ventas totales en $
id_datos.sort(key= lambda x :x[4], reverse=True)

#conteo de productos para acumular solo los primeros 5
pos = 0
for prod in id_datos:
  #se condiciona la adicion de productos a la lista hasta reunir 5
  while pos < 5:
    #Funciones para recortar el nombre del producto
    name = id_datos[pos][1]
    name = name[:30]
    print(f'{pos+1}  {id_datos[pos][0]} {name}    ${id_datos[pos][4]}')
    pos+=1
print("")

#Productos con mas busquedas

print('Productos con mas busquedas')
print('  ID  Nombre                           Busquedas')

#Ordenar por cantidad de busquedas
id_datos.sort(key= lambda x :x[6], reverse=True)

pos = 0
for prod in id_datos:
  while pos < 10:
    name = id_datos[pos][1]
    name = name[:30]
    print(f'{pos+1}  {id_datos[pos][0]} {name}     {id_datos[pos][6]}')
    pos+=1
print("")

#Productos con mejor reseña

print('Productos con mejor reseñas promedio')
print('  ID  Nombre                          Reseña')

#Ordenar de la mejor a la peor reseña promedio
id_datos.sort(key= lambda x :x[5], reverse=True)

pos = 0
for prod in id_datos:
  while pos < 5:
    name = id_datos[pos][1]
    name = name[:30]
    print(f'{pos+1}  {id_datos[pos][0]} {name}   {id_datos[pos][5]}')
    pos+=1
print("")

print('Productos con peor reseña promedio')
print('  ID  Nombre                          Reseña')

#Ordenar de la peor a la mejor reseña promedio
id_datos.sort(key= lambda x :x[5], reverse=False)

peor_reseña=[]
pos = 0
for prod in id_datos:
  if id_datos[pos][5]>0:
    peor_reseña.append(id_datos[pos])
  pos+=1

pos = 0
for prod in peor_reseña:
  while pos < 5:
    name = peor_reseña[pos][1]
    name = name[:30]
    print(f'{pos+1}  {id_datos[pos][0]} {name}   {peor_reseña[pos][5]}')
    pos+=1
print("")

#Analisis de categorias
print("Categorias")
#Generamos un arreglo que recoplie las categorias disponibles
categories =[]
for category in lifestore_products:
  cat = category[3]
  if cat not in categories:
    categories.append(cat)
print(categories)
print("")

#Arreglo que almacena las ventas totales de cada categoria
ventas_por_categoria=[] 

#Cuenta categorias segun el arreglo de categorias
conteo_cat=0 

#Se corre un ciclo para analizar cada categoria
while conteo_cat < len(categories):
  #Resetea el orden de la lista de datos del id de producto menor al mayor
  id_datos.sort(key= lambda x :x[0], reverse=False)
  
  #Recoge los datos de los productos de la cateogria
  lifestore_products_cat=[prod for prod in id_datos if prod[2]==categories[conteo_cat]]
  print(f'{conteo_cat+1} Categoria: {categories[conteo_cat]} ({len(lifestore_products_cat)} productos)')

  #Recoge los ids de los productos de la cateogria
  ids_cat=[prod[0] for prod in id_datos if prod[2]==categories[conteo_cat]]
  print('Productos disponibles:', ids_cat)
  print('')

  #Recoge las ventas totales de los productos de la cateogria
  lifestore_sales_cat=[prod[4] for prod in id_datos if prod[2]==categories[conteo_cat]]
  ventas_cat = sum(lifestore_sales_cat)
  print(f'Ventas totales categoria {categories[conteo_cat]}: ${ventas_cat}')
  ventas_por_categoria.append([categories[conteo_cat], ventas_cat])
  print("")
  
  #Productos menos vendidos por categoria
  #Ordena los productos de la categoria del menos vendido al mas vendido
  lifestore_products_cat.sort(key= lambda x :x[3], reverse=False)
  #Encabezado de tabla
  print(f'Productos menos vendidos en la categoria {categories[conteo_cat]}')
  #Encabezado de columnas
  print('  ID Nombre                         Cantidad')
  #Contador de posicion en la lista de productos de la categoria
  pos=0
  #Para cada producto de la categoria
  for prod in lifestore_products_cat:
    #Si la categoria tiene mas de 5 articulos, obtener los 5 productos con menos ventas de acuerdo a la lista previamente ordenada
    if len(ids_cat)>5:
      while pos < 5:
        name = lifestore_products_cat[pos][1]
        name = name[:30]
        print(f'{pos+1} {lifestore_products_cat[pos][0]} {name}  ({lifestore_products_cat[pos][3]} uds)')
        pos+=1
    #Si la categoria tiene menos de 5 articulos, obtener todos los articulos del menos al mas vendido
    else:
      name = lifestore_products_cat[pos][1]
      name = name[:30]
      print(f'{pos+1} {lifestore_products_cat[pos][0]} {name}  ({lifestore_products_cat[pos][3]} uds)')
      pos+=1

  print('')
  #Productos menos buscados por categoria
  #Ordena los productos de la categoria del menos buscado al mas buscado
  lifestore_products_cat.sort(key= lambda x :x[6], reverse=False)
  #Encabezado de tabla
  print(f'Productos menos buscados en la categoria {categories[conteo_cat]}')
  #Encabezado de columnas
  print('  ID Nombre                         Busquedas')
  #Contador de posicion en la lista de productos de la categoria
  pos=0
  #Para cada producto de la categoria
  for prod in lifestore_products_cat:
    #Si la categoria tiene mas de 10 articulos, obtener los 5 productos con menos ventas de acuerdo a la lista previamente ordenada
    if len(ids_cat)>10:
      while pos < 10:
        name = lifestore_products_cat[pos][1]
        name = name[:30]
        print(f'{pos+1} {lifestore_products_cat[pos][0]} {name}    {lifestore_products_cat[pos][3]}')
        pos+=1
    #Si la categoria tiene menos de 10 articulos, obtener todos los articulos del menos al mas vendido
    else:
      name = lifestore_products_cat[pos][1]
      name = name[:30]
      print(f'{pos+1} {lifestore_products_cat[pos][0]} {name}    {lifestore_products_cat[pos][3]}')
      pos+=1
  print('')
  conteo_cat+=1

#Resumen de ventas por categoria ordenadas de categoria con mayor a menos ventas en $
#Ordena las categorias por monto de venta total de mayor a menor
ventas_por_categoria.sort(key= lambda x: x[1], reverse=True)
#se activa contador de categorias
pos=0
#Encabezados de tabla resumen
print('Ventas totales por categoria')
print(' Categoria    Ventas($)')
#Ciclo para imprimir posicion, nombre de la categoria y total de ventas
for cat in ventas_por_categoria:
  print(f'{pos+1} {cat[0]} ${cat[1]}')
  pos+=1
print('')

#Ventas Mensuales y Anuales
print("Ventas Mensuales y Anuales")
print('')
# Dividir por meses las ventas
id_fecha = [ [sale[0], sale[3]] for sale in lifestore_sales if sale[4] == 0 ]
# Diccionario para categorizar meses
categorizacion_meses = {}

for par in id_fecha:
    # ID y Mes
    id = par[0]
    _, mes, _ = par[1].split('/')
    # Crear llave si el mes aun no existe
    if mes not in categorizacion_meses.keys():
        categorizacion_meses[mes] = []
    categorizacion_meses[mes].append(id)

# Recolecta ventas por mes
mes_info = {}
for mes, ids_venta in categorizacion_meses.items():
    lista_mes = ids_venta
    suma_venta = 0
    for id_venta in lista_mes:
        indice = id_venta - 1
        info_venta = lifestore_sales[indice]
        id_product = info_venta[1]
        info_prod = lifestore_products[id_product-1]
        precio = info_prod[2]
        suma_venta += precio
    mes_info[mes] = [suma_venta, len(lista_mes)]

#Arreglo de datos por mes
mes_ganancia_ventas = []
#Suma de ingresos anuales
ven_anuales = 0
#Suma de unidades vendidas anuales
uds_anuales = 0

#Ciclo para generar arreglo de datos por mes
for mes, datos in mes_info.items():
    ganancias, ventas = datos
    prom = round(ganancias/ventas, 2)
    # If para asignar mes segun numero de mes
    if mes == '01':
      m = 'Ene'
    elif mes == '02':
      m = 'Feb'
    elif mes == '03':
      m = 'Mar'
    elif mes == '04':
      m = 'Abr'
    elif mes == '05':
      m = 'May'
    elif mes == '06':
      m = 'Jun'
    elif mes == '07':
      m = 'Jul'
    elif mes == '08':
      m = 'Ago'
    elif mes == '09':
      m = 'Sep'
    elif mes == '10':
      m = 'Oct'
    elif mes == '11':
      m = 'Nov'
    elif mes == '12':
      m = 'Dic'
    #Arreglo de datos mensuales
    sub = [mes, m, ganancias, ventas, prom]
    mes_ganancia_ventas.append(sub)
    #Suma de ingresos y ventas del mes a la suma anual
    ven_anuales += ganancias
    uds_anuales += ventas
    
# Tabla de resultados mensuales
ord_mes = sorted(mes_ganancia_ventas)
print('Resultados mensuales')
print('Mes  Ingresos($)  Ventas(uds)   Prom ventas($)')
for mes in ord_mes:
  print(f'{mes[1]}    ${mes[2]}       {mes[3]}           ${mes[4]}')
print('')
# Resultados anuales
print('Resultados anuales')
print(f'Ingresos anuales: ${ven_anuales}')
print(f'Ventas realizadas anuales: {uds_anuales}')
print('')

# Resultados mensuales ordenados por ingresos mensuales
ord_gancia = sorted(mes_ganancia_ventas, key=lambda x:x[2], reverse=True)
print('Meses con mas ingresos')
print('Mes  Ingresos($)')
for mes in ord_gancia:
  print(f'{mes[1]}  ${mes[2]}')
print('')

# Resultados mensuales ordenados por ventas realizadas
ord_ventas = sorted(mes_ganancia_ventas, key=lambda x:x[2], reverse=True)
print('Meses con mas ventas')
print('Mes  Ventas')
for mes in ord_ventas:
  print(f'{mes[1]}  {mes[3]}')
print('')

print('Informacion adicional')
#Calcula el dinero devuelto a clientes
print('Devoluciones')
id_pos = 0
id_dev = []
for prod in id_ventas:
  #calcula devoluciones restando de todas las ventas las que no tuvieron devoluciones
  dev = id_ventas_todas_d[id_pos]-id_ventas_d[id_pos]
  #acortar nombre del producto
  name = lifestore_products[id_pos][1]
  name = name[:30]
  #en la lista se recoge 0: id del producto, 1 nombre, 2 unidades devueltas, 3 precio del producto
  id_dev.append([id_ventas[id_pos][0], name, dev, lifestore_prices[id_pos]])
  id_pos+=1
id_dev.sort(key= lambda x :x[2], reverse=True)

#Arroja las unidades devueltas por cada producto del mas devuelto al menos devuelto (se fltran solamente los productos que tuvieron devoluciones)
# posicion del id del producto
pos = 0
#calcula total de devoluciones en $
total_devuelto = 0
#calcula unidades devueltas
uds_devueltas = 0
#encabezado de tabla
print('ID Nombre                        Unidades  Precio/u')
for prod in id_dev:
  #si el producto tuvo devoluciones
  if id_dev[pos][2] > 0:
    #se imprimen los datos del producto devuelto
    print(f'{id_dev[pos][0]} {id_dev[pos][1]}    {id_dev[pos][2]}      ${id_dev[pos][3]}')
    #calcula el monto total de devoluciones por producto (unidades * precio)
    dev_prod = id_dev[pos][2]*id_dev[pos][3]
    #se suma la devolucion total del producto a las devoluciones totales de la tienda
    total_devuelto += dev_prod
    uds_devueltas += id_dev[pos][2]
    pos+=1
print('')
print(f'Total devoluciones a clientes: ${total_devuelto}')
print(f'Unidades devueltas por clientes: {uds_devueltas}')
print('')

# Arreglo que recolecta stock de producto por ID
lifestore_stock = []
for prod in lifestore_products:
  lifestore_stock.append(prod[4])

# Arreglo que mide stock final de productos por ID
stock_final=[]
id_pos = 0
for prod in id_ventas:
  # resta stock inicial menos ventas sin devolucion
  stock = lifestore_stock[id_pos] - id_ventas_d[id_pos]
  #agrega valor del stock del producto
  stock_final.append(stock)
  #pasa a siguiente producto
  id_pos+=1

#Resultados de stock bajos
print('Stocks finales bajos (resurtir)')
print('ID Nombre                          Stock Final   Ventas')
# Contador de posicion del id del producto
pos=0
for stock in stock_final:
  if stock_final[pos] < 0:
    id = lifestore_products[pos][0]
    name = lifestore_products[pos][1]
    name = name[:30]
    # se compara stock final con ventas para toma de decisiones
    print(f'{id}  {name}     {stock_final[pos]}          {id_ventas_d[pos]}')
  #pasa a siguiente producto
  pos+=1
print('')

#Resultados de stock altos
print('Stocks finales altos (no resurtir)')
print('ID Nombre                          Stock Final   Ventas')
# Contador de posicion del id del producto
pos=0
for stock in stock_final:
  if stock_final[pos] >= 100:
    id = lifestore_products[pos][0]
    name = lifestore_products[pos][1]
    name = name[:30]
    # se compara stock final con ventas para toma de decisiones
    print(f'{id}  {name}      {stock_final[pos]}         {id_ventas_d[pos]}')
  #pasa a siguiente producto
  pos+=1
print('')