
# Cómo instalar Docker Compose en Ubuntu

Aquí hay un tutorial para instalar Docker Compose con Brew en Ubuntu 22.04 LTS, incluyendo los pasos para instalar Brew:

1. Abre un terminal en tu sistema Ubuntu.
2. Ejecuta el siguiente comando para instalar Brew:

    ```bash
    sh -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/master/install.sh)"
    ```

3. Agrega el repositorio de Brew a tu PATH con el siguiente comando:

    ```bash
    echo 'export PATH="/home/linuxbrew/.linuxbrew/bin:$PATH"' >> ~/.bashrc
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
