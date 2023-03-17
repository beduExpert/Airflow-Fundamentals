## Sesión 1: Introducción a Apache Airflow 🤖

<div style="text-align: justify;">

### 1. Objetivos :dart: 

- Instalación de Docker-Desktop
- Ejecución de Apache Airflow usando Docker-Desktop
- Configuración del ambiente de desarrollo con VS Code
- Exploración de la interfaz web

### 2. Contenido :blue_book:

Uno de los objetivos principales de está sesión es configurar un ambiente local de desarollo para Airflow, identificar y entender las distintas piezas que componen la arquitectura de la plataforma, y finalmente familiarizarse con el ciclo de desarrollo y la interfaz web de Airflow.

---

#### <ins>Tema 1. Instalación de Docker-Desktop</ins>

![image](/Sesion-01/assets/img/docker.png)
En este tema se describe el proceso de instalación de Docker/Docker Desktop.

- [**`Mac OS Ventura 13 M1`**](/Sesion-01/Ejemplo-01/mac_os_ventura_13_1_instalacion_docker_desktop.md)
- [**`Ubuntu 22.04 x64`**](/Sesion-01/Ejemplo-01/ubuntu_22_04_instalacion_docker_desktop.md)
- [**`Windows 10 Pro x64`**](/Sesion-01/Ejemplo-01/windows_10_instalacion_docker_desktop.md)

> Nota: El proceso de instalación puede variar dependiendo de la versión del sistema operativo y el hardware de tu equipo.

---

**Reto #1** 

El primer reto consiste en seguir una de las guías anteriores para instalar Docker-Desktop y resolver los posibles conflictos de instalación usando la experiencia del equipo.

> Nota: [Aqui](/Sesion-01/Reto-01/requerimientos_de_sistema_para_docker_desktop.md) encontrás los requerimientos mínimos recomendados por Docker.

---

<img src="images/structure.png" align="right" height="90"> 

#### <ins>Tema 2. Ejecución de Apache Airflow usando Docker-Desktop</ins>

![image](/Sesion-01/assets/img/airflow_banner.jpg)
En este tema describiremos los pasos necesarios para levantar los servicios contenerizados de Airflow.

Utilizaremos la última versión de Airflow disponible a la fecha de elaboración de este contenido: 2.5.1. La siguiente tabla muestra un resumen de las últimas versiones, puedes consultar la tabla original usando la siguiente [liga](https://airflow.apache.org/docs/apache-airflow/stable/installation/supported-versions.html).


| Version | Current Patch/Minor | State     | First Release | Limited Support | EOL/Terminated |
|---------|---------------------|-----------|---------------|-----------------|----------------|
| 2       | 2.5.1               | Supported | Dec 17, 2020  | TBD             | TBD            |
| 1.10    | 1.10.15             | EOL       | Aug 27, 2018  | Dec 17, 2020    | June 17, 2021  |
| 1.9     | 1.9.0               | EOL       | Jan 03, 2018  | Aug 27, 2018    | Aug 27, 2018   |
| 1.8     | 1.8.2               | EOL       | Mar 19, 2017  | Jan 03, 2018    | Jan 03, 2018   |
| 1.7     | 1.7.1.2             | EOL       | Mar 28, 2016  | Mar 19, 2017    | Mar 19, 2017   |
---

**Reto #2**

El reto correspondiente a este tema consiste en seguir la guía de [**`Ejecución de Airflow con contenedores`**](/Sesion-01/Ejemplo-02/ejecucion_de_airflow_con_contenedores.md) y utilizar la experiencia de equipo para resolver los problemas que puedan surgir en el proceso.

---

#### <ins>Tema 3. Instalar y configurar VS Code</ins>
![image](/Sesion-01/assets/img/vscode.png)

Utilizaremos VS Code durante todo el curso porque es multiplataforma y cuenta con herramientas, en forma de plugins, para trabajar con Python y Docker.

[**Ejemplo de instalación de herramientas de desarrollo**](Sesion-01/Ejemplo-03/preparar_ambiente_de_desarrollo.md)

---
**Reto #3**

Este reto consiste en instalar VS Code y crear un ambiente virtual para Python siguiendo las siguientes [instrucciones](/Sesion-01/Ejemplo-03/preparar_ambiente_de_desarrollo.md).

---
#### <ins>Tema 4. Exploración la interfaz web</ins>
![image](/Sesion-01/assets/img/airflow_ui.png)
 En este [tema](/Sesion-01/Ejemplo-04/README.md) ejecutaremos un DAG de ejemplo y exploraremos las distintas vistas en la interfaz web de Airflow.

---

**Reto #4**

La finalidad de este [reto](/Sesion-01/Reto-04/familiarizacion_con_la_interfaz_web.md
) es que utilces las distintas vistas de DAG y ejecutes algunas de las acciones disponibles desde la interfaz de Airflow.


---
<br/>


</div>

