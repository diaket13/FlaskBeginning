from flask_restful import abort


def get_paginate(args: dict):
    page = int(args.pop('page', 1))
    size = int(args.pop('size', 10))
    return page, size


def get_filter(filter_fields: tuple, args: dict, partial=True):
    filter_args = {}
    for field in filter_fields:
        if field in args:
            filter_args[field] = args.pop(field)
        elif not partial:
            abort(400)
            raise KeyError(f'[{field}]')
    return filter_args


if '__main__' == __name__:
    a = {
        'page': '1',
        'size': '2',
        3: 'ddd',
        4:13,
        'ddd':12312
    }
    print(a)
    get_paginate(a)
    print(a)
    print(get_filter((3,4),a))
    print(a)
