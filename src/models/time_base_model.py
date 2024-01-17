from datetime import datetime
from beanie import Document, Replace, Save, SaveChanges, Update, before_event


class TimeBaseModel(Document):
    created_at: datetime = datetime.now()
    updated_at: datetime = datetime.now()

    @before_event(Save, Update, Replace, SaveChanges)
    async def changes(self):
        self.updated_at = datetime.now()

    async def setValue(self, *args):
        value = args[0]
        value['updated_at'] = datetime.now()
        await self.set(value)


