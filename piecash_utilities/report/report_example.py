import os
import traceback

import jinja2
import sys

from piecash_utilities.report import report, RangeOption, DateOption, StringOption


@report(
    title="My default example report [NAMEOFREPORT]",
    name="default-sample-NAMEOFREPORT",
    menu_tip="Default sample generated by 'gc_report_create NAMEOFREPORT'",
    options_default_section="main",
)
def generate_report(
        book_url,
        a_number: RangeOption(
            section="main",
            sort_tag="a",
            documentation_string="This is a number",
            default_value=3),
        a_str: StringOption(
            section="main",
            sort_tag="c",
            documentation_string="This is a string",
            default_value="with a default value"),
        a_date: DateOption(
            section="main",
            sort_tag="d",
            documentation_string="This is a date",
            default_value="(lambda () (cons 'absolute (cons (current-time) 0)))"),
        another_number: RangeOption(
            section="main",
            sort_tag="b",
            documentation_string="This is a number",
            default_value=3)
):
    import piecash
    with piecash.open_book(book_url, readonly=True, open_if_lock=True) as b:
        tpl_name = os.path.basename(__file__).replace("py", "html")
        env = jinja2.Environment(loader=jinja2.PackageLoader(__name__, '.'))
        return env.get_template(tpl_name).render(
            enumerate=enumerate,
            list=list,
            path_report=os.path.abspath(__file__),
            **vars()
        )


if __name__ == '__main__':
    try:
        s = generate_report()
        print(s)
    except Exception as e:
        mystdout = os.fdopen(sys.stdout.fileno(), 'w')
        owrite = mystdout.write
        owrite('<html><head><style>pre {font-family: arial;}</style></head><body>')
        def write(text):
            text = "".join("<pre>{}</pre>".format(l) for l in text.split("\n"))
            owrite(text)
        mystdout.write = write
        traceback.print_exc(file=mystdout)
        owrite("</body></html>")
