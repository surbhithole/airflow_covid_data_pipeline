from airflow.hooks.postgres_hook import PostgresHook
from airflow.models import BaseOperator
from airflow.utils.decorators import apply_defaults
from airflow.contrib.hooks.aws_hook import AwsHook

class StageToRedshiftOperator(BaseOperator):
    ui_color = '#358140'
    template_fields = ("s3_key",)
    '''
    copy_data_to_redshift_from_s3_sql = """COPY {}
        FROM '{}'
        ACCESS_KEY_ID '{}'
        SECRET_ACCESS_KEY '{}'
        COMPUPDATE OFF STATUPDATE OFF
        REGION '{}'
        FORMAT AS JSON '{}'
        FILLRECORD
        delimiter '\t' 
        IGNOREHEADER 1 
        removequotes
        emptyasnull
        blanksasnull
        maxerror 5;
        """ '''
    
    copy_data_to_redshift_from_s3_sql = ("""
        COPY {}
        FROM '{}'
        ACCESS_KEY_ID '{}'
        SECRET_ACCESS_KEY '{}'
        IGNOREHEADER 1
        DELIMITER ','
        region 'us-west-2'
    """)
    
    @apply_defaults
    def __init__(self,
                 redshift_conn_id="",
                 aws_credentials_id="",
                 table="",
                 s3_bucket="",
                 s3_key="",
                 json_path="auto",
                 region = "us-west-2",
                 *args, **kwargs):
                 # Define your operators params (with defaults) here
                 # Example:
                 # redshift_conn_id=your-connection-name

        super(StageToRedshiftOperator, self).__init__(*args, **kwargs)
        # Map params here
        # Example:
        # self.conn_id = conn_id
        self.table = table
        self.redshift_conn_id = redshift_conn_id
        self.s3_bucket = s3_bucket
        self.s3_key = s3_key
        self.aws_credentials_id = aws_credentials_id
        self.json_path = json_path
        self.region = region


    def execute(self, context):
        aws_hook = AwsHook(self.aws_credentials_id)
        credentials = aws_hook.get_credentials()
        redshift = PostgresHook(postgres_conn_id=self.redshift_conn_id)

        redshift.run("DELETE FROM {}".format(self.table))

        self.log.info("Loading data from S3 to {} in redshift cluster".format(self.table))
        rendered_key = self.s3_key.format(**context)
        # path to load table data from json files
        s3_path = "s3://{}/{}".format(self.s3_bucket, rendered_key)
        formatted_sql = StageToRedshiftOperator.copy_data_to_redshift_from_s3_sql.format(
            self.table,
            s3_path,
            credentials.access_key,
            credentials.secret_key
        )
        redshift.run(formatted_sql)




