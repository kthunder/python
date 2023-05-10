from enum import Enum
from typing import Dict


class State(Enum):
    ST_SRC = 0
    ST_READY_CMT = 1
    ST_ONE_LINE_CMT = 2
    ST_MULTI_LINE_CMT = 3
    ST_READY_SRC = 4
    ST_ERR = 99
    ST_END = 100


class Tokenizer:
    EOF = ''
    ANY = None

    # Table driven programming
    TRANSITION_TABLE: Dict[State, Dict[str | None, State]] = {
        State.ST_SRC: {
            '/': State.ST_READY_CMT,
            EOF: State.ST_END,
            ANY: State.ST_SRC,
        },
        State.ST_READY_CMT: {
            # '\n': State.ST_ERR,
            # EOF: State.ST_ERR,
            '/': State.ST_ONE_LINE_CMT,
            '*': State.ST_MULTI_LINE_CMT,
            ANY: State.ST_SRC,
        },
        State.ST_ONE_LINE_CMT: {
            '\n': State.ST_SRC,
            EOF: State.ST_SRC,
            ANY: State.ST_ONE_LINE_CMT,
        },
        State.ST_MULTI_LINE_CMT: {
            '*': State.ST_READY_SRC,
            EOF: State.ST_END,
            ANY: State.ST_MULTI_LINE_CMT,
        },
        State.ST_READY_SRC: {
            '/': State.ST_SRC,
            '*': State.ST_READY_SRC,
            EOF: State.ST_END,
            ANY: State.ST_MULTI_LINE_CMT
        },
        State.ST_END: {
        }
    }

    def __init__(self, string, verbose=False) -> None:
        self.string = string
        self.idx = 0
        self.verbose = verbose

    def next_char(self):
        if self.idx == len(self.string):
            return Tokenizer.EOF
        c = self.string[self.idx]
        self.idx += 1
        return c

    def err_handler(self, last_state):
        print('Error happened:', last_state)

    def trasform(self):
        table = self.TRANSITION_TABLE
        last = State.ST_SRC
        current = State.ST_SRC
        result_str = ''

        one_line_comment = ''

        while (True):
            raw_char = self.next_char()
            if self.verbose:
                print(f"{current:<25}  ===[{repr(raw_char):^5}]==>  ", end='')

            # Handle ANY char
            if raw_char not in table[current]:
                c = Tokenizer.ANY
            else:
                c = raw_char

            # Could not find valid char
            if c not in table[current]:
                self.err_handler(current)
                current = State.ST_ERR
                return result_str

            # Transit
            last = current
            current = table[current][c]
            if self.verbose:
                print(f"{current:<25}")

            # Main logic
            if current == State.ST_ONE_LINE_CMT:
                if last != State.ST_ONE_LINE_CMT:
                    # Enter one line comment  (throw '/')
                    result_str += '* '
                else:
                    one_line_comment += raw_char
            elif current != State.ST_ONE_LINE_CMT and last == State.ST_ONE_LINE_CMT:
                # End of one line comment
                result_str += one_line_comment.replace('*/', '* /')
                result_str += ' */'
                result_str += raw_char
                one_line_comment = ''
            else:
                result_str += raw_char

            if c == Tokenizer.EOF:
                return result_str


test_str = """
/* // **/
// *** // */
/// *** /**/
"""

# TODO: '*/'  =>  '* /'

tk = Tokenizer(test_str, verbose=True)
print(tk.trasform())
