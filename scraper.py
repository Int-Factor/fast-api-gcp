import time
import requests
from bs4 import BeautifulSoup
from collections import Counter


def href_lang_scraper(target_url):

    # CREATING SOUP
    try:
        html = requests.get(target_url)
    except:
        return {
            'status': 'error',
            'reason': 'could not connect to website'
        }
    else:
        soup = BeautifulSoup(html.content, 'lxml')

        href_links_of_webpage = soup.find_all('link', attrs = {'rel': 'alternate'})

        href_lang_dict = {
            'url': target_url,
            'hrelang_links': [], # complete urls
            'hreflang_codes': [], # raw language with culture code
            'culture_codes' : [],
            'language_codes' : [],
            'number_of_languages_on_website': None,  # total number of language codes
            'number_of_culture_codes_on_website': None,  # total number of culture codes including duplicates
            'hreflang_crawl_timestamp': int(time.time()), # timestamp of,
            'mapped': None
        }

        if len(href_links_of_webpage) == 0:
            return href_lang_dict
        else:

            hreflang_codes = []
            culture_codes = []
            language_codes = []


            # extract href links
            for link in href_links_of_webpage:
                if link['href']:
                    if link['hreflang'].lower() == 'x-default':
                        continue
                    else:
                        hreflang_codes.append(link['hreflang'])
                else:
                    pass


            #split at '-'
            # get culture code and language code

            mapped = {}
            for i in hreflang_codes:

                try:
                    culture_code = i.split('-')[1]
                    language_code = i.split('-')[0]
                except:
                    continue
                else:
                    culture_codes.append(culture_code)
                    language_codes.append(language_code)

                    if language_code not in mapped:
                        mapped[language_code] = []
                        mapped[language_code].append(culture_code)
                    else:
                        mapped[language_code].append(culture_code)


            # remove duplicate language codes
            language_codes = list(set(language_codes))

            number_of_culture_codes = len(culture_codes)
            number_of_language_codes = len(language_codes)



            href_lang_dict['hrelang_links'] = [str(i) for i in href_links_of_webpage]
            href_lang_dict['hreflang_codes'] = hreflang_codes
            href_lang_dict['culture_codes'] = [str(i) for i in culture_codes]
            href_lang_dict['language_codes'] = [str(i) for i in language_codes]
            href_lang_dict['number_of_languages_on_website'] = number_of_language_codes
            href_lang_dict['number_of_culture_codes_on_website'] = number_of_culture_codes
            href_lang_dict['mapped'] = mapped

            return href_lang_dict


if __name__ == "__main__":
    pass