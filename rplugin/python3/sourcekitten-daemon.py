import neovim

@neovim.plugin
class SourceKittenDaemon(object):
    def __init__(self, vim):
        self.vim = vim

    @neovim.function('LaunchSourceKitten')
    def launch(self, args):
        job = "sourcekittendaemon start --project {project_name} --port {port}"
        cmd = "jobstart ({job})"
        self.vim.command(cmd)

    @neovim.function('DoItPython')
    def doItPython(self, args):
        self.vim.command('echo "hello from DoItPython"')
