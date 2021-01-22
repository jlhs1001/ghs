# Iteration of highliting code from github
# V1.0 Confirmed working version

from pygments import highlight
from pygments.lexers import get_lexer_by_name
from pygments.formatters import terminal
import requests


s = requests.Session()
s.headers["user-agent"] = "<YOUR USER AGENT>"
s.headers["cookie"] = "<YOUR COOKIE>"

r = s.get("https://raw.githubusercontent.com/Lvyn/neco-net-compiler/cb80bab29cf8d8f8546d58dfdac016d94293138a/tests/benchmarks/ns_nospy/dolev_yao.py")

code = r.text

lexer = get_lexer_by_name(r.url.split('.')[-1], stripall=True)
formatter = terminal.TerminalFormatter()
result = highlight(code, lexer, formatter)
print(result)
