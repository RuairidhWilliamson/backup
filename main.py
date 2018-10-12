import datetime, utils, os, shutil, time

config = utils.load_config("config.cfg", True)
directories = utils.load_config("directories.cfg", True)

def backup_all():
    last_backup = int(utils.read_text_file("lastBackup.txt"))
    if int(time.time()) - last_backup < int(config["BackupFrequency"]) * 3600 * 24:
        print("No backup required")
        return
    backup_name = datetime.datetime.now().strftime("%y-%m-%d %H-%M-%S")
    backup_dir = config["BackupDirectory"] + "/" + backup_name
    os.makedirs(backup_dir)
    for key, loc in directories.items():
        shutil.make_archive(backup_dir + "/" + key, "zip", loc)
    utils.write_text_file("lastBackup.txt", str(int(time.time())))
    dirs = os.listdir(config["BackupDirectory"])
    dirs = sorted(dirs)
    if len(dirs) > int(config["BackupCount"]):
        shutil.rmtree(config["BackupDirectory"] + "/" + dirs[0])

if __name__ == "__main__":
    backup_all()