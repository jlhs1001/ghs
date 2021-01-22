import click
from bs4 import BeautifulSoup
import requests
from pygments import highlight
from pygments.lexers import get_lexer_by_name
from pygments.formatters import terminal
from configparser import ConfigParser
import os


def log_res(text, location=None, encoding="utf8"):
    if location is not None:
        with open(location, encoding=encoding) as f:
            f.write(str(text))
    else:
        with open("index.html", "w+", encoding="utf8") as f:
            f.write(str(text))


@click.command()
@click.argument("query")
@click.option('--type', default=None, help="Type of result (e.g. code, commits, issues, etc.)")
@click.option('--lang', default=None, help="Programming language to search for")
@click.option('--showcode', default=False, help="Show the code underneath URL location")
def ghs(query, type, lang, showcode):
    s = requests.Session()
    s.headers[
        "user-agent"] = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.141 Safari/537.36"
    s.headers[
        "cookie"] = "_octo=GH1.1.1886874357.1605281759; _device_id=d8dc52af77f92cd6452a0693a8cbe382; user_session=93yeDNxZ3x2GFO5uYbHJdFO51Gef8dj0cfTKdkZt2elnqwPp; __Host-user_session_same_site=93yeDNxZ3x2GFO5uYbHJdFO51Gef8dj0cfTKdkZt2elnqwPp; logged_in=yes; dotcom_user=jlhs1001; tz=Etc%2FGMT%2B12; has_recent_activity=1; _gh_sess=ok3t6LVtG4vYr8kU03vFt1PP8HdMOogTl93%2BBgW3hyEfQcgu2NGrDScf4wRPHFFUDlggbeLvQr3cx7nYPMXqAH6%2BM1IMNghnWvs55LZxkEZxT%2F1iV%2Bla99TyBj893bz0SBOvDukG8REr5RrvdHmJ8iHTEmkJM1wHgOwysC8NjCriQ%2By2dIKKx2bSuLjk0%2FU1OvW0%2BkRMaKQvU7GNtYf%2F%2BCiuBfmD8hcCHx5Y8vmLert%2BS99Sh1BfK4vCqk1wQBKOjvfpDzANW56ccBRGUkoFRB5lIkKCj9iz3WOq0L7FGOwj9uMXGvErzr%2F5aLBh0FjZkbDYgt0tm2kMQiAglugA54tL%2BWe%2FP7L7O8VL2R5PNLLVj1pq2P3EGoGUNkZNGkRSVsvnGgeW%2F7D7XOVBqBKeJil94axkf8TaxsstIMDr0F7Omlbg6Bj6itvSzAyGUtxhK9bx8Qj6N6DHo85XIM71XCJp6%2BHtX2VYeEAIPDE2wsZCAEnJ06RugdjJyl7DmGzobAp%2B%2BXMwb63YiNCB9Bhv4dKa0i6BFeOhAqyHQpccsMCV88ecJ8IaocjPfRCMZZUtqXwyV5qF7lAj6oE62RqtA9kI6tMxm2XW37yM5iWGzRX8YSMTANzRRBI79umb%2F%2Fh8i8%2Byu3qxZjKmMWK6fJE5C23jcXw%2BWWNbhmMXei8fmaAjEsA5re2Xi%2F0fVdNVCK8RcOGNFPvOvryQUSeO%2FH02DLNGNwjZla%2FyCq2JaOSm2GGZSzTGtWTIX%2BXjK27hWtnVfSwttFn4w0IibqZHwyTpVsq1eMxeKZIrOdBLFkX6LY%2FcPRWJVTR9yKt7hNBaTqV7NnUQz15iGYJ%2FPLWg3zx0lpEvCxKaAREXSD2rbg%3D%3D--IbR8AIRKPoYwo3EE--oIs%2FyrggJCXLbLbYU918kA%3D%3D"
    r = s.get(f"https://github.com/search?l={lang}&q={query}&type={type}")
    soup = BeautifulSoup(r.text, 'html.parser')
    res = soup.findAll("div", class_="f4 text-normal")
    for r in res:
        url = r.find("a").get("href")
        if showcode:
            re = s.get("https://raw.githubusercontent.com/" + url.replace("blob/", ""))

            code = re.text

            lexer = get_lexer_by_name(re.url.split('.')[-1], stripall=True)
            formatter = terminal.TerminalFormatter()
            result = highlight(code, lexer, formatter)
            print(result)
            print("--------------------------------------------------------------------")


if __name__ == '__main__':
    ghs()
