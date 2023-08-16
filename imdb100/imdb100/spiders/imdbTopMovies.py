import scrapy


class ImdbSpider(scrapy.Spider):
    name = "imdbTopMovies"
    start_urls = [
        "https://www.imdb.com/search/title/?groups=top_100&sort=user_rating,desc"]

    def parse(self, response):
        movies = response.css('.lister-item-content')

        for movie in movies:
            yield {
                'position': movie.css('.text-primary::text').get(),
                'titles': movie.css('a::text').get(),
                'release_year': movie.css('.text-muted.unbold::text').get(),
                'votes': movie.css('.sort-num_votes-visible span:nth-child(2)::text').get(),
                'rating': movie.css('.ratings-imdb-rating strong::text').get(),
                'gross': movie.css('.sort-num_votes-visible span:nth-child(5)::text').get()
            }

        next_page = 'https://www.imdb.com' + \
            response.css('.next-page::attr(href)').get()
        if next_page:
            yield scrapy.Request(url=next_page, callback=self.parse)
