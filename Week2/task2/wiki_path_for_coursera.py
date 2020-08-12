from bs4 import BeautifulSoup
import os
import re
from collections import deque
import unittest


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


def get_links(path, page):
    files = os.listdir(path)
    with open(os.path.join(path, page), encoding="utf-8") as file:
        links = re.findall(r"(?<=/wiki/)[\w()]+", file.read()) 
    new_links = []
    for link in links:
        if link not in files:
            continue
        new_links.append(link) 
    return new_links


def get_parents_dict(path, page, end_page):
    checked_pages = set()
    queue = deque([page])
    parents = {}
    cur_v = page
    while cur_v != end_page:
        cur_v = queue.popleft()
        for neigh_v in get_links(path, cur_v):
            if neigh_v not in checked_pages:
                checked_pages.add(neigh_v)
                queue.append(neigh_v)
                parents.update({neigh_v: cur_v})
    parents.update({page: None})
    return parents


def get_short_path(parents, page, end_page):
    short_path = [end_page]
    parent = parents[end_page]
    while parent is not None:
        short_path.append(parent)
        parent = parents[parent]
    short_path.reverse()
    return short_path


def build_bridge(path, start_page, end_page):
    """возвращает список страниц, по которым можно перейти по ссылкам со
    start_page на end_page, начальная и конечная страницы включаются в
    результирующий список"""
    parents = get_parents_dict(path, start_page, end_page)
    short_path = get_short_path(parents, start_page, end_page)
    return short_path


def get_statistics(path, start_page, end_page):
    """собирает статистику со страниц, возвращает словарь,
    где ключ - название страницы, значение - список со статистикой страницы"""
    web_sites = build_bridge(path, start_page, end_page)
    web_stat = dict()
    for web_site in web_sites:
        web_stat.update({web_site: parse(os.path.join(path, web_site))})
    return web_stat 


TESTCASES = (
    ('wiki/', 'Stone_Age', 'Python_(programming_language)',
     ['Stone_Age', 'Brain', 'Artificial_intelligence',
         'Python_(programming_language)']),

    ('wiki/', 'The_New_York_Times', 'Stone_Age',
     ['The_New_York_Times', 'London', 'Woolwich', 'Iron_Age', 'Stone_Age']),

    ('wiki/', 'Artificial_intelligence', 'Mei_Kurokawa',
     ['Artificial_intelligence', 'IBM', 'PlayStation_3',
         'Wild_Arms_(video_game)',
      'Hidamari_no_Ki', 'Mei_Kurokawa']),

    ('wiki/', 'The_New_York_Times', "Binyamina_train_station_suicide_bombing",
     ['The_New_York_Times', 'Second_Intifada', 'Haifa_bus_16_suicide_bombing',
      'Binyamina_train_station_suicide_bombing']),

    ('wiki/', 'Stone_Age', 'Stone_Age',
     ['Stone_Age', ]),
)


STATISTICS = {
    'Artificial_intelligence': [8, 19, 13, 198],
    'Binyamina_train_station_suicide_bombing': [1, 3, 6, 21],
    'Brain': [19, 5, 25, 11],
    'Haifa_bus_16_suicide_bombing': [1, 4, 15, 23],
    'Hidamari_no_Ki': [1, 5, 5, 35],
    'IBM': [13, 3, 21, 33],
    'Iron_Age': [4, 8, 15, 22],
    'London': [53, 16, 31, 125],
    'Mei_Kurokawa': [1, 1, 2, 7],
    'PlayStation_3': [13, 5, 14, 148],
    'Python_(programming_language)': [2, 5, 17, 41],
    'Second_Intifada': [9, 13, 14, 84],
    'Stone_Age': [13, 10, 12, 40],
    'The_New_York_Times': [5, 9, 8, 42],
    'Wild_Arms_(video_game)': [3, 3, 10, 27],
    'Woolwich': [15, 9, 19, 38]}


class TestGetStatistics(unittest.TestCase):
    def test_build_bridge(self):
        for path, start_page, end_page, expected in TESTCASES:
            with self.subTest(path=path,
                              start_page=start_page,
                              end_page=end_page,
                              expected=expected):
                result = get_statistics(path, start_page, end_page)
                self.assertEqual(
                            result,
                            {page: STATISTICS[page] for page in expected}
                                )


class TestBuildBrige(unittest.TestCase):
    def test_build_bridge(self):
        for path, start_page, end_page, expected in TESTCASES:
            with self.subTest(path=path,
                              start_page=start_page,
                              end_page=end_page,
                              expected=expected):
                result = build_bridge(path, start_page, end_page)
                self.assertEqual(result, expected)


if __name__ == "__main__":
    unittest.main()
