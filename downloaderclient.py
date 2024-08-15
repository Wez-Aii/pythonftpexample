import paramiko
import os

def upload_folder(sftp, local_path, remote_path):
    for item in os.listdir(local_path):
        local_item_path = os.path.join(local_path, item)
        remote_item_path = os.path.join(remote_path, item)
        if os.path.isdir(local_item_path):
            try:
                sftp.mkdir(remote_item_path)
            except IOError:
                pass  # Directory already exists
            upload_folder(sftp, local_item_path, remote_item_path)
        else:
            sftp.put(local_item_path, remote_item_path)

def main():
    transport = paramiko.Transport(('localhost', 22))
    transport.connect(username='user', password='12345')
    sftp = paramiko.SFTPClient.from_transport(transport)

    local_folder = "./upload_folder"
    remote_folder = "/ftp/upload_folder"

    upload_folder(sftp, local_folder, remote_folder)

    sftp.close()
    transport.close()

if __name__ == "__main__":
    main()
