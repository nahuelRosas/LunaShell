from typing import Union
from utils.detect_package_managers import detect_package_managers
from utils.execute_shell_commands import execute_shell_commands
from utils.package_installed import package_installed

PACKAGE_MANAGERS = detect_package_managers()
def install_package(package_name:str, force_manager:Union[str,None]=None):
    """
    Installs a package using the available package managers.

    Args:
        package_name (str): Name of the package to install.
        force_manager (str, optional): Name of the package manager to force the installation.
            Defaults to None.

    Returns:
        None
    """
    installed = False

    if package_installed(package_name) and not force_manager:
        print(f"\033[92mPackage '{package_name}' is already installed.\033[0m")
        return
    else:
        print(f"Installing package '{package_name}'...")
        for manager in PACKAGE_MANAGERS:
            if force_manager and manager != force_manager:
                continue

            print(f"Trying installation using package manager: {manager}")

            command = ""
            if manager == "apt-get":
                command = f"sudo apt-get install {package_name} -y"
            elif manager == "dnf":
                command = f"sudo dnf install {package_name} -y"
            elif manager == "flatpak":
                command = f"flatpak install {package_name} -y"
            elif manager == "snap":
                command = f"sudo snap install {package_name}"
            elif manager == "pip":
                command = f"pip install {package_name}"
            elif manager == "pip3":
                command = f"pip3 install {package_name}"

            if command:
                output = execute_shell_commands(command, False)
                if output == 0:
                    installed = True
                    break

            # Check if the installation was successful
            if package_installed(package_name):
                installed = True
                break

    if installed:
        print(f"\033[92mPackage '{package_name}' installed successfully.\033[0m")
    else:
        print(f"\033[91mFailed to install package '{package_name}'.\033[0m")
