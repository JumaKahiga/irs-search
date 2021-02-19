import itertools
import logging
from concurrent.futures import ThreadPoolExecutor
from os.path import abspath, normpath, dirname, join as pjoin

import requests

logger = logging.getLogger(__name__)

BASE_DIR = normpath(pjoin(abspath(dirname(__file__)), '..'))


class FormDataPdf:
    """Download pdfs for a given form name and year range."""

    def __init__(self, form_name: str, start: int, end: int):
        self.form_name = form_name
        self.start = start
        self.end = end

    def _gen_form_url_name(self):
        """Generate parsed form name as would appear in the url

        Returns
        -------
        url_name : str

        Examples
        --------
        >>> FormData(form_name='Form W-2', start=2018, end=2020)._gen_form_url_name()
        fw2

        """
        url_name = self.form_name.replace('Form',
                                          'f').replace(' ',
                                                       '').replace('-',
                                                                   '').lower()

        return url_name

    def _gen_download_url(self, url_name, year):
        """Generate url where form will be downloaded

        Parameters
        ----------
        url_name : str
            parsed form name as would appear in the url
        year : int
            form year

        Returns
        -------
            : str
            A url

        Examples
        --------
        >>> self._gen_download_url('fw2', 2018)
        https://www.irs.gov/pub/irs-prior/fw2--2018.pdf

        """

        return f'https://www.irs.gov/pub/irs-prior/{url_name}--{year}.pdf'

    def _download_pdf(self, year):
        """Download pdf for a specific year

        Parameters
        ----------
        year : str

        Returns
            : list of bool or str
            Either [False] if download wasn't possible or ['downloaded file path'] if successful

        """

        url_name = self._gen_form_url_name()
        filename = f'{self.form_name} - {year}.pdf'
        url = self._gen_download_url(url_name, year)
        resp = requests.get(url)

        if not (200 <= resp.status_code <= 299):
            logger.warning(
                f'could not find a pdf for {self.form_name} for the year {year}'
            )
            return [False]

        path_to_file = pjoin(BASE_DIR, 'form_pdf', 'pdf_downloads', filename)

        try:
            with open(path_to_file, 'wb+') as file:
                file.write(resp.content)
        except Exception as e:
            logger.exception(
                f'downloading the pdf failed with this exception: {e}')

        return [path_to_file]

    def download_pdfs(self):
        """Download pdfs. """

        years = []

        for year in range(self.start, self.end + 1):
            years.append(year)

        with ThreadPoolExecutor(max_workers=5) as executor:
            _result = executor.map(self._download_pdf, years)

        if not _result:
            logger.warning(
                f'no pdfs downloaded for {self.form_name} between years {self.start} and {self.end}'
            )
            return []

        result = list(itertools.chain(*_result))
        return {'downloaded pdf paths': result}
