import os
import sys
import argparse
import shutil
import json
import venv

# import patch

from .utils import printerr, printmsg, printwarn, Fore, Style
from .utils import check_python_version, check_git_installed, check_npm_installed, run_cmd

PYTHON_VERSION_REQUIRED = '3.7'

is_windows = os.name == 'nt'


class PCRA:
    def __init__(self, cli_args):
        self.current_dir = os.getcwd()
        self.has_client = cli_args.client_only or cli_args.full_stack
        self.has_server = cli_args.full_stack
        self.has_venv = not cli_args.no_virtualenv
        self.has_npm = not cli_args.no_javascript
        self.has_git = not cli_args.no_git
        self.template_dir = cli_args.template

        if self.has_server:
            printmsg("Installing full-stack scaffolding...")
        elif self.has_client:
            printmsg("Installing client-only scaffolding...")
        else:
            printmsg("Installing basic react app...")


        self.project_dir = cli_args.folder
        if not os.path.isabs(self.project_dir):
            self.project_dir = os.path.realpath(os.path.join(self.current_dir, self.project_dir))

        self.project_name = os.path.basename(os.path.normpath(self.project_dir))

        self.script_dir = os.path.dirname(os.path.realpath(__file__))
        self.fallback_dir = os.path.join(self.script_dir, 'template')

        if self.has_server:
            self.client_dir = os.path.join(self.project_dir, 'client')
        else:
            self.client_dir = self.project_dir

        if self.template_dir is None:
            self.template_dir = self.fallback_dir
        else:
            if not os.path.isabs(self.template_dir):
                self.template_dir = os.path.realpath(os.path.join(self.current_dir, self.template_dir))

    def _update_project_name(self):
        with open('package.json', 'r') as f:
            json_data = json.load(f)
            json_data['name'] = self.project_name

        with open('package.json', 'w') as f:
            f.write(json.dumps(json_data, indent=2))

    def _copy_template_file(self, destination_dir, file_name):
        if os.path.isfile(os.path.join(self.template_dir, file_name)):
            shutil.copy2(os.path.join(self.template_dir, file_name), destination_dir)
        else:
            shutil.copy2(os.path.join(self.fallback_dir, file_name), destination_dir)

    def validate_template(self) -> bool:
        printmsg('Validating template...')

        if not os.path.isdir(self.template_dir):
            printerr("The template path specified does not exist!")
            return False

        if not self.has_client and not os.path.isdir(os.path.join(self.template_dir, 'default')):
            printerr("The 'default' folder for basic setup does not exist in the template!")
            return False

        if self.has_client and not os.path.isdir(os.path.join(self.template_dir, 'client')):
            printerr("The 'client' folder does not exist in the template!")
            return False

        if self.has_git and self.has_npm and not os.path.isdir(os.path.join(self.template_dir, 'client', 'src')):
            printerr("The 'client' folder does have an src folder in the template!")
            return False

        if self.has_server and not os.path.isdir(os.path.join(self.template_dir, 'server')):
            printerr("The 'server' folder does not exist in the template!")
            return False

        if self.has_venv and not os.path.isfile(os.path.join(self.template_dir, 'client', 'requirements.txt')):
            printwarn("The client 'requirements.txt' pip dependency file does not exist in the template...using default")

        if self.has_npm and not os.path.isfile(os.path.join(self.template_dir, 'client', 'package.json')):
            printwarn("The client 'package.json' file does not exist in the template...using default")

        patch_name = 'asset.js.win.patch' if is_windows else 'asset.js.patch'
        if self.has_npm and not os.path.isfile(os.path.join(self.template_dir, patch_name)):
            printwarn(f"The '{patch_name}' file does not exist in the template...using default")

        if self.has_server and not os.path.isfile(os.path.join(self.template_dir, 'dev-server.js')):
            printwarn("The 'dev-server.js' middleware proxy file does not exist in the template...using default")

        if self.has_server and self.has_venv and not os.path.isfile(os.path.join(self.template_dir, 'server', 'requirements.txt')):
            printwarn("The server 'requirements.txt' pip dependency file does not exist in the template...using default")

        if self.has_git and not os.path.isfile(os.path.join(self.template_dir, '.gitignore')):
            printwarn("The '.gitignore' file does not exist in the template...using default")

        return True

    def copy_template(self):
        printmsg('Copying template...')
        if self.has_client:
            shutil.copytree(os.path.join(self.template_dir, 'client'), self.client_dir,
                            ignore=shutil.ignore_patterns('__pycache__'))
        else:
            shutil.copytree(os.path.join(self.template_dir, 'default'), self.client_dir,
                            ignore=shutil.ignore_patterns('__pycache__'))

        if self.has_server:
            shutil.copytree(os.path.join(self.template_dir, 'client'), self.client_dir,
                            ignore=shutil.ignore_patterns('__pycache__'))
            self._copy_template_file(self.client_dir, 'dev-server.js')

            if self.has_npm:
                os.mkdir(os.path.join(self.client_dir, '.git'))  # Empty folder so that npm version works
            printmsg('Copying server template...')
            shutil.copytree(os.path.join(self.template_dir, 'server'), os.path.join(self.project_dir, 'server'))

        if self.has_git:
            self._copy_template_file(self.project_dir, '.gitignore')

        if os.path.isfile(os.path.join(self.template_dir, 'README.md')):
            shutil.copy2(os.path.join(self.template_dir, 'README.md'), self.project_dir)

    def make_venv(self):
        os.chdir(self.client_dir)

        if self.has_venv:
            printmsg('Creating virtual environment...')
            venv.create('venv', with_pip=True)
            printmsg('Installing Python dependencies...')
            script_folder = 'Scripts' if is_windows else 'bin'

            # Use the default requirements.txt if the supplied template doesn't have one
            source_dir = 'client' if self.has_client else 'default'
            if not os.path.isfile(os.path.join(self.template_dir, source_dir, 'requirements.txt')):
                shutil.copy2(os.path.join(self.fallback_dir, 'client', 'requirements.txt'), '.')

            run_cmd([os.path.join('.', 'venv', script_folder, 'pip'), 'install', '-r', 'requirements.txt'])

            if self.has_server:
                printmsg('Creating server virtual environment...')
                os.chdir(os.path.join(self.project_dir, 'server'))
                venv.create('venv', with_pip=True)
                printmsg('Installing Python dependencies...')

                # Use the default requirements.txt if the supplied template doesn't have one
                if not os.path.isfile(os.path.join(self.template_dir, 'server', 'requirements.txt')):
                    shutil.copy2(os.path.join(self.fallback_dir, 'server', 'requirements.txt'), '.')

                run_cmd([os.path.join('.', 'venv', script_folder, 'pip'), 'install', '-r', 'requirements.txt'])
                os.chdir(self.client_dir)
        else:
            printwarn('SKIPPING virtual environment creation!')

    def make_npm(self):
        os.chdir(self.client_dir)

        if self.has_npm:
            printmsg('Installing JavaScript dependencies...')

            # Use the default package.json if the supplied template doesn't have one
            source_dir = 'client' if self.has_client else 'default'
            if not os.path.isfile(os.path.join(self.template_dir, source_dir, 'package.json')):
                shutil.copy2(os.path.join(self.fallback_dir, 'client', 'package.json'), '.')

            self._update_project_name()
            run_cmd(['npm', 'install'])

            printmsg('Patching Transcrypt Parcel Plugin...')
            patch_name = 'asset.js.win.patch' if is_windows else 'asset.js.patch'

            try:
                import patch

                # Use the default patch if the supplied template doesn't have one
                if not os.path.isfile(os.path.join(self.template_dir, patch_name)):
                    patch_set = patch.fromfile(os.path.join(self.fallback_dir, patch_name))
                else:
                    patch_set = patch.fromfile(os.path.join(self.template_dir, patch_name))

                patch_set.apply(root=os.path.join('.', 'node_modules', 'parcel-plugin-transcrypt'))
            except Exception as e:
                printerr("Transcrypt Parcel Plugin patch failed!")
                printerr(e)
        else:
            printwarn('SKIPPING JavaScript dependencies!')
            if os.path.isfile(os.path.join(self.client_dir, 'package.json')):
                os.remove(os.path.join(self.client_dir, 'package.json'))

    def make_git(self):
        os.chdir(self.project_dir)

        if self.has_git:
            printmsg('Committing project to local Git repository...')
            run_cmd(['git', 'init'])
            run_cmd(['git', 'add', '.'])
            run_cmd(['git', 'commit', '-m', '"Initial Commit"'])
        else:
            printwarn('SKIPPING Git repository creation!')

        if self.has_npm and self.has_git:
            printmsg('Setting npm version...')
            os.chdir(self.client_dir)
            run_cmd(['npm', 'version', 'minor'])
        else:
            printwarn('SKIPPING npm version!')

    def print_instructions(self):
        os.chdir(self.current_dir)
        printmsg(f'Project [{self.project_name}] created in:')
        print(f'  {self.project_dir}')

        if is_windows:
            printwarn("\nNOTE: Windows users will need to set the 'script-shell' option for npm in order for the scripts to work:")
            printwarn('  npm config set script-shell "C:\\Program Files\\git\\bin\\bash.exe"\n')

        print(f"{Fore.YELLOW}")
        print(f"\nInstructions{' to run' if self.has_venv and self.has_npm else ''}:")
        print('=' * 20)

        script_folder = 'Scripts' if is_windows else 'bin'
        script_sh = '' if is_windows else '. '
        if self.has_server:
            print(f"cd {os.path.join(self.project_dir, 'server')}")
            if self.has_venv:
                print(f"{script_sh}{os.path.join('.', 'venv', script_folder, 'activate')}")
                print("python -m appserver")
            print()
            print(f"cd {os.path.join(self.project_dir, 'client')}")
            if self.has_venv:
                print(f"{script_sh}{os.path.join('.', 'venv', script_folder, 'activate')}")
                if self.has_npm:
                    print("npm run dev")
                    print()
                    print("Access application in web browser at http://localhost:8080")
        else:
            print(f"cd {self.project_dir}")
            if self.has_venv:
                print(f"{script_sh}{os.path.join('.', 'venv', script_folder, 'activate')}")
                if self.has_npm:
                    print("npm start")
                    print()
                    print("Access application in web browser at http://localhost:1234")

        print(f"{Style.RESET_ALL}")


