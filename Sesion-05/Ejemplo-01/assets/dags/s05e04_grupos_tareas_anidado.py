from airflow.utils.task_group import TaskGroup
from airflow.operators.empty import EmptyOperator
from airflow.decorators import dag, task_group, task
import pendulum

@dag(
    schedule=None,
    start_date=pendulum.datetime(2023, 3, 30, tz="UTC"),
    catchup=False
)
def grupo_tareas_anidado():
    groups = []
    for g_id in range(1,3):
        @task_group(group_id=f"group{g_id}")
        def tg1():
            t1 = EmptyOperator(task_id="task1")
            t2 = EmptyOperator(task_id="task2")

            sub_groups = []
            for s_id in range(1,3):
                @task_group(group_id=f"sub_group{s_id}")
                def tg2():
                    st1 = EmptyOperator(task_id="task1")
                    st2 = EmptyOperator(task_id="task2")

                    st1 >> st2
                sub_groups.append(tg2())

            t1 >> sub_groups >> t2
        groups.append(tg1())

    groups[0] >> groups[1]

grupo_tareas_anidado()
