readme3

# Introducción al Laboratorio tercero de Sistemas Operativo

### Grupo:

Virtualized, nombrado así en honor a la técnica empleada por los sistemas operativos.

### Integrantes:

Conformado por

- Leonardo Torres, (leo.torres@mi.unc.edu.ar)
- Matías Scantamburlo, (matias.scantamburlo@mi.unc.edu.ar)
- Maciel Salguero, (maciel.salguero@mi.unc.edu.ar)

# Desarrollo

En este laboratorio se trabajo para resolver y desarrollar respuestas a mutiples enunciados segmentados en 4 etapas :

1.  Realizar una lecto-comprensión del código de xv6 para así responder las preguntas características de dicho sistema.
2.  Extender el estudio de xv6 viendo las distintas reacciones ocurridas al modificar el quantum y ponerlo a prueba con los test dados en la catedra.
3.  Empezar a modificar el planificador estándar de xv6 por MLFQ. Para esto y antes que nada deberemos implementar las prioridades de los programas a ejecutar.
4.  Implementación del planificador MLFQ

***A continuación describiremos que se hizo en cada Tarea, los problemas que surgieron y su las soluciones que les dimos.***

## Primera Parte

### Ejercicio 1:

Esta primera parte fue más bien de lectura y comprensión por lo que no nos fue de mucha dificultad, entre los tres estudiamos el código de la función **scheduler()** del archivo **proc.c** y si bien al principio presidimos de la comprensión total de la función **switchkvm()** pensamos que era importante tener que entender que realizaba **acquire()** y **release()** para poder contestar con certeza, aun así nosotros después de leer el archivo **lapic.c** ya teníamos la sospecha de un planificador en particular. Después de la clase de Nico sobre *look y unlook* y la lectura de **spinlook.c** comprendimos bien y llegamos a la conclusión de que era un RR (Round-robin) de un quantum, de momento, complejo.

### Ejercicio 2:

Para este ejercicio pusimos pilas al estudio y comprensión del archivo **lapic.c**, centrándonos concretamente en la linea 69, donde se encuentra la llamada:

```
lapicw(TICR, 10000000)
```

Que sin entender al 100% que es lo que esto realizaba pudimos encontrar, donde tocar para modificar el quantum, ya sea de forma directa o indirecta. Ahora para poder responder la pregunta "¿cuanto tiempo dura el quantum en xv6?" tuvimos que recurrir nuevamente al estudio del código, llegando así a la siguiente conclusión:
Un **timer interrupt** es la interrupción que hace el sistema operativo cada un periodo de tiempo para así ganar el control del cpu, podremos decir que un quantum es la distancia temporal entre dos timer interrupt, donde dicha distancia estará expresada en *Ticks*. Ya con esto pudimos entender mejor la función **lapicw()** y saber que el quantum dura diez millones de Ticks. Si se quisiera alterar este tiempo bastaría con cambiar el valor de variable predeterminado de la función **lapcw()**

## Segunda Parte

$$
Grafico...


$$

## Tercera Parte

### Ejercicio 1:

### Ejercicio 2: