import os
import re
import json
import tempfile

def prompt_yes_no(prompt, default_val=""):
    while True:
        default_prompt = "(yes/no)"
        if default_val != "":
            default_val = default_val.lower()
            if default_val == "y" or default_val == "yes":
                default_val = True
                default_prompt = "(Yes/no)"
            if default_val == "n" or default_val == "no":
                default_val = False
                default_prompt = "(yes/No)"

        answer = input("{} {} : ".format(prompt, default_prompt))
        answer = answer.lower().strip()
        if answer == "y" or answer == "yes":
            return True
        elif answer == "n" or answer == "no":
            return False
        elif answer == "" and default_val != "":
            return default_val


def prompt_string(prompt, default_val=""):
    while True:
        default_prompt = ""
        if default_val != "":
            default_prompt = " ({})".format(default_val)
        answer = input("{}{} : ".format(prompt, default_prompt))
        answer = answer.strip()
        if answer != "":
            return answer
        else:
            if default_val != "":
                return default_val

def prompt_integer(prompt, default_val=""):
    while True:
        default_prompt = ""
        if default_val != "":
            default_prompt = " ({})".format(default_val)
        answer = input("{}{} : ".format(prompt, default_prompt))
        if answer != "":
            return int(answer)
        else:
            if default_val != "":
                return int(default_val)


def generate_short_name(full_name):
    short_name = full_name.lower()
    short_name = re.sub(r'[^a-z_]', '', short_name)
    return short_name

def replace_string_in_file(file, search, replace):
    s = str(search)
    r = str(replace)
    file_contents = ""
    with open(file, "r") as f:
        file_contents = f.read()
    file_contents = file_contents.replace(s, r)
    with open(file, "w") as f:
        f.write(file_contents)

def update_app_info(app_json_path, key, value):
    with open(app_json_path, 'r') as app_info_file:
        app_data = json.load(app_info_file)
    app_data[key] = value
    with open(app_json_path, 'w') as app_info_file:
        json.dump(app_data, app_info_file, indent=4)

def clear_dist_folder(app_dir, short_name):
    dist_folder = app_dir+"/dist"
    if os.path.exists(dist_folder):
        dist_filename = app_dir+"/dist/"+short_name+".tar.gz"
        if os.path.isfile(dist_filename):
            os.remove(dist_filename)

def create_dist_tarball(app_dir, short_name):
    # Create tarball in temp
    with tempfile.TemporaryDirectory() as tmpdirname:
        app_tarball = tmpdirname + "/app.tar.gz"
        tmp_app_dir = "{}/{}".format(tmpdirname, short_name)
        os.system("mkdir -p {}".format(tmp_app_dir))
        os.system("rsync -a {}/ {}".format(app_dir, tmp_app_dir))
        os.system("tar --exclude='.*' -zcf {} -C /{} {}".format(app_tarball, tmpdirname, short_name))
        
        # Make dist folder again
        dist_folder = app_dir+"/dist"
        os.system("mkdir -p {}".format(dist_folder))

        # Save tarball to dist folder
        os.system("cp -f {} {}".format(app_tarball, dist_folder+"/"+short_name+".tar.gz"))