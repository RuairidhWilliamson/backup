import datetime
def read_text_file(name):
    f = open(name, "r")
    out = f.read()
    f.close()
    return out
def write_text_file(name, text):
    f = open(name, "w")
    f.write(text)
    f.close()

def load_config(name, dictionary = False):
    lines = read_text_file(name).split("\n")
    if dictionary:
        return {convert_slashes(x.split("=")[0]) : convert_slashes(x.split("=")[1]) for x in lines if "=" in x}
    else:
        return [convert_slashes(x) for x in lines]
def convert_slashes(x):
    return "".join(["/" if i == "\\" else i for i in x])

def log(message):
    f = open("log.log", "a")
    f.write("{} {}\n".format(datetime.datetime.now().strftime("[%y/%m/%d %H:%M:%S]"), message))
    f.close()