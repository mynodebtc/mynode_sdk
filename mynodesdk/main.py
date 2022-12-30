import os
from argparse import ArgumentParser
import tempfile
from mynodesdk.util import *

APP_TEMPLATE_URL    =   "https://mynodebtc.com/dl/sdk/sdk_app_template.tar.gz"

def create():
    # Init data
    cwd = os.getcwd()

    # Prompt for data
    full_app_name = prompt_string("Enter the application name (Ex. BTCPay Server)")
    short_name = generate_short_name(full_app_name)
    short_name = prompt_string("Enter the application identifier", short_name)
    app_dir = "{}/{}".format(cwd, short_name)
    is_service = True

    if os.path.exists(app_dir):
        print("App folder aleady exists. Exiting.")
        exit(1)

    # Download latest app template
    with tempfile.TemporaryDirectory() as tmpdirname:
        print("Downloading latest app template... ", end='')
        sdk_tarball = tmpdirname + "/sdk_app_template.tar.gz"
        os.system("wget -q {} -O {}".format(APP_TEMPLATE_URL, sdk_tarball))
        os.system("tar -xf {} -C {}".format(sdk_tarball, tmpdirname))
        os.system("mv {}/sampleapp {}".format(tmpdirname, app_dir))
        print("Done.")

    # Replace sampleapp with shortname
    app_json_file = "{}/sampleapp.json".format(app_dir)
    update_app_info(app_json_file, "name", full_app_name)
    update_app_info(app_json_file, "app_tile_name", full_app_name)
    replace_string_in_file(app_dir+"/www/python/sampleapp.py",      "sampleapp", short_name)
    replace_string_in_file(app_dir+"/nginx/https_sampleapp.conf",   "sampleapp", short_name)
    replace_string_in_file(app_dir+"/sampleapp.service",            "sampleapp", short_name)
    replace_string_in_file(app_dir+"/sampleapp.json",               "sampleapp", short_name)

    # Is this a service?
    is_service = prompt_yes_no("Is this application a service (can be enabled/disabled and not a cli tool)?")
    if not is_service:
        os.remove(app_dir+"/sampleapp.service")

    # Process application (is it a web app?)
    if prompt_yes_no("Does this application have a web-based user interface?"):
        http_port = prompt_integer("Enter the HTTP port for the application?")
        https_port = prompt_integer("Enter the HTTPS port for the application?", (http_port+1))
        update_app_info(app_json_file, "http_port", http_port)
        update_app_info(app_json_file, "https_port", https_port)
        replace_string_in_file(app_dir+"/nginx/https_sampleapp.conf", "8000", http_port)
        replace_string_in_file(app_dir+"/nginx/https_sampleapp.conf", "8001", https_port)
    else:
        # Remove web template items
        os.remove(app_dir+"/nginx/https_sampleapp.conf".format(short_name))
        update_app_info(app_json_file, "http_port", None)
        update_app_info(app_json_file, "https_port", None)
        update_app_info(app_json_file, "app_page_show_open_button", False)

    # Process application (does it depend on Bitcoin / Lightning?)
    if prompt_yes_no("Does this application depend on an active Lightning wallet?"):
        update_app_info(app_json_file, "requires_bitcoin", True)
        update_app_info(app_json_file, "requires_lightning", True)
        update_app_info(app_json_file, "category", "lightning_app")
    else:
        update_app_info(app_json_file, "requires_lightning", False)
        if prompt_yes_no("Does this application depend on Bitcoin?", default_val="y"):
            update_app_info(app_json_file, "requires_bitcoin", True)
            update_app_info(app_json_file, "category", "bitcoin_app")
        else:
            update_app_info(app_json_file, "requires_bitcoin", False)
            update_app_info(app_json_file, "category", "uncategorized")

    # Process application (does it depend on docker?)
    if prompt_yes_no("Does this application depend on Docker?", default_val="n"):
        update_app_info(app_json_file, "requires_docker_image_installation", True)
    else:
        update_app_info(app_json_file, "requires_docker_image_installation", False)

    # Process application (does it depend on electrum server?)
    if prompt_yes_no("Does this application depend on Electrum Server?", default_val="n"):
        update_app_info(app_json_file, "requires_electrs", True)
    else:
        update_app_info(app_json_file, "requires_electrs", False)

    
    # Finally, rename files for app (makes them easier to search for when many apps are loaded)
    rename_files = [
        "www/python/sampleapp.py",
        "www/templates/sampleapp.html",
        "nginx/https_sampleapp.conf",
        "scripts/pre_sampleapp.sh",
        "scripts/post_sampleapp.sh",
        "scripts/uninstall_sampleapp.sh",
        "scripts/install_sampleapp.sh",
        "sampleapp.json",
        "sampleapp.service",
        "sampleapp.png",
    ]
    for orig_name in rename_files:
        new_name = orig_name.replace("sampleapp", short_name)
        old_path = "{}/{}".format(app_dir, orig_name)
        new_path = "{}/{}".format(app_dir, new_name)
        if os.path.exists(old_path):
            os.rename(old_path, new_path)

    # Done
    print("")
    print("Application Created!")
    print("  Available at: {}".format(app_dir))
    print("")
    print("Tips:")
    print(" - Review and update the app data file: {}.json".format(short_name))
    print(" - Update the install script: scripts/install_{}.sh".format(short_name))
    print(" - Update the service file: {}.service".format(short_name))
    print(" - Update the app icon: {}.png".format(short_name))
    print(" - Add app screenshots in the screenshots folder")
    print(" - Review other files for necessary updates")

def build(short_name):
    # If name set, go into folder. If not, use current dir.
    cwd = os.getcwd()
    if os.path.exists(cwd+"/"+short_name):
        app_dir = cwd+"/"+short_name
        clear_dist_folder(app_dir, short_name)
        create_dist_tarball(app_dir, short_name)
    elif os.path.exists(cwd+"/"+short_name+".json"):
        app_dir = cwd
        clear_dist_folder(app_dir, short_name)
        create_dist_tarball(app_dir, short_name)
    else:
        print("Cannot find app to build. Exiting.")
        exit(1)

    print("Application built!")
    print("  Available at: {}".format(app_dir+"/dist/"+short_name+".tar.gz"))

def main():
    parser = ArgumentParser(prog='mynode-sdk')
    subparsers = parser.add_subparsers(dest='command')
    parser_create = subparsers.add_parser('create', help='Create new applicatio')
    parser_install = subparsers.add_parser('build', help='Creat app tarball')
    parser_install.add_argument('app', help='App to install')
    parser_help = subparsers.add_parser('help', help='Display Help')
    args = parser.parse_args()

    if args.command == "create":
        create()
    elif args.command == "build":
        app_name = args.app
        build(app_name)
    elif args.command == "help":
        parser.print_help()
    else:
        parser.print_help()
