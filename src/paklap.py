import requests
from bs4 import BeautifulSoup
from mongodb import MongoDBHandler


def getGraphicCards(db_handler):
    url = 'https://www.paklap.pk/accessories/computer-accessories/graphic-cards.html'
    product_images = []
    product_titles = []
    product_prices = []
    product_descriptions = []
    product_links = []

    try:
        # Make a GET request to fetch the main page
        response = requests.get(url)
        response.raise_for_status()  # Check if the request was successful
        soup = BeautifulSoup(response.content, 'html.parser')  # Parse the HTML content
        products = soup.find_all(class_='item product product-item')  # Find all product containers

        for product in products:
            try:
                # Extract product image URL
                product_images.append(product.find(class_='product-image-photo')['src'])
                # Extract product title
                product_titles.append(product.find(class_='product-item-link').text.strip())
                # Extract product price
                product_prices.append(float(product.find(class_='price').text.replace('Rs. ', '').replace(',', '')))
                # Extract product link
                product_links.append(product.find(class_='product-item-link')['href'])

                # Fetch the product detail page
                inner_response = requests.get(product.find(class_='product-item-link')['href'])
                inner_response.raise_for_status()  # Check if the request was successful
                inner_soup = BeautifulSoup(inner_response.content, 'html.parser')  # Parse the HTML content

                details_list = []
                data_content = inner_soup.find(class_='data item content')  # Find the section with details

                # Check if details are listed in <ul>
                if data_content.find('ul'):
                    li_tags = data_content.find_all('li')
                    col_left_exists = data_content.find(class_='col-left')
                    for point in li_tags:
                        if col_left_exists:
                            col_left = point.find(class_='col-left col').text.replace('\xa0', ' ')
                            col_right = point.find(class_='col-right col').text.replace('\xa0', ' ')
                            details_list.append(f'{col_left}: {col_right}')
                        else:
                            details_list.append(point.text.replace('\xa0', ' '))
                # Check if details are in a table format <tr>
                elif data_content.find('tr'):
                    tr_tags = data_content.find_all('tr')
                    th_exists = data_content.find('th')
                    for tr in tr_tags:
                        if th_exists:
                            th = tr.find('th').text.replace('\xa0', ' ')
                            td = tr.find('td').text.replace('\xa0', ' ')
                            details_list.append(f'{th}: {td}')
                        elif tr.find('td'):
                            td_tags = tr.find_all('td')
                            if len(td_tags) == 2:
                                label = td_tags[0].text.replace('\xa0', ' ')
                                value = td_tags[1].text.replace('\xa0', ' ')
                                details_list.append(f'{label}: {value}')
                # Check if details are in <p> tags with <strong> tags
                elif data_content.find('p'):
                    strong_tags = data_content.find_all('strong')
                    for point in strong_tags:
                        details_list.append(point.text.replace('\xa0', ' ').lstrip())

                # Join all details into a single description
                product_descriptions.append('\n'.join(details_list))
            except Exception as e:
                print(f"Error processing product: {e}")
    except Exception as e:
        print(f"Failed to retrieve the webpage: {e}")

    try:
        # Save collected data to the database
        db_handler.saveToDB('paklap', 'graphic_card', product_images, product_titles, product_prices,
                            product_descriptions, product_links)
    except Exception as e:
        print(f"Error saving to database: {e}")


def paklapRunAll():
    db_handler = MongoDBHandler()  # Create a new database handler instance
    try:
        getGraphicCards(db_handler)  # Run the scraping function for graphic cards
    except Exception as e:
        print(f"Error in paklapRunAll: {e}")
    finally:
        db_handler.close_connection()  # Close the database connection
