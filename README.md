# ApacheBeam-dataflow-template
Template for quickly setting up ApacheBeam pipeline with for usage on GoogleCloud Dataflow

## Getting started
Environment variable `GOOGLE_APPLICATION_CREDENTIALS` has to point to a valid credentials json-file exported from [Google Cloud IAM](https://gitlab.com/subsidia/backend/size-mapping-pipeline/-/blob/main/doc/main.pdf, "IAM").
And you need to create a bucket `<your bucket name>` and folder `<your temporary folder>` on Google Cloud Storage, where logs and execution metadate is stored temporarily. When executed, these files may be deleted, but you can as well let them be.

### Run the pipeline locally:
```
python main.py --project <your gcp project> --temp_location gs://<your bucket name>/<your temporary folder>
```
In this case, the pipeline is executed by whatever Python interpreter you have defined on your local machine using `DirectRunner`. For local execution, only `./main.py` is considered.

### Run on Google Cloud
run the pipeline on google cloud dataflow:
```
python main.py --project <your gcp project> --runner DataflowRunner --temp_location gs://<your bucket name>/<your temporary folder> --setup_file ./setup.py --region europe-west6
```
Pipeline is executed on Google Cloud using `DataflowRunner`. First, dependencies are installed as defined by `setup.py` in a virtual environment on Google Cloud and tests (identified by python module names starting with `test`) are run. Next, `./main.py` is executed by that environment on the Cloud.

### Deploy Pipeline Template
Deploy pipeline as templated file to google cloud dataflow:
```
python main.py --project <your gcp project> --runner DataflowRunner --temp_location gs://<your bucket name>/<your temporary folder> --setup_file ./setup.py --region europe-west6
```
Pipeline templates can be rerun at any time without needing to recompile them. Google Cloud Scheduler can trigger pipelines periodically, so you don't need to think of all your pipelines to run.
When deployed via Gitlab, the file `./.gitlab-ci.yml` is executed.