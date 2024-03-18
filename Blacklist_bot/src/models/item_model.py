import config as conf


class Item:
    def __init__(
            self, item_id, name, item_lvl, quality,
            inventory_type, item_type, required_lvl, has_sockets,
            item_gs
    ):
        self.item_id = item_id
        self.name = name
        self.item_lvl = item_lvl
        self.quality = quality
        self.inventory_type = inventory_type
        self.item_type = item_type
        self.required_lvl = required_lvl
        self.has_sockets = has_sockets
        self.enchant = conf.DEFAULT_ENCHANT_VALUE
        self.gems = conf.DEFAULT_GEMS_VALUE
        self.item_gs = item_gs
