import paramiko
import os

def upload_folder(sftp, local_folder, remote_folder):
    """Uploads a folder recursively to the SFTP server."""
    if not os.path.isdir(local_folder):
        raise NotADirectoryError(f"{local_folder} is not a directory")

    for root, dirs, files in os.walk(local_folder):
        # Construct the remote path
        remote_path = os.path.join(remote_folder, os.path.relpath(root, local_folder)).replace('\\', '/')
        
        # Ensure the directory exists on the remote side
        try:
            sftp.mkdir(remote_path)
            print(f"Directory created: {remote_path}")
        except IOError:
            print(f"Directory already exists: {remote_path}")

        for file in files:
            local_file_path = os.path.join(root, file)
            remote_file_path = os.path.join(remote_path, file).replace('\\', '/')
            
            # Upload the file
            sftp.put(local_file_path, remote_file_path)
            print(f"Uploaded {local_file_path} to {remote_file_path}")


def download_folder(sftp, remote_path, local_path):
    for item in sftp.listdir(remote_path):
        remote_item_path = os.path.join(remote_path, item)
        local_item_path = os.path.join(local_path, item)
        if sftp.stat(remote_item_path).st_mode & 0o40000:  # Check if it's a directory
            if not os.path.exists(local_item_path):
                os.makedirs(local_item_path)
            download_folder(sftp, remote_item_path, local_item_path)
        else:
            sftp.get(remote_item_path, local_item_path)


if __name__=="__main__":
    try:
        # pkey = paramiko.RSAKey.from_private_key_file('/workspaces/test_rsa.key')
        pkey = None
        transport = paramiko.Transport(('server', 2222))
        transport.connect(username='admin', password='admin', pkey=pkey)
        sftp = paramiko.SFTPClient.from_transport(transport)
        files = sftp.listdir('.')
        print(files)
        upload_folder(sftp=sftp, local_folder="uploaddir1", remote_folder="remotedir")
        download_folder(sftp=sftp, remote_path="remotedir", local_path="downloaddir2")
    except Exception as e:
        print(e)
    transport.close()
    sftp.close()
