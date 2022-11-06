# TP3_MAAN
M´etodos Anal´ıticos Aplicados a los Negocios II
Segundo Cuatrimestre 2022
TP3
Recomendaciones generales
Esta gu´ıa contiene un Trabajo Pr´actico de MAAN II. El mismo debe ser resuelto ´ıntegramente
en Python. La resoluci´on no es simple y se espera que resolverlo tome cierto tiempo por fuera
de las clases.
Recuerden que pueden consultarlos sin ning´un tipo de problema y que este trabajo y los
siguientes son parte de la evaluaci´on que tendr´an de la materia. Se sugiere que empiecen a
resolver el TP con tiempo de modo de tener tiempo para hacer consultas y no estar apurados
a ´ultimo momento.
El Trabajo Pr´actico debe resolverse de a grupos de 2 o 3 alumnos, no m´as y no menos.
Las consultas podr´an realizarse por mail y en los momentos asignados en clase. Tener en
cuenta que si la consulta es realizada a ´ultimo momento puede no ser factible responderla.
No est´a permitida la interacci´on entre grupos.
implementar
Scraping Yahoo! Finance
Existen distintas formas de evaluar un activo o una acci´on, por ejemplo en funci´on de su
retorno esperado y/o su riesgo. En general estas m´etricas se calculan en base a datos hist´oricos,
com´unmente en formatos de series de tiempo que consideran a los precios. Muchos sitios web
y p´aginas de finanzas ofrecen diversas m´etricas sobre los distintos activos del mercado de
forma resumida. Sin embargo, si uno quisiera desarrollar su propia metodolog´ıa el acceso a
la informaci´on detallada es, para el usuario com´un, engorroso y dif´ıcil de llevar adelante. En
este ejercicio nos concentraremos en obtener datos hist´oricos sobre acciones a partir de Yahoo!
Finance de forma simple y f´acil usando Python.
Para obtener los datos, Yahoo! Finance provee una p´agina web donde se pueden consultar
desde un navegador. Si bien es posible bajar la p´agina y analizar su c´odigo HTML , Yahoo!
Finance provee, escondido dentro de su sitio, una Application Programming Interface (API)
que nos permite obtener la misma informaci´on que a trav´es de su p´agina web pero en un
formato mucho m´as c´omodo para trabajar desde nuestros c´odigos. Para poder accederlo,
necesitamos saber dos cosas:
1. d´onde est´a ubicado, y c´omo acceder a la informaci´on espec´ıfica de una acci´on;
2. una vez que localizamos la informaci´on, en qu´e formato viene y c´omo podemos trabajar
con ella.
Para el primer punto, s´olo es cuesti´on de generar una direcci´on URL de forma conveniente y
Yahoo! Finance nos devolver´a el resultado. La direcci´on est´a compuesta por una direcci´on base
sumado a algunos par´ametros que nos permiten determinar los par´ametros de la b´usqueda.
1
Esto mismo puede hacerse desde la p´agina web, donde podemos elegir cu´al es la acci´on elegida,
el rango de fechas que buscamos y el intervalo de tiempo para el que nos retorna los precios.
Puede verse un ejemplo en la siguiente imagen.
Al acceder mediante la API podemos especificarle lo mismo. Supongamos que queremos acciones de Apple, cuyo c´odigo es AAPL en un rango determinado de fechas a intervalo de una
semana. La direcci´on es la que sigue a continuaci´on, que luego explicaremos que significa cada
parte.
https://query2.finance.yahoo.com/v8/finance/chart/AAPL?period1=1472785200&period2=1504321200&interval=1wk&events=history
Aquello marcado en color azul corresponde a la direcci´on base, o son tecnicismos relacionados el el formato de direcci´on URL. Son cosas que NO vamos a modificar.
Las partes marcadas en verde son los nombres de los par´ametros que refinan nuestra
b´usqueda. Entre ellos: ´
 period1: fecha de inicio de la consulta.
 period2: fecha de fin de la consulta.
 interval: cada cuanto queremos que nos retorne el precio.
