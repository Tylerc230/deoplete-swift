import neovim
from pathlib import Path

@neovim.plugin
class SourceKittenDaemon(object):
    def __init__(self, vim):
        self.vim = vim
        self.job_id = None

    @neovim.function('LaunchSourceKitten')
    def launch(self, args):
        project_name = args[0]
        port = args[1]
        try:
            self._launch(project_name, port)
        except Exception as error:
            msg = error.args[0]
            print(msg)
            self._echom(msg)


    @neovim.function('TerminateSourceKitten')
    def terminate(self):
        if self.job_id != None:
            self.vim.funcs.jobstop(self.job_id)
            self.job_id = None

    def _launch(self, project_name, port):
        if not self._check_project_exists(project_name):
            raise FileNotFoundError(f"Couldn't find project {project_name}")
        if self.job_id == None:
            job = f"sourcekittendaemon start --project {project_name} --port {port}"
            self.job_id = self.vim.funcs.jobstart(job)
            if self.job_id == None:
                raise SystemError(f"Failed to start job: {job}")
        else:
            raise SystemError(f"Daemon already running at job id {self.job_id}")

    def _check_project_exists(self, project_name):
        project_path = Path(project_name)
        if project_path.exists():
            return True
        else:
            return False

    def _echom(self, msg):
        self.vim.command(f"echom \"{msg}\"")




