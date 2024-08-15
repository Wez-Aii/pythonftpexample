import paramiko
import os

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

def main():
    transport = paramiko.Transport(('localhost', 22))
    transport.connect(username='user', password='12345')
    sftp = paramiko.SFTPClient.from_transport(transport)

    remote_folder = "/ftp/upload_folder"
    local_folder = "./download_folder"

    download_folder(sftp, remote_folder, local_folder)

    sftp.close()
    transport.close()

if __name__ == "__main__":
    main()