def _validate_system(cli_args) -> bool:
    if not check_python_version(PYTHON_VERSION_REQUIRED):
        printerr(f'This command requires Python {PYTHON_VERSION_REQUIRED} and you are using Python {sys.version.split()[0]}')
        return False

    if os.path.isdir(cli_args.folder):
        printerr('The path specified already exists!')
        return False

    if not cli_args.no_git and not check_git_installed():
        printerr('This command requires git to be installed.  Please install it and try again.')
        return False

    if not cli_args.no_javascript and not check_npm_installed():
        printerr('This command requires npm to be installed.  Please install Node.js and try again.')
        return False

    return True


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

    option_group = parser.add_mutually_exclusive_group(required=False)

    option_group.add_argument('-co',
                              '--client-only',
                              action='store_true',
                              help='only create client project (not full stack)')

    option_group.add_argument('-fs',
                              '--full-stack',
                              action='store_true',
                              help='create full-stack project (with Flask back-end)')

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

    if _validate_system(args):
        project = PCRA(args)

        if not project.validate_template():
            printerr(f"Supplied template folder at {project.template_dir} is not valid!")
            sys.exit()

        project.copy_template()
        project.make_venv()
        project.make_npm()
        project.make_git()
        project.print_instructions()
    else:
        sys.exit()


if __name__ == '__main__':
    main()
