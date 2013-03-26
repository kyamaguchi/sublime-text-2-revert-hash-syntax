import sublime, sublime_plugin, re

# http://www.sublimetext.com/docs/2/api_reference.html#sublime_plugin.TextCommand
# http://net.tutsplus.com/tutorials/python-tutorials/how-to-create-a-sublime-text-2-plugin/

# The code to detect line is copied from Packages/Default/duplicate_line.py

def old_style_hash(matchobj):
    spaces = len(matchobj.group(2))
    if spaces < 1:
        spaces = 1

    return ":%s =>%s%s" % (matchobj.group(1), spaces * ' ', matchobj.group(3))

class RevertHashSyntaxCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        for region in self.view.sel():
            if region.empty():
                line = self.view.line(region)
                self.revert_hashes(edit, line)
            else:
                self.revert_hashes(edit, region)

    def revert_hashes(self, edit, region):
        # Get the selected text
        s = self.view.substr(region)
        # Transform Ruby 1.9 hash syntax to 1.8
        s = re.sub(r'([a-zA-Z_0-9]+)\:(\s*)([^:])', old_style_hash, s)
        # Replace the selection with transformed text
        self.view.replace(edit, region, s)
