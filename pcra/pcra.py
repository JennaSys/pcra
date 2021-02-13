import os
import sys
import argparse
import shutil
import subprocess
import re
import json
import venv

# import patch

is_windows = os.name == 'nt'

PYTHON_VERSION_REQUIRED = '3.7'

try:
    from colorama import Fore, Style, init as colorama_init
    colorama_init()
except ModuleNotFoundError:
    # If colorama is not installed create failover classes for colored text output
    if is_windows:
        print("[Colored output not available]")
        class Fore:
            CYAN = ''
            YELLOW = ''
            RED = ''
        class Style:
            RESET_ALL = ''
    else:
        class Fore:
            CYAN = '\033[1;36;48m'
            YELLOW = '\033[1;33;48m'
            RED = '\033[1;31;48m'
        class Style:
            RESET_ALL = '\033[1;37;0m'


process_kwargs = dict(stdout=subprocess.PIPE,
                      stderr=subprocess.PIPE,
                      universal_newlines=True,
                      text=True
                      )
if is_windows:
    process_kwargs['shell'] = True  # Windows npm commands fail without shell: FileNotFoundError


def printmsg(msg):
    print(f'{Fore.CYAN}{msg}{Style.RESET_ALL}')


def printerr(msg):
    print(f'{Fore.RED}{msg}{Style.RESET_ALL}')


def printwarn(msg):
    print(f'{Fore.YELLOW}{msg}{Style.RESET_ALL}')


def check_python_version():
    python_version = sys.version_info
    required_version = tuple(tuple(map(int, PYTHON_VERSION_REQUIRED.split('.'))))
    return (python_version.major, python_version.minor) == required_version


def check_git_installed():
    try:
        process = subprocess.Popen(['git', '--version'], **process_kwargs)
        return process.stdout.readline().startswith('git version')
    except FileNotFoundError as e:
        print(e)
        return False


def check_npm_installed():
    try:
        process = subprocess.Popen(['npm', '--version'], **process_kwargs)
        r = re.compile(r'^\d+\.\d+\.\d+$')  # 6.14.8
        return r.match(process.stdout.readline()) is not None
    except FileNotFoundError as e:
        print(e)
        return False


def run_cmd(args):
    process = subprocess.Popen(args, **process_kwargs)

    while True:
        output = process.stdout.readline()
        output_text = output.strip()
        if len(output_text) > 0:
            print(output_text)
        # Do something else
        return_code = process.poll()
        if return_code is not None:
            # Process has finished, read rest of the output
            for output in process.stdout.readlines():
                output_text = output.strip()
                if len(output_text) > 0:
                    print(output_text)

            if return_code != 0:
                print('RETURN CODE:', return_code)
                for output in process.stderr.readlines():
                    output_text = output.strip()
                    if len(output_text) > 0:
                        print(output_text)

            break


def update_project_name(new_name):
    with open('package.json', 'r') as f:
        json_data = json.load(f)
        json_data['name'] = new_name

    with open('package.json', 'w') as f:
        f.write(json.dumps(json_data, indent=2))


def validate_template(template_dir, is_fs=True, has_venv=True, has_npm=True, has_git=True) -> bool:
    if not os.path.isdir(template_dir):
        printerr("The template path specified does not exist!")
        return False

    if not os.path.isdir(os.path.join(template_dir, 'client')):
        printerr("The 'client' folder does not exist in the template!")
        return False

    if has_git and has_npm and not os.path.isdir(os.path.join(template_dir, 'client', 'src')):
        printerr("The 'client' folder does have an src folder in the template!")
        return False

    if is_fs and not os.path.isdir(os.path.join(template_dir, 'server')):
        printerr("The 'server' folder does not exist in the template!")
        return False

    if has_venv and not os.path.isfile(os.path.join(template_dir, 'client', 'requirements.txt')):
        printwarn("The client 'requirements.txt' pip dependency file does not exist in the template...using default")

    if has_npm and not os.path.isfile(os.path.join(template_dir, 'client', 'package.json')):
        printwarn("The client 'package.json' file does not exist in the template...using default")

    patch_name = 'asset.js.win.patch' if is_windows else 'asset.js.patch'
    if has_npm and not os.path.isfile(os.path.join(template_dir, patch_name)):
        printwarn(f"The '{patch_name}' file does not exist in the template...using default")

    if is_fs and not os.path.isfile(os.path.join(template_dir, 'dev-server.js')):
        printwarn("The 'dev-server.js' middleware proxy file does not exist in the template...using default")

    if is_fs and has_venv and not os.path.isfile(os.path.join(template_dir, 'server', 'requirements.txt')):
        printwarn("The server 'requirements.txt' pip dependency file does not exist in the template...using default")

    if has_git and not os.path.isfile(os.path.join(template_dir, '.gitignore')):
        printwarn("The '.gitignore' file does not exist in the template...using default")

    return True


