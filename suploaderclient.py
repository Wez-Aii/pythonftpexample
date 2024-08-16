import os
import paramiko

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

def download_folder(sftp, remote_folder, local_folder):
    """Downloads a folder recursively from the SFTP server."""
    if not os.path.exists(local_folder):
        os.makedirs(local_folder)

    for item in sftp.listdir_attr(remote_folder):
        remote_path = os.path.join(remote_folder, item.filename).replace('\\', '/')
        local_path = os.path.join(local_folder, item.filename)

        if stat.S_ISDIR(item.st_mode):
            # Recursively download the directory
            download_folder(sftp, remote_path, local_path)
        else:
            # Download the file
            sftp.get(remote_path, local_path)
            print(f"Downloaded {remote_path} to {local_path}")

def main():
    # Server details
    hostname = 'sftpserver'
    port = 2222
    username = 'user1'
    password = 'password123'

    # Paths to upload and download
    local_folder_to_upload = '/workspaces/uploaddir1'
    remote_folder_upload_path = '/remotedir'
    remote_folder_to_download = '/remotedir'
    local_download_path = 'folder2'

    # Using SFTPClient
    with paramiko.SSHClient() as client:
        client.load_system_host_keys()
        client.connect('sftpserver', port=2222, username=username, password=username)
        with client.open_sftp() as sftp:
            sftp.put(local_folder_to_upload, remote_folder_upload_path)

    # Connect to the server
    transport = paramiko.Transport((hostname, port))
    transport.connect(username=username, password=password)
    # transport.connect()

    sftp = paramiko.SFTPClient.from_transport(transport)

    try:
        # Upload a folder
        print("Uploading folder...")
        upload_folder(sftp, local_folder_to_upload, remote_folder_upload_path)

        # Download a folder
        print("Downloading folder...")
        download_folder(sftp, remote_folder_to_download, local_download_path)

    except Exception as e:
        print(f"Error: {e}")
    
    finally:
        sftp.close()
        transport.close()

if __name__ == "__main__":
    main()
