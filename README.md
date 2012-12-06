routing-trial
=============

RoutingUC recibe diariamente archivos con información de fundaciones para correr nuevos modelos de optimización. 
Para que los modelos se ejecuten correctamente hay que cerciorarse que la información es consistente.
Se necesita un software que recibiendo los archivos los procese y revise su integridad. En caso de ser válidos, deben ser agregados a la base de datos principal.

Archivos de Datos
--------------------
3 archivos: Todos en formato CSV
* Paraderos: 
  Ubicación, destino alumnos por curso.
* Escuelas: 
	Ubicación, capacidad alumnos por curso.
* Rutas: 
	Paraderos recorridos para dejar alumnos.

Nombrados: {Id}-(P|E|R).csv

    Ejemplo: 12-P.csv, 12-E.csv, 12-R.csv
    
Paraderos
----------

<ID, LOCATION, NAME, #C1, #C2, #C3, #C4>

\#Ci, i = {1,...,4} alumnos curso i esperando bus.
LOCATION = "{LAT};{LONG}"

Ejemplos:

    2,"23,78901;-45,21112","P3-2B",10,15,0,8
    2,"78,19;-44,121","P7-3A",19,7,5,3
    4,"23,661;-44,242","P9-1C",0,8,16,30

Escuelas
----------

<ID, LOCATION, NAME, #C1, #C2, #C3, #C4>

\#Ci, i = {1,...,4} capacidad alumnos curso i.
LOCATION = "{LAT};{LONG}"

Ejemplos:

    2,"25,78901;-48,112","Joao Lima",20,20,20,20
    2,"27,92;-47,123","Maria do Santos",10,10,25,25
    4,"26,361;-43,211","Vinicius de Moraes",30,25,20,15

Rutas
--------

<ID, ROUTE, POINT, ORDER>

ROUTE: Nombre Ruta
ORDER: "{Type}:{id}". Type: S o P.

Ejemplos:

    1,"Paulo","P:71",1
    2,"Paulo","E:81",2
    5,"René","P:18",1
    
  