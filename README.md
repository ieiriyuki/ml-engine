# Kaggle House Price Prediction
Predict the prices of houses in Kaggle competition

https://www.kaggle.com/c/house-prices-advanced-regression-techniques

### Docker images
Container images are based on `google/cloud-sdk:226.0.0`.

##### houseprice:1.0.0
This is written in Dockerfile, which copies relevant files to /airflow/dags.
To build, `docker build -t houseprice:1.0.0 .`
This assumes everything are on a production environment.
Therefore, you should do
`docker run --it -p 8080:8080 -p 5000:5000 houseprice:1.0.0 /bin/bash`

### google-cloud-sdk
Read below.

* https://github.com/GoogleCloudPlatform/cloud-sdk-docker/
* https://hub.docker.com/r/google/cloud-sdk
* http://docs.docker.jp/engine/reference/builder.html#volume

Google Cloud authentication is necessary.
We will do them like below.

1. copy service-account-credential to `/airflow/dags/.gcp/your-credential.json`
2. `export GOOGLE_APPLICATION_CREDENTIALS=/airflow/dags/.gcp/your-credential.json`
3. `gcloud auth activate-service-account --key-file=${GOOGLE_APPLICATION_CREDENTIALS}`
4. `rm -r .gcp`
5. `export PROJECT_ID="your-project-id" REGION="your-region" BUCKET_NAME="your-bucket-name" MODEL_NAME="your-model-name"`
6. `gcloud config set core/project ${PROJECT_ID}`
7. `gcloud config set compute/region ${REGION}`

Basic configuration is done.

### .py description
By default

1. `src/inspect_data.py` loads `data/raw/new.csv` and check its dtype.

2. `src/alignment.py` loads `data/raw/old.csv`, extract necessary features, alignment them, and saves `data/prepared/alignmented_data.csv`.

3. `src/split.py` loads `data/prepared/alignmented_data.csv` and split it into `data/prepared/data_train.csv` and `data/prepared/data_valid.csv`.

4. `src/train.py` loads `data/prepared/data_train.csv`, and train a linear regression model, which will be saved into `data/pickles/model.pkl` or `data/pickles/${DATE}/model.pkl`.
This code also uses MLflow modules and track the coefficient of determinant R^2, Rooted Mean Squared Log Error, the linear model called `lm` in `mlruns` directory.

    4.1 `calculate_metrics` in `src/evaluate.py` is called by `src/train.py` to save metrics of performance of the model into `data/profile/metrics.json`.

5. `src/predict.py` loads `data/pickles/model.pkl` and `data/raw/test.csv`, and them make a prediction file `data/prepared/my_submission.csv`.

These steps are controled by Airflow jobs that is written in `src/dags.py`.

### MLFlow and Airflow
It is supposed that applicatioins are evoked in a container. <br>
Expose ports 5000 and 8080 for MLflow and Airflow respectively.

MLflow tutorial is https://mlflow.org/docs/latest/quickstart.html

Airflow tutorial is https://airflow.apache.org/tutorial.html

Commands below are written in `misc/start_server` so that you can just kick `./misc/start_server`

Run below then airflow works on localhost:8080
```
airflow initdb
airflow webserver -p 8080 2>&1 > /airflow/logs/webserver.log &
```

To enable scheduled process, you have to run
```
airflow scheduler 2>&1 > /airflow/logs/scheduler/scheduler.log &
```
This is necessary for SequentialExecuter.

Run below then mlflow works on localhost:5000
```
mlflow ui -h 0.0.0.0 2>&1 > /airflow/logs/mlflow.log &
```
