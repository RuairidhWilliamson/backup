import datetime, utils, os, shutil, time
from math import floor

config = utils.load_config("config.cfg", True)
directories = utils.load_config("directories.cfg", True)

def backup_all():
    last_backup = int(utils.read_text_file("lastBackup.txt"))
    # Check if the minimum time has passed since the last backup
    delta_time = int(config["BackupFrequency"]) * 3600 * 24 - int(time.time()) + last_backup
    if delta_time > 0:
        utils.log("No backup required for {}h {}m".format(floor(delta_time / 3600), round((delta_time / 60) % 60)))
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
        utils.log("Deleting old backup: {}".format(dirs[0]))
        shutil.rmtree(config["BackupDirectory"] + "/" + dirs[0])
    utils.log("Backup completed: {}".format(backup_name))

if __name__ == "__main__":
    backup_all()