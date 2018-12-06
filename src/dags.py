#!/usr/local/bin/python

import os
import sys
from datetime import datetime, timedelta
from airflow import DAG
from airflow.utils.dates import days_ago
from airflow.operators.bash_operator import BashOperator
from airflow.operators.python_operator import PythonOperator

sys.path.append(os.path.dirname(__file__))
from inspect_data import inspect_data
from report_profile import wrap_report_profile
from alignment import wrap_alignment
from split import wrap_train_test_split
from train import wrap_train_and_validate
from predict import wrap_predict


TODAY = datetime.today().strftime("%Y%m%d")
DAYDIFF = str((datetime.today() - datetime(2018, 12, 1)).days)
AIRFLOW_HOME = os.environ['AIRFLOW_HOME']
DAGS_FOLDER = os.environ['AIRFLOW__CORE__DAGS_FOLDER']


default_args = {
    'owner': 'your.name',
    'depends_on_past': False,
    'start_date': days_ago(2),
    'email': 'your-email@mail.com',
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}


dag = DAG(
    'house_price_prediction',
    default_args=default_args,
    description='house price prediction',
    schedule_interval=None
)


t00 = PythonOperator(
    task_id='printing',
    depends_on_past=False,
    python_callable=print,
    op_args=['hello'],
    dag=dag
)


new_data = DAGS_FOLDER + '/data/raw/new.csv'


t10 = PythonOperator(
    task_id='inspection',
    depends_on_past=True,
    python_callable=inspect_data,
    op_kwargs={ 'input': new_data },
    dag=dag
)


t20 = PythonOperator(
    task_id='profiling',
    depends_on_past=True,
    python_callable=wrap_report_profile,
    op_kwargs={ 'input': new_data,
                'output': DAGS_FOLDER + \
                    '/data/profile/profile_' + TODAY + '.html' },
    dag=dag
)


aliginmented_data = DAGS_FOLDER + \
    '/data/prepared/alignmented_data_' + \
    TODAY + \
    '.csv'


t30 = PythonOperator(
    task_id='alignmenting',
    depends_on_past=True,
    python_callable=wrap_alignment,
    op_kwargs={ 'input': new_data,
                'output': aliginmented_data },
    dag=dag
)


data_train = DAGS_FOLDER + '/data/prepared/data_train_' + TODAY + '.csv'
data_valid = DAGS_FOLDER + '/data/prepared/data_valid_' + TODAY + '.csv'


t32 = PythonOperator(
    task_id='spliting',
    depends_on_past=True,
    python_callable=wrap_train_test_split,
    op_kwargs={ 'input': aliginmented_data,
                'train': data_train,
                'valid': data_valid,
                'ratio': 0.25,
                'seed': 1234 },
    dag=dag
)


pipeline_pickle = DAGS_FOLDER + '/data/pickles/' + TODAY + '/model.pkl'
metrics_file = DAGS_FOLDER + '/data/profile/metrics_' + TODAY + '.json'


t38 = BashOperator(
    task_id='making_dir',
    depends_on_past=True,
    bash_command='mkdir {{ params.path }}',
    params={ 'path': DAGS_FOLDER + '/data/pickles/' + TODAY },
    dag=dag
)


t40 = PythonOperator(
    task_id='training',
    depends_on_past=True,
    python_callable=wrap_train_and_validate,
    op_kwargs={ 'train': data_train,
                'valid': data_valid,
                'output': pipeline_pickle,
                'metrics': metrics_file,
                'model': 'lm' },
    dag=dag
)


BUCKET_NAME = os.environ['BUCKET_NAME']
DESTINATION = TODAY + '/model.pkl'


t50 = BashOperator(
    task_id='putting_gcs',
    depends_on_past=True,
    bash_command='gsutil cp \
        {{ params.file }} \
        {{ params.gcs }}',
    params={ 'file': pipeline_pickle,
             'gcs': 'gs://' + BUCKET_NAME + '/' + DESTINATION },
    dag=dag
)


VERSION_BASE = 'v1_0_'
VERSION_NAME = VERSION_BASE + DAYDIFF
DEPLOYMENTURI = 'gs://' + BUCKET_NAME + '/' + TODAY + '/'
PROJECT_ID = os.environ['PROJECT_ID']
MODEL_NAME = os.environ['MODEL_NAME']
TARGET_URL = \
    'https://ml.googleapis.com/v1/projects/{0}/models/{1}/versions'.format(\
    PROJECT_ID, MODEL_NAME)
PREDICT_URL = '"' + TARGET_URL + '/' + VERSION_NAME + ':predict"'


t60 = BashOperator(
    task_id='gcloud_ml-engine_create_version',
    depends_on_past=True,
    bash_command='gcloud ml-engine versions \
        create {{ params.version_name }} \
        --model {{ params.model_name }} \
        --origin {{ params.model_dir }} \
        --runtime-version=1.10 \
        --framework "SCIKIT_LEARN" \
        --python-version="3.5"',
    params={ 'version_name': VERSION_NAME,
             'model_name': MODEL_NAME,
             'model_dir': DEPLOYMENTURI },
    dag=dag
)


t64 = BashOperator(
    task_id='REST_mlengine_prediction',
    depends_on_past=True,
    bash_command='curl -X POST -H "Content-Type: application/json" \
        -d {{ params.input_file }} \
        -H "Authorization: Bearer `gcloud auth print-access-token`" \
        {{ params.predict_url }}',
    params={ 'input_file': '@' + 'data/prepared/test.json',
             'predict_url': PREDICT_URL },
    dag=dag
)


t70 = PythonOperator(
    task_id='local_prediction',
    depends_on_past=True,
    python_callable=wrap_predict,
    op_kwargs={ 'input': DAGS_FOLDER + '/data/raw/test.csv',
                'output': DAGS_FOLDER + '/data/prepared/my_submission.csv',
                'pipeline': pipeline_pickle },
    dag=dag
)


t00 >> t10 >> t20
t10 >> t30 >> t32 >> t38 >> t40 >> t70
t40 >> t50 >> t60 >> t64
