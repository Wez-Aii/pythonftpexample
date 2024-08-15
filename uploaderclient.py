import ftplib
import os
from ftplib import FTP

def upload_folder(ftp, local_folder, remote_folder):
    try:
        ftp.cwd(remote_folder)
    except ftplib.error_perm:
        ftp.mkd(remote_folder)
        ftp.cwd(remote_folder)

    for root, dirs, files in os.walk(local_folder):
        for dir in dirs:
            remote_dir = os.path.join(root, dir)[len(local_folder)+1:]
            try:
                ftp.mkd(remote_dir)
            except ftplib.error_perm:
                pass
            ftp.cwd(remote_dir)
            ftp.cwd("..")

        for file in files:
            local_path = os.path.join(root, file)
            remote_path = os.path.join(root, file)[len(local_folder)+1:]
            with open(local_path, 'rb') as f:
                ftp.storbinary(f"STOR {remote_path}", f)
            print(f"Uploaded: {remote_path}")
    
    # for item in os.listdir(local_folder):
    #     local_path = os.path.join(local_folder, item)
    #     remote_path = f"{remote_folder}/{item}"

    #     if os.path.isfile(local_path):
    #         with open(local_path, 'rb') as file:
    #             ftp.storbinary(f'STOR {remote_path}', file)
    #         print(f"Uploaded: {remote_path}")
    #     elif os.path.isdir(local_path):
    #         try:
    #             ftp.mkd(remote_path)
    #         except:
    #             pass  # Directory might already exist
    #         upload_folder(ftp, local_path, remote_path)

def main():
    # Connect to the FTP server
    ftp = FTP()
    ftp.connect('ftpserver', 2121)
    # ftp.connect('139.59.222.214', 21, timeout=120)
    ftp.login('user', 'password')

    # Local and remote folder paths
    local_folder = '/workspaces/uploaddir1'
    remote_folder = 'remote_dir1'

    # Create remote folder if it doesn't exist
    try:
        ftp.mkd(remote_folder)
    except:
        pass  # Folder might already exist

    # Upload the folder
    upload_folder(ftp, local_folder, remote_folder)

    # Close the connection
    ftp.quit()

if __name__ == '__main__':
    main()