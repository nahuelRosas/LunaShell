from utils.detect_package_managers import detect_package_managers
import subprocess

PACKAGE_MANAGERS = detect_package_managers()

def package_installed(package_name):
    """
    Checks if a package is installed on the system.

    Args:
        package_name (str): Name of the package to check.

    Returns:
        bool: True if the package is installed, False otherwise.
    """
    # Check using command -v
    if subprocess.run(["command", "-v", package_name], stdout=subprocess.PIPE, stderr=subprocess.PIPE).returncode == 0:
        return True

    # Check using package managers
    for manager in PACKAGE_MANAGERS:
        if manager == "apt-get":
            if (
                subprocess.run(["dpkg", "-s", package_name], stdout=subprocess.PIPE, stderr=subprocess.PIPE).returncode == 0
            ):
                return True
        elif manager == "dnf":
            if (
                subprocess.run(["rpm", "-q", package_name], stdout=subprocess.PIPE, stderr=subprocess.PIPE).returncode == 0
            ):
                return True
        elif manager == "flatpak":
            if (
                subprocess.run(
                    ["flatpak", "list", "--app", "--columns=application"],
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                )
                .stdout.decode()
                .count(package_name) > 0
            ):
                return True
        elif manager == "snap":
            if (
                subprocess.run(["snap", "list", package_name], stdout=subprocess.PIPE, stderr=subprocess.PIPE).returncode == 0
            ):
                return True
        elif manager == "pip":
            try:
                subprocess.check_output(["pip", "show", package_name], stderr=subprocess.DEVNULL)
                return True
            except subprocess.CalledProcessError:
                pass
        elif manager == "pip3":
            try:
                subprocess.check_output(["pip3", "show", package_name], stderr=subprocess.DEVNULL)
                return True
            except subprocess.CalledProcessError:
                pass

    return False
