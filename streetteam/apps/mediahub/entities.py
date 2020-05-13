from dataclasses import dataclass


class MediaPost:
    def __init__(self, events):
        for event in events:
            self.apply(event)

    def apply(self, event):
        if isinstance(event, UploadImage):
            pass
        elif isinstance(event, CropImage):
            pass
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


EVENTS_LIST = [AddCaption, ModifyCaption, UploadImage, CropImage]
