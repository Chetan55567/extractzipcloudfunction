
def hello_gcs(data, context):
	from google.cloud import bigquery
	client = bigquery.Client()
	table_id = "innate-infusion-306605.demo.demotable"
	job_config = bigquery.LoadJobConfig(
        schema=[
        bigquery.SchemaField("Name", "STRING"),
        bigquery.SchemaField("Emp_ID", "STRING"),
		bigquery.SchemaField("Role", "STRING"),
		bigquery.SchemaField("ProjectAssigned", "STRING"),
		bigquery.SchemaField("Rating", "STRING"),
		bigquery.SchemaField("Comments", "STRING")
        ],
		create_disposition="CREATE_IF_NEEDED",
		write_disposition="WRITE_APPEND",
        skip_leading_rows=1,
    # The source format defaults to CSV, so the line below is optional.
        source_format=bigquery.SourceFormat.CSV,
    )
	uri = "gs://testbucketofgcp/*.csv"

	load_job = client.load_table_from_uri(
		uri, table_id, job_config=job_config
	)	
	load_job.result()  # Waits for the job to complete.

	destination_table = client.get_table(table_id)  # Make an API request.
	print("Loaded {} rows.".format(destination_table.num_rows))

	bucket_name = 'testbucketofgcp2'
	project = "innate-infusion-306605"
	dataset_id = "demo"
	table_id = "demotable"

	destination_uri = "gs://{}/{}".format(bucket_name, "FullReport.csv")
	dataset_ref = bigquery.DatasetReference(project, dataset_id)
	table_ref = dataset_ref.table(table_id)

	extract_job = client.extract_table(
		table_ref,
		destination_uri,
		# Location must match that of the source table.
		location="US",
	)  # API request
	extract_job.result()  # Waits for job to complete.

	print(
		"Exported {}:{}.{} to {}".format(project, dataset_id, table_id, destination_uri)
	)
	# #replace with your projectID
	# project = "innate-infusion-306605"
	# job = project + " " + str(data['timeCreated'])
	# #path of the dataflow template on google storage bucket
	# template = "gs://testbucketofgcp2/template/jsontemp"
	# inputFile = "gs://" + str(data['bucket']) + "/" + str(data['name'])
	# #user defined parameters to pass to the dataflow pipeline job
	# parameters = {
	# }
	# #tempLocation is the path on GCS to store temp files generated during the dataflow job
	# environment = {'tempLocation': 'gs://testbucketofgcp2/temp',
	# 				'zone': 'us-central1-f'}

	# service = build('dataflow', 'v1b3', cache_discovery=False)
	# #below API is used when we want to pass the location of the dataflow job
	# request = service.projects().locations().templates().launch(
	# 	projectId=project,
	# 	gcsPath=template,
	# 	location='us-central1',
	# 	body={
	# 		'jobName': job,
	# 		'parameters': parameters,
	# 		'environment':environment
	# 	},
	# )
	# response = request.execute()
	# print(str(response))
