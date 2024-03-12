class Item:
    def __init__(
            self, item_id, name, item_lvl, quality,
            inventory_type, required_lvl, has_sockets
    ):
        self.item_id = item_id
        self.name = name
        self.item_lvl = item_lvl
        self.quality = quality
        self.inventory_type = inventory_type
        self.required_lvl = required_lvl
        self.has_sockets = has_sockets
