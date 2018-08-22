import inspect
import json
import sys
import oyaml
from celery_app import app
from collections import OrderedDict


def _get_module(obj):
    module = inspect.getmodule(obj)
    if module:
        return module.__name__

    module = type(obj).__qualname__
    return module


def _pretty_obj(obj):
    if inspect.isclass(obj):
        return obj.__name__

    if inspect.isfunction(obj):
        return obj.__name__

    return repr(obj)


def serialize_item(item):
    return f'{_get_module(item)}:{_pretty_obj(item)}'


def serialize_items(items):
    if not items:
        return None

    return list(map(serialize_item, items))


def kind_to_string(kind):
    return {
        inspect.Parameter.KEYWORD_ONLY: 'keyword_only',
        inspect.Parameter.POSITIONAL_ONLY: 'positional_only',
        inspect.Parameter.POSITIONAL_OR_KEYWORD: 'positional_or_keyword',
        inspect.Parameter.VAR_KEYWORD: 'var_keyword',
        inspect.Parameter.VAR_POSITIONAL: 'var_positional',
    }[kind]


def generate_schema_for_task(task):
    signature = inspect.signature(task.run)
    return [
        OrderedDict([
            ['default', (
                None
                if param.default is inspect.Parameter.empty
                else serialize_item(param.default)
            )],
            ['kind', kind_to_string(param.kind)],
            ['name', param.name],
        ])
        for param in signature.parameters.values()
    ]


def generate_tasks_schema(celery_app):
    return OrderedDict([
        (task.name, generate_schema_for_task(task))
        for task in sorted(celery_app.tasks.values(), key=lambda t: t.name)
    ])


if __name__ == '__main__':
    sys.path.insert(0, '')
    print(oyaml.dump(generate_tasks_schema(app), default_flow_style=False))
