from scrapy.linkextractors import LinkExtractor


class PracujLinkExtractor(LinkExtractor):
    def __init__(self, *args, filter_link=None, **kwargs):
        """LinkExtractor for pracuj.pl site.

        Accepts all LinkExtractor arguments and one custom `filter_link`
        argument, which should be one of:
            string: spider method name used for filtering links from
            pracuj.pl
            None: accept all links
            callable: function used for filtering links

        Any callable should accept 2 parameters: url and its category
        name.
        """
        super().__init__(*args, **kwargs)
        self.filter_link = filter_link

    def extract_links(self, response):
        links = list()
        for link in super().extract_links(response):
            if self.filter_link(link.url, response.meta['category_name']):
                links.append(link)
        return links