def copy_template_file(template_dir, fallback_dir, destination_dir, file_name):
    if os.path.isfile(os.path.join(template_dir, file_name)):
        shutil.copy2(os.path.join(template_dir, file_name), destination_dir)
    else:
        shutil.copy2(os.path.join(fallback_dir, file_name), destination_dir)


def print_instructions(project_path, full_stack):
    print(f"{Fore.YELLOW}")
    print("\nInstructions to run:")
    print('=' * 20)

    script_folder = 'Scripts' if is_windows else 'bin'
    script_sh = '' if is_windows else '. '
    if full_stack:
        print(f"cd {os.path.join(project_path, 'server')}")
        print(f"{script_sh}{os.path.join('.', 'venv', script_folder, 'activate')}")
        print("python -m appserver")
        print()
        print(f"cd {os.path.join(project_path, 'client')}")
        print(f"{script_sh}{os.path.join('.', 'venv', script_folder, 'activate')}")
        print("npm run dev")
        print()
        print("Access application in web browser at http://localhost:8080")
    else:
        print(f"cd {project_path}")
        print(f"{script_sh}{os.path.join('.', 'venv', script_folder, 'activate')}")
        print("npm start")
        print()
        print("Access application in web browser at http://localhost:1234")

    print(f"{Style.RESET_ALL}")


def make_project(project_path, full_stack=True, has_venv=False, has_npm=False, has_git=False, template_dir=None):
    current_dir = os.getcwd()
    project_folder = os.path.basename(os.path.normpath(project_path))
    if not os.path.isabs(project_path):
        project_path = os.path.realpath(os.path.join(current_dir, project_path))

    script_dir = os.path.dirname(os.path.realpath(__file__))
    fallback_dir = os.path.join(script_dir, 'template')
    if template_dir is None:
        template_dir = fallback_dir
    else:
        if not os.path.isabs(template_dir):
            template_dir = os.path.join(current_dir, template_dir)

        printmsg('Validating template...')
        if not validate_template(template_dir, full_stack, has_venv, has_npm, has_git):
            printerr(f"Supplied template folder at {template_dir} is not valid!")
            return

    printmsg('Copying template...')
    if full_stack:
        client_dir = os.path.join(project_path, 'client')
        shutil.copytree(os.path.join(template_dir, 'client'), client_dir, ignore=shutil.ignore_patterns('__pycache__'))
        copy_template_file(template_dir, fallback_dir, client_dir, 'dev-server.js')

        if has_npm:
            os.mkdir(os.path.join(client_dir, '.git'))  # Empty folder so that npm version works
        printmsg('Copying server template...')
        shutil.copytree(os.path.join(template_dir, 'server'), os.path.join(project_path, 'server'))
    else:
        client_dir = project_path
        shutil.copytree(os.path.join(template_dir, 'client'), client_dir, ignore=shutil.ignore_patterns('__pycache__'))

    if has_git:
        copy_template_file(template_dir, fallback_dir, project_path, '.gitignore')

    if os.path.isfile(os.path.join(template_dir, 'README.md')):
        shutil.copy2(os.path.join(template_dir, 'README.md'), project_path)

    os.chdir(client_dir)

    if has_venv:
        printmsg('Creating virtual environment...')
        venv.create('venv', with_pip=True)
        printmsg('Installing Python dependencies...')
        script_folder = 'Scripts' if is_windows else 'bin'

        # Use the default requirements.txt if the supplied template doesn't have one
        if not os.path.isfile(os.path.join(template_dir, 'client', 'requirements.txt')):
            shutil.copy2(os.path.join(fallback_dir, 'client', 'requirements.txt'), '.')

        run_cmd([os.path.join('.', 'venv', script_folder, 'pip'), 'install', '-r', 'requirements.txt'])

        if full_stack:
            printmsg('Creating server virtual environment...')
            os.chdir(os.path.join(project_path, 'server'))
            venv.create('venv', with_pip=True)
            printmsg('Installing Python dependencies...')

            # Use the default requirements.txt if the supplied template doesn't have one
            if not os.path.isfile(os.path.join(template_dir, 'server', 'requirements.txt')):
                shutil.copy2(os.path.join(fallback_dir, 'server', 'requirements.txt'), '.')

            run_cmd([os.path.join('.', 'venv', script_folder, 'pip'), 'install', '-r', 'requirements.txt'])
            os.chdir(client_dir)
    else:
        printwarn('SKIPPING virtual environment creation!')

    if has_npm:
        printmsg('Installing JavaScript dependencies...')

        # Use the default package.json if the supplied template doesn't have one
        if not os.path.isfile(os.path.join(template_dir, 'client', 'package.json')):
            shutil.copy2(os.path.join(fallback_dir, 'client', 'package.json'), '.')

        update_project_name(project_folder)
        run_cmd(['npm', 'install'])

        printmsg('Patching Transcrypt Parcel Plugin...')
        patch_name = 'asset.js.win.patch' if is_windows else 'asset.js.patch'

        try:
            import patch

            # Use the default patch if the supplied template doesn't have one
            if not os.path.isfile(os.path.join(template_dir, patch_name)):
                patch_set = patch.fromfile(os.path.join(fallback_dir, patch_name))
            else:
                patch_set = patch.fromfile(os.path.join(template_dir, patch_name))

            patch_set.apply(root=os.path.join('.', 'node_modules', 'parcel-plugin-transcrypt'))
        except Exception as e:
            printerr("Transcrypt Parcel Plugin patch failed!")
            printerr(e)
    else:
        printwarn('SKIPPING JavaScript dependencies!')
        if os.path.isfile(os.path.join(client_dir, 'package.json')):
            os.remove(os.path.join(client_dir, 'package.json'))

    if has_git:
        printmsg('Committing project to local Git repository...')
        os.chdir(project_path)
        run_cmd(['git', 'init'])
        run_cmd(['git', 'add', '.'])
        run_cmd(['git', 'commit', '-m', '"Initial Commit"'])
    else:
        printwarn('SKIPPING Git repository creation!')

    if has_npm and has_git:
        printmsg('Setting npm version...')
        os.chdir(client_dir)
        run_cmd(['npm', 'version', 'minor'])
    else:
        printwarn('SKIPPING npm version!')

    os.chdir(current_dir)
    printmsg(f'Project [{project_folder}] created in:')
    print(f'  {project_path}')

    if is_windows:
        printwarn("\nNOTE: Windows users will need to set the 'script-shell' option for npm in order for the scripts to work:")
        printwarn('  npm config set script-shell "C:\\Program Files\\git\\bin\\bash.exe"\n')

    print_instructions(project_path, full_stack)


