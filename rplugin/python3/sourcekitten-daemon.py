import neovim

@neovim.plugin
class SourceKittenDaemon(object):
    def __init__(self, vim):
        self.vim = vim
        self.job_id = None

    @neovim.function('LaunchSourceKitten')
    def launch(self, args):
        project_name = args[0]
        port = args[1]
        self._launch(project_name, port)

    @neovim.function('TerminateSourceKitten')
    def terminate(self):
        if self.job_id != None:
            self.vim.funcs.jobstop(self.job_id)
            self.job_id = None

    def _launch(self, project_name, port):
        if self.job_id == None:
            job = f"sourcekittendaemon start --project {project_name} --port {port}"
            self.job_id = self.vim.funcs.jobstart(job)



