# Instalación de Docker Compose

## Ubuntu 20.04 LTS

Aquí hay un tutorial para instalar Docker Compose con Brew en Ubuntu 22.04 LTS, incluyendo los pasos para instalar Brew:

1. Abre un terminal en tu sistema Ubuntu.
2. Ejecuta el siguiente comando para instalar Brew:

    ```bash
    sh -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/master/install.sh)"
    ```

3. Agrega el repositorio de Brew a tu PATH con el siguiente comando:

    ```bash
    echo 'export PATH="/home/linuxbrew/.linuxbrew/bin:$PATH"' >>~/.bashrc
    ```

4. Actualiza la sesión actual de tu terminal con el siguiente comando:

    ```bash
    source ~/.bashrc
    ```

5. Verifica la instalación de Brew con el siguiente comando:

    ```bash
    brew doctor
    ```

6. Ejecuta el siguiente comando para asegurarte de tener una versión reciente de Brew:

    ```bash
    brew update
    ```

7. Instala Docker Compose con el siguiente comando:

    ```bash
    brew install docker-compose
    ```

8. Verifica la versión de Docker Compose instalada con el siguiente comando:

    ```bash
    docker-compose -v
    ```

9. Para asegurarte de que Docker Compose está funcionando correctamente, ejecuta el siguiente comando para crear un archivo de configuración de ejemplo:

    ```bash
    docker-compose config
    ```

10. Si se muestra una salida que contiene información sobre la configuración, entonces Docker Compose está funcionando correctamente en tu sistema Ubuntu.

##  Mac OS

Utilizaremos el manejador de paquetes Homebrew para instalar Docker Compose.
Si ya tienes instalado Homebrew sigue los pasos de instalación de Docker Compose.

1. Abre la terminal en tu Mac y ejecuta el siguiente comando para instalar Homebrew:

    ```bash
    /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/master/install.sh)"
    ```

2. Ejecuta el siguiente comando para asegurarte de que la instalación de Homebrew se haya completado correctamente:

    ```bash
    brew doctor
    ```

3. Para asegurarte de que la última versión de Homebrew esté instalada, ejecuta el siguiente comando:

    ```bash
    brew update
    ```

4. Verifica la instalación de Homebrew con el siguiente comando:

    ```bash
    brew -v
    ```

5. Abre la terminal en la Mac y ejecuta el siguiente comando para instalar Docker Compose:

    ```bash
    brew install docker-compose
    ```

6. Verifica la instalación de Docker Compose con el siguiente comando:

    ```bash
    docker-compose --version
    ```

7. Ejecuta el siguiente comando para verificar que Docker está instalado y funcionando correctamente:

    ```bash
    docker run hello-world
    ```

8. Si la instalación es correcta, verás un mensaje que indica que Docker se ha ejecutado correctamente y que está descargando una imagen de prueba.

## Windows 10

1. Descarga e instala Docker Desktop para Windows en tu computadora desde el siguiente enlace: https://hub.docker.com/editions/community/docker-ce-desktop-windows/

2. Verifica que Docker Desktop esté ejecutándose correctamente en tu computadora.

3. Descarga la última versión de Docker Compose desde el siguiente enlace: https://github.com/docker/compose/releases

4. Descomprime el archivo ZIP de Docker Compose descargado en una ubicación accesible en tu computadora.

5. Abre una ventana de línea de comandos (cmd) como administrador en tu computadora.

6. Navega hasta la ubicación donde has descomprimido el archivo de Docker Compose en el paso 4.

7. Ejecuta el siguiente comando para copiar el archivo de Docker Compose en la ruta de acceso de tu computadora:

    ```cmd
    copy docker-compose.exe %ProgramFiles%\Docker\
    ```

8. Verifica la versión de Docker Compose instalada con el siguiente comando:

    ```cmd
    docker-compose -v
    ```

9. Para asegurarte de que Docker Compose está funcionando correctamente, crea un archivo de configuración de ejemplo con el siguiente comando:

    ```bash
    docker-compose config
    ```

10. Si se muestra una salida que contiene información sobre la configuración, entonces Docker Compose está funcionando correctamente en tu computadora Windows 10.
