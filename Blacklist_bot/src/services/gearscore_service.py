"""source code found at:
    # https://github.com/Rdyx/warmane-armory-bot/blob/master/src/gearScore.py
    # Thank you author for that!
"""


def get_item_gear_score(item_type, item_level, item_quality):
    # Need to include also Shields. They are just Off-Hands
    # Items like: Librams, Idols, Sigls etc. in itemDb they have None type
    if item_type == 'Shield':
        item_type = 'Off-Hand'
    elif item_type == 'None' and item_quality == '0':
        item_type = 'Relic'
        item_quality = '4'
    elif item_quality == '0':
        item_quality = '4'

    if item_type in ['Shirt', 'Tabard']:
        return 0

    try:
        return __create_gear_score()[item_type][item_level][item_quality]

    # In case of any error, simply return 0
    # pylint: disable=bare-except
    except:
        return 0


def __create_gear_score():
    """ Create a dictionary to link item levels and their corresponding gear score """
    dictionary = {}

    # Rare, Epic
    # We use this because items with ilvl 200 can be Rare, Epic or Legendary
    item_rarities = ['3', '4', '5']
    item_levels = [200, 213, 219, 226, 232, 239, 245, 251, 258, 259, 264, 271, 272, 277, 284]
    item_slots = [
        'Head', 'Chest', 'Robe', 'Legs', 'Main Hand',
        'One-Hand', 'Off-Hand', 'Held In Off-hand', 'Shoulder',
        'Hands', 'Waist', 'Feet', 'Neck',
        'Cloak', 'Wrist', 'Finger', 'Trinket',
        'Ranged', 'Relic', 'Thrown', 'Two-Hand', 'Ranged Right'
    ]

    highest_gs_slots_names = [
        'Head', 'Chest', 'Robe', 'Legs',
        'Main Hand', 'One-Hand', 'Off-Hand', 'Held In Off-hand'
    ]
    highest_gs_slots_values = [271, 310, 348, 365, 385, 402, 422, 439, 457, 463, 477, 494, 514, 523, 531, 551]

    second_highest_gs_slots_names = ['Shoulder', 'Hands', 'Waist', 'Feet']
    second_highest_gs_slots_values = [
        203, 233, 261, 274, 289,
        301, 316, 329, 342, 346, 357, 370, 385, 391, 398, 413
    ]

    middle_gs_slots_names = ['Neck', 'Cloak', 'Wrist', 'Finger', 'Trinket']
    middle_gs_slots_values = [
        152, 174, 195, 205, 216, 226,
        237, 247, 257, 268, 269, 278, 289, 290, 298, 310
    ]

    ranged_gs_slot_names = ['Ranged', 'Relic', 'Thrown', 'Ranged Right']
    ranged_gs_slot_values = [86, 98, 110, 115, 121, 127, 133, 139, 144, 143, 150, 156, 162, 165, 168, 174]

    two_hand_gs_slot_name = ['Two-Hand']
    two_hand_gs_slot_values = [
        543, 621, 696, 730, 770, 805,
        845, 879, 914, 954, 967, 988, 1028, 1045, 1062, 1103
    ]

    # Those items are sharing ilvl with epics equivalent but have
    # more gs due to their quality difference
    legendary_gs_items_names = ['Val\'anyr, Hammer of Ancient Kings', 'Shadowmourne']
    legendary_gs_items_values = [571, 1433]

    # Many conditions to retrieve the wanted information
    # pylint: disable=too-many-nested-blocks
    for item_slot in item_slots:
        gs_values_copy = []
        dictionary[item_slot] = {}

        # Creating a separated copy of array to be able to pop it and use it for multiple item_slots
        if item_slot in highest_gs_slots_names:
            gs_values_copy = highest_gs_slots_values.copy()
        elif item_slot in second_highest_gs_slots_names:
            gs_values_copy = second_highest_gs_slots_values.copy()
        elif item_slot in middle_gs_slots_names:
            gs_values_copy = middle_gs_slots_values.copy()
        elif item_slot in ranged_gs_slot_names:
            gs_values_copy = ranged_gs_slot_values.copy()
        elif item_slot in two_hand_gs_slot_name:
            gs_values_copy = two_hand_gs_slot_values.copy()

        for item_lvl in item_levels:
            # Dict goal, converting int to str to use as key
            item_lvl = str(item_lvl)
            dictionary[item_slot][item_lvl] = {}

            for item_rarity in item_rarities:
                # Legendary item, special values, break loop after data is used
                for legendary_gs_item_name in legendary_gs_items_names:
                    # Break statement earlier to avoid useless process
                    if item_rarity != '5':
                        break
                    if item_rarity == '5':
                        if (
                                item_slot == 'Main Hand' and
                                item_lvl == '245' and
                                legendary_gs_item_name == legendary_gs_items_names[0]
                        ):
                            dictionary[item_slot][item_lvl][item_rarity] = legendary_gs_items_values[0]
                            break
                        if (
                                item_slot == 'Two-hand' and
                                item_lvl == '284' and
                                legendary_gs_item_name == legendary_gs_items_names[1]
                        ):
                            dictionary[item_slot][item_lvl][item_rarity] = legendary_gs_items_values[1]
                            break

                # Using .pop() to get the first value and reduce array length
                # each time we loop over item_lvl
                # We ignore rarity 5 because we already used a loop over it before
                if item_lvl == '200' and item_rarity in ['3', '4']:
                    dictionary[item_slot][item_lvl][item_rarity] = gs_values_copy.pop(0)
                elif item_rarity == '4':
                    dictionary[item_slot][item_lvl][item_rarity] = gs_values_copy.pop(0)

    return dictionary
