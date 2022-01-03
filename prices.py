raw_iron: bool = False
raw_copper: bool = False
raw_gold: bool = False
# Raw ores have their value decreased (excluding ancient debris, for obvious reasons)
raw_decrease: float = 10 # The value deduction given as a percentage decrease
netherite_bonus: float = 0 # Given as a percentage increase in value
allow_bonus: bool = False # For discounts and such
allow_netherite: bool = True # True by default
preference: bool = True # True by default
conversion_type: int = 0 # 0 is IV to items, 1 is items to IV.
preferred: str = "" # You can either enter your preferred value here, or enter it when prompted.
rounding: int = 65 # Selects the first item that is worth more


# You can enter your values here
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

items = dict()
if conversion_type == 1:
    while True:
        action = input("Do you want to 'add' items, 'set' item count, 'list' the current items, or 'continue'? ").lower()
        if action == 'set':
            while True:
                item = input("Enter the identifier of the item you want to set, or 'cancel': ")
                if item in prices:
                    break
                elif item == "cancel":
                    item = None
                    break
                else:
                    print("This item is not registered.")
            if item is not None:
                while True:
                    try:
                        value = int(input(f"Enter the value you wish to set '{item}' to: "))
                        break
                    except:
                        print("Please enter an actual number.")
                items[item] = value
        elif action == 'add':
            while True:
                item = input("Enter the identifier of the item you want to add, or 'cancel': ")
                if item in prices:
                    break
                elif item == "cancel":
                    item = None
                    break
                else:
                    print("This item is not registered.")
            if item is not None:
                while True:
                    try:
                        value = int(input(f"Enter the value you wish to add to '{item}': "))
                        break
                    except:
                        print("Please enter an actual number.")
                if item in items:
                    items[item] += value
                else:
                    items[item] = value
        elif action == 'continue':
            break
        elif action == 'list':
            "\n".join([": ".join((k,str(v))) for k,v in items.items()])
        else:
            print("Unrecognized action.\n")
    x = False
    print(items)
    if any((i<0 for i in items.values())):
        while True:
            x = input("Do you wish to keep negative values ('yes' or 'no')? ")
            if x == "yes":
                x = True
            elif x == "no":
                x = False
    if not x:
        items = dict(((k,v) for k,v in items.items() if v > 0))
    else:
        items = dict(((k,v) for k,v in items.items() if v != 0))
    print("\n"+", ".join([f"{v} {k}" for k,v in items.items()]))
    print("The above items translate to:")
    print(f"{sum((prices[k]*items[k] for k in items))} IV")
    
else:
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


    sorted_prices = sorted(((v,k) for k,v in prices.items()), reverse=True)
    rounding_sort = min((v,k) for k,v in prices.items() if v >= rounding)
    if preference:
        try:
            k = sorted_prices.index((prices[preferred], preferred))
            sorted_prices = [(prices[preferred], preferred)]+sorted_prices
            del sorted_prices[k+1]
        except:
            pass
    lst = []
    rounded = False
    for idx,price in enumerate(sorted_prices):
        if price[0] < rounding:
            if x != 0:
                if lst:
                    try:
                        l = [i[1] for i in lst].index(rounding_sort[1])
                        lst[l] = (lst[l][0]+1,rounding_sort[1])
                    except ValueError:
                        lst.append((1, rounding_sort[1]))
                else:
                    lst.append((1, rounding_sort[1]))
            break
        if price[0] <= x:
            if (k:=(x//price[0]).__trunc__()):
                lst.append((k, price[1]))
                x -= k*price[0]
    print("\nPrice:")
    print(", ".join([f"{i[0]} {i[1]}" for i in lst]))

        
