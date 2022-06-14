
from __future__ import absolute_import

import argparse
import apache_beam as beam
from apache_beam.options.pipeline_options import PipelineOptions
import typing

# query for Google Cloud BigQuery
BQ_QUERY = '''
    SELECT 
		a,
		b,
		c
    FROM `<your dataset>.<your table>`
	LIMIT %s
    '''

class MyClass(typing.NamedTuple):
    a: str
    b: int

class UserOptions(PipelineOptions):
    @classmethod
    def _add_argparse_args(cls, parser):
      parser.add_value_provider_argument('--min_size', type=int, default=1000)
      parser.add_value_provider_argument('--threshold', type=float, default=0.01)

def run():
    parser = argparse.ArgumentParser()
    parser.add_argument('--data_limit', type=int, default=None)
    app_args, pipeline_args = parser.parse_known_args()
    
    pipeline_options = PipelineOptions(pipeline_args)

    project = pipeline_options.get_all_options()['project']
    limit = app_args.data_limit


    with beam.Pipeline(options=pipeline_options) as p:
        user_options = pipeline_options.view_as(UserOptions)
        
        (
            p 
            | 'read sales' >> beam.io.ReadFromBigQuery(
                    query=BQ_QUERY % limit, 
                    use_standard_sql=True
                ).with_output_types(MyClass)
            | beam.WithKeys(lambda x: x['a']) 
            | beam.GroupByKey()
            | beam.Filter(lambda x: sum([i['b'] for i in x[1]]) > user_options.min_size.get())
			| beam.io.WriteToBigQuery(
				table='<your table>',
				dataset='<your dataset>',
				project=project,
				schema='a:STRING,\
                        b:INTEGER',
				create_disposition=beam.io.BigQueryDisposition.CREATE_IF_NEEDED,
				write_disposition=beam.io.BigQueryDisposition.WRITE_TRUNCATE
			)     
        )

if __name__ == '__main__':
    run()