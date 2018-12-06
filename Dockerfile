FROM google/cloud-sdk:226.0.0

RUN apt-get -qy update \
    && apt-get -qy install python3 python3-pip

ENV LANG=C.UTF-8 \
    SLUGIFY_USES_TEXT_UNIDECODE=yes \
    AIRFLOW_HOME=/airflow \
    AIRFLOW__CORE__DAGS_FOLDER=/airflow/dags

WORKDIR /airflow/dags

COPY ./airflow.cfg /airflow

COPY . /airflow/dags

RUN pip install \
        enum==0.4.7 \
        scipy==1.1.0 \
        scikit-learn==0.19.2 \
        tensorflow==1.12.0 \
    && pip3 install -r requirements.txt

CMD ["python3"]
