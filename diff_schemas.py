import sys
import oyaml


def diff_schemas(old_schema, new_schema):
    added = {
        task_name: task
        for task_name, task in new_schema.items()
        if task_name not in old_schema
    }
    changed = {
        task_name: {'old': task, 'new': new_schema[task_name]}
        for task_name, task in old_schema.items()
        if (
            task_name in new_schema
            and new_schema[task_name] != task
        )
    }
    removed = {
        task_name: task
        for task_name, task in old_schema.items()
        if task_name not in new_schema
    }

    return added, changed, removed


def assess_changed_task(task):
    old_args_iter = iter(task['old'])
    new_args_iter = iter(task['new'])

    for old, new in zip(old_args_iter, new_args_iter):
        old_name = old['name']
        new_name = new['name']
        if old['name'] != new['name']:
            print(f'[ERROR] Argument {old_name} was replaced with {new_name}.')

    for old in old_args_iter:
        name = old['name']
        print(f'[ERROR] Missing argument: {name}.')

    for new in new_args_iter:
        name = new['name']
        if new['default'] is None:
            print(f'[ERROR] New argument {name} without default value.')
            continue

        default = new['default']
        print(f'[INFO] New argument {name} with default value: {default}.')


def main(old_filename, new_filename):
    with open(old_filename) as f:
        old_schema = oyaml.load(f)

    with open(new_filename) as f:
        new_schema = oyaml.load(f)

    added, changed, removed = diff_schemas(old_schema, new_schema)

    for task in added:
        print(f'[INFO] Added task: {task}')

    for task_name, task in changed.items():
        assess_changed_task(task)

    for task in removed:
        print(f'[WARNING] Removed task: {task}')


if __name__ == '__main__':
    main(sys.argv[1], sys.argv[2])
