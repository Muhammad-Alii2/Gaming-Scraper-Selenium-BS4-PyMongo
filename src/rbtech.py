from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from mongodb import MongoDBHandler


def getGamingPcs(db_handler):
    url = 'https://rbtechngames.com/product-category/pre-builts/'
    product_images = []
    product_titles = []
    product_prices = []
    product_descriptions = []
    product_links = []

    # Configure Chrome WebDriver to run in headless mode
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    driver = webdriver.Chrome(options=chrome_options)

    try:
        driver.get(url)  # Open the URL
        soup = BeautifulSoup(driver.page_source, 'html.parser')  # Parse HTML
        products = soup.find(
            class_='products row row-small large-columns-4 medium-columns-3 small-columns-2 equalize-box')

        for product in products:
            try:
                # Extract product image URL
                product_images.append(product.find(class_='image-zoom_in').img['src'])
                # Extract product title
                product_titles.append(
                    product.find(class_='woocommerce-LoopProduct-link woocommerce-loop-product__link').text)
                # Extract product price
                if product.find('ins'):
                    product_prices.append(float(product.find('ins').bdi.text.replace('₨', '').replace(',', '')))
                else:
                    product_prices.append(float(product.find('bdi').text.replace('₨', '').replace(',', '')))
                # Navigate to product page
                driver.get(product.a['href'])
                inner_soup = BeautifulSoup(driver.page_source, 'html.parser')
                # Extract product description
                if inner_soup.find(class_='product-short-description').p:
                    product_descriptions.append(
                        inner_soup.find(class_='product-short-description').p.decode_contents().replace('<br/>', ''))
                else:
                    description_list = inner_soup.find(class_='product-short-description').find_all('li')
                    description = [point.text for point in description_list]
                    product_descriptions.append('\n'.join(description))
                # Extract product link
                product_links.append(product.a['href'])
            except Exception as e:
                print(f"Error processing product: {e}")

        # Save data to database
        db_handler.saveToDB('rbtechngames', 'gaming_pc', product_images, product_titles, product_prices,
                            product_descriptions, product_links)
    except Exception as e:
        print(f"Failed to retrieve the webpage or save to database: {e}")
    finally:
        driver.quit()  # Close the browser


def getGraphicCards(db_handler):
    next_page_url = 'https://rbtechngames.com/product-category/computers/graphics-card/'

    product_images = []
    product_titles = []
    product_prices = []
    product_descriptions = []
    product_links = []

    # Configure Chrome WebDriver to run in headless mode
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    driver = webdriver.Chrome(options=chrome_options)

    try:
        while True:
            driver.get(next_page_url)  # Open the URL
            soup = BeautifulSoup(driver.page_source, 'html.parser')  # Parse HTML
            products = soup.find(
                class_='products row row-small large-columns-4 medium-columns-3 small-columns-2 equalize-box')

            for product in products:
                try:
                    # Extract product image URL
                    if product.find(class_='image-zoom_in').img.has_attr('data-src'):
                        product_images.append(product.find(class_='image-zoom_in').img['data-src'])
                    else:
                        product_images.append(product.find(class_='image-zoom_in').img['src'])
                    # Extract product title
                    product_titles.append(
                        product.find(class_='woocommerce-LoopProduct-link woocommerce-loop-product__link').text)
                    # Extract product price
                    if product.find('ins'):
                        product_prices.append(float(product.find('ins').bdi.text.replace('₨', '').replace(',', '')))
                    else:
                        product_prices.append(float(product.find('bdi').text.replace('₨', '').replace(',', '')))
                    # Navigate to product page
                    driver.get(product.a['href'])
                    inner_soup = BeautifulSoup(driver.page_source, 'html.parser')
                    # Extract product description
                    if inner_soup.find(class_='product-short-description').find('ul'):
                        li_tags = inner_soup.find(class_='product-short-description').find_all('li')
                        details_list = [' '.join(point.strings).replace('\xa0', '') for point in li_tags]
                        product_descriptions.append('\n'.join(details_list))
                    elif inner_soup.find(class_='product-short-description').find('p'):
                        p_tag = inner_soup.find(class_='product-short-description').find_all('p')
                        if inner_soup.find(class_='product-short-description').find('strong'):
                            inner_soup.find(class_='product-short-description').find('strong').decompose()
                        if len(p_tag) == 2:
                            points = p_tag[-1].decode_contents().split('<br>')
                            for point in points:
                                product_descriptions.append(
                                    point.replace('– ', '').replace('<br/>', '').replace('\xa0', ' ').lstrip())
                        elif len(p_tag) == 1:
                            for point in p_tag:
                                product_descriptions.append(
                                    point.text.replace('– ', '').replace('– ', '').replace('\xa0', ' '))
                    # Extract product link
                    product_links.append(product.a['href'])
                except Exception as e:
                    print(f"Error processing product: {e}")

            # Check if there is a next page
            if not soup.find(class_='next page-number'):
                break
            else:
                next_page_url = soup.find(class_='next page-number')['href']

        # Save data to database
        db_handler.saveToDB('rbtechngames', 'graphic_card', product_images, product_titles, product_prices,
                            product_descriptions, product_links)
    except Exception as e:
        print(f"Failed to retrieve the webpage or save to database: {e}")
    finally:
        driver.quit()  # Close the browser


