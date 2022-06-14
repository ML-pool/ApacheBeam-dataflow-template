# ApacheBeam-dataflow-template
Template for quickly setting up ApacheBeam pipeline with for usage on GoogleCloud Dataflow

## Getting started

run the pipeline locally:
```
python main.py --project <your gcp project> --temp_location gs://<bucket>/<folder>
```

run the pipeline on google cloud dataflow:
```
python main.py --project <your gcp project> --runner DataflowRunner --temp_location gs://<bucket>/<folder> --setup_file ./setup.py --region europe-west6
```

deploy pipeline as templated file to google cloud dataflow:
```
python main.py --project <your gcp project> --runner DataflowRunner --temp_location gs://<bucket>/<folder> --setup_file ./setup.py --region europe-west6
```