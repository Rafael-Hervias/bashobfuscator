import string
import base64
import random
import time

skip_chars = [" ", "\""]
random_unicode = tuple(chr(i) for i in range(400, 8000) if chr(i).isprintable())
random.seed(time.perf_counter())


def random_insert():
    output = random.choice(["@#", "*#", "@%", "*%"])
    for x in range(random.randrange(2, 5)):
        addon_type = random.randrange(1, 9)
        match addon_type:
            case 1:
                # random char
                output += random.choice(string.ascii_letters)
            case 2:
                output += random.choice(["~", "@", "#", "$", "%", "|", " "])
            case 3:
                # random whitespaces
                output += " " * random.randrange(1, 10)
            case 4:
                output += random.choice(random_unicode)
            case 5:
                output += random.choice(["$", "\\{", "\\}", "$", "\\\"", "\\\'", "@#", "*#", "@%", "*%"])
            case 6:
                output += random.choice([
                    "chcon","chgrp",
                    "chown", "chmod",
                    "cp", "dd", "df",
                    "dir", "dircolors", "install",
                    "ln", "ls", "mkdir",
                    "mkfifo", "mknod", "mktemp",
                    "mv", "realpath", "rm",
                    "rmdir", "shred", "sync",
                    "touch", "truncate", "vdir",
                    "b2sum", "base32", "base64",
                    "cat", "cksum", "comm",
                    "csplit", "cut", "expand",
                    "fmt", "fold", "head",
                    "join", "md5sum", "nl",
                    "numfmt", "od", "paste",
                    "ptx", "pr", "sha1sum"])
            case 7:
                if output[len(output) - 1] == "$":
                    output += " "
                output += "${" + ''.join([random.choice(string.ascii_letters) for _ in range(random.randrange(5, 10))]) + "}"
            case 8:
                output += random_string(random.randrange(5, 10)) + "=" + "\\\"" + hexify(random_string(1)) + "\\\""
    return "${" + output + "}"


def basify(script):
    return "echo '" + str(base64.b64encode(script.encode()).decode())[::-1] + "' | rev | base64 -d | sh"


def random_string(length):
    return ''.join(random.choice(string.ascii_letters) for _ in range(length))


def choppify(script, chunk_size):
    return [script[i:i+chunk_size] for i in range(0, len(script), chunk_size)]


def choppa(script, size):
    chunks = choppify(script, size)
    variables = ""
    eval_str = ""
    for chunk in chunks:
        variable_name = random_string(random.randrange(5, 10))
        if chunk in string.ascii_letters:
            chunk = hexify(chunk)
        else:
            chunk = f'\"{chunk}\"'
        variables += f'{variable_name}={chunk};'
        eval_str += f'${variable_name}'
        if random.randrange(1, 3) == 1:
            eval_str += f'${random_string(random.randrange(5, 10))}'
    eval_str = eval_str.replace("$", "$")
    exec_segment = "${eNdSeG}" + f'$\'\\x65\'$\'\\x63\'$\'\\x68\'$\'\\x6f\' {eval_str} | $\'\\x73\'$\'\\x68\''
    return variables + exec_segment


def hexify(script):
    output = ""
    for x in script:
        if x in skip_chars:
            output += x
            continue
        hex_code = str(hex(ord(x))).replace("0x", "x")
        output += "$\'\\{}\'".format(hex_code)
    return output


def add_random_stuff(script):
    segments = script.split("${eNdSeG}")
    first_chunks = list()
    [first_chunks.append(x) for x in segments[0]]
    for x in range(len(first_chunks)):
        if first_chunks[x] == ";":
            if x != 0 and x != len(first_chunks) - 1:
                if first_chunks[x - 1] != "\"" and first_chunks[x + 1] != "\"":
                    first_chunks[x] = ";" + random_insert() + ";"
    segments[0] = ''.join(first_chunks)
    second_chunks = list()
    [second_chunks.append(x) for x in segments[1]]
    for x in range(len(second_chunks)):
        if second_chunks[x] == "$":
            second_chunks[x] = random_insert() + "$"
    segments[1] = ''.join(second_chunks)
    return random_insert() + ";" + segments[0] + segments[1] + ";" + random_insert() + random_insert() + random_insert()


def reverse(script):
    return script[::-1]


def revify(script):
    return f'echo "{script}" | rev | rev | rev | sh'


def order(script):
    script = basify(script)
    script = choppa(script, 1)
    script = add_random_stuff(script)
    script = basify(script)
    script = reverse(script)
    script = revify(script)
    script = script.replace("\"", "\\\"")
    script = choppa(script, 100)
    script = add_random_stuff(script)
    return script

