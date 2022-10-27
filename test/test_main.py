from pyparsing import Regex
import pytest
from sequencers import files_sequences


@pytest.mark.parametrize(
    "test_in, test_out",
    [
        ([], []),
        (
            [
                "alpha.txt",
                "file01_0040.rgb",
                "file01_0041.rgb",
                "file01_0042.rgb",
                "file01_0043.rgb",
                "file02_0044.rgb",
                "file02_0045.rgb",
                "file02_0046.rgb",
                "file02_0047.rgb",
                "file1.03.rgb",
                "file2.03.rgb",
                "file3.03.rgb",
                "file4.03.rgb",
                "file.info.03.rgb",
            ],
            [
                (1, "alpha.txt", ""),
                (4, "file01_%04d.rgb", "40-43"),
                (4, "file02_%04d.rgb", "44-47"),
                (4, "file%d.03.rgb", "1-4"),
                (1, "file.info.03.rgb", ""),
            ],
        ),
        (
            [
                "elem.info",
                "sd_fx29.0112.rgb",
                "sd_fx29.0113.rgb",
                "sd_fx29.0115.rgb",
                "sd_fx29.0116.rgb",
                "sd_fx29.0117.rgb",
                "strange.xml",
            ],
            [
                (1, "elem.info", ""),
                (5, "sd_fx29.%04d.rgb", "112-113 115-117"),
                (1, "strange.xml", ""),
            ],
        ),
    ],
)
def test_format_sequences(test_in, test_out):
    result = files_sequences.format_sequences(test_in)
    assert test_out == result


@pytest.mark.parametrize(
    "in_test, out_test",
    [
        (
            ["file01_0041.rgb", "file01_0040.rgb"],
            {
                "name": "file01_%04d.rgb",
                "varians": {40, 41},
                "count": 2,
                "regex": True,
            },
        ),
        (
            ["file01_0041.rgb", ""],
            {
                "name": "file01_0041.rgb",
                "varians": set(),
                "count": 1,
                "regex": False,
            },
        ),
    ],
)
def test_generate_obj_sequence(in_test, out_test):
    result = files_sequences.generate_obj_sequence(*in_test)
    assert out_test == result.dict()


@pytest.mark.parametrize(
    "groups_in, groups_out",
    [
        (
            [
                ["file", "01", "_", "0040", ".rgb"],
                ["file", "01", "_", "0041", ".rgb"],
            ],
            ("file01_%04d.rgb", 40, 41),
        ),
        (
            [
                ["file", "02", "_", "0044", ".rgb"],
                ["file", "02", "_", "0045", ".rgb"],
            ],
            ("file02_%04d.rgb", 44, 45),
        ),
        (
            [
                ["file", "1", "_", "0044", ".rgb"],
                ["file", "2", "_", "0044", ".rgb"],
            ],
            ("file%d_0044.rgb", 1, 2),
        ),
        (
            [
                ["file", "01", "_", "0040", ".rgb"],
                ["file", "02", "_", "0045", ".rgb"],
            ],
            (),
        ),
        ([["alpha.txt"], ["file", "02", "_", "0045", ".rgb"]], ()),
        ([["alpha.txt"], []], ()),
    ],
)
def test_contiguous_groups(groups_in, groups_out):
    result = files_sequences.contiguous_groups(*groups_in)
    assert groups_out == result


@pytest.mark.parametrize(
    "in_test, out_test",
    [
        (
            {
                "obj_a": {
                    "name": "file01_%04d.rgb",
                    "varians": {40, 10, 4},
                    "count": 3,
                    "regex": True,
                },
                "obj_b": {
                    "name": "file01_%04d.rgb",
                    "varians": {41, 11, 5},
                    "count": 3,
                    "regex": True,
                },
            },
            {
                "name": "file01_%04d.rgb",
                "varians": {40, 41, 10, 11, 4, 5},
                "count": 6,
                "regex": True,
            },
        )
    ],
)
def test_combine_Sequences(in_test, out_test):
    obj_a = files_sequences.Sequence(**in_test["obj_a"])
    obj_b = files_sequences.Sequence(**in_test["obj_b"])
    obj_a += obj_b
    assert isinstance(obj_a, files_sequences.Sequence)
    assert out_test == obj_a.dict()
