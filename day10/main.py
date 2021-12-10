import io


class ChunkParsingException(Exception):
    def __init__(self, found, expected, *kwarg):
        self.found = found
        self.expected = expected
        super(ChunkParsingException, self).__init__(*kwarg)

class ChunkIncompleteException(Exception):
    def __init__(self, *kwarg):
        super(ChunkIncompleteException, self).__init__(*kwarg)


class Tag:
    __slots__ = "open_t", "close_t", "is_closing", "has_been_closed"

    def __init__(self, open_t, close_t, is_closing):
        self.open_t = open_t
        self.close_t = close_t
        self.is_closing = is_closing
        self.has_been_closed = is_closing

    @property
    def opposite_t(self):
        return self.open_t if self.is_closing else self.close_t

    @property
    def type(self):
        return self.close_t if self.is_closing else self.open_t

    def __repr__(self):
        return f"{self.type}"


TAGS = {
    '(': lambda: Tag('(', ')', False),
    '[': lambda: Tag('[', ']', False),
    '{': lambda: Tag('{', '}', False),
    '<': lambda: Tag('<', '>', False),
    ')': lambda: Tag('(', ')', True),
    ']': lambda: Tag('[', ']', True),
    '}': lambda: Tag('{', '}', True),
    '>': lambda: Tag('<', '>', True),
}


class ChunkParser:
    def __init__(self, chunk_data):
        self.raw = chunk_data
        self.stream = io.StringIO(chunk_data)
        self.tags = []

    def __repr__(self):
        return f"{self.raw}"

    def _last_open_tag(self) -> Tag:
        for c in self.tags[::-1]:
            if not c.is_closing and not c.has_been_closed:
                return c

    def parse(self):
        while True:
            c = self.stream.read(1)
            if not c:
                break
            tag = TAGS[c]()
            if tag.is_closing:
                last_open = self._last_open_tag()
                if last_open.opposite_t == tag.type:
                    self.tags.append(tag)
                    last_open.has_been_closed = True
                else:
                    raise ChunkParsingException(
                        tag.type,
                        last_open.opposite_t,
                        f"Failed to parse chunk, expected {last_open.opposite_t} at col {self.stream.tell()} found {tag.type}"
                    )
            else:
                self.tags.append(tag)

        open_tags = 0
        close_tags = 0
        for chunk in self.tags:
            if chunk.is_closing:
                close_tags += 1
            else:
                open_tags += 1

        if open_tags != close_tags:
            raise ChunkIncompleteException(f"Failed to parse chunk, data is missing {open_tags - close_tags} closing tags")

    def fix_closing(self):
        appended_data = ""
        tags = 0
        for chunk in self.tags:
            tags += -1 if chunk.is_closing else +1

        while tags != 0:
            last_open_tag = self._last_open_tag()
            last_open_tag.has_been_closed = True
            new_tag = TAGS[last_open_tag.opposite_t]()
            self.tags.append(new_tag)
            appended_data += last_open_tag.opposite_t

            tags = 0
            for chunk in self.tags:
                tags += -1 if chunk.is_closing else +1

        return appended_data

input_data = open("input.txt", "r").readlines()
chunks = [ChunkParser(data.replace("\n","")) for data in input_data]

scores_parsing = {
    ")": 3,
    "]": 57,
    "}": 1197,
    ">": 25137,
}
scores_incomplete = {
    ")": 1,
    "]": 2,
    "}": 3,
    ">": 4,
}
score_parsing = 0
score_incomplete = []

for chunk in chunks:
    try:
        chunk.parse()
        # Do smthg I don't know
    except ChunkIncompleteException as e:
        print(f"Failed to parse chunk {chunk} :  {e}. Fixing...")
        missing_tags = chunk.fix_closing()
        s = 0
        for c in missing_tags:
            s *= 5
            s += scores_incomplete[c]
        score_incomplete.append(s)
    except ChunkParsingException as e:
        print(f"Failed to parse chunk {chunk} :  {e}")
        score_parsing += scores_parsing[e.found]

score_incomplete.sort()
print(f"Score parsing: {score_parsing}")
print(f"Score incomplete: {score_incomplete}")
print(f"Score incomplete: {score_incomplete[len(score_incomplete)//2]}")