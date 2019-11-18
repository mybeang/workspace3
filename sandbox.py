import re
from os import listdir
from pathlib2 import Path

def check_apply_exit(text, line, config_file, k):
    if 'apply' in text:
        return 0
    if k == 0 and 'exit' not in text:
        raise ValueError("{} in {} lines check".format(config_file, line))
    else:
        return 1

def check_receiver(text, line, config_file):
    if 'receive' in text:
        print("%.15s:%4d lines: %s" % (config_file, line, text), end="")

def show_auto_reset(text, line, config_file):
    if 'auto-reset' in text:
        print("%.15s:%4d lines: %s" % (config_file, line, text), end="")

def check_hangul(text, line, config_file):
    if len(re.findall('[\u3130-\u318F\uAC00-\uD7A3]+', text)) > 0:
        print("%.15s:%4d lines: %s" % (config_file, line, text), end="")

def check_jumboframe(text, line, config_file):
    if "jumbo" in text:
        print("%.15s:%4d lines: %s" % (config_file, line, text), end="")

def main():
    path = Path(__file__).parent.parent.joinpath('python-lgu-sct')
    path = path.joinpath('sct')
    path = path.joinpath('tftpboot')
    d_list = listdir(str(path))
    for d in d_list:
        _path = path.joinpath(d).joinpath('Config')
        config_list = listdir(str(_path))
        for config in config_list:
            config_path = str(_path.joinpath(config))
            with open(config_path, 'r') as f:
                t_list = f.readlines()
            k = 1
            for i, t in enumerate(t_list):
                k = check_apply_exit(t, i, config, k)
                check_receiver(t, i, config)
                show_auto_reset(t, i, config)
                check_hangul(t, i, config)
                check_jumboframe(t, i, config)

if __name__=="__main__":
    main()