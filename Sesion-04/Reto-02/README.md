# Reto # - Uso de Variables Airflow

## Objetivo

* Utilizar Variables Airflow para controlar el flujo de trabajo

## Desarrollo

Para completar este desafío deberás

1. Clonar el archivo DAG que usaste para resolver el [reto anterior](/Sesion-04/Reto-02/README.md)
2. Renombrarlo e integrar la siguiente variable para controlar la lista de municipios en el DAG
3. Usa el nombre del municipio en el nombre de la tarea

```json
    [{
        "name": "Azcapotzalco",
        "id": 2
    },
    {
        "name": "Coyoacan",
        "id": 3
    },
    {
        "name": "Cuajimalpa De Morelos",
        "id": 4
    },
    {
        "name": "Gustavo A. Madero",
        "id":5
    },
    {
        "name": "Iztacalco",
        "id": 6
    },
    {
        "name": "Iztapalapa",
        "id": 7
    },
    {
        "name": "La Magdalena Contreras",
        "id": 8
    },
    {
        "name": "Milpa Alta",
        "id": 9
    },
    {
        "name": "Alvaro Obregon",
        "id": 10
    },
    {
        "name": "Tlahuac",
        "id": 11
    },
    {
        "name": "Tlalpan",
        "id": 12
    },
    {
        "name": "Xochimilco",
        "id":13
    },
    {
        "name": "Benito Juarez",
        "id": 14
    },
    {
        "name": "Cuauhtemoc",
        "id": 15
    },
    {
        "name": "Miguel Hidalgo",
        "id": 16
    },
    {
        "name": "Venustiano Carranza",
        "id": 17
    }]
```
