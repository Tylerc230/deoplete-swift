import neovim

@neovim.plugin
class SourceKittenDaemon(object):
    def __init__(self, vim):
        self.vim = vim

    @neovim.function('LaunchSourceKitten')
    def launch(self, args):
        project_name = args[0]
        port = args[1]
        job = f"sourcekittendaemon start --project {project_name} --port {port}"
        self.vim.funcs.jobstart(job)

