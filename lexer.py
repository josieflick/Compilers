# Josie Flickinger
# LEXER FOR P2
import sys
import re



def lexer(lines):
    if len(sys.argv) < 2:
        print("Please Specify a File")
        sys.exit(0)

    comment = False
    for line in open(sys.argv[1], "r"):
        print(line.strip())
        comment1 = False
        things = line.split()
        patterns = [
            ("KEYWORD", r"else|if|int|return|void|while"),
            ("SYMBOL", r"\+|-|\*|/|>=|>|<=|<|==|!=|=|;|,|\(|\)|\[|\]|\{|\}"),
            ("INT", r"[0-9]+"),
            ("ID", r"[a-zA-Z]+"),
            ("FLOAT", r"[0-9]+(\.[0-9]+)?((e|E)[0-9]+)?"),
        ]
        for token in things:
            while len(token) > 0:
                max_so_far = ("ERROR", "")
                if comment:  # if comment = true
                    # token = token[1:]
                    if token.startswith('*/'):
                        token = token[2:]  # cuts off 2
                        comment = False
                    else:
                        token = token[1:]
                    continue
                if comment1:  # if comment1 = true
                    token = token[1:]
                    continue
                if token.startswith('/*'):  # for the case that a comment is mid line
                    comment = True
                    continue
                if token.startswith('//'):
                    token = token[2:]
                    comment1 = True
                    continue
                for pattern in patterns:
                    result = re.match(pattern[1], token)
                    if not result:
                        continue
                    if result.start() != 0:
                        continue
                    match_string = result.string[0:result.end()]
                    if len(max_so_far[1]) < len(match_string):
                        max_so_far = (pattern[0], match_string)
                if max_so_far == ("ERROR", ""):
                    max_so_far = ("ERROR", token[0])
                token = token[len(max_so_far[1]):]
                print(max_so_far)
