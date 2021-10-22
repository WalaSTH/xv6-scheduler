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

$\text{A continuación describiremos que se hizo en cada Tarea,}$
$\text{los problemas que surgieron y su las soluciones que les dimos.}$

## Primera Parte

### Ejercicio 1:

Esta primera parte fue más bien de lectura y comprensión por lo que no nos fue de mucha dificultad, entre los tres estudiamos el código de la función `scheduler()` del archivo **proc.c** y si bien al principio presidimos de la comprensión total de la función `switchkvm()` pensamos que era importante tener que entender que realizaba `acquire()` y `release()` para poder contestar con certeza, aun así nosotros después de leer el archivo **lapic.c** ya teníamos la sospecha de un planificador en particular. Después de la clase de Nico sobre *look y unlook* y la lectura de **spinlook.c** comprendimos bien y llegamos a la conclusión de que era un RR (Round-robin) de un quantum, de momento, complejo.

### Ejercicio 2:

Para este ejercicio pusimos pilas al estudio y comprensión del archivo **lapic.c**, centrándonos concretamente en la linea 69, donde se encuentra la llamada:

```
lapicw(TICR, 10000000)
```

Que sin entender al 100% que es lo que esto realizaba pudimos encontrar, donde tocar para modificar el quantum, ya sea de forma directa o indirecta. Ahora para poder responder la pregunta "¿cuanto tiempo dura el quantum en xv6?" tuvimos que recurrir nuevamente al estudio del código, llegando así a la siguiente conclusión:
Un **timer interrupt** es la interrupción que hace el sistema operativo cada un periodo de tiempo para así ganar el control del cpu, podremos decir que un quantum es la distancia temporal entre dos timer interrupt, donde dicha distancia estará expresada en $Ticks$. Ya con esto pudimos entender mejor la función `lapicw()`y saber que el quantum dura diez millones de Ticks. Si se quisiera alterar este tiempo bastaría con cambiar el valor de variable predeterminado de la función `lapcw()`

## Segunda Parte

$\text{Grafico...}$

## Tercera Parte

### Ejercicio 1:

Para este ejercicio se agrego el campo $prio$ en la estructura del proceso donde se guardara una prioridad de proceso que tendrá un rango de {0,1,2}, de la siguiente forma:

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

Nuestro siguiente objetivo es lograr que al iniciar un nuevo proceso se le asigne la mayor prioridad `prio = 0`
Para esto agregamos la inicialización en cero del estado prio junto a la inicialización del proceso en cuestión en la función `allocproc()` del archivo **proc.c**. Ahora dentro de la función `scheduler()` agregamos la definición:

```
struct proc *p, *p1, *hprio;
```

Donde *p* es el proceso evaluado, *p1* sera usado como demás procesos y *hprio* donde guardaremos el de mayor prioridad. Con esto, e implementado de forma correcta, nos aseguraremos de siempre correr el el programa con mayor prioridad.

### Ejercicio 2:
