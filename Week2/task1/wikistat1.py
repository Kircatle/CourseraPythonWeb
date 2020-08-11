"""парсер для сбора статистики со страниц Википедии
imgs - количество картинок с шириной не меньше 200
headers - количество заголовков с первой буквой E, T, C
linkslen - длина максимальной последовательности ссылок,
между которыми нет других тегов
lists - количество списков, которые не вложены в другие списки
"""

import re
import unittest
from bs4 import BeautifulSoup


def get_image_count_more_200_width(soup):
    imgs = soup.find_all("img")
    imgs_num = 0
    for img in imgs:
        if int(img.get("width", 0)) >= 200:
            imgs_num += 1
    return imgs_num


def get_headers_first_letter_ETC(soup):
    header_num = 0
    headers = soup.find_all(re.compile("h\d"))
    for header in headers:
        if re.search("^[ETC]", header.text):
            header_num += 1
    return header_num


def get_max_length_link_sequence(soup):
    max_len = 0
    tmp_len = 0
    tag = soup.find_next('a')
    dec = soup.descendants
    while True:
        if tag is None or not (tag in dec):
            break
        tag_next = tag.find_next_sibling()
        if tag.name == 'a':
            tmp_len += 1
            if tmp_len > max_len:
                max_len = tmp_len
        if tag_next is None:
            tmp_len = 0
            tag = tag.find_next('a')
        elif tag_next.name == 'a':
            tag = tag_next
        elif tag_next.name != 'a':
            tmp_len = 0
            tag = tag.find_next('a')
    return max_len


def get_lists(soup):
    count_lists = 0
    lists = soup.find_all(['ul', 'ol'])
    for list_tag in lists:
        parents = [parent.name for parent in list_tag.parents]
        if 'ol' in parents or 'ul' in parents:
            continue
        else:
            count_lists += 1
    return count_lists


def parse(path_to_file):
    with open(path_to_file, encoding='utf-8') as website:
        html = website.read()
        soup = BeautifulSoup(html, 'lxml')
        soup = soup.find('div', id='bodyContent')
        imgs = get_image_count_more_200_width(soup)
        headers = get_headers_first_letter_ETC(soup)
        link_len = get_max_length_link_sequence(soup)
        list_count = get_lists(soup)
        return [imgs, headers, link_len, list_count]


class TestParse(unittest.TestCase):
    def test_parse(self):
        test_cases = (
            ('wiki/Stone_Age', [13, 10, 12, 40]),
            ('wiki/Brain', [19, 5, 25, 11]),
            ('wiki/Artificial_intelligence', [8, 19, 13, 198]),
            ('wiki/Python_(programming_language)', [2, 5, 17, 41]),
            ('wiki/Spectrogram', [1, 2, 4, 7]),)
        for path, expected in test_cases:
            with self.subTest(path=path, expected=expected):
                self.assertEqual(parse(path), expected)


if __name__ == '__main__':
    unittest.main()
