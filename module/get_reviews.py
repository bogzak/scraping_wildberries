from bs4 import BeautifulSoup
import json
import re
import glob


def try_except(func):
    def wrapper(*args, **kwargs):
        try:
            data = func(*args, **kwargs)
        except:
            data = None

        return data

    return wrapper


@try_except
def get_page():
    return glob.glob(r"data/products/*.html")


@try_except
def get_html(page):
    with open(page, "r", encoding="utf-8") as file:
        return file.read()


@try_except
def get_h1(soup):
    return soup.h1.string


@try_except
def get_sku(soup):
    return soup.find("span", attrs={"id": "productNmId"}).get_text()


@try_except
def get_name(soup):
    return soup.find("div", class_="comment-card__wrap").find("button", class_="comment-card__name "
                                                                               "j-user-profile").get_text().strip()


@try_except
def get_stars(soup):
    return soup.find("div", attrs={"class": "product-page__common-info"}).find("span", attrs={"data-link": "text{: "
                                                                                                           "product^star}"}).get_text()


@try_except
def get_list_review(soup):
    review_list_items = soup.find_all("div", class_="swiper-slide comment-card j-feedback-slide")
    reviews = []
    for review in review_list_items:
        name = review.find("div", class_="comment-card__wrap").find("button", class_="comment-card__name "
                                                                               "j-user-profile").get_text().strip()
        date = review.find("div", class_="comment-card__wrap").find("p", class_="comment-card__date").get_text().strip()
        stars_str = str(review.find("div", class_="comment-card__wrap").find("div",
                                                                                class_="comment-card__side").find(
            "span")).strip()

        stars = re.sub(r"<span class=\"comment-card__stars stars-line star([0-9])\"></span>", r"\1", stars_str)
        comment_str = review.find("div", class_="comment-card__content").find("p", class_="comment-card__message "
                                                                                      "j-feedback-text").get_text(

        )
        comment = re.sub(r" ещё|\n", "", comment_str).strip()

        review_info = {
            "name": name,
            "date": date,
            "review_stars": stars,
            "comment": comment
        }
        reviews.append(review_info)
    return reviews


def parse_reviews():
    products_list = get_page()
    product_info_list = []
    for product_html in products_list:
        html = get_html(product_html)
        soup = BeautifulSoup(html, "lxml")
        h1 = get_h1(soup)
        sku = get_sku(soup)
        stars = get_stars(soup)
        reviews = get_list_review(soup)

        product_info = {
            "h1": h1,
            "sku": sku,
            "product_stars": stars,
            "reviews": reviews
        }

        product_info_list.append(product_info)

    write_to_json(product_info_list)
    print("Parsing completed")


def write_to_json(data):
    with open(f"data/reviews_from_wildberies.json", "a", encoding="utf-8") as file:
        json.dump(data, file, indent=4, ensure_ascii=False)