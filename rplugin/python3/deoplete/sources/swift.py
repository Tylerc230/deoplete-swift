import os
import re
import sys
import json
import urllib.request as urllib2

from .base import Base

from deoplete.util import charpos2bytepos
from deoplete.util import error

class Source(Base):
    def __init__(self, vim):
        Base.__init__(self, vim)

        self.name = 'Swift'
        self.mark = '[Swift]'
        self.filetypes = ['swift']
        self.input_pattern = r'(?:\b[^\W\d]\w*|[\]\)])(?:\.(?:[^\W\d]\w*)?)*\(?'
        self.rank = 500
        
        self.temp_file_directory = "~/.swifts/"

        if not os.path.exists(self.temp_file_directory):
            os.makedirs(self.temp_file_directory)

    def get_complete_position(self, context):
        m = re.search(r'\w*$', context['input'])
        return m.start() if m else -1

    def gather_candidates(self, context):
        line = self.vim.current.window.cursor[0]
        column = self.vim.current.window.cursor[1]

        filename = self.vim.call('expand', '%:p').split('/')[-1]
        buf = self.vim.current.buffer
        offset = self.vim.call('line2byte', line) + \
            charpos2bytepos(self.vim, context['input'], column) - 1

        source = '\n'.join(buf)
        tmp_path = os.path.expanduser("~/.swifts/"+filename)
        tmp_file = open(tmp_path, 'w+')
        tmp_file.write(source)
        tmp_file.close()

        request = urllib2.Request("http://localhost:8081/complete")
        request.add_header("X-Path", tmp_path)
        request.add_header("X-Offset", offset - 1)
        request.add_header("X-File", filename)
        response = urllib2.urlopen(request).read().decode('utf-8')

        return self.identifiers_from_result(json.loads(response))

    def identifiers_from_result(self, result):
        out = []

        candidates = []
        longest_desc_length = 0
        longest_desc = ''
        for complete in result:
            candidates.append(complete)

            desc_len = len(complete['descriptionKey'])

            if desc_len > longest_desc_length:
                longest_desc = complete['descriptionKey']
                longest_desc_length = desc_len

        for completion in candidates:
            description = completion['descriptionKey']
            _type = completion['typeName']
            abbr = description + ' : ' + _type.rjust((len(description) - longest_desc_length) + 3)
            info = _type

            candidate = dict(word=description,
                              abbr=abbr,
                              dup=1
                              )

            out.append(candidate)

        return out

    def calltips_from_result(self, result):
        out = []

        result = result[1:]
        for calltip in result:
            candidate = dict(
                abbr=calltip,
                word=self.parse_function_parameters(calltip),
                info=calltip
            )

            out.append(candidate)

        return out

    def parse_function_parameters(self, decl):
        """Parses the function parameters from a function decl, returns them as a string"""
        last_lparen = decl.rfind('(')
        last_rparen = decl.rfind(')')

        param_list = decl[last_lparen + 1 : last_rparen]
        param_list = param_list.split(' ')
        # take only the names
        param_list = param_list[1::2]

        return ' '.join(param_list)

    def source_kitten_binary(self):
        try:
            if os.path.isfile(self._source_kitten_binary):
                return self._source_kitten_binary
            else:
                raise
        except Exception:
            return self.find_binary_path('sourcekitten')

    def find_binary_path(self, cmd):
        def is_exec(fpath):
            return os.path.isfile(fpath) and os.access(fpath, os.X_OK)

        fpath, fname = os.path.split(cmd)
        if fpath:
            if is_exec(cmd):
                return cmd
        else:
            for path in os.environ["PATH"].split(os.pathsep):
                path = path.strip('"')
                binary = os.path.join(path, cmd)
                if is_exec(binary):
                    return binary
        return error(self.vim, cmd + ' binary not found')

