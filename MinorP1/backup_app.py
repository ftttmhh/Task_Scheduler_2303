import schedule
import time
import shutil
import os
import platform

class BackupApp:
    def __init__(self, source_dir, dest_dir, backup_time, maintenance_time):
        self.source_dir = source_dir
        self.dest_dir = dest_dir
        self.backup_time = backup_time
        self.maintenance_time = maintenance_time

    def backup_files(self):
        print("Backing up files from", self.source_dir, "to", self.dest_dir)
        try:
            # Copy files from source directory to destination directory
            for root, dirs, files in os.walk(self.source_dir):
                for file in files:
                    src_file = os.path.join(root, file)
                    dest_file = os.path.join(self.dest_dir, os.path.relpath(src_file, self.source_dir))
                    dest_path = os.path.dirname(dest_file)
                    if not os.path.exists(dest_path):
                        os.makedirs(dest_path)
                    shutil.copy2(src_file, dest_file)
            print("Backup completed.")
        except Exception as e:
            print("Error during backup:", str(e))

    def clean_temporary_files(self):
        print("Performing system maintenance...")
        try:
            # Perform disk cleanup based on the operating system
            if platform.system() == "Windows":
                # On Windows, use the built-in cleanup tool (cleanmgr) via command line
                os.system("cleanmgr /sagerun:1")  # Run cleanup using saved settings (Sagerun 1)
            elif platform.system() == "Linux":
                # On Linux, clean up temporary files using commands (e.g., apt clean)
                os.system("sudo apt clean")  # Example: Clean package cache on Debian-based systems
            elif platform.system() == "Darwin":
                # On macOS, clean up temporary files using commands (e.g., brew cleanup)
                os.system("brew cleanup")  # Example: Clean up Homebrew packages and formulae
            else:
                print("Unsupported operating system.")
        except Exception as e:
            print("Error performing system maintenance:", str(e))

    def schedule_backup(self):
        schedule.every().day.at(self.backup_time).do(self.backup_files)
        print("Backup scheduled for", self.backup_time)

    def schedule_maintenance(self):
        schedule.every().day.at(self.maintenance_time).do(self.clean_temporary_files)
        print("Maintenance scheduled for", self.maintenance_time)

    def run_backup_and_maintenance(self):
        self.schedule_backup()
        self.schedule_maintenance()
        while True:
            schedule.run_pending()
            time.sleep(1)
