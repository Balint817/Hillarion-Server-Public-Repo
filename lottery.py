"""
Type your name in a new line, followed by 5 numbers, from 1 to 3.
The order of these numbers matter.
After you've done that, just leave the fee of 1 iron ingot in the chest along with the book.
Every day I'll come get the book and announce the results.
Each time nobody wins the prize, the prize will increase.
"""

"""
This book is where you need to put your name and numbers!
Use the format:
first, your name, then a semicolon, then the numbers seperated by a single space. In my case, this would be:
Balint817;1 2 3 1 2
If you're done with that, write your name on the next page
"""

"""
First => all 5 numbers
Second => 4 numbers
Third => 3 numbers

Current prizes:

First prize:
Roughly 5 diamonds (20000 Re)

Second prize:
Roughly 1 diamond (4250 Re)

Third prize:
Roughly 5 gold
(1000 Re)

P.S.: "Re" is just a non-existent measure I use for calculations and such.
Easier to code conversion from one value to multiple, than conversion from multiple to multiple, ya know? I'm lazy.
"""



"""
If nobody wins a prize, then all of the IV that has been gained will be added to the prize pool
Starting values: 
 - 22500
 - 4250
 - 1025
"""

current_prizes = [65769, 33297, 5750]

from random import randint

class Results:
    def __init__(self, row: str) -> None:
        data = row.strip().split(";")
        if len(data) != 2:
            raise ValueError("Incorrect data received!")
        self.name = data[0].strip()
        self.numbers = [int(i) for i in data[1].strip().split()]
        if len(self.numbers) != 5:
            raise ValueError("Count of numbers is not correct!")
    def __str__(self) -> str:
        return f"{self.name};{' '.join(map(str, self.numbers))}"

with open("lottery.txt", "r", encoding="utf-8") as f:
    lst: list[Results] = []
    incorrect: list[str] = []
    for row in f:
        try:
            if row.strip():
                lst.append(Results(row))
        except:
            incorrect.append(row.strip())
if incorrect:
    incorrect = '\n'.join(incorrect)
    print(f"Incorrect items found: {incorrect}")
numbers = [randint(1, 3) for _ in range(5)]
print(f"The numbers are:   {' '.join(map(str, numbers))}\n")
players = dict(((player.name, (0, ())) for player in lst))
for player in lst:
    count = 0
    y = player.numbers
    for i in range(len(numbers)):
        if y[i] == numbers[i]:
            count += 1
    if count > players[player.name][0]:
        players[player.name] = (count, y)

first_prize = tuple(set(k for k,v in players.items() if v[0] == 5))
second_prize = tuple(set(k for k,v in players.items() if v[0] == 4))
third_prize = tuple(set(k for k,v in players.items() if v[0] == 3))
if lst:
    if third_prize:
        if len(third_prize) < 2:
            print(f"{third_prize[0]} won the third prize!")
        else:
            print(f"{', '.join(third_prize[:-1])} and {third_prize[-1]} won the third prize!")
    else:
        print("Nobody won the third prize!")

    if second_prize:
        if len(second_prize) < 2:
            print(f"{second_prize[0]} won the second prize!")
        else:
            print(f"{', '.join(second_prize[:-1])} and {second_prize[-1]} won the second prize!")
    else:
        print("Nobody won the second prize!")

    if first_prize:
        if len(first_prize) < 2:
            print(f"{first_prize[0]} won the first prize!")
        else:
            print(f"{', '.join(first_prize[:-1])} and {first_prize[-1]} won the first prize!")
    else:
        print("Nobody won the first prize!")

    if not first_prize:
        if not second_prize:
            if not third_prize:
                print(f"Value to add to the first prize: {(a:=((len(lst)-len(first_prize))*40)*4+current_prizes[0]*0.01)}")
                print(f"Value to add to the second prize: {(b:=((len(lst)-len(second_prize))*16)*3+current_prizes[1]*0.01)}")
                print(f"Value to add to the third prize: {(c:=((len(lst)-len(third_prize))*8)*2+current_prizes[2]*0.01)}")
                current_prizes[0] += a
                current_prizes[1] += b
                current_prizes[2] += c
            else:
                print(f"The third prize will decrease.")
                k = ((len(lst)-len(third_prize))*8)*2
                print(f"Value to add to the first prize: {(a:=((len(lst)-len(first_prize))*40+k/2)*4+current_prizes[0]*0.01)}")
                print(f"Value to add to the second prize: {(b:=((len(lst)-len(second_prize))*16+k/2)*3+current_prizes[1]*0.01)}")
                current_prizes[0] += a
                current_prizes[1] += b
                current_prizes[2] //= 2
                if current_prizes[2] < 1025:
                    current_prizes[2] = 1025
        else:
            print(f"The second prize will decrease.")
            if not third_prize:
                k = ((len(lst)-len(second_prize))*16)*3
                print(f"Value to add to the first prize: {(a:=((len(lst)-len(first_prize))*40+k/2)*4+current_prizes[0]*0.01)}")
                print(f"Value to add to the third prize: {(b:=((len(lst)-len(third_prize))*8+k/2)*2+current_prizes[2]*0.01)}")
                current_prizes[0] += a
                current_prizes[2] += b
            else:
                print(f"The third prize will decrease.")
                k = ((len(lst)-len(third_prize))*8)*2 + ((len(lst)-len(second_prize))*16)*3
                print(f"Value to add to the first prize: {(a:=((len(lst)-len(first_prize))*40+k/2)*4+current_prizes[0]*0.01)}")
                current_prizes[0] += a
                current_prizes[2] //= 2
                if current_prizes[2] < 1025:
                    current_prizes[2] = 1025
            current_prizes[1] //= 1.5
            if current_prizes[1] < 4250:
                current_prizes[1] = 4250
    else:
        print(f"The first prize has been won, so the prizes will reset.")
        current_prizes = [22500, 4250, 1025]
else:
    print("Nobody participated!\nPrizes will increase by 5%.")
    current_prizes = [i*1.05 for i in current_prizes]
current_prizes = [round(i, 0).__trunc__() for i in current_prizes]
print("New prizes:")
print(current_prizes)