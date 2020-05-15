from dataclasses import dataclass
from .forms import CropBox


class MediaPost:
    def __init__(self, events):
        for event in events:
            self.apply(event)

    def apply(self, event):
        if isinstance(event, UploadImage):
            self.crop_box = None
        elif isinstance(event, CropImage):
            self.crop_box = event.crop_box
        elif isinstance(event, AddCaption):
            self.caption = event.caption
        elif isinstance(event, ModifyCaption):
            self.caption = event.caption
        else:
            raise NotImplementedError


class Event:
    @classmethod
    def match(cls, event):
        return event["type"] == cls.name


@dataclass
class AddCaption(Event):
    name = "add_caption"
    caption: str


@dataclass
class ModifyCaption(Event):
    name = "modify_caption"
    caption: str


@dataclass
class UploadImage(Event):
    name = "upload_image"


@dataclass
class CropImage(Event):
    name = "crop_image"

    def __init__(self, top, left, bottom, right):
        self.crop_box = CropBox(top=top, left=left, bottom=bottom, right=right)


EVENTS_LIST = [AddCaption, ModifyCaption, UploadImage, CropImage]
