



class Character:
    def __init__(self, name, series, art_urls = {}):
        #short
        self.name = name
        self.series = series
        self.art_urls = art_urls
        #game stats
        self.wishlists = 0

    def create_card(id):
        pass
    def get_listing(self, type="short"):
        match type:
            case "long":
                listing = CharacterListing(
                    self.name,
                    self.series,
                    self.art_urls
                )
            case "short":
                listing = CharacterListing(
                    self.name,
                    self.series
                )
        return listing

class CharacterListing:
    def __init__(self, name, series, art_urls=None):
        self.name = name
        self.series = series
        if art_urls:
            self.art_urls = art_urls