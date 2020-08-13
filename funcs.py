""" Funcs of COVID Russia Stats """
import locale
from datetime import datetime
from dateutil.parser import parse
import requests
from bs4 import BeautifulSoup
from translate import Translator


class Voids:
    """Main funcs class"""

    def get_page_code(self, url):
        """Getting page HTML code"""
        return requests.get(url).text

    def get_data(self, text):
        """Getting data from HTML"""
        soup = BeautifulSoup(text, features="lxml")
        data = []
        data_str = soup.find(
            'div', {'class': 'cv-countdown'}).text

        data_str = data_str.replace('\n\n\n', ',')
        data_str = data_str.replace('\n', ',')
        data_str = data_str.replace('\t', '')
        data_str = data_str.replace(',,', ',')
        data_str = data_str.replace(' ', '')
        data = data_str.split(',')

        while len(data) > 4:
            for i in data:
                if i.isdigit() is False:
                    data.remove(i)
        return data

    def get_date_time(self, text):
        """Getting date and time from HTML code"""
        locale.setlocale(locale.LC_ALL, 'en_US')
        translator = Translator(to_lang="en", from_lang="ru")
        soup = BeautifulSoup(text, features="lxml")
        stat_date = soup.find(
            'div', {'class': 'cv-banner__description'}).text
        time = stat_date[-5:]
        stat_date = stat_date.replace('По состоянию на ', '')
        stat_date = stat_date.replace(stat_date[-6:], '')
        today = datetime.today()
        stat_date = stat_date + ' ' + str(today.year)
        stat_date = translator.translate(stat_date)
        try:
            stat_date = datetime.strptime(
                stat_date, '%d %B %Y').strftime('%d.%m.%Y')
        except ValueError:
            try:
                stat_date = datetime.strptime(
                    stat_date, '%B %d, %Y').strftime('%d.%m.%Y')
            except ValueError:
                try:
                    stat_date = datetime.strptime(
                        stat_date, '%d-%b-%Y').strftime('%d.%m.%Y')
                except ValueError:
                    try:
                        stat_date = datetime.strptime(
                            stat_date, '%d %B').strftime('%d.%m')
                        stat_date += '.'+str(datetime.now().year)
                    except ValueError:
                        stat_date = parse(stat_date).strftime('%d.%m.%Y')
        return stat_date, time

    def analysis(self, new_data, data):
        """Calculating analysis"""
        count = int(new_data)-int(data)
        dynamic = float('{:.2f}'.format(
            100 - (int(data)/int(new_data))*100))
        return count, dynamic
