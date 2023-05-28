from utils.install_package import install_package
import subprocess
import platform
import distro
import os

def modify_dnf_conf():
    try:
        dnf_conf_path = "/etc/dnf/dnf.conf"
        new_lines = {
            "max_parallel_downloads": "10",
            "fastestmirror": "True",
            "deltarpm": "True",
            "clean_requirements_on_remove": "True",
            "best": "True",
            "skip_if_unavailable": "True",
            "gpgcheck": "True",
            "installonly_limit": "10",
            "zchunk": "True"
        }

        if os.path.isfile(dnf_conf_path):
            modified = False
            updated_lines = []

            with open(dnf_conf_path, "r") as dnf_conf:
                for line in dnf_conf:
                    updated_line = line.rstrip()

                    for key, value in new_lines.items():
                        if key in updated_line:
                            existing_value = updated_line.split("=")[1].strip()
                            if existing_value != value:
                                updated_line = f"{key}={value}"
                                modified = True
                            break

                    updated_lines.append(updated_line)

            if modified:
                with open(dnf_conf_path, "w") as dnf_conf:
                    dnf_conf.write("\n".join(updated_lines))
                print("dnf.conf modified.")
            else:
                print("dnf.conf already up to date.")
        else:
            print("dnf.conf not found.")
    except Exception as e:
        print("Failed to modify dnf.conf:", str(e))



def add_dnf_repositories():
    print("Adding repositories for DNF...")
    repositories = [
        "rpmfusion-free-release",
        "rpmfusion-nonfree-release",
        "dnf-utils"
    ]
    for repo in repositories:
      install_package(repo)

    subprocess.run(["sudo", "dnf", "group", "update", "core", "-y"])

    fedora_version = distro.linux_distribution(full_distribution_name=False)[1]
    config_repos = [
        "https://brave-browser-rpm-release.s3.brave.com/brave-browser.repo",
        f"https://dl.winehq.org/wine-builds/fedora/{fedora_version}/winehq.repo",
        f"https://developer.download.nvidia.com/compute/cuda/repos/fedora{fedora_version}/x86_64/cuda-fedora{fedora_version}.repo"
    ]
    for repo in config_repos:
        if subprocess.run(["sudo", "dnf", "config-manager", "--add-repo", repo], stderr=subprocess.DEVNULL).returncode != 0:
            print("Failed to add repository:", repo)
        else:
            print("Added repository:", repo)

    subprocess.run(["sudo", "rpm", "--import", "https://brave-browser-rpm-release.s3.brave.com/brave-core.asc"])
    subprocess.run(["sudo", "rpm", "--import", "https://packages.microsoft.com/keys/microsoft.asc"])

    vscode_repo_path = "/etc/yum.repos.d/vscode.repo"
    if not os.path.isfile(vscode_repo_path):
        with open(vscode_repo_path, "w") as vscode_repo:
            vscode_repo.write("[code]\nname=Visual Studio Code\nbaseurl=https://packages.microsoft.com/yumrepos/vscode\nenabled=1\ngpgcheck=1\ngpgkey=https://packages.microsoft.com/keys/microsoft.asc\n")
        print("Visual Studio Code repository added.")
    else:
        print("Visual Studio Code repository already exists.")

    print("Repositories added for DNF.")

def add_apt_repositories():
    print("Adding repositories for apt-get...")
    repositories = [
        f"deb http://archive.ubuntu.com/ubuntu/ {distro.linux_distribution(full_distribution_name=False)[2]} main universe",
        f"deb http://security.ubuntu.com/ubuntu/ {distro.linux_distribution(full_distribution_name=False)[2]}-security main universe",
        f"deb http://archive.ubuntu.com/ubuntu/ {distro.linux_distribution(full_distribution_name=False)[2]}-updates main universe",
        f"deb http://archive.canonical.com/ubuntu {distro.linux_distribution(full_distribution_name=False)[2]} partner",
        f"deb http://extras.ubuntu.com/ubuntu {distro.linux_distribution(full_distribution_name=False)[2]} main",
        "deb http://ppa.launchpad.net/webupd8team/java/ubuntu {0} main".format(distro.linux_distribution(full_distribution_name=False)[2]),
        "deb http://ppa.launchpad.net/webupd8team/y-ppa-manager/ubuntu {0} main".format(distro.linux_distribution(full_distribution_name=False)[2])
    ]
    for repo in repositories:
        if subprocess.run(["grep", "-q", "^" + repo, "/etc/apt/sources.list", "/etc/apt/sources.list.d/*"], stderr=subprocess.DEVNULL).returncode != 0:
            subprocess.run(["sudo", "add-apt-repository", repo, "-y"], stderr=subprocess.DEVNULL)
            print("Added repository:", repo)
        else:
            print("Repository already exists:", repo)

    print("Repositories added for apt-get.")

def add_flatpak_repository():
    if "flathub" in subprocess.check_output(["flatpak", "remote-list", "--show-disabled"]).decode():
        print("Flathub remote already configured. Skipping configuration.")
    else:
        print("Configuring Flathub remote...")
        if subprocess.run(["flatpak", "remote-add", "--if-not-exists", "flathub", "https://flathub.org/repo/flathub.flatpakrepo"]).returncode == 0:
            print("Flathub remote configured successfully.")
        else:
            print("Failed to configure Flathub remote.")

def add_repositories():
    print("Adding repositories...\n")

    if platform.system() == "Linux" and (distro.id() == "fedora" or distro.id() == "nobara"):
        print ("Adding repositories for Fedora or System base on Fedora...")
        modify_dnf_conf()
        # add_dnf_repositories()
    elif platform.system() == "Linux" and distro.id() == "ubuntu":
        # add_apt_repositories()
        print("Ubuntu is not supported yet.")
    else:
        print("Unsupported Linux distribution.")

    # add_flatpak_repository()

    print("\nAll repositories have been added successfully.")