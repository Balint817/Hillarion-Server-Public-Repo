raw_iron: bool = False
raw_copper: bool = False
raw_gold: bool = False
# Raw ores have their value decreased (excluding ancient debris, for obvious reasons)
raw_decrease: float = 10 # The value deduction given as a percentage decrease
netherite_bonus: float = 0 # Given as a percentage increase in value
allow_bonus: bool = False # For discounts and such
allow_netherite: bool = False
preference: bool = True

preferred: str = "diamond"


prices: dict[str: int] = dict()
prices["emerald"] = 3
prices["coal"] = 8
prices["lapis"] = 32
prices["copper"] = 40
prices["iron"] = 64
prices["gold"] = 196
prices["diamond"] = 4096
prices["scrap"] = 5120

# Redstone has an Item Value of 1

# ----------------------------------------------
# ----------------------------------------------
# ----------------------------------------------


raw_decrease /= 100
if allow_netherite:
    try:
        prices["netherite"] = prices["scrap"]*4+prices["gold"]*4
        prices["netherite"] *= 1+(netherite_bonus/100)
    except:
        pass
if raw_iron:
    prices["iron"] = prices["iron"]*raw_decrease
if raw_copper:
    prices["copper"] = prices["copper"]*raw_decrease
if raw_gold:
    prices["gold"] = prices["gold"]*raw_decrease


prices["redstone"] = 1
x = float(input("The price in terms of IV: ").replace(",", "."))
if allow_bonus:
    price_deduction: float = float(input("The price deduction given as a percentage decrease: ").replace(",", "."))
else:
    price_deduction = 0

if preference:
    while preferred not in prices:
        preferred = input("The identifier of your preferred item: ")
        if preferred not in prices:
            print("This item is not registered.\n")
x *= 1-(price_deduction/100)
if price_deduction:
    print(f"Price after deduction: {x}")
x = (-(-x//1)).__trunc__()


sorted_prices = sorted([(v,k) for k,v in prices.items()], reverse=True)
if preference:
    try:
        k = sorted_prices.index((prices[preferred], preferred))
        sorted_prices = [(prices[preferred], preferred)]+sorted_prices
        del sorted_prices[k+1]
    except:
        pass
lst = []
for price in sorted_prices:
    if price[0] <= x:
        if (k:=(x//price[0]).__trunc__()):
            lst.append((k, price[1]))
            x -= k*price[0]
string = ", ".join([f"{i[0]} {i[1]}" for i in lst])
print("\nPrice:")
print(string)

        
