readme

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

A continuación describiremos que se hizo en cada Tarea, los problemas que surgieron y su las soluciones que les dimos.

## Primera Parte

### Ejercicio 1:

Esta primera parte fue más bien de lectura y comprensión por lo que no nos fue de mucha dificultad, entre los tres estudiamos el código de la función `scheduler()` del archivo **proc.c**. Al analizar dicha función nos encontramos con muchas cosas que nos resultaban desconocidas así que tratamos de concentrarnos en la parte más conceptual del algoritmo sin dejarnos perder por las funciones y estructuras que desconocíamos. Comenzamos estudiando la estructura ptable, la cual contiene todos los procesos del sistema operativo, entender esto fue fundamental ya que nos permitió ver que el segundo for efectivamente recorre cada uno de los procesos, buscando por uno que este en estado RUNNABLE. A continuación se utilizan distintas funciones de cambio de contexto, sin embargo nos fue prescindible entenderlas al 100% debido a un comentario posterior al ultimo cambio de contexto

```
switchkvm();

      // Process is done running for now.
      // It should have changed its p->state before coming back.
```

Esto nos dio a entender, que lo que hace el algoritmo es elegir un preoceso en estado RUNNABLE, lo ejecuta por un lapso de tiempo y lo suelta. Con esto concluimos que el scheduler que utiliza XV6 es un RR (Round Robin)

### Ejercicio 2:

Intentamos buscar el quantum por varios caminos pero el camino que nos llevo resultado buscado fue buscar la buscar la función `yield()` utilizando la herramienta `grep -r` de bash. buscamos `yield()` ya que sabemos, gracias a la siguiente foto adjunta, que esta función permite a los procesos desplanificarlos, por tanto intuimos que el quantum estaba involucrado en este proceso.

