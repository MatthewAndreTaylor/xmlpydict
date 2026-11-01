# Python version of PyDictHandler


class NativePyDictHandler:
    """
    Handler class for parsing XML content into a Python dictionary using the expat parser.
    """

    def __init__(
        self,
        attr_prefix: str = "@",
        cdata_key: str = "#text",
    ):
        self.attr_prefix = attr_prefix
        self.cdata_key = cdata_key
        self.item = None
        self.data = []
        self.item_stack = []
        self.data_stack = []

    def characters(self, data):
        self.data.append(data)

    def startElement(self, name, attrs):
        self.item_stack.append(self.item)
        self.data_stack.append(self.data)
        self.item = (
            None if not attrs else {self.attr_prefix + k: v for k, v in attrs.items()}
        )
        self.data = []

    @staticmethod
    def update_children(target, key, value):
        if target is None:
            target = {}

        if not key in target:
            target[key] = value
        else:
            existing = target[key]
            if isinstance(existing, list):
                existing.append(value)
            else:
                target[key] = [existing, value]
        return target

    def endElement(self, name):
        if self.data_stack:
            py_data = "".join(self.data).strip() or None
            temp_item = self.item

            self.item = self.item_stack.pop()
            self.data = self.data_stack.pop()

            if temp_item is not None:
                if py_data:
                    temp_item[self.cdata_key] = py_data
                self.item = self.update_children(self.item, name, temp_item)
            else:
                self.item = self.update_children(self.item, name, py_data)
