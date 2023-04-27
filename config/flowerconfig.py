import json


def format_task(task):
    kw = json.loads(task.kwargs.replace("'", '"'))
    kw.pop("segreto", None)
    task.kwargs = json.dumps(kw).replace('"', "'")
    return task
