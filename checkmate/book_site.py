import requests
from lxml import etree
from objects import *
from PIL import Image
class BookSite:
    #region fields
    slug = '' #2-letter abbreviation for booksite
    base = '' #home-page url for booksite
    stripped = '' #same as 'base', but stripped of surrounding 'https://' and '/'
    search = '' #extension to 'base' used for making book searches
    #endregion

    def __init__(self):
        self.slug = 'bs'
        self.base = 'https://book.site.url/'
        self.search = 'find/'

    def get_book_data_from_site(self, url):
        response = requests.get(url)
        root = etree.fromstring(response.content, etree.HTMLParser())
        data = SiteBookData()

        data.book_format = self._find_book_format(root)
        data.book_image_url = self._find_book_image_url(root)
        data.book_image = self._find_book_image(data.book_image_url)
        data.isbn_13 = self._format_isbn(self._find_isbn(root))
        data.description = self._find_description(root)
        data.title = self._find_title(root)
        data.subtitle = self._find_subtitle(root)
        data.series = self._find_series(root)
        data.authors = self._find_authors(root)
        
        data.ready_for_sale = self._find_ready_for_sale(root)
        data.book_id = url[len(self.base):]
        data.site_slug = self.slug
        data.url = url
        data.content = response.content
        data.parse_status = self._find_parse_status(data)
        data.extras = self._find_extras(root)
        
        return data

#results for google books are weird - pages with previews do not contain isbns
#it still seems to come up with the right results though
    def find_book_matches_at_site(self, book_data):
        response = requests.get(self.base + self.search, params=self._construct_params_of_search(book_data))
        root = etree.fromstring(response.content, etree.HTMLParser())
        links = self._find_results_of_search(root)
        results = []
        graded_results = []
        for l in links:
            results.append(self.get_book_data_from_site(l))
        for result in results:
            graded_results.append((result, self.evaluate_potential_match(book_data, result)))

        return graded_results

    def evaluate_potential_match(self, baseline, match):
        value = 0
        prop = 1
        if baseline.isbn_13 != "":
            prop *= 2
            if baseline.isbn_13 == match.isbn_13:
                value += 1/prop
        if baseline.title != "":
            prop *= 2
            value += (1/prop) *self._evaluate_string_fields(baseline.title.lower(), match.title.lower())
        if baseline.authors != []:
            prop *= 2
            value += (1/prop) * self._evaluate_author_names(baseline.authors, match.authors)
        if baseline.book_format != "":
            prop *= 2
            if baseline.book_format == match.book_format:
                value += 1/prop
        if baseline.subtitle != "":
            prop *= 2
            value += (1/prop) *  self._evaluate_string_fields(baseline.subtitle.lower(), match.subtitle.lower())
        if baseline.series != "":
            prop *= 2
            value += (1/prop) * self._evaluate_string_fields(baseline.series.lower(), match.series.lower())
        if baseline.description != "":
            prop *= 2
            value += (1/prop) * self._evaluate_string_fields(baseline.description, match.description)
        if baseline.book_image != None:
            prop *= 2
            if baseline.book_image == match.book_image:
                value += 1/prop
        if value > 0:
            value += 1/prop
        return value * 100

    def _evaluate_author_names(self, baseline, match):
        try:
            total = 0
            for author in baseline:
                current_best = 0
                for author2 in match:
                    result = self._compare_strings(author.lower(), author2.lower())
                    if result > current_best:
                        current_best = result
                total += current_best
            if len(baseline) > len(match):
                return total / len(baseline)
            else:
                return total / len(match)
        except:
            return 0

    def _compare_strings(self, baseline, match):
        try:
            author = baseline.split()
            author2 = match.split()
            for word in author:
                word.strip(",.'")
            for word in author2:
                word.strip(",.'")
            total = 0
            for word in author:
                current_best = 0
                for word2 in author2:
                    if word == word2:
                        current_best = 1
                total += current_best
            if (len(author) > len(author2)):
                return total / len(author)
            else:
                return total / len(match)
        except:
            return 0

    def _evaluate_string_fields(self, baseline, match):
        try:
            value = 0
            b = baseline.split()
            m = match.split()
            size = len(b)
            if len(b) < len(m):
                size = len(m)
            for index in range(0, len(b)):
                word = b[index]
                if word in m:
                    matches = [i for i, x in enumerate(m) if x == word]
                    proximity = 0
                    for same in matches:
                        prox = (size - abs(index - same))
                        if prox > proximity:
                            proximity = prox
                    value += proximity / size
            return value / size
        except:
            return 0

    def convert_book_id_to_url(self, book_id):
        return self.base + book_id


    def _construct_params_of_search(self, book_data):
        return {}

    def _find_results_of_search(self, root):
        return []

    #region parse subfunctions
    def _find_parse_status(self, data):
        if data.book_format != "" and data.isbn_13 != "" and data.description != "" and data.title != "" and data.authors != []:
            return "FULLY_PARSED"
        else:
            return "UNSUCCESSFUL"

    def _find_book_format(self, root):
        return "NO_FORMAT"

    def _find_book_image_url(self, root):
        return ""

    def _find_book_image(self, url):
        return None

    def _find_isbn(self, root):
        return ""

    def _find_description(self, root):
        return ""

    def _find_title(self, root):
        return ""

    def _find_subtitle(self, root):
        return ""

    def _find_series(self, root):
        return ""

    def _find_authors(self, root):
       return []

    def _find_ready_for_sale(self, root):
        return False
    
    def _find_extras(self, root):
        return {}

    def _format_isbn(self, isbn):
        if len(isbn) == 13:
            return isbn
        elif len(isbn) == 10:
            nine_digits = isbn[0:9] #slice off the old check digit
            final_isbn = "978"
            final_isbn += (nine_digits)
            final_isbn += str(self._calc_check_digit(final_isbn))
            return final_isbn
        else:
            return ""

    def _calc_check_digit(self, isbn_string):
        products = []
        for i in range(0, 12):
            if ((i + 1) % 2) != 0: #we are looking at the first, third, fifth ... digit
                products.append(int(isbn_string[i]) * 1)
            else: #we are looking at the second, fourth, sixth ... digit
                products.append(int(isbn_string[i]) * 3)

        accumulator = 0
        for p in products:
            accumulator += p

        modulated = accumulator % 10

        if modulated == 0:
            check_digit = modulated
        else:
            check_digit = 10 - modulated

        return check_digit

    #endregion