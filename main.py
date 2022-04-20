from pprint import pprint
from datetime import datetime
from csv import writer

import requests
from bs4 import BeautifulSoup


# splash container needed https://splash.readthedocs.io/en/stable/install.html
def get_soup(url):
    response = requests.get('http://localhost:8050/render.html', params={'url': url, 'wait': 0})
    soup = BeautifulSoup(response.text, 'html.parser')
    return soup


def get_reviews(soup, csv_writer):
    reviews_list = soup.findChildren(id="cm_cr-review_list")
    for review in reviews_list:
        review = review.find_all('div', attrs={'data-hook': 'review'})
        for item in review:
            # vvvvvvvv  CHANGE FOR SELENIUM    vvvvvvvv

            # Getting the title
            if item.find('a', {'data-hook': 'review-title'}):
                item_title = item.find('a', {'data-hook': 'review-title'}).get_text().replace("\n", "")
            elif item.find('span', {'data-hook': 'review-title'}):
               item_title = item.find('span', {'data-hook': 'review-title'}).get_text().replace("\n", "")
            else:
                item_title = 'NO TITLE'
            # Getting the name: 
            item_author = item.find_all('span', {'class': 'a-profile-name'})[0].get_text()
            # Getting the stars:
            item_stars =  item.find_all('i', {'data-hook': 'review-star-rating'})
            item_stars =  item_stars[0].find('span').get_text().split()[0].replace(',','.') if item_stars else 'NO RATING'
            # Getting the date:
            item_date = item.find('span', {'data-hook': 'review-date'}).get_text().split('Revisado en ')[1].split(' el ')[1]
            # Getting the review:
            item_review =  item.find_all('span', {'data-hook': 'review-body'})[0].find('span').get_text()

            item = [
                item_title,
                item_author,
                item_stars,
                item_date,
                item_review
                ]

            csv_writer.writerow(item)


def main ():
    page = 1
    amazon_url = 'https://www.amazon.es/'
    item_url_review = f'Tapones-para-o%C3%ADdos-SleepDreamz%C2%AE-pares/product-reviews/B07C3Q5F32/ref=cm_cr_getr_d_paging_btm_prev_1?ie=UTF8&reviewerType=all_reviews&pageNumber={page}'
    url = f'{amazon_url}{item_url_review}'
    time_stamp = datetime.today().strftime('%Y-%m-%d-%H-%M-%S')
    file_type = ".csv"
    file_name = f'TAPONES-{time_stamp}{file_type}'


    with open (file_name, "w", encoding='utf-8' ) as csv_file:
        csv_writer = writer(csv_file)
        csv_writer.writerow(["item_title",
                       "item_author",
                       "item_stars",
                       "item_date",
                       "item_review"])
        while url:
            pprint(f'Scraping page: {page}')
            page_soup = get_soup(url)
            get_reviews(page_soup, csv_writer)
            
            if page_soup.find('li', attrs={'class': 'a-disabled a-last'}):
                break
            else: 
                next_btn = page_soup.find("li", attrs={"class":"a-last"})
                next_url = next_btn.find('a')['href'] if next_btn else None
                url = f'{amazon_url}{next_url}' 
                page +=1


if '__main__' == __name__:
    try:
        main()
    except PermissionError as err:
        print(err, 'If you have the file open close it please!')
    except KeyboardInterrupt as err:
        print(err, 'The user has cancelled the scraping...')
    # except IndexError as err:
    #     print(err)
    except:
        raise
    finally:
        print('Scraping done...')




