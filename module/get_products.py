from module.product_selenium import SavePage


def save_products(all_links):
    i = 1
    for product_link in all_links:
        file_name = f"product_{str(i)}.html"
        url = product_link
        SavePage(url, file_name).get_sourse_html()
        print(f"Product page-{i} parsing completed\n{url}")

        i += 1