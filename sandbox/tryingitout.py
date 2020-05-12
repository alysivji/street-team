from typing import NamedTuple

events = [
    {"type": "upload_image", "performed_by": 1, "details": {}},
    {"type": "crop_image", "performed_by": 1, "details": {"top": 2, "left": 3, "bottom": 4, "right": 5}},
    {"type": "add_caption", "performed_by": 1, "details": {"caption": "hanging out with the ChiPy cr3w"}},
    {"type": "modify_caption", "performed_by": 1, "details": {"caption": "hanging out with the ChiPy crew"}},
]


class CropBox(NamedTuple):
    left: int
    top: int
    right: int
    bottom: int


class CurrentState:
    def __init__(self, events):
        for event in events:
            self.apply(event)

    def apply(self, event):
        if event["type"] == "upload_image":
            pass
        elif event["type"] == "crop_image":
            self.cropbox = event["details"]
        elif event["type"] == "add_caption":
            self.caption = event["details"]["caption"]
        elif event["type"] == "modify_caption":
            self.caption = event["details"]["caption"]
        else:
            raise NotImplementedError
