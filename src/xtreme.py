from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from mongodb import MongoDBHandler


# Function to scrape gaming PCs from XtremeHardware
def getGamingPcs(db_handler):
    next_page_url = 'https://xtremehardware.pk/product-category/pre-build-pc/'
    product_images = []
    product_titles = []
    product_prices = []
    product_descriptions = []
    product_links = []

    # Set up headless Chrome options
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    driver = webdriver.Chrome(options=chrome_options)

    try:
        # Loop through each page
        while True:
            driver.get(next_page_url)

            soup = BeautifulSoup(driver.page_source, 'html.parser')

            # Find all products on the current page
            products = soup.find(class_='products wd-products wd-grid-g elements-list pagination-pagination')
            for product in products:
                try:
                    # Extract image source, title, price, description, and link
                    product_images.append(product.find(class_='product-image-link').img['src'])
                    product_titles.append(product.find(class_='wd-entities-title').text)
                    product_prices.append(float(
                        product.find(class_='woocommerce-Price-amount amount').text.replace('₨', '').replace(',', '')))

                    # Extract product description
                    description_element = product.find(class_='woocommerce-product-details__short-description')
                    if description_element.find('p'):
                        product_descriptions.append(description_element.text)
                    elif description_element.find('ul'):
                        li_tags = description_element.find_all('li')
                        details_list = [point.text for point in li_tags]
                        product_descriptions.append('\n'.join(details_list))

                    # Extract product link
                    product_links.append(product.find(class_='wd-entities-title').a['href'])
                except Exception as e:
                    print(f"Error processing product: {e}")

            # Check if there's a next page, otherwise break the loop
            if not soup.find(class_='next page-numbers'):
                break
            else:
                next_page_url = soup.find(class_='next page-numbers')['href']
    except Exception as e:
        print(f"Error fetching gaming PCs: {e}")
    finally:
        driver.quit()

    # Save the extracted data to the database
    db_handler.saveToDB('xtremehardware', 'gaming_pc', product_images, product_titles, product_prices,
                        product_descriptions, product_links)


# Function to scrape graphic cards from XtremeHardware
def getGraphicCards(db_handler):
    next_page_url = 'https://xtremehardware.pk/product-category/graphic-cards/'
    product_images = []
    product_titles = []
    product_prices = []
    product_descriptions = []
    product_links = []

    # Set up headless Chrome options
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    driver = webdriver.Chrome(options=chrome_options)

    try:
        # Loop through each page
        while True:
            driver.get(next_page_url)

            soup = BeautifulSoup(driver.page_source, 'html.parser')

            # Find all products on the current page
            products = soup.find(class_='products wd-products wd-grid-g elements-list pagination-pagination')
            for product in products:
                try:
                    # Extract image source, title, price, description, and link
                    product_images.append(product.find(class_='product-image-link').img['src'])
                    product_titles.append(product.find(class_='wd-entities-title').text)
                    product_prices.append(float(
                        product.find(class_='woocommerce-Price-amount amount').text.replace('₨', '').replace(',', '')))

                    # Extract product description
                    description_element = product.find(class_='woocommerce-product-details__short-description')
                    if description_element.find('ul'):
                        li_tags = description_element.find_all('li')
                        details_list = [point.text.replace('\xa0', ' ') for point in li_tags]
                        product_descriptions.append('\n'.join(details_list))
                    elif description_element.find('p'):
                        p_tags = description_element.find_all('p')
                        details_list = [point.text.replace('\xa0', ' ') for point in p_tags]
                        product_descriptions.append('\n'.join(details_list))
                    else:
                        product_descriptions.append(description_element.text.replace('\xa0', ' '))

                    # Extract product link
                    product_links.append(product.find(class_='wd-entities-title').a['href'].replace('\xa0', ' '))
                except Exception as e:
                    print(f"Error processing product: {e}")

            # Check if there's a next page, otherwise break the loop
            if not soup.find(class_='next page-numbers'):
                break
            else:
                next_page_url = soup.find(class_='next page-numbers')['href']
    except Exception as e:
        print(f"Error fetching graphic cards: {e}")
    finally:
        driver.quit()

    # Save the extracted data to the database
    db_handler.saveToDB('xtremehardware', 'graphic_card', product_images, product_titles, product_prices,
                        product_descriptions, product_links)


# Function to scrape processors from XtremeHardware
def getProcessors(db_handler):
    next_page_url = 'https://xtremehardware.pk/product-category/processors/'
    product_images = []
    product_titles = []
    product_prices = []
    product_descriptions = []
    product_links = []

    # Set up headless Chrome options
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    driver = webdriver.Chrome(options=chrome_options)

    try:
        # Loop through each page
        while True:
            driver.get(next_page_url)

            soup = BeautifulSoup(driver.page_source, 'html.parser')

            # Find all products on the current page
            products = soup.find(class_='products wd-products wd-grid-g elements-list pagination-pagination')
            for product in products:
                try:
                    # Extract image source, title, price, description, and link
                    product_images.append(product.find(class_='product-image-link').img['src'])
                    product_titles.append(product.find(class_='wd-entities-title').text)
                    product_prices.append(float(
                        product.find(class_='woocommerce-Price-amount amount').text.replace('₨', '').replace(',', '')))

                    # Extract product description
                    description_element = product.find(class_='woocommerce-product-details__short-description')
                    if description_element.find('tr'):
                        rows = description_element.find_all('tr')
                        formatted_text = []
                        for row in rows:
                            cells = row.find_all('td')
                            if len(cells) == 2:
                                attribute = cells[0].get_text(strip=True)
                                value = cells[1].get_text(strip=True)
                                formatted_text.append(f"{attribute}: {value}")
                        product_descriptions.append('\n'.join(formatted_text))
                    elif description_element.find('ul'):
                        li_tags = description_element.find_all('li')
                        details_list = [point.text.replace('\xa0', ' ') for point in li_tags]
                        product_descriptions.append('\n'.join(details_list))
                    elif description_element.find('p'):
                        p_tags = description_element.find_all('p')
                        details_list = [point.text.replace('\xa0', ' ') for point in p_tags]
                        product_descriptions.append('\n'.join(details_list))
                    else:
                        product_descriptions.append(description_element.text.replace('\xa0', ' '))

                    # Extract product link
                    product_links.append(product.find(class_='wd-entities-title').a['href'].replace('\xa0', ' '))
                except Exception as e:
                    print(f"Error processing product: {e}")

            # Check if there's a next page, otherwise break the loop
            if not soup.find(class_='next page-numbers'):
                break
            else:
                next_page_url = soup.find(class_='next page-numbers')['href']
    except Exception as e:
        print(f"Error fetching processors: {e}")
    finally:
        driver.quit()

    # Save the extracted data to the database
    db_handler.saveToDB('xtremehardware', 'processor', product_images, product_titles, product_prices,
                        product_descriptions, product_links)


# Function to run all scraping tasks
def xtremeRunAll():
    db_handler = MongoDBHandler()
    try:
        # Call the scraping functions
        getGamingPcs(db_handler)
        getGraphicCards(db_handler)
        getProcessors(db_handler)
    except Exception as e:
        print(f"Error in xtremeRunAll: {e}")
    finally:
        # Close the database connection
        db_handler.close_connection()
