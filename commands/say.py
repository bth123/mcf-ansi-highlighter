class text:
    type = "text borderless"
    color = "string"

class say:
    type = "command"
    color = "command"
    valid_variants = {"say": text}

class command:
    root = say
