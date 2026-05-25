import nox


@nox.session
def lint(session):
    session.run("uv", "sync", "--dev", external=True)
    session.run("uv", "run", "ruff", "check", ".", external=True)
    session.run("uv", "run", "ruff", "format", "--check", ".", external=True)


@nox.session
def tests(session):
    session.run("uv", "sync", "--dev", external=True)
    session.run("uv", "pip", "install", "-e", ".", external=True)
    session.run("uv", "run", "pytest", external=True, env={"PYTHONPATH": "src"})


