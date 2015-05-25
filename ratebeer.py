import plugintypes
from ratebeer import RateBeer
from ratebeer import rb_exceptions

class RateBeerPlugin(plugintypes.TelegramPlugin):
    rb = RateBeer()

    patterns = {
        "^!beer (.*)" : "beer_search",
    }

    usage = [
        "!beer <beer search>",
    ]

    def beer_search(self, msg, matches):
        beers = self.rb.search(matches.group(1))["beers"]
        if len(beers) == 0:
            return "No such beer found"
        if len(beers) == 1:
            try:
                beer = self.rb.beer(beers[0]['url'])
            except rb_exceptions.AliasedBeer as err:
                beer = self.rb.beer(err.newurl)

            return '{name} - {style}\nOverall: {overall_rating} | Style: {style_rating} | User: {weighted_avg}/5\n{url}'.format(
                    name=beer['name'],
                    overall_rating = beer.get('overall_rating', 'unrated'),
                    style=beer['style'],
                    style_rating = beer.get('style_rating', 'unrated'),
                    weighted_avg = beer.get('weighted_avg', 'unrated'),
                    url = 'ratebeer.com' + beer['url']
            )
        else:
            text = 'Found {} beers matching {}{}: \n'.format(len(beers), (matches.group(1)),
                                                             ' (showing top 20 by score)' if len(beers) >= 20 else '')
            beers = sorted(beers, key=lambda beer: beer.get('overall_rating', -1), reverse=True)[:20]
            for a, b in zip(beers[::2], beers[1::2]):
                text += '{name} ({overall_rating})'.format(name = a['name'], overall_rating = a.get('overall_rating', 'unrated'))
                if b is not None:
                    text += ', {name} ({overall_rating})\n'.format(name = b['name'], overall_rating = b.get('overall_rating', 'unrated'))
            return text


    def run(self, msg, matches):
       pass