Las partes marcadas en violeta son los valores de los par´ametros que refinan nuestra
b´usqueda. Estos son: ´
 c´odigo de la acci´on: en nuestro caso, AAPL.
 fecha de inicio de la consulta, expresada en cantidad de segundos desde 1/1/1970.
 fecha de fin de la consulta, expresada en cantidad de segundos desde 1/1/1970.
 granularidad de los datos: ”1wk”significa una semana. Puede ser cualquier de los siguientes: ”1d”,”5d”,”1wk”,”1mo”,”3mo”,”6mo”,”1y”,”2y”,”5y”,”10y”,”ytd”,”max”.
A modo de ejemplos, si quisi´esemos realizar exactamente la misma consulta pero para Google
(GOOG) en lugar de Apple usar´ıamos (con la diferencia respecto de la anterior marcada en
rojo):
https://query2.finance.yahoo.com/v8/finance/chart/GOOG?period1=1472785200&period2=1504321200&interval=1wk&events=history
Si adem´as quisi´eramos los datos cada intervalos de un mes, agregamos la siguiente modificaci´on:
2
https://query2.finance.yahoo.com/v8/finance/chart/GOOG?period1=1472785200&period2=1504321200&interval=1mo&events=history
Una vez generada la consulta, Yahoo! Finance responde con los datos usando el formato de
intercambio muy utilizado en la pr´actica, JavaScript Object Notation (JSON), visto en clase.
El mismo no es otra cosa que una combinaci´on entre listas, strings y diccionarios que con un
formato definido por el emisor del mensaje permite transmitir la informaci´on deseada.
El objetivo del trabajo es desarrollar la primera herramienta completa (sin necesidad de
modificar el c´odigo para poder ejecutarla con distintas opciones) de la materia, enfocada en
acceder a informaci´on de acciones a trav´es de Yahoo! Finance y procese la informaci´on. El
alcance del trabajo llegar´a a realizar algunas visualizaciones respecto de las acciones, pero
sienta las bases para que ustedes puedan extenderla.:
El trabajo consiste en los siguientes puntos:
1. (1.50 puntos) Lectura de par´ametros de ejecuci´on. El programa debe leer la
informaci´on relacionada a las acciones y la configuraci´on de la ejecuci´on de un archivo
de texto ubicado en el mismo directorio de ejecuci´on del programa, y con el nombre
input.cfg. El archivo tendr´a un par´ametro por l´ınea, en el siguiente orden: fecha de
inicio (formato yyyy-mm-dd), fecha de fin (formato yyyy-mm-dd), intervalo (como
se especifica respecto a la granularidad), lista de acciones a buscar, una por l´ınea.
Esta ´ultima no tiene l´ımite y puede ser variable. Se muestra a continuaci´on un ejemplo
con 4 acciones:
2014-08-01
2017-08-31
1mo
GOOG
AAPL
AMZN
MELI
Sugerencia: en caso de tener problemas con el caracter ’\n’, considerar la documentaci´on de la funci´on strip para string.
2. (1.00 puntos) Consulta a API Yahoo! Finance y utilizaci´on JSON. Siguiendo
los lineamientos descriptos en este enunciado y las librer´ıas vistas en clase, implementar
una funci´on que tome la fecha de inicio, la de fin, el intervalo y una acci´on, acceda a la
API de Yahoo! Finance y obtenga el correspondiente JSON con la informaci´on requerida
para ser procesada.
3. (2.00 puntos) C´alculo de m´etricas para todas las acciones. Para cada acci´on,
extraer del correspondiente JSON la estructura que contiene las fechas, la de los precios
y calcular una m´etrica a fin de poder visualizarla. Puede ser el precio, o el rendimiento
diario, o una media m´ovil, o alguna otra opci´on que el grupo considere relevante. Respecto al rendimiento, llamemos pi al precio de la acci´on del d´ıa i. Luego, si compramos
la acci´on en un d´ıa i y la vendemos en el d´ıa j, con j > i, el rendimiento obtenido se
calcula como
r =
pj − pi
pi
=
pj
pi
− 1.
3
4. (1.50 puntos) Visualizaciones de resultados. Utilizar la librer´ıa matplotlib para
visualizar la evoluci´on de las series (precios o rendimientos) en el per´ıodo elegido. Si
bien la librer´ıa ofrece m´ultiples opciones, inicialmente la utilizaremos en su versi´on m´as
b´asica. En este contexto, uno debe incluir el paquete correspondiente. Luego, utilizando plot agrega una a una las series y, finalmente, el m´etodo show muestra el gr´afico
correspondiente generado hasta el momento. Se muestra a continuaci´on un ejemplo:.
import matplotlib.pyplot as plt
# y = x**2 y z = x**3 son dos series distintas.
x = list(range(10))
y = [0]*10
z = [0]*10
for i in range(10):
y[i] = x[i]**2
z[i] = x[i]**3
# Agregamos la serie (x,y)
# El tercer parametro es el formato (’o’ es punto, "-" linea)..
plt.plot(x,y,’o-’)
# Agregamos la serie (x,z)
# El tercer parametro es el formato (’x’ es cruz, "-" linea)..
plt.plot(x,z,’x-’)
# Agregamos la leyenda.
plt.legend([’x’,’y’])
# Mostramos el grafico
plt.show()
Si uno quisiera generar un segundo gr´afico, se puede a continuaci´on agregar nuevas series
y finalmente hacer un nuevo show.
5. (2.50 puntos) C´alculos adicionales. Queremos calcular algunas m´etricas adicionales.
Estamos interesados en evaluar, para cada acci´on, las siguientes m´etricas:
Per´ıodo con la m´axima cantidad de d´ıas consecutivos con rendimiento positivo. En
caso de haber m´as de uno, devolver cualquiera.
Per´ıodo con la m´axima cantidad de d´ıas consecutivos con rendimiento negativo.
En caso de haber m´as de uno, devolver cualquiera.
El m´aximo rendimiento obtenible en el per´ıodo (independientemente de la cantidad
de d´ıas), junto las fechas correspondientes de compra / venta, y la cantidad de d´ıas
transcurridos.
An´alogo al anterior, el m´ınimo rendimiento obtenible en el per´ıodo (eventualmente,
negativo), junto con las fechas correspondientes de compra / venta, y la cantidad
de d´ıas transcurridos.
4
Se pide entonces agregar el c´alculo de estas m´etricas al c´odigo. Para ello, se recomienda
investigar c´omo operar con el m´odulo datetime. Adicionalmente, es requisito implementar casos de test unitario adecuados para cada funcionalidad utilizando unittest. Este
punto tambi´en contemplar´a en su correcci´on la modularizaci´on, funciones auxiliares y
comentarios de todo el c´odigo as´ı como tambi´en los casos de test unitario dise˜nados
para este ´ıtem en particular.
Los valores obtenidos pueden ser reportados por pantalla o en alg´un archivo adicional
(formato a elecci´on, JSON o texto plano son dos opciones).
Aclaraci´on: las m´etricas deben calcularse asumiendo que solamente se puede invertir en
long. No se posible hacer un short.
6. (1.50 puntos) Utilizaci´on de la herramienta. Buscar utilizando la herramienta un
conjunto de acciones (al menos 3) y un per´ıodo que resulte interesante desde el an´alisis
de los precios y/o rendimientos durante el per´ıodo. Comentar ventajas y desventajas
respecto a la utilizaci´on, y posibles mejoras a incorporar.
7. Se pide agregar un informe, de a lo sumo 8 p´aginas, explicando brevemente la visualizaciones generadas, la estrategia para resolver el ejercicio 5 y la explicaci´on del caso
propuesto en el ejercicio 6.
Modalidad de entrega
Adem´as del c´odigo con las implementaciones es posible entregar un mini informe de no m´as
de tres carillas en donde detallen, en caso de considerarlo necesario, decisiones que tomaron
para resolver uno o m´as ejercicios y que ayuden a entender la estrategia de resoluci´on.
Fechas de entrega
Formato Electr´onico: lunes 7 de noviembre, hasta las 23:59 hs., enviando el trabajo
(informe + c´odigo) a la direcci´on maan2utdt@gmail.com. El subject del email debe comenzar
con el texto [TP3 MAAN II] seguido de la lista de apellidos de los integrantes del grupo.
Todos los integrantes del grupo deben estar copiados en el email.
Importante: El horario es estricto. Los correos recibidos despu´es de la hora indicada ser´an
considerados re-entrega.
5
