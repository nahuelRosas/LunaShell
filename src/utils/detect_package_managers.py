import subprocess

PACKAGE_MANAGERS = []

PACKAGE_MANAGER_NAMES = {
    "apt-get": "Advanced Package Tool (APT)",
    "dnf": "Dandified Yum",
    "flatpak": "Flatpak",
    "snap": "Snap",
    "pip": "pip",
    "pip3": "pip3"
}

def detect_package_managers(quiet=True):
    """
    Detects the available package managers on the system and prints the results.

    Args:
        quiet (bool): If True, suppresses printing the package manager detection results. Default is False.

    Returns:
        list: List of detected package managers.

    Raises:
        SystemExit: If no compatible package manager is found.
    """
    global PACKAGE_MANAGERS

    if PACKAGE_MANAGERS:
        if not quiet:
            print("\033[93mPackage manager(s) detected:\033[0m")
            for manager in PACKAGE_MANAGERS:
                print(f"  \033[96m{PACKAGE_MANAGER_NAMES[manager]}\033[0m - {manager}")
        return PACKAGE_MANAGERS

    available_managers = ["apt-get", "dnf", "flatpak", "snap", "pip", "pip3"]
    detected_managers = []

    for manager in available_managers:
        if subprocess.run(["command", "-v", manager], stdout=subprocess.PIPE).returncode == 0:
            detected_managers.append(manager)

    if not detected_managers:
        print("\033[91mError: No compatible package manager found.\033[0m")
        exit(1)

    PACKAGE_MANAGERS = detected_managers

    if not quiet:
        print("\033[93mPackage manager(s) detected:\033[0m")
        for manager in PACKAGE_MANAGERS:
            print(f"  \033[96m{PACKAGE_MANAGER_NAMES[manager]}\033[0m - {manager}")

    return PACKAGE_MANAGERS
