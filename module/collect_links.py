from bs4 import BeautifulSoup
import glob


def get_pages():
    return glob.glob(r"data/categories/*.html")


def get_html(page):
    with open(page, "r", encoding="utf-8") as file:
        return file.read()


def parse_data(html):
    soup = BeautifulSoup(html, "lxml")
    items_divs = soup.find_all("div", class_="product-card j-card-item")

    urls = []
    for item in items_divs:
        item_url = item.find("div", class_="product-card__wrapper").find("a").get("href")
        urls.append(item_url)

    return set(urls)


def get_links():
    pages = get_pages()

    all_links = []

    for page in pages:
        html = get_html(page)
        links = parse_data(html)
        all_links = all_links + list(links)

    with open("data/item_urls.txt", "w", encoding="utf-8") as file:
        for link in all_links:
            file.write(f"{link}\n")

    return all_links
