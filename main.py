import datetime, utils, os, shutil, time

config = utils.load_config("config.cfg", True)
directories = utils.load_config("directories.cfg", True)

def backup_all():
    last_backup = int(utils.read_text_file("lastBackup.txt"))
    # Check if the minimum time has passed since the last backup
    if int(time.time()) - last_backup < int(config["BackupFrequency"]) * 3600 * 24:
        print("No backup required")
        return
    # Create backup folder
    backup_name = datetime.datetime.now().strftime("%y-%m-%d %H-%M-%S")
    backup_dir = config["BackupDirectory"] + "/" + backup_name
    os.makedirs(backup_dir)
    # Create zips for folders
    for key, loc in directories.items():
        shutil.make_archive(backup_dir + "/" + key, "zip", loc)
    # Update last backup time
    utils.write_text_file("lastBackup.txt", str(int(time.time())))
    # Check if backup limit is met
    dirs = os.listdir(config["BackupDirectory"])
    dirs = sorted(dirs)
    if len(dirs) > int(config["BackupCount"]):
        # Delete oldest backup
        shutil.rmtree(config["BackupDirectory"] + "/" + dirs[0])
    print("Backup completed")

if __name__ == "__main__":
    backup_all()