import subprocess
from pathlib import Path

from jinja2.ext import Extension


class GitInfoExtension(Extension):
    """Expose git and folder context values to Copier Jinja defaults."""

    def __init__(self, environment):
        super().__init__(environment)

        environment.globals["git_user_name"] = self._get_git_config("user.name")
        environment.globals["git_user_email"] = self._get_git_config("user.email")
        environment.globals["current_folder_name"] = Path.cwd().name

        remote_url = self._get_git_config("remote.origin.url")
        web_url = self._parse_git_url(remote_url)
        environment.globals["git_remote_url"] = web_url
        environment.globals["git_repo_name"] = (
            web_url.split("/")[-1] if web_url else None
        )

    def _get_git_config(self, key):
        try:
            result = subprocess.run(
                ["git", "config", "--get", key],
                capture_output=True,
                text=True,
            )
            value = result.stdout.strip()
            return value if value else None
        except (subprocess.CalledProcessError, FileNotFoundError):
            return None

    def _parse_git_url(self, url):
        if not url:
            return None

        url = url.strip()
        if url.startswith("git@"):
            url = url.replace(":", "/").replace("git@", "https://")
        elif url.startswith("ssh://"):
            url = url.replace("ssh://git@", "https://")

        if url.endswith(".git"):
            url = url[:-4]

        return url
