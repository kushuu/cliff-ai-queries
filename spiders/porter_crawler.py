# importing required libraries
import scrapy


# class for scraping topwear
class TopwearSpider(scrapy.Spider):
    name = "topwear_crawler"
    start_urls = [
        'https://www.net-a-porter.com/en-in/shop/clothing/tops',
    ]

    def get_float_val(self, val):
        '''
        This function cleans the topwear's price (input as string) and returns it as a float value.
        '''
        string_without_punc = ""
        if val is not None:    
            for ele in val:
                if ele.isnumeric():
                    string_without_punc += ele
            return float(string_without_punc)
    

    def clean_name(self, name):
        '''
        This function cleans the name of the product (removal of +) and returns the cleaned name.
        '''
        if name is not None:
            if name[0] == '+':
                return name[2:].strip()
            return name.strip()


    def parse(self, response):
        '''
        This is the main function that scrapes data from the webpage and returns (yields) it to the pipelines (if any).
        '''
        for dress in response.css('.ProductListWithLoadMore52__listingGrid a'):    # this is the css selector that lets us traverse over all the objects of interest on the page
            yield {
                'name' : self.clean_name(dress.css(".ProductItem24__name::text").get()),
                'brand' : dress.css(".ProductItem24__designer::text").get(),
                'original_price($)' : self.get_float_val(dress.css(".PriceWithSchema9__value span::text").get()),
                'sale_price($)' : self.get_float_val(dress.css(".PriceWithSchema9__value span::text").get()),
                # this fild and the next field store the image urls of only first 14 products (I'm not sure how to make this right).
                'primary image_url' : str(dress.css(".ProductItem24__imageContainer .primaryImage img::attr(src)").get()),
                'secondary image_url' : str(dress.css(".ProductItem24__imageContainer .secondaryImage img::attr(src)").get()),
                'product_page_url' : str("https://www.net-a-porter.com/" + str(dress.css("a::attr(href)").get())),
                'product_category' : "topwear",
            }

        # this is where I handle pagination (storing data from the first 25 pages only).
        next_url = response.css(".Pagination7__next::attr(href)").get()
        page_number = next_url.split("=")[-1]
        print("\n\n\n", next_url, page_number, "\n\n\n")
        if next_url is not None and int(page_number) <= 25:
            next_page = response.urljoin(next_url)
            yield scrapy.Request(next_page, callback=self.parse)


# class to scrape footwear
class FootwearSpider(scrapy.Spider):
    name = "footwear_crawler"
    start_urls = [
        'https://www.net-a-porter.com/en-in/shop/shoes',
    ]

    def get_float_val(self, val):
        '''
        This function cleans the footwear's price (input as string) and returns it as a float value.
        '''
        string_without_punc = ""
        if val is not None:    
            for ele in val:
                if ele.isnumeric():
                    string_without_punc += ele
            return float(string_without_punc)
    

    def clean_name(self, name):
        '''
        This function cleans the name of the product (removal of +) and returns the cleaned name.
        '''
        if name is not None:
            if name[0] == '+':
                return name[2:].strip()
            return name.strip()

    def parse(self, response):
        '''
        This is the main function that scrapes data from the webpage and returns (yields) it to the pipelines (if any).
        '''
        for dress in response.css('.ProductListWithLoadMore52__listingGrid a'):
            yield {
                'name' : self.clean_name(dress.css(".ProductItem24__name::text").get()),
                'brand' : dress.css(".ProductItem24__designer::text").get(),
                'original_price($)' : self.get_float_val(dress.css(".PriceWithSchema9__value span::text").get()),
                'sale_price($)' : self.get_float_val(dress.css(".PriceWithSchema9__value span::text").get()),
                # this fild and the next field store the image urls of only first 14 products (I'm not sure how to make this right).
                'primary image_url' : str(dress.css(".ProductItem24__imageContainer .primaryImage img::attr(src)").get()),
                'secondary image_url' : str(dress.css(".ProductItem24__imageContainer .secondaryImage img::attr(src)").get()),
                'product_page_url' : str("https://www.net-a-porter.com/" + str(dress.css("a::attr(href)").get())),
                'product_category' : "footwear",
            }

        # this is where I handle pagination (storing data from the first 25 pages only).
        next_url = response.css(".Pagination7__next::attr(href)").get()
        page_number = next_url.split("=")[-1]
        print("\n\n\n", next_url, "\n\n\n")
        if next_url is not None and int(page_number) <= 25:
            next_page = response.urljoin(next_url)
            yield scrapy.Request(next_page, callback=self.parse)