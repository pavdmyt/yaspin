import shutil

from yaspin import yaspin


def test_wo_ellipsis():
    sp = yaspin()
    frame, timer = 2, 10
    max_len = shutil.get_terminal_size().columns - (frame + len(" ") + timer)

    assert sp._get_max_text_length(frame, timer) == max_len


def test_with_ellipsis():
    ellipsis = "..."
    sp = yaspin(ellipsis=ellipsis)
    frame, timer = 2, 10
    max_len = shutil.get_terminal_size().columns - (frame + len(" ") + timer + len(ellipsis))
    assert sp._get_max_text_length(frame, timer) == max_len
