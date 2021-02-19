import click

from form_json.script import FormDataJson
from form_pdf.script import FormDataPdf


@click.group()
def app():
    pass


@app.command()
@click.option('--form_names',
              prompt='Please enter comma separated form names',
              help='For example: Form W-2, Form 1095-C')
def run_json_script(form_names):
    _parsed_form_names = form_names.split(',')
    parsed_form_names = []

    for name in _parsed_form_names:
        parsed_form_names.append(name.strip())

    click.echo(FormDataJson(parsed_form_names).get_data())


@app.command()
@click.option('--form_name',
              prompt='Please enter a form name',
              help='Name of form')
@click.option('--start',
              prompt='Please specify start year',
              help='Year from when the downloads will be made')
@click.option('--end',
              prompt='Please specify end year',
              help='Year upto when the downloads will be made')
def run_pdf_script(form_name, start, end):
    try:
        start = int(start)
        end = int(end)
    except ValueError:
        click.echo(
            'The start and end years must be numbers eg 1999, 2000, 2020 etc')
        return

    click.echo(
        FormDataPdf(form_name=form_name, start=start, end=end).download_pdfs())


if __name__ == '__main__':
    app()
