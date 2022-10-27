from configparser import NoOptionError
from lib2to3.pgen2.token import OP
from pprint import pprint
import re
import itertools as itt
import logging as log
from typing import List, Set, Dict, Tuple, Optional, Sequence, Union
from pydantic import BaseModel


class SequenceModel(BaseModel):
    name: str = ""
    varians: Set[int] = set()
    count: int = 0
    regex: bool = False


class Sequence(SequenceModel):
    def __init__(self, *args, **kwargs):
        super(Sequence, self).__init__(*args, **kwargs)

    def __str__(self) -> str:
        range = self.generate_range()
        return "{count}  {name}  {range}".format(**self.dict(), range=range)

    def __add__(self, file_format: SequenceModel) -> SequenceModel:
        regex = False
        varians = self.varians.union(file_format.varians)
        count = len(varians)
        name = self.name

        if self.regex < file_format.regex:
            name = file_format.name

        if not count:
            count = 1

        if self.regex + file_format.regex:
            regex = True

        return Sequence(name=name, varians=varians, count=count, regex=regex)

    def generate_range(self) -> str:
        if not self.varians:
            return ""

        varians = sorted(self.varians)
        last_varian: int = varians[0]
        result = [str(last_varian)]
        size = len(varians) - 2
        for id, varian in enumerate(varians[1:]):
            if last_varian + 1 == varian and size == id:
                result.extend(["-", str(varian)])
            if last_varian + 1 < varian:
                result.extend(["-", str(last_varian), " ", str(varian)])

            last_varian = varian

        return "".join(result)


def groups_to_regex(groups: Tuple, varian: str) -> str:
    name = "".join(groups)
    regex = "%d"
    if len(varian) > 1 and varian[0] == "0":
        regex = "%0{}d".format(len(varian))

    result = name.replace(varian, regex)
    return result


def contiguous_groups(group_a: Tuple, group_b: Tuple) -> Tuple[str, int, int]:
    if len(group_a) != len(group_b):
        return ()

    varians = []
    for val_a, val_b in zip(group_a, group_b):
        if val_a == val_b:
            continue
        elif varians:
            return ()

        if not val_a.isdigit() or not val_b.isdigit():
            return ()

        if abs(int(val_a) - int(val_b)) > 0:
            varians = [val_a, val_b]

    if varians:
        regex = groups_to_regex(group_a, varians[0])
        return regex, int(varians[0]), int(varians[1])

    return ()


def generate_obj_sequence(file_a: str, file_b: str) -> Sequence:
    groups_a = re.findall("(\d+|\D+)", file_a)
    groups_b = re.findall("(\d+|\D+)", file_b)

    if not groups_a:
        return Sequence(name=file_a, varians=set(), count=1)

    is_contigu = contiguous_groups(groups_a, groups_b)
    if is_contigu:
        regex, va, vb = is_contigu
        return Sequence(name=regex, varians={va, vb}, count=2, regex=True)

    return Sequence(name=file_a, varians=set(), count=1)


def format_sequences(files: List[str] = []) -> List[Tuple[int, str, str]]:
    data: Dict[Sequence] = {}
    last_obj: Sequence = Sequence()
    last_file: str = ""
    varians: Set = set()
    file_b: str = ""

    for file_a, file_b in itt.combinations(files, 2):
        obj = generate_obj_sequence(file_a, file_b)
        if last_file and file_a != last_file:
            if file_a in varians:
                continue
            elif not data.get(last_obj.name):
                data[last_obj.name] = last_obj

            last_obj = Sequence()

        if file_a == last_file and obj.regex:
            last_obj += obj
            varians = varians.union({file_a, file_b})

        if not last_obj.regex:
            last_obj = obj

        last_file = file_a

    if file_b and file_b not in varians:
        data[file_b] = generate_obj_sequence(file_b, file_b)

    result = []
    for regex, datum in data.items():
        range = datum.generate_range()
        result.append((datum.count, regex, range))
        # result.append(str(datum))

    # if result:
    #     result.sort(key=lambda x: x[1])

    return result
