import subprocess
from pathlib import Path

from build import ProjectBuilder
from build.env import IsolatedEnvBuilder

__all__ = ['run_python_in_env']


def run_python_in_env(srcdir, args, **kwargs):
    """
    Execute ``python <args>`` in path in the build environment.

    The build environment will be read from the ``srcdir/pyproject.toml`` file.
    """
    srcdir = Path(srcdir).expanduser().absolute()
    builder = ProjectBuilder(srcdir)

    cwd = kwargs.pop("cwd", srcdir)

    with IsolatedEnvBuilder() as env:
        builder.python_executable = env.executable
        env.install(builder.build_dependencies)

        sub_args = [builder.python_executable] + list(args)
        return subprocess.call(sub_args, cwd=cwd, **kwargs)
