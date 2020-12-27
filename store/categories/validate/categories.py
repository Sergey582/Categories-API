from categories.models import Category


class CategoryValidate:
    def __init__(self):
        self.errors = []
        self.names = []
        self.validated_data = []

    def is_unique(self, name):
        if name in self.names:
            return False
        self.names.append(name)
        name_from_db = Category.objects.filter(name=name).first()
        if name_from_db:
            return False
        return True

    def data_is_dict(self, data):
        if not isinstance(data, dict):
            self.errors.append({"structure error": "input data must be dict"})
            return False
        return True

    def check_name(self, name):
        if not name or not isinstance(name, str):
            self.errors.append({"value error": f"name {name} must be string"})
        if not self.is_unique(name):
            self.errors.append({"value error": f"{name} must be unique"})

    def validate(self, data):
        if not self.data_is_dict(data):
            return
        name = data.get('name', "")
        self.check_name(name)
        self.validated_data.append({"name": name, "parent": None})
        queue = [data, ]
        while queue:
            category = queue.pop(0)
            parent = category['name']
            children = category.get('children', [])
            if not isinstance(children, list):
                self.errors.append({"structure error": "input data must be dict"})
            for child in children:
                name = child["name"]
                self.validated_data.append({"name": name, "parent": parent})
                self.check_name(name)
                queue.append(child)