class WideFormatter(argparse.HelpFormatter):
    def __init__(self, prog):
        width = shutil.get_terminal_size()[0]
        super().__init__(prog, max_help_position=40, width=width)


def main():
    parser = argparse.ArgumentParser(prog='py-create-react-app',
                                     description='Python Create React App: Template based Python React project scaffolding creator',
                                     epilog=f'NOTE: Must be run with Python version {PYTHON_VERSION_REQUIRED}',
                                     formatter_class=WideFormatter,
                                     allow_abbrev=False,
                                     )
    parser.add_argument('folder',
                        metavar='FOLDER_NAME',
                        type=str,
                        help='name of the project folder (must not already exist)')

    parser.add_argument('-co',
                        '--client-only',
                        action='store_true',
                        help='only create client project (not full stack)')

    parser.add_argument('-nv',
                        '--no-virtualenv',
                        action='store_true',
                        help='DO NOT create virtual environments')

    parser.add_argument('-njs',
                        '--no-javascript',
                        action='store_true',
                        help='DO NOT install JavaScript libraries')

    parser.add_argument('-ng',
                        '--no-git',
                        action='store_true',
                        help='DO NOT create Git repository')

    parser.add_argument('-t',
                        '--template',
                        action='store',
                        help='alternate template folder to use')

    args = parser.parse_args()
    project_path = args.folder

    if not check_python_version():
        printerr(f'This command requires Python {PYTHON_VERSION_REQUIRED} and you are using Python {sys.version.split()[0]}')
        sys.exit()

    if os.path.isdir(project_path):
        printerr('The path specified already exists!')
        sys.exit()

    if not args.no_git and not check_git_installed():
        printerr('This command requires git to be installed.  Please install it and try again.')
        sys.exit()

    if not args.no_javascript and not check_npm_installed():
        printerr('This command requires npm to be installed.  Please install Node.js and try again.')
        sys.exit()

    # All good so proceed...
    make_project(project_path, not args.client_only, not args.no_virtualenv, not args.no_javascript, not args.no_git, args.template)


if __name__ == '__main__':
    main()
