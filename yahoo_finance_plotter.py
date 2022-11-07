import datetime
import json
import urllib.request
import matplotlib.pyplot as plt


############################# FUNCIONES AUXILIARES DEFINIDAS POR EL GRUPO ############################### 

def leer_cfg(filename):
    parametros = []
    file_archivo = open(filename,encoding='utf-8')
    for line in file_archivo:
        parametros.append(line.strip())
    file_archivo.close()
    return parametros

def get_quote_json(q, init_date, end_date, interval):
    period1= to_date(init_date)
    period2 = to_date(end_date)
    '''agarramos el link base para el query y queremos modificar algunos paramentros. tamamos esos parametros como elementos de una lista para finalmente unirlos todos'''
    
    query = ['https://query2.finance.yahoo.com/v8/finance/chart/',str(q),'?','period1=',str(period1),'&period2=',str(period2),'&interval=',str(interval),'&events=history']

    query_completado =''.join(query)
    req = urllib.request.Request(query_completado)
    r = urllib.request.urlopen(req).read()
    result = json.loads(r.decode('utf-8'))
    #si quieren exportar el Json descomentar las siguientes lineas.
    f_out = open('acciones.json', 'w')
    json.dump(result, f_out)
    f_out.close()
    return result

#funcion auxiliar de ayuda para el codigo no se entrega
def lista_dias_YMD(lista_dias):
    YMD_list = list(map(to_ymd, lista_dias))
    return YMD_list

def diccionario(lista_cierre,lista_dias):
    diccionario_precio_dias = {}
    for i in range(len(lista_dias)):
        diccionario_precio_dias[to_ymd(lista_dias[i])] = lista_cierre[i]
    return diccionario_precio_dias

def calculo_rendimiento(lista_cierre,lista_dias):
    rendimientos = []
    print('Rendimientos Diarios')
    for i in range(len(lista_cierre)-1):
        rendimiento = (lista_cierre[i+1]/lista_cierre[i])-1 #calculo rendimiento diario
        rendimientos.append(rendimiento)
        rendimiento_1 = round(rendimiento*100,2)
        print(str(rendimiento_1)+'% ' + to_ymd(lista_dias[i+1])) #redondeamos el valor y agregamos el simbolo de porcentaje para una mejor lectura en terminal
    return rendimientos

def media_movil(lista_cierre):
    i = 0
    M = 3 # media movil con m = 3 (cada 3 dias)
    medias = []
    while i < len(lista_cierre) - M + 1:
        muestra_M = lista_cierre[i: i + M] #movemos la posicion de nuestros 3 elementos
        Promedio_M = round(sum(muestra_M)/ M,2) #hacemos el calculo del promedio
        medias.append(Promedio_M) #agregamos el resultado
        i = i + 1
    return medias

def grafico_matplot(q,lista_dias,lista_cierre):
    lista_dias_Y_M_D = []
    for i in lista_dias:
        lista_dias_Y_M_D.append(to_ymd(i))
    
    x = lista_dias_Y_M_D
    y = lista_cierre
    
    plt.plot(x, y,'o-')
    plt.title(q)
    plt.xlabel('date')
    plt.ylabel('Price')
    plt.xticks(rotation = 45)
    #plt.show()  
    #descomentar para poder ver los graficos
    ############### Grafico ##########



################################### Ejercicio 5 ###########################################################

def periodo_maxima_cantidad_dias_positivos(lista_rendimientos,lista_dias):  #Chequiar caso en que el periodo entre en final de lista
    contador_indice_max = 0 
    longitud = 0 # la longitud mas larga encontrada hasta el momento
    longitud_actual = 0 # en cada iteracion del if guardamos la longitud del periodo y la comparamos contra la longitud total
    indice = 0 #el indice se guarda
    for i in range(len(lista_rendimientos)):
        if lista_rendimientos[i] > 0:
            longitud_actual = longitud_actual + 1

            if longitud_actual == 1:
                indice = i
        else:
            if longitud_actual > longitud: # si la longitud actual es mayor queremos actualizar el contador de longitud global
                longitud = longitud_actual
                contador_indice_max = indice
            longitud_actual = 0 #resetiamos la longitud actual a 0 para la proxima iteracion.

    if longitud_actual > longitud:
        longitud = longitud_actual
        contador_indice_max = indice

    if longitud > 0: 
        print('comienzo del periodo rendimientos positivos: ', to_ymd(lista_dias[contador_indice_max+1]))
        print('final del perido rendimientos positivos : ', to_ymd(lista_dias[contador_indice_max+longitud]))
    
    else: #si no hay longitud es debido a que no hubo rendimientos negativos en el periodo.
        print("No hay rendimientos negativos en el periodo")
    
    
