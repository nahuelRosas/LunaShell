from utils.detect_package_managers import detect_package_managers
from utils.execute_shell_commands import execute_shell_commands
from tqdm import tqdm

def upgrade_system_all():
    """
    Upgrades the system and performs cleanup using the available package managers.
    """
    package_managers = detect_package_managers(quiet=True)

    print("\033[93mUpgrading system and performing cleanup...\033[0m")

    total_commands = 0
    for manager in package_managers:
        if manager == "apt-get":
            total_commands += 4
        elif manager == "dnf":
            total_commands += 3
        elif manager == "flatpak":
            total_commands += 2
        elif manager == "snap":
            total_commands += 1

    with tqdm(total=total_commands) as pbar:
        for manager in package_managers:
                if manager == "apt-get":
                    commands = [
                        "sudo apt-get update -y",
                        "sudo apt-get dist-upgrade -y",
                        "sudo apt-get autoremove -y",
                        "sudo apt-get autoclean -y"
                    ]
                    for command in commands:
                        execute_shell_commands(command)
                        pbar.update(1)
                elif manager == "dnf":
                    execute_shell_commands("sudo dnf upgrade -y --refresh", quiet=False)
                    pbar.update(1)
                    commands = [
                        "sudo dnf autoremove -y",
                        "sudo dnf clean all"
                    ]
                    for command in commands:
                        execute_shell_commands(command)
                        pbar.update(1)

                elif manager == "flatpak":
                    execute_shell_commands("sudo flatpak remote-add --if-not-exists flathub https://flathub.org/repo/flathub.flatpakrepo")
                    pbar.update(1)
                    execute_shell_commands("sudo flatpak update -y")
                    pbar.update(1)

                elif manager == "snap":
                    execute_shell_commands("sudo snap refresh")
                    pbar.update(1)


    print("\033[92mSystem upgrade and cleanup completed.\033[0m")
