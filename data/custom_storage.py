from dataclasses import dataclass, asdict, field


def decode_to_custom_dict(d):
    custom_dict = d
    for elem in custom_dict:
        if type(custom_dict[elem]) == dict:
            custom_dict[elem] = decode_to_custom_dict(custom_dict[elem])
        else:
            custom_dict = Storage(storage=custom_dict)
    return custom_dict


@dataclass
class Storage:
    storage: dict
    __setattr__ = dict.__setitem__
    __delattr__ = dict.__delitem__

    def __getattr__(self, item):
        return self.get(item, None)

    def add_user(self, user_id):
        self.storage[user_id] = user_id

    def __getattr__(self, item):
        return self.get(item, None)


@dataclass
class TaskStorage:
    task_no: int
