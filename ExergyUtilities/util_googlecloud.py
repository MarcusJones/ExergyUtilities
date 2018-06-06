import os

import google.cloud.storage

# OLD CODE OBSELETE
# 
# os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "/home/batman/gcloud_credentials/Test First-48dd42d10d05.json"
# 
# # Create a storage client.
# storage_client = google.cloud.storage.Client()
# print(storage_client)
# 
# # TODO (Developer): Replace this with your Cloud Storage bucket name.
# bucket_name = 'test-bucket-1s'
# bucket = storage_client.get_bucket(bucket_name)
# 
# # TODO (Developer): Replace this with the name of the local file to upload.
# source_file_name = 'Local file to upload, for example ./file.txt'
# blob = bucket.blob(os.path.basename(source_file_name))
# 
# # Upload the local file to Cloud Storage.
# blob.upload_from_filename(source_file_name)
# 
# print('File {} uploaded to {}.'.format(
#     source_file_name,
#     bucket))
#                 