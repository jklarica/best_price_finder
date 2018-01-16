import time
from datetime import timedelta

from products.models import PricingBlock, Product


def _get_offers(pricing_blocks, start_date, nights):
    """
    Retrieve all offers based on start date, total number of nights and pricing blocks which match the given time range.

    Recursion is used to find the most granular price block and assemble a collection of block combinations. The output
    will contain all block combos, so once it's sorted by price, the first one will represent the cheapest deal.

    Improvement ideas:
        1.) Reduce number of price blocks - the more pricing blocks we have, the longer it takes to compute all
            combinations
        2.) Use memoization - cache already computed combinations so we don't have to recompute them again
        3.) Server side caching - consider caching searches by using (start_date, nights, product_id) as a key
    """
    offers = []

    candidate_pricing_blocks = filter(
        lambda block: (
            block.start_date <= start_date and
            block.end_date >= start_date + timedelta(days=block.nights) and
            block.nights <= nights
        ),
        pricing_blocks
    )

    for pricing_block in candidate_pricing_blocks:
        if pricing_block.nights < nights:
            child_blocks = _get_offers(
                pricing_blocks,
                start_date + timedelta(days=pricing_block.nights),
                nights - pricing_block.nights
            )
            for child_block in child_blocks:
                offers.append({
                    'price': pricing_block.price + child_block['price'],
                    'blocks': [pricing_block] + child_block['blocks']
                })
        elif pricing_block.nights == nights:
            offers.append({
                'price': pricing_block.price,
                'blocks': [pricing_block]
            })
    return offers


def get_price(product_id, start_date, nights):
    """
    Find the cheapest price for 'product' ranging from 'start_date' to 'start_date' + 'nights'

    This function will retrieve all pricing blocks from the DB, matching the given product ID, and compute all offer
    combinations (for the given time range) in order to find the best/cheapest block combination.
    """
    start = time.time()

    price_blocks = get_lowest_price_blocks(product_id)
    offers = _get_offers(price_blocks, start_date, nights)

    print("Found total {} offers.".format(len(offers)))

    # Return and empty dictionary is no offers were found
    if len(offers) > 0:
        offers = sorted(offers, key=lambda r: r['price'])

        print(
            "The best price is '{}' with the following block configuration: '{}'.".format(
                offers[0]['price'], ','.join(
                    [str(block.id) for block in offers[0]['blocks']]
                )
            )
        )

        print("It took {} second(s) to find the best price.\n".format(time.time() - start))

        # Get the currency for the given product
        offers[0]['currency'] = Product.objects.values('currency').get(id=product_id)['currency']

        return offers[0]
    return {}


def get_lowest_price_blocks(product_id):
    """
    Retrieve price blocks for the given product ID

    If multiple price-block instances with same (start_date, end_date, nights) exist, then pick the one with the
    lowest price.

    Improvement ideas:
        1.) Remove pricing blocks which are obviously out-of-range when compared to given 'start_date' + 'nights'
        2.) If a price block exists which spans across several other blocks and: a) it has the same number of nights
            as all of its child blocks, b) it's cheaper compared to all child blocks - then remove all matching child
            blocks.

            Example:
                [2018. 01. 01. - 2018. 01. 10.] 2 nights cost 100 EUR - KEEP
                [2018. 01. 02. - 2018. 01. 10.] 2 nights cost 120 EUR - REMOVE
                [2018. 01. 03. - 2018. 01. 10.] 2 nights cost 123 EUR - REMOVE

        3.) There's probably a better way to retrieve the min-price blocks per group by leveraging the QuerySet API
    """
    lowest_price_blocks = {}
    for block in PricingBlock.objects.filter(product=product_id).iterator():
        key = (block.start_date, block.end_date, block.nights)
        if key not in lowest_price_blocks:
            lowest_price_blocks[key] = block
        elif lowest_price_blocks[key].price > block.price:
            lowest_price_blocks[key] = block

    return lowest_price_blocks.values()
