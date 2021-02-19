import itertools
import json
import logging
import urllib.parse
from concurrent.futures import ThreadPoolExecutor

import lxml.html as lh
import pandas as pd
import requests

logger = logging.getLogger(__name__)


class FormDataJson:
    """Generate information results for provided form names. """

    def __init__(self, form_names: list):
        self.form_names = form_names

    def generate_urls(self, form_name: str):
        parsed_name = urllib.parse.quote_plus(form_name)
        url_1 = "https://apps.irs.gov/app/picklist/list/priorFormPublication.html?indexOfFirstRow=0&sortColumn=currentYearRevDate&value={}&criteria=formNumber&resultsPerPage=25&isDescending=true".format(
            parsed_name)
        url_2 = "https://apps.irs.gov/app/picklist/list/priorFormPublication.html?indexOfFirstRow=0&sortColumn=currentYearRevDate&value={}&criteria=formNumber&resultsPerPage=25&isDescending=false".format(
            parsed_name)

        return {'desc': url_1, 'asc': url_2}

    def _get_extrema(self, df, form_name, max_=True):
        """Get either maximum or minimum years for a given form name

        Parameters
        ----------
        df : Pandas dataframe
            Dataframe containing results for a given form name

        form_name : str
            Name of form to be searched

        max_ : bool
            If True, it returns maximum year else minimum year

        """

        if max_:
            _result = df.loc[df['Product Number'] == form_name].groupby(
                ['Product Number', 'Title'])['Revision Date'].max()
        else:
            _result = df.loc[df['Product Number'] == form_name].groupby(
                ['Product Number', 'Title'])['Revision Date'].min()

        result = _result.to_dict()
        return result

    def _retrieve_html(self, url, form_name):
        """Retrieve html from search results url

        Parameters
        ----------
        url : str
            Search results url

        form_name : str
            Name of form to be searched

        Returns
        -------
        df : Pandas dataframe
            Dataframe containing results for a given form name

        """

        page = requests.get(url)
        doc = lh.fromstring(page.content)

        tr_elements = doc.xpath('//table[@class="picklist-dataTable"]//tr')

        col = []
        i = 0

        for t in tr_elements[0]:
            i += 1
            name = t.text_content()
            col.append((name.strip(), []))

        for j in range(1, len(tr_elements)):
            T = tr_elements[j]

            if len(T) != 3:
                break

            i = 0

            for t in T.iterchildren():
                data = t.text_content()

                col[i][1].append(data.strip())
                i += 1

        Dict = {title: column for (title, column) in col}
        df = pd.DataFrame(Dict)

        return df

    def _get_data(self, form_name):
        """Get data for a specific form name

        Parameters
        ----------
        form_name : str
            Name of form to be searched

        Returns
        -------
            : list of dict
            The dict is in the following format:
                {
                    'form_number': str,
                    'form_title': str,
                    'min_year': int,
                    'max_year': int
                }

        """
        urls = self.generate_urls(form_name)
        form_dict = {}

        asc_df = self._retrieve_html(url=urls.get('asc'), form_name=form_name)

        desc_df = self._retrieve_html(url=urls.get('desc'),
                                      form_name=form_name)

        asc_result = self._get_extrema(asc_df, form_name, max_=False)
        desc_result = self._get_extrema(desc_df, form_name)

        if not asc_result and desc_result:
            return []

        number_title = list(asc_result.keys())[0]
        number = number_title[0]
        title = number_title[1]

        form_dict['form_number'] = number
        form_dict['form_title'] = title
        form_dict['min_year'] = asc_result.get(number_title)
        form_dict['max_year'] = desc_result.get(number_title)

        return [form_dict]

    def get_data(self):
        """Generate informational results for given form names. """

        with ThreadPoolExecutor(max_workers=5) as executor:
            _data = executor.map(self._get_data, self.form_names)

        if not _data:
            logger.warning(
                f'No data was retrieved for the following form_names {json.dumps(self.form_names)}'
            )
            return []

        data = list(itertools.chain(*_data))

        return json.dumps(data, indent=4, sort_keys=True)
