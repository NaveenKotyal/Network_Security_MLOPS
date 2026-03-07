import os

class S3Sync:

    def sync_folder_to_s3(self, folder, aws_bucket_url):

        folder = folder.replace("\\", "/")   # fix Windows path

        command = f'aws s3 sync "{folder}" "{aws_bucket_url}"'
        print(command)

        os.system(command)


    def sync_folder_from_s3(self, folder, aws_bucket_url):

        folder = folder.replace("\\", "/")

        command = f'aws s3 sync "{aws_bucket_url}" "{folder}"'
        print(command)
        print('finished')
        
