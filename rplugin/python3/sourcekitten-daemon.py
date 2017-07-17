import neovim
import yaml
from pathlib import Path

@neovim.plugin
class SourceKittenDaemon(object):
    def __init__(self, vim):
        self.vim = vim
        self.job_id = None

    @neovim.function('LaunchSourceKittenWithXCodeProj')
    def launch_with_xcodeproj(self, args):
        project_name = args[0]
        port = args[1]
        try:
            self._launch(project_name, port)
        except Exception as error:
            msg = error.args[0]
            self._echom(msg)

    @neovim.function('LaunchSourceKittenFromVexProject')
    def launch_from_vex_project(self, args):
        try:
            vexproj = self._load_vex_project()
            self._launch(vexproj['xcodeproj'], 8081)
        except Exception as error:
            msg = error.args[0]
            self._echom(msg)


    @neovim.function('TerminateSourceKitten')
    def terminate(self):
        if self.job_id != None:
            self.vim.funcs.jobstop(self.job_id)
            self.job_id = None

    def _launch(self, project_name, port):
        self._check_file_exists(project_name)
        if self.job_id == None:
            job = f"sourcekittendaemon start --project {project_name} --port {port}"
            self.job_id = self.vim.funcs.jobstart(job)
            if self.job_id == None:
                raise SystemError(f"Failed to start job: {job}")
        else:
            raise SystemError(f"Daemon already running at job id {self.job_id}")

    def _check_file_exists(self, file_name):
        file_path = Path(file_name)
        if not file_path.exists():
            raise FileNotFoundError(f"Couldn't find file {file_name}")

    def _load_vex_project(self):
        file_name = "vex.yaml"
        self._check_file_exists(file_name)
        vex_proj_path = Path(file_name)
        with vex_proj_path.open() as stream:
            return yaml.load(stream)


    def _echom(self, msg):
        print(msg)
        self.vim.command(f"echom \"{msg}\"")




