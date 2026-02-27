"""Recursive-descent expression parser."""

from __future__ import annotations


class _Parser:
    def __init__(self, expr: str) -> None:
        self.expr = expr
        self.i = 0

    def parse(self) -> int | float:
        value = self._parse_add_sub()
        self._skip_ws()
        if self.i != len(self.expr):
            raise ValueError(f"Unexpected token at position {self.i}")
        return value

    def _skip_ws(self) -> None:
        while self.i < len(self.expr) and self.expr[self.i].isspace():
            self.i += 1

    def _peek(self, s: str) -> bool:
        self._skip_ws()
        return self.expr.startswith(s, self.i)

    def _consume(self, s: str) -> bool:
        if self._peek(s):
            self.i += len(s)
            return True
        return False

    def _parse_add_sub(self) -> int | float:
        value = self._parse_mul_div()
        while True:
            if self._consume("+"):
                value = value + self._parse_mul_div()
            elif self._consume("-"):
                value = value - self._parse_mul_div()
            else:
                return value

    def _parse_mul_div(self) -> int | float:
        value = self._parse_power()
        while True:
            if self._peek("**"):
                return value
            if self._consume("*"):
                value = value * self._parse_power()
            elif self._consume("/"):
                value = value / self._parse_power()
            else:
                return value

    def _parse_power(self) -> int | float:
        left = self._parse_unary()
        if self._consume("**"):
            # Right-associative exponentiation: a ** b ** c == a ** (b ** c)
            right = self._parse_power()
            return left**right
        return left

    def _parse_unary(self) -> int | float:
        if self._consume("-"):
            return -self._parse_unary()
        return self._parse_primary()

    def _parse_primary(self) -> int | float:
        if self._consume("("):
            value = self._parse_add_sub()
            if not self._consume(")"):
                raise ValueError("Missing closing parenthesis")
            return value
        return self._parse_number()

    def _parse_number(self) -> int | float:
        self._skip_ws()
        start = self.i

        saw_digit = False
        saw_dot = False

        while self.i < len(self.expr):
            ch = self.expr[self.i]
            if ch.isdigit():
                saw_digit = True
                self.i += 1
                continue
            if ch == "." and not saw_dot:
                saw_dot = True
                self.i += 1
                continue
            break

        if not saw_digit:
            raise ValueError(f"Expected number at position {start}")

        token = self.expr[start:self.i]
        return float(token) if saw_dot else int(token)


def parse_expr(expr: str) -> int | float:
    """Parse and evaluate an arithmetic expression without using eval()."""

    return _Parser(expr).parse()
