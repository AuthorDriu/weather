# У номинатима есть ограничения по количеству запросов в секунду,
# поэтому чтобы меньше обращаться к сервису я буду сохранять найденные
# координаты в базе данных, а потом выдавать их по запросу

import peewee
from src.database.connection import db


class CityModel(peewee.Model):
    """CityModel
    Модель для кэширования локаций
    Поиск в базе данных должен проходить по хэшу названия

    Если longitude и latitude пусты, значит, такого адреса не существует,
    но мы всё равно его записали, чтобы меньше обращаться к номинатиму.
    """
    hash = peewee.BlobField(null=False, index=True, unique=True)
    longitude = peewee.DoubleField(null=True)
    latitude = peewee.DoubleField(null=True)

    class Meta:
        database = db  
        db_table = 'cities'