def calculate_total(items):
    return sum(
        item["qty"] * item["price"]
        for item in items
    )
def calculate_tax(total, tax_rate):
    return int(total * tax_rate)

def calculate_final(total, tax):
    return total + tax