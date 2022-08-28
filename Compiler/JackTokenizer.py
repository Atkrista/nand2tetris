from constants import TokenType, KeyWord, Symbols, token_keyword_map
import re


class JackTokenizer:
    def __init__(self, input) -> None:
        """Opens the input .jack file/stream and gets ready to tokeninze it."""
        self.tokens = []
        self.current_token = ""
        for line in input.readlines():
            self.tokens.append(line.split())

    def has_more_tokens(self) -> bool:
        """Are there any more tokens in the input?"""
        return bool(self.tokens)

    def advance(self) -> None:
        """Gets the next token from the input and makes it the current token.
        This method should be called only if has_more_tokens returns True.
        Initially there is no current token."""
        self.current_token = self.tokens.pop(0)

    def token_type(self) -> TokenType:
        """Returns the type of the current token."""
        if self.current_token in (e.value for e in KeyWord):
            return TokenType.KEYWORD
        elif self.current_token in Symbols:
            return TokenType.SYMBOL
        elif re.match(r"^\d+$", self.current_token):
            return TokenType.INT_CONST
        elif re.match(r"^[a-zA-Z]+$", self.current_token):
            return TokenType.STRING_CONST
        elif re.match(r"^\D\w+$", self.current_token):
            return TokenType.IDENTIFIER

    def key_word(self) -> KeyWord:
        """Returns the keyword which is the current token as a constant."""
        return token_keyword_map[self.current_token]

    def symbol(self) -> str:
        """Returns the character which is the current token. Should only be
        called if token_type is SYMBOL."""
        return self.current_token

    def identifier(self) -> str:
        """Returns the string which is the current token. Should only be
        called if token_type is IDENTIFIER."""
        return self.current_token

    def int_val(self) -> int:
        """Returns the integer value of the current token. Should only be
        called if token_type is INT_CONST."""
        return int(self.current_token)

    def string_val(self) -> str:
        """Returns the string value of the current token without the opening and
        closing double quotes. Should only be called if token_type is STRING_CONST."""
        return self.current_token[1:-1]
