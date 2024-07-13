from motor.motor_asyncio import AsyncIOMotorClient
from bson import ObjectId


class DBManager:
    def __init__(self, uri: str, database_name: str):
        self.client = AsyncIOMotorClient(uri)
        self.db = self.client[database_name]

    async def create_item(self, item):
        result = await self.db.items.insert_one(item)
        return await self.read_item(result.inserted_id)

    async def read_item(self, item_id: ObjectId):
        item = await self.db.items.find_one({"_id": item_id})
        if item:
            item["id"] = str(item["_id"])
            # del item["_id"]
        return item

    async def read_items(self) -> list:
        items = []
        cursor = self.db.items.find({})
        async for item in cursor:
            item["id"] = str(item["_id"])
            # del item["_id"]
            items.append(item)
        return items

    async def update_item(self, item_id: ObjectId, item):
        await self.db.items.update_one({"_id": item_id}, {"$set": item})
        return await self.read_item(item_id)

    async def delete_item(self, item_id: ObjectId) -> bool:
        result = await self.db.items.delete_one({"_id": item_id})
        return result.deleted_count > 0
    
    async def prepare_filter(self, study):
        filter = []
        if study.FileName is not None:
            filter.append({'FileName' : { '$regex' : study.FileName, '$options' : 'i' } })
        if study.PatientName is not None:
            filter.append({'PatientName' : { '$regex' :  study.PatientName, '$options' : 'i' } })
        if study.StudyDate is not None:
            filter.append({'StudyDate' : { '$regex' :  study.StudyDate, '$options' : 'i' } })
        if study.PatientID is not None:
            filter.append({'PatientID' : { '$regex' :  study.PatientID, '$options' : 'i' } })
        if study.StudyDescription is not None:
            filter.append({'StudyDescription' : { '$regex' : study.StudyDescription, '$options' : 'i' } })
        if study.SeriesInstanceUID is not None:
            filter.append({'SeriesInstanceUID' : { '$regex' :  study.SeriesInstanceUID, '$options' : 'i' } })
        if study.StudyID is not None:
            filter.append({'StudyID' : { '$regex' :  study.StudyID, '$options' : 'i' } })
        if study.PatientBirthDate is not None:
            filter.append({'PatientBirthDate' : { '$regex' :  study.PatientBirthDate, '$options' : 'i' } })
        return filter
       

    async def search(self, study) -> list:
        result = list()      
        filter = await self.prepare_filter(study)
        cursor = self.db.items.find({'$and':  filter })
        for item in await cursor.to_list(length=100):
            result.append(item)
 
        return result


db_manager = DBManager(uri="mongodb://mongodb:27017", database_name="db_local")
