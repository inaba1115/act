from __future__ import annotations

import re
import typing

from act.temporal_context import TemporalContext


class TidalTracker:
    def __init__(self, commands: typing.Any) -> None:
        self._commands = commands

    def __repr__(self) -> str:
        class_name = type(self).__name__
        return f"{class_name}(commands={self._commands!r})"

    def run(
        self,
        tctx: TemporalContext,
        sequences: list[str],
        duration: float,
        repeats: int,
        is_parallel: bool = True,
    ) -> None:
        asts = [ASTBar.parse(sequence, 0, duration) for sequence in sequences]
        if is_parallel:
            for i in range(repeats):
                for ast in asts:
                    ast.eval(tctx, self._commands)
                tctx.sleep(duration)
        else:
            for i in range(repeats):
                for ast in asts:
                    ast.eval(tctx, self._commands)
                    tctx.sleep(duration)


class ASTBar:
    def __init__(self, children: list[ASTBar | ASTCmd]) -> None:
        self._children = children

    @classmethod
    def parse(cls, text: str, start: float, duration: float) -> ASTBar:
        splitted = split_no_depth(text)
        preprocessed = []
        for token in splitted:
            preprocessed.extend(preprocess(token))

        all_len = 0
        for token in preprocessed:
            _, n, _ = extract_from_marked_str("@", token)
            all_len += n

        children = []
        unit_duration = duration / all_len
        start_tmp = start

        for token in preprocessed:
            token, n, _ = extract_from_marked_str("@", token)
            this_start = start_tmp
            this_duration = unit_duration * n
            start_tmp += this_duration

            if token.startswith("["):
                token = token[1 : len(token) - 1]
                ast = ASTBar.parse(token, this_start, this_duration)
            else:
                ast = ASTCmd.parse(token, this_start, this_duration)
            children.append(ast)

        return ASTBar(children)

    def eval(self, tctx: TemporalContext, commands: typing.Any) -> None:
        for child in self._children:
            child.eval(tctx, commands)


class ASTCmd:
    def __init__(self, cmd: str, args: list[str], start: float, duration: float) -> None:
        self._cmd = cmd
        self._args = args
        self._start = start
        self._duration = duration

    @classmethod
    def parse(cls, text: str, start: float, duration: float) -> ASTCmd:
        xs = text.split(":")
        cmd = xs[0]
        args = xs[1:]
        return ASTCmd(cmd, args, start, duration)

    def eval(self, tctx: TemporalContext, commands: typing.Any) -> None:
        if self._cmd == "_":
            return
        if self._cmd not in commands:
            raise

        context = {
            "ts": tctx.now() + self._start,
            "dur": self._duration,
        }

        commands[self._cmd](context, *self._args)


def split_no_depth(text: str) -> list[str]:
    text = text.strip()
    i = 0
    j = 0
    stack = 0
    ret = []
    while i < len(text):
        if j >= len(text) or text[j] == " ":
            if stack == 0:
                ret.append(text[i:j])
                j += 1
                i = j
                continue
        elif text[j] == "[":
            stack += 1
        elif text[j] == "]":
            stack -= 1
        j += 1
    return ret


RE_AT = re.compile(r"^(.+)@(\d+)$")
RE_SLASH = re.compile(r"^(.+)\/(\d+)$")
RE_ASTER = re.compile(r"^(.+)\*(\d+)$")


def extract_from_marked_str(mark: str, text: str) -> tuple[str, int, bool]:
    m = None
    if mark == "@":
        m = RE_AT.search(text)
    elif mark == "/":
        m = RE_SLASH.search(text)
    elif mark == "*":
        m = RE_ASTER.search(text)

    if m is None:
        return text, 1, False
    else:
        return m.group(1), int(m.group(2)), True


def preprocess(text: str) -> list[str]:
    token, n, matched = extract_from_marked_str("/", text)
    if matched:
        return ["[{}]".format(" ".join([token] * n))]
    token, n, matched = extract_from_marked_str("*", text)
    if matched:
        return [token] * n
    return [text]
