# Sesión #7: Plugins

## :dart: Objetivos

- Crear un calendario laboral con los dias feriados de México
- Diseñar y crer un pruebas unitaria para este plugin

## ⚙ Requisitos

+ Ambiente de Airflow
+ VS Code

## Desarrollo

De los tres tipos de plugins que revisamos en esta sección, la tabla de tiempo es una característica común que probablemente tendrán que implementar.

### Parte I

En este postworks tendrán que crear una tabla de tiempo que funcione de acuerdo al calendario de su organización.

El calendario base será el laboral con días feriados de México, el cuál deberán ajustar al candelario que utilizan en su organización, por ejemplo, agreagar o quitar fechas.

Alternativamente pueden pensar en un caso de uso real y modificar la tabla de tiempo para que se adapte a los días y horarios que necesiten.

1. Crear un archivo Python en la carpeta `/Plugins`
2. Crear una clase derivada de `AbstractHolidayCalendar`
3. Implementar la clase derivada de `TimeTable`
4. Rigistrar el Plugin
5. Crear un archivo DAG de prueba que utilice la tabla de tiempo como plan de ejecución
6. Activar y ejecutar el DAG de prueba desde el inicio de año a la fecha para verificar el comportamiento esperado.

**Tip**: Usar una [serie de tiempo de Pandas](https://pandas.pydata.org/pandas-docs/version/0.17/timeseries.html) para crear el calendario

 ```python
     from pandas.tseries.holiday import (
        Holiday,
        DateOffset,
        MO,
        AbstractHolidayCalendar,
    )

    class MexicanHolidays(AbstractHolidayCalendar):
        rules = [
            Holiday("New Year's Day", month=1, day=1, offset=DateOffset(weekday=MO(1))),
            Holiday("Epiphany", month=1, day=6),
            Holiday("Constitution Day", month=2, day=6),
            Holiday("Benito Juarez Day", month=3, day=21),
            Holiday("Labour Day", month=5, day=1, offset=DateOffset(weekday=MO(1))),
            Holiday("Battle of Puebla Day", month=5, day=5),
            Holiday("Independence Day", month=9, day=16),
            Holiday("Revolution Day", month=11, day=20, offset=DateOffset(weekday=MO(3))),
            Holiday("Lady of Guadalupe Day", month=12, day=12),
            Holiday("Christmas Day", month=12, day=25),
        ]

    holiday_calendar = MexicanHolidays()
```

### Parte II. Crear una prueba unitaria (puntos extras)

Una vez que el plugin este creado, deberán diseñar y e implementar una prueba unitaria sencilla para validar que el calendario funciona como se espera.
