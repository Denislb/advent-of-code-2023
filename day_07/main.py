def determine_hand_type(hand, part):
    ignore_card = []
    if part == 2:
        ignore_card = ["J"]
    values = {}
    for card in hand:
        if card in ignore_card:
            continue
        values[card] = hand.count(card)
        ignore_card.append(card)
    values = sorted(values.values())
    if len(values) == 0:
        values = "5"
    elif "J" in hand and part == 2:
        values[-1] += hand.count("J")
    if len(values) == 1: # Five of a kind
        return 6
    if max(values) == 4: # Four of a kind
        return 5
    if len(values) == 2 and max(values) == 3: # Full house
        return 4
    if len(values) == 3 and max(values) == 3: # Three of a kind
        return 3
    if len(values) == 3 and max(values) == 2: # Two pairs
        return 2
    if len(values) == 4 : # One pair
        return 1
    # High card
    return 0

def sort_based_on_strength(hand, strengths):
    return [strengths.index(character) for character in hand]

def sort_hands(hands_types, strengths):
    sorted_hands = {}
    for hands in hands_types:
        sorted_hands[hands] = sorted(hands_types[hands], key=lambda hands : sort_based_on_strength(hands, strengths))
    return sorted_hands

def resolve(filename, strengths, part):
    hands_types = {x: [] for x in range(0, 7)}
    hands_bids = {}
    with open(filename) as f:
        for l in f:
            splitted = l.split()
            hand = splitted[0]
            bid = splitted[1]
            t = determine_hand_type(hand, part)
            hands_types[t].append(hand)
            hands_bids[hand] = int(bid)
    sorted_hands = sort_hands(hands_types, strengths)
    sum = 0
    idx = 1
    for types in sorted_hands:
        for hand in sorted_hands[types]:
            sum += idx * hands_bids[hand]
            idx += 1
    return sum

if __name__ == "__main__":
    input_path = "./day_07/input.txt"
    print("---Part One---")
    print(resolve(input_path, ["2", "3", "4", "5", "6", "7", "8", "9", "T", "J", "Q", "K", "A"], 1))

    print("---Part Two---")
    print(resolve(input_path, ["J", "2", "3", "4", "5", "6", "7", "8", "9", "T", "Q", "K", "A"], 2))
