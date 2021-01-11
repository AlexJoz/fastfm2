import configparser
import subprocess


def write_release_version(version, commit):
    with open("version.txt", "w") as f:
        f.write(f"{version}\n\n{commit}\n\n"
                "Version number and commit hash are <auto-generated> "
                "for external release. \n"
                "DO NOT CHANGE! \n")


def read_release_version():
    try:
        with open("version.txt", "r") as f:
            version = f.readlines()[0]
            return version.strip()
    except:
        return None


def get_version_from_txt():
    version = read_release_version()

    if version is None:
        raise ValueError("Cannot find the version number!")

    return version


def get_version_from_pyproject():
    config = configparser.ConfigParser()
    config.read('pyproject.toml')
    if 'tool.poetry' not in config.sections():
        raise ValueError("Invalid pyproject.toml")
    return config['tool.poetry'].get('version', '0').strip('"')


def get_commit_hash():
    res = subprocess.check_output(['git', 'rev-parse', 'HEAD'])
    return res.strip().decode()


def check_update_current_version():
    previous_version = get_version_from_txt()
    current_version = get_version_from_pyproject()
    current_commit = get_commit_hash()
    write_release_version(current_version, current_commit)
    return previous_version, current_version


if __name__ == "__main__":
    print(f"Version check: v{get_version_from_txt()} "
          f"-> v{get_version_from_pyproject()}")
    check_update_current_version()