def Periodo_maxima_cantidad_dias_negativos(lista_rendimientos, lista_dias): #funcion analoga a periodo_maxima_cantidad_dias_positivos.
    contador_indice_max = 0 
    longitud = 0
    longitud_actual = 0
    indice = 0
    for i in range(len(lista_rendimientos)):
        if lista_rendimientos[i] < 0:
            longitud_actual = longitud_actual + 1

            if longitud_actual == 1:
                indice = i
        else:
            if longitud_actual > longitud:
                longitud = longitud_actual
                contador_indice_max = indice
            longitud_actual = 0

    if longitud_actual > longitud:
        longitud = longitud_actual
        contador_indice_max = indice

    if longitud > 0:
        print('comienzo del periodo rendimientos negativos: ', to_ymd(lista_dias[contador_indice_max+1]))
        print('final del perido rendimientos negativos : ', to_ymd(lista_dias[contador_indice_max+longitud]))


    else:
        print("No hay rendimientos negativos en el periodo")


def maximo_rendimiento(lista_cierre,lista_dias):
    rendimientos_diarios = [] #creamos lista con todos las combinanciones de rendimientos posiblees
    diccionario_rendimientos = {} #Creamos diccionario usando como clave los rendimientos y sus values con la informacion asociada a dicho rendimineto
    
    for i in range(len(lista_cierre)-1):
        for j in range(len(lista_cierre)-1):
            if i < j:
                rend = (lista_cierre[j]/lista_cierre[i])-1 #calculo rendimiento diario
                rendimientos_diarios.append(rend)
            diccionario_rendimientos[(lista_cierre[j]/lista_cierre[i])-1] = ['fecha_compra',to_ymd(lista_dias[i]),'fecha_venta',to_ymd(lista_dias[j]),'cantidad_dias',(int(lista_dias[j]-lista_dias[i]))/86400]
            '''cada dia tiene 86400 segundos por lo cual dividimos el tiempo en formato posix por la cantidad de segundos del dia y nos retorna los dias que transcurieron'''

    valor_rendiminto_max = max(rendimientos_diarios) #nos interesa del diccionario la clave con el mayor valor
    valor_rendiminto_max_formateado = str(round(valor_rendiminto_max*100,2))+'%' #formateamos el valor para permitir una mejor lectura en terminal
    print('Maximo rendimiento',valor_rendiminto_max_formateado) 
    print(diccionario_rendimientos[valor_rendiminto_max])

def minimo_rendimiento(lista_cierre,lista_dias):
    rendimientos_diarios = [] #creamos lista con todos las combinanciones de rendimientos posiblees
    diccionario_rendimientos = {} #Creamos diccionario usando como clave los rendimientos y sus values con la informacion asociada a dicho rendimineto

    for i in range(len(lista_cierre)-1):
        for j in range(len(lista_cierre)-1):
            if i < j:
                rend = (lista_cierre[j]/lista_cierre[i])-1 #calculo rendimiento diario
                rendimientos_diarios.append(rend)
            diccionario_rendimientos[(lista_cierre[j]/lista_cierre[i])-1] = ['fecha_compra',to_ymd(lista_dias[i]),'fecha_venta',to_ymd(lista_dias[j]),'cantidad_dias',(int((lista_dias[j]-lista_dias[i])/86400))]
            '''cada dia tiene 86400 segundos por lo cual dividimos el tiempo en formato posix por la cantidad de segundos del dia y nos retorna los dias que transcurieron'''

    valor_rendiminto_min = min(rendimientos_diarios) #nos interesa del diccionario la clave con el mayor valor
    valor_rendiminto_min_formateado = str(round(valor_rendiminto_min*100,2))+'%' #formateamos el valor para permitir una mejor lectura en terminal
    print('Minimo rendimiento',valor_rendiminto_min_formateado) 
    print(diccionario_rendimientos[valor_rendiminto_min])



