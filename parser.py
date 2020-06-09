# -*- coding: utf-8 -*-

import requests
from bs4 import BeautifulSoup


class BS:
    """
    Парсер
    """

    def __init__(self, url="https://ms.neurol.ru/centers-of-multiple-sclerosis/"):
        self.url = url
        self.html = self.get_html(self.url)
        self.soup = self.get_soup()

    def get_html(self, url):
        """
        Принимает URL,
        Возвращает html этой страницы.
        """
        r = requests.get(url)
        print(r)
        return r.text

    def get_soup(self):
        """
        Принимает URL,
        Возвращает soup-объект этой страницы.
        """
        page = self.html
        soup = BeautifulSoup(page, "lxml")
        return soup

    def get_rows(self):
        table = self.soup.find('table')
        rows = table.find_all('tr')
        return rows[2:]

    def create_mscenters_list(self):
        rows = self.get_rows()
        ms_centers = []
        for row in rows:
            tds = row.find_all('td')

            if len(tds) == 5:
                city = tds[1].get_text()
                title = tds[2].get_text()
                address = tds[3].get_text()
            elif len(tds) == 4:
                city = ms_centers[-1][1]
                title = tds[1].get_text()
                address = tds[2].get_text()

            country = "Россия"

            ms_centers.append((country, city, title, address))
        return ms_centers


if __name__ == '__main__':
    bs = BS()
    print(bs.create_mscenters_list())