![XV6 FSA](https://media.discordapp.net/attachments/882386883643056129/897971286628761651/unknown.png?width=418&height=373)

Así fue como llegamos al directorio **trap.c** , en el caul encontramos la linea de codigo:

```
// Force process to give up CPU on clock tick.
  // If interrupts were on while locks held, would need to check nlock.
  if(myproc() && myproc()->state == RUNNING &&
     tf->trapno == T_IRQ0+IRQ_TIMER)
    yield();
```

Para posteriormente rastrear valores **T_IRQ0** y **IRQ_TIMER** para finalmente llegar al directorio **lapic.c**. Nos enfocamos en su estudio y comprensión, centrándonos así concretamente en la linea 69, donde se encuentra la llamada:

```
lapicw(TICR, 10000000)
```

Que sin entender al 100% que es lo que esto realizaba pudimos encontrar, donde tocar para modificar el quantum, ya sea de forma directa o indirecta. Ahora para poder responder la pregunta "¿cuanto tiempo dura el quantum en xv6?" tuvimos que recurrir nuevamente al estudio del código, llegando así a la siguiente conclusión:
Un **timer interrupt** es la interrupción que hace el sistema operativo cada un periodo de tiempo para así ganar el control del cpu, podremos decir que un quantum es la distancia temporal entre dos timer interrupt, donde dicha distancia estará expresada en Ticks. Ya con esto pudimos entender mejor la función `lapicw()`y saber que el quantum dura diez millones de Ticks. Si se quisiera alterar este tiempo bastaría con cambiar el valor de variable predeterminado de la función `lapicw()`

## Segunda Parte

### Sobre los experimentos

Los experimentos consistían en ejecutar programas dados por la cátedra en distintos escenarios y situaciones. La forma que se llevó a cabo de realizar dichos experimentos fue ejecutar cada caso en un lapso de 4 minutos respetando lo siguiente

- Ejecutar los programas siempre en la misma computadora
- Ejecutar siempre imitando el contexto usado en la primer medición (i.e programas abiertos,procesos,conexiones etc )
- Emular qemu con un solo procesador

Todas las métricas generadas por los programas se redirigieron a archivos de texto dentro de xv6 para que puedan ser manipulados.

### ¿Cómo se organizó la información?

Durante este laboratorio se tuvo que manipular y trabajar con muchos datos generados de los distintos experimentos que se debían realizar, por tanto uno de los principales desafíos de este trabajo fue el plantear cómo íbamos a organizar, comparar y mostrar toda esta información. A continuación se detallará por lo que se ha optado en este proyecto.

Como decisión central se eligió, basándonos en el dataset, que la mejor forma de poder comparar, analizar y compartir los resultados sería usando gráficos de barra.
Antes de pasar a la descripción de los gráficos se debe aclarar que las métricas que forman parte de los gráficos son un promedio de los datos obtenidos en cada caso de experimentación.

### Descripción general de los gráficos:

Aclaración sobre la terminología: En este informe llamamos “caso” a cada distinta forma de ejecución de los programas en experimentación, o sea a las ejecuciones n cpubench; m iobench, con n,m enteros en el intervalo cerrado \[0,2\]. Y llamamos escenario a la realización de estos casos con distintos quantums.

En el eje x se encuentra los distintos casos de experimentación
En el eje y se hallan la unidad de medida (puede ser KFPT o IOPT)
En cada caso se encuentra distintas barras distinguidas por color, las cuales representan el valor promedio del respectivo caso pero en distintos escenarios.
Cada uno de estos gráficos se hace por scheduler (RR,MLFQ)

Debido a que trabajamos con 2 unidades de medida distintas cada una de las gráficas de schedulers se tuvo que separar en 2, una donde en el eje y se encuentra Kilo Flops Per Tick, la otra donde en el eje y se encuentra IO Per Tick.

¿Por qué optamos por esta forma? creemos que esta forma de organización de datos permite una rica comparación de los resultados tanto si la comparación es entre casos,escenarios y/o schedulers. Además facilita el análisis global de todos los datos, permite utilizar toda la información recolectada y minimiza notablemente la cantidad de gráficos necesarios

### Sobre la automatización de los gráficos

A continuación se describirá brevemente cómo se desarrolló el script que manipula la información y que genera los gráficos.
El lenguaje de programación utilizado para esta tarea fue python, se optó por este debido a su facilidad y la disposición de librerías que tiene para este tipo de tareas.
Lo primero que se hizo luego de realizar los experimentos fue copiar y pegar los resultados de los .txt en archivos .csv fuera de xv6. Optamos por este formato de archivo ya que debido a cómo es la salida de los benchs, si tomamos como delimitador el espacio (‘ ‘) entonces se facilita mucho la obtención de de las métricas que nos interesan.
Una vez teniendo estos datos en .csv fue muy fácil manipularlos en python y obtener el promedio de cada uno.
Dentro de este programa se decidió usar la estructura de datos diccionario de python, donde un diccionario representa un escenario específico n, con n entero en \[0,3\], y cada elemento del diccionario es un caso de experimento, y su valor es el respectivo promedio.
El procesos que realiza esta transformación (de .csv a los diccionarios) es la función

***PRE: Se asume que los nombres de los directorios coinciden con el patrón pre establecido***
`readScenary(esPath,form)`

Donde:

- esPath es un string que representa la ruta relativa del escenario que se quiere obtener. Ej: “Escenario0”
- form es un char que representa qué tipo de experimento queremos (Cpu o IO) puede tomar valores ‘c’ o ‘i’

Como se mencionó anteriormente, la función asume que los nombres de los archivos cumplen con cierto patrón, he aquí el patrón necesario:

“Casoi_f-n-m.csv” donde:
i representa el caso y es un entero en el intervalo \[0,7\]
f representa el tipo del experimento, puede ser ‘c’ o i’
n,m son enteros que representan en caso y el ID del programa (en caso que se hagan mas de un cpubench y/o iobench)

Ejemplo: Caso5_i-5-2.csv representa el caso 5, iobench siendo el segundo que se ejecuta.

*Se debe respetar el formato de forma estricta, ya que el script NO usa expresiones regulares.*

Esta función entra al directorio que se le paso, busca todos los .csv que coincidan con el nombre preestablecido que debe tener el archivo, los que sean de un mismo caso los promedia, y luego lo agrega al diccionario que retorna.
Finalmente la función que realiza los gráficos es makeChart(esPath,form) la cual usa la función anterior para crear los diccionarios y finalmente se usa el módulo matplotlib para la realización de los gráficos.

* * *

A continuación analizaremos y compararemos todos los datos contenido y sacaremos conclusiones

### Análisis de gráfica de IO

![IOBENCH Metricas RR](https://media.discordapp.net/attachments/882386883643056129/902297867371282442/unknown.png?width=697&height=397)

Los mejores resultados en todos los distintos escenarios siempre están dados por el caso 0 (1 iobench) y el caso 7 (2 iobench). Es muy interesante observar que al comparar estos 2 casos se aprecia que cuando RR funciona con el quantum por defecto el claro ganador es el caso que ejecuta sólo un iobench, pero a medida que lo vamos disminuyendo empiezan a tener resultados similares hasta que en el último escenario con el quantum mas chico el caso 7 tiene un mejor desempeño.

Los peores resultados se aprecian en todos los casos que hay por lo menos un cpubench, la gráficas muestran un cambio significativo en comparación con los otros casos. Esto ocurre porque cuando corremos los casos con cpubench estos programas consumen siempre todo su quantum y por tanto los programas IO en cada ronda deben esperar a que estos procesos cpu-bound suelten el procesador. Una consecuencia de esto es que efectivamente se aprecia en la gráfica que si fijamos un caso de los que tienen cpu vemos que si disminuimos su quantum su rendimiento mejora, ya que estos procesos cpu-bound sueltan antes el procesador permitiendo a los programas IO-bound un mejor desempeño.

#### Resumen

- Disminuir el quantum empeora el rendimiento de los casos que solo tienen iobenchs y mejora los casos que mezclan iobench con cpubench (Exceptuando por el escenario 4 )
    
- La mayor cantidad de IOPT obtenida fue en el caso 0 con quantum por defecto
    
- La menor cantidad de IOPT obtenida fue en el caso 2 con quantum/1000 (Escenario 3)
    
- El escenario con mejor promedio es el escenario 2 (quantum/100) siendo estos los resultados:
    
    ```
         	Escenario 0: 1742.6709602767417
      	Escenario 1: 2025.1486125378076
      	Escenario 2: 2303.985178609142
      	Escenario 3: 1085.7201714348455 
    ```
    

### Análisis de gráfica de CPU

![IOBENCH Metricas RR](https://media.discordapp.net/attachments/882386883643056129/902297312250974299/captura_3.png?width=685&height=397)

*Aclaración :
En esta parte del análisis se optó por dividir el gráfico en 2 ya que el escenario 3 no se puede apreciar debido a las escalas utilizadas.*

Al analizar los resultados de cpubench para RoundRobin una cosa nos queda clara: El mejor escenario es el que tiene el quantum por defecto, es decir aquél con mayor quantum.
La diferencia es bastante visible, siendo por ejemplo el desempeño 10 veces mayor en el quantum por defecto comparado al quantum 10 veces menor.
En el caso en el que solo tenemos un cpubench corriendo, el quantum por defecto promedia en 577 Kflops mientras que para un quantum 10 veces menor promedia en 53 Kflops, luego para 100 veces menor es de 2,4 kflops y finalmente el escenario con quantum 1000 veces menor promedia en apenas 1 Kflop.
Lo que estamos viendo acá es que claramente en lo que disminuimos el quantum, el performance de cpubench disminuye.
Esto ocurre porque mientras mayor sea el quantum el scheduler se comporta cada vez más parecido a un FIFO, el cual es muy beneficioso para procesos CPU bound (es decir, aquellos que pasan el mayor tiempo de ejecucion utilizando el procesador). Si el quantum es el tiempo que le voy a prestar a un proceso el CPU antes de quitarselo, cuanto mayor sea este tiempo, mejor será su desempeño.
El resultado entonces resulta bastante intuitivo, al disminuir este quantum a lo largo de los escenarios vemos como cpubench comienza a tener peor y peor desempeño, al punto de que para un quantum mil veces menor es muy dificil de ver en la grafica su resultado, y tenemos que recurrir a una segunda grafica auxiliar con otra escala.
Otra cosa que podemos sacar de estos resultados es como se comporta cpubench junto con otros procesos. Concretamente cuando tiene otros cpubench o iobench corriendo en paralelo.
Como se puede ver en el grafico, el mejor resultado de cpubench se obtiene cuando no hay otro cpubench corriendo a la vez. Es decir cuando o bien no tiene que compartir el cpu, o bien tiene que hacerlo con iobench.
Esto se contempla en el primer, tercer y cuarto caso, en los que en ninguno se tiene más de un cpubench corriendo en paralelo. Luego en el resto de casos vemos que el rendimiento de cpubench baja a un poco más de la mitad.
¿Por que ocurre esto?
Sencillo, cuando cpubench tiene que compartir tiempo de CPU con iobench, este no tiene mucho problema, ya que iobench es un proceso IO bound, lo que significa que ocupará poco tiempo de CPU y podrá devolver rápidamente el procesador a cpubench para continuar ejecutandose hasta que se acabe su quantum.
Distinto es el caso en el que corremos dos cpubench en paralelo. Cuando esto ocurre, tenemos dos procesos CPU bound compartiendo el procesador. Ambos querrán utilizar todo su quantum, así que uno debe esperar que el otro termine antes de continuar. Una forma de verlo es que si tenemos dos procesos CPU bound, hay que dividir el tiempo de CPU en dos, y no nos preocupamos tanto por procesos IO bound, pues estos no están muy interesados en utilizar mucho tiempo el CPU. Es por esto que a la hora de correr dos cpubench en paralelo, para todos los escenarios de quantums distintos, el performance disminuye a un valor cercano a la mitad.

#### Resumen:

Para concluir podemos decir que para procesos CPU bound, el quantum es muy importante. Estos al utilizar mucho el CPU es facil pensar que van a mejorar en su desempeño si les damos más tiempo de CPU, y empeorar si les damos menos. Ademas, que si tenemos multiples procesos CPU bound, estos al tener que compartir tiempo de CPU van a empeorar su desempeño, a diferencia de tener que compartirlo con procesos IO bound que no van a “robarle” su preciado tiempo de CPU. Ambas conclusiones son apreciables en los graficos.

## Tercera Parte

### Ejercicio 1:

Para este ejercicio se agrego el campo **prio** en la estructura del proceso, donde se guardara una prioridad de proceso que tendrá un rango de {0,1,2}, de la siguiente forma:

```
#define NPRIO 3

// Per-process state
struct proc {
  uint sz;                     // Size of process memory (bytes)
  pde_t* pgdir;                // Page table
  char *kstack;                // Bottom of kernel stack for this process
  enum procstate state;        // Process state
  int pid;                     // Process ID
  struct proc *parent;         // Parent process
  struct trapframe *tf;        // Trap frame for current syscall
  struct context *context;     // swtch() here to run process
  void *chan;                  // If non-zero, sleeping on chan
  int killed;                  // If non-zero, have been killed
  struct file *ofile[NOFILE];  // Open files
  struct inode *cwd;           // Current directory
  char name[16];               // Process name (debugging)
  int prio;                    // Process scheduler priority
};
```

Nuestro siguiente objetivo es lograr que al iniciar un nuevo proceso se le asigne la mayor prioridad `prio = 0`.
Para esto lo que hicimos fue localizar donde se creaban los procesos y esto nos llevo a la función `allocproc()` del archivo **proc.c**, una vez ahí agregamos la inicialización del estado prio junto a la inicialización del proceso en cuestión. Pensamos que esté era el lugar indicado ya que dicha función buscara de la ptable aquellos nuevos procesos cuales se encuentran con el estado UNUSED, para posteriormente ser cambiados por EMBRYO. Por lo tanto es en este lugar donde nosotros creemos que es optimo inicializar su prioridad.
Ahora para descender la prioridad no nos fue, tampoco fue de mucha dificultad la implementación, sin embargo y al igual que en el ejercicio anterior, tuvimos que detenernos a pensar en que momento, de la vida del programa, hay que bajar la prioridad. Utilizando la imagen referenciada en el ejercicio dos, de la primera parte, y el documento adjunto a la cita más relevante, llegamos a la siguiente conclusión:

[XV6-Sched-Sync.pdf](https://www.google.com/url?sa=t&rct=j&q=&esrc=s&source=web&cd=&ved=2ahUKEwip-c3_i-HzAhWkr5UCHbiWB5kQFnoECAYQAQ&url=https%3A%2F%2Fwww.cse.iitb.ac.in%2F~mythili%2Fteaching%2Fcs347_autumn2016%2Fnotes%2F06-xv6-sched-sync.pdf&usg=AOvVaw1wDT_dAjk-fbIiVi6OUniy)

"A process that wishes to relinquish the CPU calls the function sched. This function triggers a context switch, and when the process is switched back in at a later time, it resumes execution again in sched itself. Thus a call to sched freezes the execution of a process temporarily.

When does a process relinquish its CPU in this fashion? When a timer interrupt occurs and it is deemed that the process has run for too long, the trap function calls yield, which in turn calls sched.

When a process terminates itself using exit, it calls sched one last time to give up the CPU

When a process has to block for an event and sleep, it calls sched to give up the CPU. The function sched simply checks various conditions, and calls swtch to switch to the scheduler thread."

Con esto entendido, implementamos dentro de la función `yield()`
una condición para aquellos programas con indice de prioridad menor a dos, tal que se les sume un punto. Es importante recordar que las prioridades están dadas en valores de {0,1,2} donde cero es la mayor prioridad y dos la menor.

## Cuarta Parte

Habiendo concluido la tercera parte, ahora nuestros procesos tienen prioridades asignadas, y estas variarán según cuanto usen el CPU, siendo las que piden mucho tiempo de CPU las que bajen de prioridad, y las que necesiten menos las que suban de prioridad, donde en total tenemos tres niveles de prioridad (0, 1 y 2) y a menor numero, mayor prioridad.
El objetivo de esta tarea es aprovechar estas prioridades para obtener un planificador más inteligente, que sepa utilizar las prioridades mara maximizar el uso del hardware. Asi nace el concepto de Multilevel Feedback Queue (MLFQ), un sistema de planificacion que ejecute primero aquellos procesos con mayor prioridad, y que utilice la experiencia para determinar la prioridad de un proceso.
Lo resuelto en la parte tres responde el cómo aprender de la experiencia para determinar la prioridad de un proceso. Al utilizar un proceso todo su quantum, esto significa que es un proceso aparentemente CPU bound, y convendría bajarle su prioridad, ya que mientras este se ejecute perdemos interactividad con el sistema. Y analogamente, al utilizar un proceso menos tiempo del CPU de lo que permite un quantum, subir su prioridad, ya que es un proceso que aparenta ser IO bound, es decir que va a dedicarse mayoritariamente a actividades de entrada y salida, y no va a requerir tanto tiempo en el CPU. Estos son los procesos que queremos que tengan prioridad, ya que son los procesos interactivos, y podemos esperar a que se bloqueen al hacer una operacion input/output para recien entonces correr los procesos más CPU bound que tendrán menor prioridad.
Podemos pensar entonces a los procesos ubicados en diferentes colas, segun su prioridad asignada.
Sumado a las reglas introducidas en la parte tres, en esta parte se introducen dos nuevas reglas:
MLFQ regla 1: Si el proceso A tiene mayor prioridad que el proceso B, corre A. (y no B) MLFQ regla 2: Si dos procesos A y B tienen la misma prioridad, corren en round-robin por el quantum determinado.
Reglas que en su total describen el comportamiento del planificador MLFQ.
Genial, entonces nos queda una pregunta, ¿Como implementamos MLFQ en xv6?
Para conseguirlo, debemos modificar el planificador por defecto, el cual funciona con Round-Robin y se encuentra en el modulo proc.c.

```
void
scheduler(void)
{
..
 for(;;){   
 acquire(&ptable.lock);
   for(p = ptable.proc; p < &ptable.proc[NPROC]; p++){
     if(p->state != RUNNABLE)
       continue;

```

Vemos que lo que hace el planificador es, luego de adquirir y lockear la tabla de procesos, itera en ella hasta encontrar un proceso cuyo estado sea el de runnable, que es equivalente a listo o ready, y una vez encontrado simplemente lo ejecuta, realizando el context switch, y luego liberando esta tabla de procesos para que se vuelva actualizar, y finalmente ejecutando el procesos de nuevo. Mientras itera la tabla, cuando un proceso no cumple la condicion necesaria para ser ejecutado, se descarta y se sigue iterando en la tabla.
Bien, nuestro primer acercamiento a un modelo MLFQ entonces es el siguiente:
Al iterar por la tabla de procesos buscamos uno que ademas de tener el estado de runnable, tenga la prioridad deseada. Queremos empezar a buscar procesos con la prioridad más alta (0) y si no encontramos ningun proceso con dicha prioridad, entonces ahí la bajamos y repetimos. Entonces creamos una variable que nos indique esta prioridad deseada y la inicializamos en 0, y luego cambiaremos la condicion que cumple un proceso para ser descartado.

```
void
scheduler(void)
{
..
 int curr_pri = 0;
 for(;;){
   sti();
   acquire(&ptable.lock);
   for(p = ptable.proc; p < &ptable.proc[NPROC]; p++){
     if(p->state != RUNNABLE || p->prio != curr_pri){
```

ahora al iterar en la tabla de procesos, descartaremos aquellos que o bien no sean runnable, o bien no tengan la prioridad deseada.
Genial, ahora si hallamos un proceso con prioridad 0, este será ejecutado. Pero, ¿que ocurre si llegamos al final de la tabla y no hemos encontrado procesos?
Entonces es necesario saber en que posicion de la tabla estamos al iterar, y si estamos en la utlima, ya que es aquí cuando tomamos una desicion: bajamos la prioridad requerida y volvemos a iterar, ¿y si ya recorrimos las tres prioridades y no hubo procesos? debemos salir del ciclo for, liberar la ptable y volver a empezar todo de nuevo.
Entonces un contador “co” que se actualice en cada iteracion del for nos ayudará a saber en que posicion nos encontramos, para tomar las decisiones segun el caso.

```
co = 0;
..
   for(p = ptable.proc; p < &ptable.proc[NPROC]; p++){
     co++;
     if(p->state != RUNNABLE || p->prio != curr_pri){
       if(co > 63){
         //We have reached the end of the table

```

entonces si llegamos al final de la tabla, entrará al if y podremos tomar la desicion.
Otra cuestion importante: Regla 2.
La regla 2 de MLFQ dice: Si dos procesos A y B tienen la misma prioridad, corren en round-robin.

A nuestra forma de entender, en el momento de recorrer una cola de prioridad X, debemos ejecutar todos los procesos que hayan llegado en ese instante a esa cola.
La pregunta que nos hicimos es: ¿Qué ocurre luego de ejecutar un proceso?
¿Volvemos a refrescar la tabla de procesos y arrancamos de nuevo buscando con la prioridad 0?
La respuesta final, que cumple con la condicion de la regla dos es que si estamos iterando en la process table con una prioridad, por ejemplo 1, debemos correr en round-robin todos los procesos que en ese instante (en ese aquire de la p-table) tengan prioridad 1, y una vez terminemos de correrlos, ahi si volver a actualizar la tabla de procesos en busqueda de los que esten en la prioridad más alta (0). Lo que esto produce es que si dos procesos tienen la misma prioridad, se ejecutan en RR, pero que si luego llega un proceso de mayor prioridad, volvamos a la primer cola luego de terminar el RR en la actual cola. Solo vamos a bajar de prioridad si no hemos encontrado ningun proceso a ejecutar (runnable) en nuestra cola de prioridad actual, pero si encontramos alguno, ejecutamos todos los que tengan esa prioradad en RR y luego al llegar al final de la cola, volvemos al empezar todo de nuevo, buscando desde la prioridad más alta.
Una solucion como esta puede producir starvation, es decir que haya procesos que nunca se corran, ya que si por ejemplo siempre tenemos procesos con prioridad 0 y 1 en estado runnable en cada aquire de la process table, si tambien tenemos algunos con prioridad 2 listos para ser ejecutados, estos nunca llegarán a ejecutarse.
Por eso fue necesario crear una variable booleana found, que vale 0 si en la cola no apareció ningun proceso, o vale 1 si hemos ejecutado al menos 1. Si hemos ejecutado al menos 1, esto significa que si llegamos al final de la process table debemos volver a subir, ya que hemos terminado de hacer el RR para los procesos de igual prioridad. Si vale 0, significa que en esta prioridad no hemos encontrado ningun proceso en runnable, y debemos bajar a buscar en las colas más bajas.
Entonces, el codigo, al la hora de ejecutar un proceso, se ve asi:

```
     c->proc = p;
     switchuvm(p);
     p->state = RUNNING;
     swtch(&(c->scheduler), p->context);
     switchkvm();
...
     c->proc = 0;
     found = 1; //Means we have executed at least one proccess on this priority queue;
     continue;
Para luego, en caso de llegar al final de la process table, tomar la decision:
 
     if(p->state != RUNNABLE || p->prio != curr_pri){
       if(co > 63){
         //We have reached the end of the table
         co = 0;
         if (found){
         //We ran one or multiple proccesses on this priority, so we should go back to first priority queue
             found = 0;
             curr_pri = 0;
             goto end; //Exit and re-aquire ptable
         }
         //We did not enconter any process in this priority, so we must search on lower queues
         p = ptable.proc;
         curr_pri++;

```

Si no se cumple found, entonces debemos volver a iterar en la tabla, pero esta vez buscando con una prioridad inferior.

Finalmente, el planificador queda de la siguiente manera:
```
void
scheduler(void)
{
  struct proc *p;
  struct cpu *c = mycpu();
  c->proc = 0;
  int curr_pri = 0;
  int co;
  int found = 0;
  for(;;){
    // Enable interrupts on this processor.
    sti();
    // Loop over process table looking for process to run.
    co = 0;
    acquire(&ptable.lock);
    for(p = ptable.proc; p < &ptable.proc[NPROC]; p++){
      co++;
      if(p->state != RUNNABLE || p->prio != curr_pri){
        if(co > 63){
          //We have reached the end of the table
          co = 0;
          if (found){
          //We ran one or multiple proccesses on this priority, so we should go back to first priority queue
              found = 0;
              curr_pri = 0;
              goto end; //Exit and re-aquire ptable
          }
          //We did not enconter any process in this priority, so we must search on lower queues
          p = ptable.proc;
          curr_pri++;
          if(curr_pri > NPRIO){
              //We searched through all queues with no luck
              //Exit and re-aquire ptable
              curr_pri = 0;
              goto end;
          }
        }
        continue;
      }
      // Switch to chosen process. 
      c->proc = p;
      switchuvm(p);
      p->state = RUNNING;
      swtch(&(c->scheduler), p->context);
      switchkvm();
      // Process is done running for now.
      // It should have changed its p->state before coming back.
      c->proc = 0;
      found = 1; //Means we have executed at least one proccess on this priority queue;
      continue;
    }
end:
    release(&ptable.lock);
  }
}
```

Sumando algunas cosillas extras en el codigo, esta implementacion asegura las dos reglas que faltaban de MLFQ:

- Debido a que primero buscamos y ejecutamos aquellos procesos en estado runnable con mayor prioridad, y solo buscamos en colas de menores prioridades si en las mayores no encontramos nada, se cumple que: Si el proceso A tiene mayor prioridad que el proceso B, corre A. (y no B)
- Y debido a que si encontramos un proceso en una cola, entonces terminamos de correr dicha cola antes de volver a empezar todo de nuevo con la prioridad más elevada, se cumple que: Si dos procesos A y B tienen la misma prioridad, corren en round-robin por el quantum determinado.

Concluyendo así con la implementación de MLFQ.
