from sqlalchemy import delete, insert, select, update

from pydantic import BaseModel


class BaseRepository:
    model = None

    def __init__(self, session):
        self.session = session

    async def get_all(self):
        query = select(self.model)
        result = await self.session.execute(query)
        return result.scalars().all()

    async def get_one_or_none(self, **filter_by):
        query = select(self.model).filter_by(**filter_by)
        result = await self.session.execute(query)
        return result.scalars().one_or_none()

    # .returning works only with PostgreSQL and SQLite 3.35+
    async def add(self, model_instance: BaseModel):
        stmt = insert(self.model).values(**model_instance.model_dump()).returning(self.model.id)
        result = await self.session.execute(stmt)
        return result.scalars().one()

    async def delete(self, id_: int):
        stmt = delete(self.model).where(self.model.id == id_).returning(self.model.id)
        result = await self.session.execute(stmt)
        return result.scalars().one()

    async def update(self, id_: int, model_instance: BaseModel):
        values = model_instance.model_dump(exclude={"id"})
        stmt = (
            update(self.model)
            .where(self.model.id == id_)
            .values(**values)
            .returning(self.model.id)
        )
        result = await self.session.execute(stmt)
        return result.scalars().one()