# Ejemplo #2 - Almacenar y recuperar variables con AWS Secret Manager

## Objetivo

* Integrar AWS Secret Manager con Airflow
* Utilizar un manejador de secretos alternativo

## Desarrollo

Vamos a configurar AWS Secret Manager como backend de las variables genéricas

1. Abrimos el archivo de docker-compose.yaml
2. Agregamos un par de variables de configuración

    ```yaml
    x-airflow-common:
    &airflow-common
    image: ${AIRFLOW_IMAGE_NAME:-apache/airflow:2.5.1}
    # build: .
    environment:
        &airflow-common-env
        AIRFLOW__SECRETS__BACKEND: airflow.providers.amazon.aws.secrets.secrets_manager.SecretsManagerBackend
        AIRFLOW__SECRETS__BACKEND_KWARGS_VARIABLES_PREFIX: airflow/variables    
        AIRFLOW__SECRETS__BACKEND_KWARGS_VARIABLES_PROFILE_NAME: default
        AWS_DEFAULT_REGION: us-west-2
        AWS_ACCESS_KEY_ID: <YOUR-KEY-ID>
        AWS_SECRET_ACCESS_KEY: <YOUR-SECRET>
        ...
    ```

3. Reiniciamos los servicios

    ```bash
    docker compose stop && docker compose up
    ```

3. Creamos una variable usando AWS CLI

    ```bash
    aws secretsmanager \
    create-secret \
    --name airflow/variables/mi_otra_variable \
    --secret-string "Usando un administrador de secretos alternativo" \
    --region us-west-2
    ```

4. Comprobamos que el secreto se guardo correctamente

    ```bash
    aws secretsmanager \
      get-secret-value \
      --secret-id airflow/variables/mi_otra_variable \
      --region us-west-2
    ```

5. Creamos un DAG para obtener y mostrar el valor de la variable

    ```python
    @task
    def display():
        mi_variable = Variable.get('mi_otra_variable',None)
        print(mi_variable)
    display()
    ```

6. Actualizamos el secreto

    ```bash
    aws secretsmanager \
        put-secret-value \
        --secret-id airflow/variables/mi_otra_variable \
        --secret-string "el valor fue cambiado fuera del ambiente de Airflow" \
        --region us-west-2
    ```

7. Volvemos a ejecutar nuestro DAG y comprobamos que el mensaje haya cambiado.

