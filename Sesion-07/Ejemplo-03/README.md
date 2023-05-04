# Ejemplo #3 - Ejecutar un DAG dos veces al dia en intervalos diferentes

## Objetivo

* Demostrar el uso de las tablas de tiempo para casos de uso particulares

## Desarrollo

1. Creamos un archivo python `uneven_intervals_timetable.py` en dentro de la carpeta `Plugins`
2. Importamos `AirflowPlugin`, algunas clases del módulo `airflow.timetables.base` y otras bibliotecas de tiempo auxliares

    ```python
    from datetime import timedelta
    from typing import Optional
    from pendulum import Date, DateTime, Time, timezone

    from airflow.plugins_manager import AirflowPlugin
    from airflow.timetables.base import DagRunInfo, DataInterval, TimeRestriction, Timetable
    ```

3. Definimos una clase nueva derivada de `Timetable`

    ```python
    class UnevenIntervalsTimetable(Timetable):
    def infer_manual_data_interval(self, run_after: DateTime) -> DataInterval:
        delta = timedelta(days=1)
        # If time is between 6:00 and 16:30, period ends at 6am and starts at 16:30 previous day
        if run_after >= run_after.set(hour=6, minute=0) and run_after <= run_after.set(hour=16, minute=30):
            start = (run_after-delta).set(hour=16, minute=30, second=0).replace(tzinfo=UTC)
            end = run_after.set(hour=6, minute=0, second=0).replace(tzinfo=UTC)
        # If time is after 16:30 but before midnight, period is between 6:00 and 16:30 the same day
        elif run_after >= run_after.set(hour=16, minute=30) and run_after.hour <= 23:
            start = run_after.set(hour=6, minute=0, second=0).replace(tzinfo=UTC)
            end = run_after.set(hour=16, minute=30, second=0).replace(tzinfo=UTC)
        # If time is after midnight but before 6:00, period is between 6:00 and 16:30 the previous day
        else:
            start = (run_after-delta).set(hour=6, minute=0).replace(tzinfo=UTC)
            end = (run_after-delta).set(hour=16, minute=30).replace(tzinfo=UTC)
        return DataInterval(start=start, end=end)

    def next_dagrun_info(
        self,
        *,
        last_automated_data_interval: Optional[DataInterval],
        restriction: TimeRestriction,
    ) -> Optional[DagRunInfo]:
        if last_automated_data_interval is not None:  # There was a previous run on the regular schedule.
            last_start = last_automated_data_interval.start
            delta = timedelta(days=1)
            if last_start.hour == 6: # If previous period started at 6:00, next period will start at 16:30 and end at 6:00 following day
                next_start = last_start.set(hour=16, minute=30).replace(tzinfo=UTC)
                next_end = (last_start+delta).replace(tzinfo=UTC)
            else: # If previous period started at 14:30, next period will start at 6:00 next day and end at 14:30
                next_start = (last_start+delta).set(hour=6, minute=0).replace(tzinfo=UTC)
                next_end = (last_start+delta).replace(tzinfo=UTC)
        else:  # This is the first ever run on the regular schedule. First data interval will always start at 6:00 and end at 16:30
            next_start = restriction.earliest
            if next_start is None:  # No start_date. Don't schedule.
                return None
            if not restriction.catchup: # If the DAG has catchup=False, today is the earliest to consider.
                next_start = max(next_start, DateTime.combine(Date.today(), Time.min).replace(tzinfo=UTC))
            next_start = next_start.set(hour=6, minute=0).replace(tzinfo=UTC)
            next_end = next_start.set(hour=16, minute=30).replace(tzinfo=UTC)
        if restriction.latest is not None and next_start > restriction.latest:
            return None  # Over the DAG's scheduled end; don't schedule.
        return DagRunInfo.interval(start=next_start, end=next_end)
    ```

4. Registramos el Plugin

    ```python
    class UnevenIntervalsTimetablePlugin(AirflowPlugin):
    name = "uneven_intervals_timetable_plugin"
    timetables = [UnevenIntervalsTimetable]
    ```

5. Reiniciamos el ambiente

    ```bash
    docker compose stop
    docker compose up
    ```

6. Verificamos que el plugin está registrado

    - Nos conectamos al contendor del Scheduler en VS Code
    - Ejecutamos el comando `airflow plugins` y revisamos que `UnevenIntervalsTimetable` aparezca en la lista.


7. Creamos una tarea para probrar el nuevo operador

    ```python
    with DAG(
        dag_id="ejemplo_timetable",
        start_date=pendulum.datetime(2023, 3, 1, tz="UTC"),
        catchup=True,
        schedule=UnevenIntervalsTimetable()
    ) as dag:
    t1 = BashOperator(
        task_id="imprime_fecha",
        bash_command="echo $(date)"
    )
    ```

8. Guardamos el archivo DAG, lo activamos y esperamos a que se ejecute por sí mismo
9. Cambiamos a la vista de rejilla (Grid) y comprobamos que las ejecuciones se hallan realizado a las 06:00 y 16:30 UTC

En los siguientes enlaces encontrarás las versiones finales del operador y el DAG de ejemplo.

* [uneven_intervals_timetable.py](/Sesion-07/Ejemplo-03/assets/plugins/uneven_intervals_timetable.py)
* [ejemplo_timetable.py](Sesion-07/Ejemplo-03/assets/dags/ejemplo_timetable.py)
