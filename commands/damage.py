class cause:
    type = "selector"
    color = "selector"
    next = None

class _from:
    type = "command"
    color = "command"
    next = cause

class entity:
    type = "selector"
    color = "selector"
    next = _from

class location:
    type = "coords"
    color = "num"
    next = None

class atby_subc:
    type = "subcommand"
    color = "subcommand"
    valid_variants = {"at": location, "by": entity}

class damage_type:
    type = "path"
    color = "path"
    next = atby_subc

class amount:
    type = "num"
    color = "num"
    next = damage_type

class target:
    type = "selector"
    color = "selector"
    next = amount

class damage:
    type = "command"
    color = "command"
    next = target

class command:
    root = damage