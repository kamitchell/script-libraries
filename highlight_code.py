import codecs
import locale
import sys
from bs4 import BeautifulSoup
import pygments
import pygments.formatters
import pygments.lexers


def highlight(html):
    soup = BeautifulSoup(html)
    codeblocks = soup.findAll('code')
    for block in codeblocks:
        if block.parent.name == 'pre':
            try:
                code = ''.join([unicode(item) for item in block.contents]).strip()
                if block.has_attr('class'):
                    classname = block['class'][0]
                else:
                    classname = "text"
                lexer = pygments.lexers.get_lexer_by_name(classname)
                formatter = pygments.formatters.HtmlFormatter(encoding='utf-8',
                                                              noclasses=True
                                                              )
                code_hl = pygments.highlight(code, lexer, formatter)
                block.parent.replace_with(BeautifulSoup(code_hl).div)
            except:
                raise
    return soup.decode(formatter='html')

if __name__ == '__main__':
    encoding = locale.getpreferredencoding()
    sys.stdin = codecs.getreader(encoding)(sys.stdin)
    sys.stdout = codecs.getwriter(encoding)(sys.stdout)
    hl = highlight(sys.stdin.read())
    # Remove newline before end of <pre> block; Evernote adds even one more, and the
    # result is a blank line.
    hl = hl.replace('\n</pre>', '</pre>')
    sys.stdout.write(hl)
