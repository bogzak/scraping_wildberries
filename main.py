import module.collect_links
import module.get_pages
import module.get_products
import module.get_reviews


def main():
    # module.get_pages.save_categories()
    # all_links = module.collect_links.get_links()
    # module.get_products.save_products(all_links)
    module.get_reviews.parse_reviews()


if __name__ == '__main__':
    main()