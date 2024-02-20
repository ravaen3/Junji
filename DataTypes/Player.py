
class Player:
    def __init__(self, user_id):
        self.user_id = user_id
        self.curreny = 0
        self.rolls = 20
        self.grabs = 1
        self.max_rolls = 10
        self.max_grabs = 2
        self.last_roll_time = 0
        self.last_grab_time = 0
        self.wishlist = []
        self.cards = []
        self.upgrades = []
        self.inventory = []
    def create_book(self, sort, characters):
        book = []
        page = []
        i = 0
        cards = []
        for card in self.cards:
            card.index = i
            card.get_character(characters)
            i+=1
            cards.append(card)
        match sort:
            case "index":
                pass
            case "series":
                cards = sorted(cards, key=lambda x: x.character.series[0])
            case "name":
                cards = sorted(cards, key=lambda x: x.character.name)
            case "id":
                cards = sorted(cards, key=lambda x: x.id)
        for card in cards:
            page.append(card)
            if len(page) == 20:
                book.append(page)
                page = []
        book.append(page)
        self.book = book
        return book
