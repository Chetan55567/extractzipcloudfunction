def extractzip(data, context):
    import tarfile
    import os 
    import io
    from google.cloud import storage
    client = storage.Client()
    inputbucket= client.get_bucket(data['bucket'])
    outputbucket= client.get_bucket('testbucketofgcp2')
    input_blob = inputbucket.get_blob(data['name']).download_as_string()

    my_tar = tarfile.open(fileobj=io.BytesIO(input_blob))
    for member in my_tar.getnames():
        file_object = my_tar.extractfile(member)
        if file_object:
            output_blob = outputbucket.blob(os.path.join('Extracted', member))
            output_blob.upload_from_string(file_object.read())
    my_tar.close()
    print("Extracted to Testbucketofgcp2/extracted folder")

#inputFile = "gs://" + str(data['bucket']) + "/" + str(data['name'])