############################# FUNCIONES AUXILIARES DEFINIDAS POR LA CATEDRA ############################### 
def to_date(strdate):
    '''toma un string en formato %Y-%m-%d y lo convierte a algo de tipo fecha'''
    return int(datetime.datetime.strptime(strdate, '%Y-%m-%d').timestamp())

def to_ymd(ts):
    ''' Toma un timestamp y lo convierte a un string con formato %Y-%m-%d'''
    return datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d')

def to_posix_timestamp(date):
    '''Toma un datetime y lo convierte a timestamp formato POSIX'''
    return (date - datetime.datetime.utcfromtimestamp(0)).total_seconds() + 14400


############################# FUNCION PRINCIPAL ############################### 
def main():
    ''' Es la funcion principal donde se ejecuta nuestro programa.'''
    
    # Leemos el archivo input.cfg con los parametros para la ejecucion.

    # Recordar que las fechas estan en formato yyyy-mm-dd
    # Recordar que los posibles valores para el intevalo son los siguientes:
    # ["1d","5d","1wk","1mo","3mo","6mo","1y","2y","5y","10y","ytd","max"]

    # Obtenemos las fechas de inicio y fin, el intervalo, y las acciones a analizar.
    
    # Las guardamos en quotes.

    parametros = leer_cfg('input.cfg')[0:3]
    acciones = leer_cfg('input.cfg')[3:]
    quotes = acciones
    print(quotes)
    print(parametros)
    

    for q in quotes:
        print()
        # Obtenemos el JSON.
        get_quote_json(q,parametros[0],parametros[1],parametros[2])
        print()
         # Extraemos y procesamos la informacion.
        lista_cierre = get_quote_json(q,parametros[0],parametros[1],parametros[2])['chart']['result'][0]['indicators']['quote'][0]['close']
    
        lista_dias = get_quote_json(q,parametros[0],parametros[1],parametros[2])['chart']['result'][0]['timestamp']
        print(q)
        print()
        #calculo_rendimiento(lista_cierre,lista_dias) #calculamos las metricas
        print('lista_precios',lista_cierre)
        print()
        print(lista_dias_YMD(lista_dias))
        print()
        print('lista Dias en formato YMD',lista_dias_YMD(lista_dias)) #imprimimos la lista de diasS
        print()
        print(diccionario(lista_cierre,lista_dias))
        print()
        rendimientos = calculo_rendimiento(lista_cierre,lista_dias) #creamos lista rendimientos para utiliza en funcion Maxima cantidad dias
        print()
        print('media movil M = 3',media_movil(lista_cierre))
        print()
        periodo_maxima_cantidad_dias_positivos(rendimientos,lista_dias)
        print()
        Periodo_maxima_cantidad_dias_negativos(rendimientos,lista_dias)
        print()
        maximo_rendimiento(lista_cierre,lista_dias)
        print()
        minimo_rendimiento(lista_cierre,lista_dias)
        
        grafico_matplot(q,lista_dias,lista_cierre)


    parametros = leer_cfg('input_ejercicio_5.cfg')[0:3]
    acciones = leer_cfg('input_ejercicio_5.cfg')[3:]
    quotes = acciones
    print()
    print('ejercicio 6 cambio de acciones')
    print(quotes)
    print(parametros)

    #nuevo for loop para el analisis de las acciones ejercicio 6
    for q in quotes:
        print()
        # Obtenemos el JSON.
        get_quote_json(q,parametros[0],parametros[1],parametros[2])
        print()
        # Extraemos y procesamos la informacion.
        lista_cierre = get_quote_json(q,parametros[0],parametros[1],parametros[2])['chart']['result'][0]['indicators']['quote'][0]['close']
    
        lista_dias = get_quote_json(q,parametros[0],parametros[1],parametros[2])['chart']['result'][0]['timestamp']
        print(q)
        print()
        print('lista_precios',lista_cierre)
        print()
        print(lista_dias_YMD(lista_dias))
        print()
        print(diccionario(lista_cierre,lista_dias))
        print()
        print('media movil M = 6',media_movil(lista_cierre))
        print()        
        minimo_rendimiento(lista_cierre,lista_dias)

        grafico_matplot(q,lista_dias,lista_cierre) #graficamos

        #probando branch
        ################## Graficamos #####
        

if __name__ == '__main__':
    main()
