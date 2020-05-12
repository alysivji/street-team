# https://breadcrumbscollector.tech/implementing-event-sourcing-in-python-part-1-aggregates/


class Order:
    def __init__(self, user_id: int, status: str = "new"):
        self.user_id = user_id
        self.status = status

    def set_status(self, new_status: str):
        if new_status not in ("new", "paid", "confirmed", "shipped"):
            raise ValueError(f"{new_status} is not a correct status!")

        self.status = new_status


order = Order(user_id=1)  # 1
order.set_status("confirmed")  # 2
order.set_status("paid")  # 3
order.set_status("shipped")  # 4


class OrderCreated:
    def __init__(self, user_id: int):
        self.user_id = user_id


class StatusChanged:
    def __init__(self, new_status: str):
        self.new_status = new_status


class Order:
    def __init__(self, events: list):  # 1
        for event in events:
            self.apply(event)  # 2

        self.changes = []  # 3

    def apply(self, event):
        if isinstance(event, OrderCreated):
            self.user_id = event.user_id
            self.status = "new"
        elif isinstance(event, StatusChanged):
            self.status = event.new_status
        else:
            raise ValueError("Unknown event!")

    def set_status(self, new_status: str):  # 5
        if new_status not in ("new", "paid", "confirmed", "shipped"):
            raise ValueError(f"{new_status} is not a correct status!")

        event = StatusChanged(new_status)  # 6
        self.apply(event)
        self.changes.append(event)  # 7


events_stream = [
    OrderCreated(user_id=1),  # 1
    StatusChanged("confirmed"),  # 2
    StatusChanged("paid"),  # 3
    StatusChanged("shipped"),  # 4
]
