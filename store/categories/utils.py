from categories.models import Category


def get_data_from_object(obj):
    return {"id": obj.pk, "name": obj.name, "parent": obj.parent}


def get_data_from_query(query):
    result = [get_data_from_object(category)
              for category in query]
    return result


def get_data_from_object_without_parent(obj):
    return {"id": obj.pk, "name": obj.name}


def get_data_from_query_without_parent(query):
    result = [get_data_from_object_without_parent(category)
              for category in query]
    return result


def get_parents(parent):
    queue = get_data_from_query(Category.objects.filter(name=parent))
    result_parents = []
    while queue:
        category = queue.pop(0)
        result_parents.append({"id": category["id"], "name": category["name"]})
        parents = Category.objects.filter(name=category["parent"])
        for parent_category in parents:
            queue.append(get_data_from_object(parent_category))
    return result_parents
