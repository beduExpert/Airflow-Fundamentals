from airflow.models import BaseOperator
from airflow.utils.decorators import apply_defaults

from airflow.providers.postgres.hooks.postgres import PostgresHook

class NombraPelicula(BaseOperator):
    ui_color = "#e9c46a"
    @apply_defaults            
    def __init__(self, genero: str, postgres_conn_id: str='postgres_default', database: str='dvdrental', **kwargs) -> None:
        super().__init__(**kwargs)
        self.genero = genero
        self.postgres_conn_id = postgres_conn_id
        self.database = database

    def execute(self, context):
        hook = PostgresHook(postgres_conn_id=self.postgres_conn_id, schema=self.database)
        sql = f"""select
                    f.title,
                    f.description
                from film f
                inner join film_category fc
                on (f.film_id = fc.film_id)
                inner join category c
                on (fc.category_id = c.category_id)
                where
                    c.name = '{self.genero}'
                limit 1
                ;"""
        connection = hook.get_conn()
        cursor = connection.cursor()
        cursor.execute(sql)
        result = cursor.fetchall()
        cursor.close()
        print(result)
        return result