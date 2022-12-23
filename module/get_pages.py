from module.page_selenium import SavePage


def save_categories():
    with open(r"D:\pycharm_projects\scraping_wildberries\url.txt", encoding="utf-8") as file:
        url = file.read()

    i = 1

    while i <= 20:
        filename = f"page_{str(i)}.html"
        url_param = f"{url}?page={str(i)}"
        SavePage(url_param, filename).get_sourse_html()
        print(f"Categorie page-{i} parsing completed\n{url_param}")

        i += 1