from airflow.hooks.postgres_hook import PostgresHook
from airflow.models import BaseOperator
from airflow.utils.decorators import apply_defaults

class SchemaOperator(BaseOperator):

    ui_color = '#80BD9E'
    truncate_table_query = """
        TRUNCATE TABLE {}
        """
    
    insert_into_table_query = """
        INSERT INTO {} {}
        """

    @apply_defaults
    def __init__(self,
                 redshift_conn_id = "",
                 table = "",
                 insert_table_query = "",
                 truncate_table = False,
                 *args, **kwargs):

        super(SchemaOperator, self).__init__(*args, **kwargs)
        self.redshift_conn_id = redshift_conn_id
        self.table = table
        self.insert_table_query = insert_table_query
        self.truncate_table = truncate_table

    def execute(self, context):
        redshift = PostgresHook(postgres_conn_id=self.redshift_conn_id)
        self.log.info("MY SQL QUERY IS - ")
        self.log.info(self.insert_table_query)
        if self.truncate_table:
            self.log.info("Truncate the table {} before inserting new data".format(self.table))
            redshift.run(SchemaOperator.truncate_table_query.format(self.table))
            self.log.info("My SQL is - ")
            self.log.info(SchemaOperator.insert_into_table_query.format(self.table, self.insert_table_query))
            self.log.info("Truncated the table {}, and now ready to insert the data".format(self.table))
            
        redshift.run(SchemaOperator.insert_into_table_query.format(self.table, self.insert_table_query))