def getProcessors(db_handler):
    next_page_url = 'https://rbtechngames.com/product-category/computers/processors/'

    product_images = []
    product_titles = []
    product_prices = []
    product_descriptions = []
    product_links = []

    # Configure Chrome WebDriver to run in headless mode
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    driver = webdriver.Chrome(options=chrome_options)

    try:
        while True:
            driver.get(next_page_url)  # Open the URL
            soup = BeautifulSoup(driver.page_source, 'html.parser')  # Parse HTML
            products = soup.find(
                class_='products row row-small large-columns-4 medium-columns-3 small-columns-2 equalize-box')

            for product in products:
                try:
                    # Extract product image URL
                    if product.find(class_='image-zoom_in').img.has_attr('data-src'):
                        product_images.append(product.find(class_='image-zoom_in').img['data-src'])
                    else:
                        product_images.append(product.find(class_='image-zoom_in').img['src'])
                    # Extract product title
                    product_titles.append(
                        product.find(class_='woocommerce-LoopProduct-link woocommerce-loop-product__link').text)
                    # Extract product price
                    if product.find('ins'):
                        product_prices.append(float(product.find('ins').bdi.text.replace('₨', '').replace(',', '')))
                    else:
                        product_prices.append(float(product.find('bdi').text.replace('₨', '').replace(',', '')))
                    # Extract product link
                    product_links.append(product.a['href'])
                    # Navigate to product page
                    driver.get(product.a['href'])
                    inner_soup = BeautifulSoup(driver.page_source, 'html.parser')
                    # Extract product description
                    if inner_soup.find(class_='product-short-description').find('ul'):
                        li_tags = inner_soup.find(class_='product-short-description').find_all('li')
                        details_list = [' '.join(point.strings).replace('\xa0', '') for point in li_tags]
                        product_descriptions.append('\n'.join(details_list))
                    else:
                        product_descriptions.append(inner_soup.find(class_='product-short-description').text)
                except Exception as e:
                    print(f"Error processing product: {e}")

            # Check if there is a next page
            if not soup.find(class_='next page-number'):
                break
            else:
                next_page_url = soup.find(class_='next page-number')['href']

        # Save data to database
        db_handler.saveToDB('rbtechngames', 'processor', product_images, product_titles, product_prices,
                            product_descriptions, product_links)
    except Exception as e:
        print(f"Failed to retrieve the webpage or save to database: {e}")
    finally:
        driver.quit()  # Close the browser


def rbtechRunAll():
    db_handler = MongoDBHandler()  # Create a new database handler instance
    try:
        # Run the scraping functions for different product categories
        getGamingPcs(db_handler)
        getGraphicCards(db_handler)
        getProcessors(db_handler)
    except Exception as e:
        print(f"Error in rbtechRunAll: {e}")
    finally:
        db_handler.close_connection()  # Close the database connection
