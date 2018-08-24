from bs4 import BeautifulSoup
import re
import os


def get_raw_article(path_to_article):
    with open(path_to_article) as f:
        return f.read()


def get_all_links(raw_page, compile_pattern=None):
    if not compile_pattern:
        compile_pattern = re.compile("")
    article = BeautifulSoup(raw_page, "lxml")
    tags_with_local_links = article.find_all(href=compile_pattern)

    links_to_articles = []
    for tag in tags_with_local_links:
        directory, child_name = os.path.split(tag["href"])
        links_to_articles.append(child_name)
    return links_to_articles


def build_tree(start, end, path):
    link_re = re.compile(r"(?<=/wiki/)[\w()]+")
    files = dict.fromkeys(os.listdir(path))
    queue = [start]

    for current in queue:
        if not files[end] is None:
            return files

        raw_page = get_raw_article(os.path.join(path, current))
        all_links = get_all_links(raw_page, link_re)

        children = {link for link in all_links if link in files and not files[link]}
        for child in children:
            if child not in queue:
                queue.append(child)
            files[child] = current
    return files


def build_bridge(tree, start, end, i=None):
    i = [] if not i else i
    i.append(end)
    if tree[end] == start:
        i.append(start)
        i.reverse()
        return i
    return build_bridge(tree, start, tree[end], i)


def parse(start, end, path):
    tree = build_tree(start, end, path)
    bridge = build_bridge(tree, start, end)

    out = {}
    for file in bridge:
        with open(os.path.join(path, file)) as data:
            soup = BeautifulSoup(data, "lxml")
        body = soup.find(id="bodyContent")
        imgs = len(get_img_width_more(body, 200))
        headers = len(get_headers(body))
        linkslen = get_max_quantity_neighboring_tags(body, "a")
        lists = get_unattached_lists(body)
        out[file] = [imgs, headers, linkslen, lists]
    return out


def get_img_width_more(soup_obj, number: int):
    all_img = soup_obj.find_all("img")
    imgs = [tag for tag in all_img if int(tag.get("width", 0)) >= number]
    return imgs


def get_headers(soup_obj):
    all_headers = soup_obj.find_all(re.compile(r"h[1-9]"))
    headers = [tag for tag in all_headers if re.findall(r"^[ETC]", tag.text[0])]
    return headers


def get_max_quantity_neighboring_tags(soup_obj, tag):
    pattern = str(tag)
    linkslen = 0
    while True:
        result = soup_obj.select(pattern)
        if not result:
            break
        linkslen += 1
        pattern += f" + {tag}"
    return linkslen


def get_unattached_lists(soup_obj):
    ol = soup_obj.find_all("ol")
    ol = [1 for o in ol if not (o.find_parent("ol") or o.find_parent("ul"))]
    ul = soup_obj.find_all("ul")
    ul = [1 for o in ul if not (o.find_parent("ul") or o.find_parent("ol"))]
    return len(ol) + len(ul)

