from typing import NamedTuple
from constants import TokenType, KeyWord, token_keyword_map
import re


class Token(NamedTuple):
    token_type: TokenType
    value: str


class JackTokenizer:
    def __init__(self, input) -> None:
        """Opens the input .jack file/stream and gets ready to tokeninze it."""
        self._tokens = []
        self._tokenize(input)
        # print(self._tokens)

    def _get_next_token(self):
        return self._tokens[0]

    def has_more_tokens(self) -> bool:
        """Are there any more tokens in the input?"""
        return bool(self._tokens)

    def advance(self) -> None:
        """Gets the next token from the input and makes it the current token.
        This method should be called only if has_more_tokens returns True.
        Initially there is no current token."""
        self.current_token = self._tokens.pop(0)
        print(self.current_token)

    def token_type(self) -> TokenType:
        """Returns the type of the current token."""
        return self.current_token.token_type

    def key_word(self) -> KeyWord:
        """Returns the keyword which is the current token as a constant."""
        # return self.current_token.value
        if not self.token_type() == TokenType.KEYWORD:
            raise RuntimeError(f"Expected: keyword, Got: {self.current_token.value}.")
        return token_keyword_map[self.current_token.value].value

    def symbol(self) -> str:
        """Returns the character which is the current token. Should only be
        called if token_type is SYMBOL."""
        if not self.token_type() == TokenType.SYMBOL:
            raise RuntimeError(f"Expected: symbol, Got: {self.current_token.value}.")
        if self.current_token.value == "<":
            return "&lt;"
        elif self.current_token.value == ">":
            return "&gt;"
        elif self.current_token.value == "&":
            return "&amp;"
        return self.current_token.value

    def identifier(self) -> str:
        """Returns the string which is the current token. Should only be
        called if token_type is IDENTIFIER."""
        if not self.token_type() == TokenType.IDENTIFIER:
            raise RuntimeError(
                f"Expected: identifier, Got: {self.current_token.value}."
            )
        return self.current_token.value

    def int_val(self) -> int:
        """Returns the integer value of the current token. Should only be
        called if token_type is INT_CONST."""
        if not self.token_type() == TokenType.INT_CONST:
            raise RuntimeError(f"Expected: int_const, Got: {self.current_token.value}.")
        return int(self.current_token.value)

    def string_val(self) -> str:
        """Returns the string value of the current token without the opening and
        closing double quotes. Should only be called if token_type is STRING_CONST."""
        if not self.token_type() == TokenType.STRING_CONST:
            raise RuntimeError(f"Expected: str_const, Got: {self.current_token.value}.")
        return self.current_token.value[1:-1]

    def _tokenize(self, input):
        keyword_spec = (r"\b" + e.value + r"\b" for e in KeyWord)
        token_specification = [
            # Skip whitespace and comments
            ("KEYWORD", rf"{'|'.join(keyword_spec)}"),
            ("SYMBOLS", r"\{|\}|\(|\)|\[|\]|\.|,|;|\-|\+|\*|/|&|\||<|>|=|~"),
            ("INT_CONST", r"\d+"),
            ("STRING_CONST", r'".*"'),
            ("IDENTIFIER", r"\w+"),
            ("SKIP", r"(?:\s+)"),
        ]
        tok_regex = "|".join(r"(?P<%s>%s)" % pair for pair in token_specification)
        block_comment_regex = r"/\*.*?\*/"
        inline_comment_regex = r"//.*?\n"
        temp = input.read()
        # Remove inline and block comments
        temp = re.sub(inline_comment_regex, "\n", temp)
        temp = re.sub(block_comment_regex, "", temp, flags=re.DOTALL)
        for mo in re.finditer(tok_regex, temp):
            kind = mo.lastgroup
            value = mo.group()
            if kind == "SKIP":
                continue
            if value:
                if kind == "KEYWORD":
                    token_type = TokenType.KEYWORD
                elif kind == "SYMBOLS":
                    token_type = TokenType.SYMBOL
                elif kind == "INT_CONST":
                    token_type = TokenType.INT_CONST
                elif kind == "IDENTIFIER":
                    token_type = TokenType.IDENTIFIER
                else:
                    token_type = TokenType.STRING_CONST
                self._tokens.append(Token(token_type, value))
