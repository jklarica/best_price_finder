from datetime import timedelta

from products.models import PricingBlock


def _f(pricing_blocks, start_date, nights):
    results = []
    current_blocks = filter(
        lambda block: (
            block.start_date <= start_date and
            block.end_date >= start_date + timedelta(
                days=block.nights
            ) and
            block.nights <= nights
        ),
        pricing_blocks
    )

    for block in current_blocks:
        if block.nights < nights:
            child_blocks = _f(
                pricing_blocks,
                start_date + timedelta(days=block.nights),
                nights - block.nights
            )
            for child_block in child_blocks:
                results.append({
                    'price': (
                        block.price +
                        child_block['price']
                    ),
                    'blocks': [block] + child_block['blocks']
                })
        elif block.nights == nights:
            results.append({
                'price': block.price,
                'blocks': [block]
            })

    return results


def get_price(product, start_date, nights):
    """Find the cheapest price for `product` from `start_date` for `nights."""
    pricing_blocks = PricingBlock.objects.filter(product=product)
    result = _f(pricing_blocks, start_date, nights)
    result = sorted(result, key=lambda r: r['price'])
    return result[0]
