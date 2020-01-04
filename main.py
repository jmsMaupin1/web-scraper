#!/usr/bin/env python

__author__ = 'jmsMaupin1'

import argparse
import requests
import sys
import re
from HTMLParser import HTMLParser


class SiteHTMLParser(HTMLParser):
    urls = set()
    emails = set()
    phone_numbers = set()

    def handle_starttag(self, tag, attrs):
        """Search for URLs and Emails in the starting anchor tag"""
        if tag == 'a':
            for tag, content in attrs:
                if tag == 'href':
                    if content.startswith('mailto'):
                        self.emails.add(content[7:])
                    elif content.startswith('http'):
                        self.urls.add(content)

    def handle_data(self, data):
        phone_exp = r'1?\W*([2-9][0-8][0-9])\W*([2-9][0-9]{2})\W*([0-9]{4})(\se?x?t?(\d*))?'
        email_exp = r'[\w-]+@([\w-]+\.)+[\w-]+'
        phone_match = re.match(phone_exp, data)
        email_match = re.match(email_exp, data)

        if phone_match:
            self.phone_numbers.add(phone_match.group())

        elif email_match:
            self.emails.add(email_match.group())


def scrape(url):
    res = requests.get(url)
    res.raise_for_status()
    return res.text


def parse_scraped_text(scraped_text):
    scraper = SiteHTMLParser()
    scraper.feed(scraped_text)

    print('-----URL List-----')
    if len(scraper.urls):
        for url in scraper.urls:
            print(url)
    else:
        print('None')
    print('-----Email List-----')
    if len(scraper.emails):
        for email in scraper.emails:
            print(email)
    else:
        print('None')
    print('-----Phone List-----')
    if len(scraper.phone_numbers):
        for number in scraper.phone_numbers:
            print(number)
    else:
        print('None')


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('url', help='URL to scrape information from')
    args = parser.parse_args()

    if not args:
        parser.print_usage()
        sys.exit(1)

    with open('kenzie.academy.html') as html:
        parse_scraped_text(html.read())

    # parse_scraped_text(scrape(args.url))


if __name__ == '__main__':
    main()
