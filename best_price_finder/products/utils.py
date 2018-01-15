from datetime import timedelta

from products.models import PricingBlock
import time


def _get_offers(pricing_blocks, start_date, nights):
    """
    Retrieve all offers based on start_date, total number of nights and pricing blocks which match the given time range.
    """
    results = []

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
                results.append({
                    'price': pricing_block.price + child_block['price'],
                    'blocks': [pricing_block] + child_block['blocks']
                })
        elif pricing_block.nights == nights:
            results.append({
                'price': pricing_block.price,
                'blocks': [pricing_block]
            })
    return results


def get_price(product_id, start_date, nights):
    """ Find the cheapest price for 'product' from 'start_date' and given number of 'nights' """
    start = time.time()

    price_blocks = get_lowest_price_blocks(product_id)
    result = _get_offers(price_blocks, start_date, nights)

    print("Found total {} offer combinations.".format(len(result)))

    if len(result) > 0:
        result = sorted(result, key=lambda r: r['price'])

        print(
            "Best price: {}\nBlocks: {}".format(result[0]['price'], ','.join([str(y.id) for y in result[0]['blocks']]))
        )
        print("It took {} seconds to find the best price.\n".format(time.time() - start))

        return result[0]
    return {}


def get_lowest_price_blocks(product_id):
    """
    Retrieve price blocks for the given product ID. If multiple price-block instances with same (start_date, end_date,
    nights) exist, then pick the one with the lowest price.

    TODO: There's probably a better way to do this by leveraging the QuerySet API
    """
    lowest_price_blocks = {}
    for block in PricingBlock.objects.filter(product=product_id).iterator():
        key = (block.start_date, block.end_date, block.nights)
        if key not in lowest_price_blocks:
            lowest_price_blocks[key] = block
        elif lowest_price_blocks[key].price > block.price:
            lowest_price_blocks[key] = block

    return lowest_price_blocks.values()
