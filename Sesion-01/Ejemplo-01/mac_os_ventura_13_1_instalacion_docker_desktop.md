### Cómo instalar Docker en OS X

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


## Preparar el ambiente de desarrollo

1. Instalar [Visual Studio Code](https://code.visualstudio.com/download) (VS Code)
2. Instalar [paquete de extension para Python](https://marketplace.visualstudio.com/items?itemName=ms-python.python)
3. Instalar [paquete de extension para Docker](https://marketplace.visualstudio.com/items?itemName=ms-azuretools.vscode-docker)
4. Instalar modulo de airflow, de preferencia en una ambiente virtual con Python 3.10

    ```bash
    pip install "apache-airflow[celery]==2.5.1" --constraint "https://raw.githubusercontent.com/apache/airflow/constraints-2.5.1/constraints-3.7.txt"
    ```
