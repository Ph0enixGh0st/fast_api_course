from sqlalchemy import delete, insert, select, update

from pydantic import BaseModel


class BaseRepository:
    model = None
    schema: type[BaseModel] = None

    def __init__(self, session):
        self.session = session

    async def get_all(self, *args, **kwargs):
        query = select(self.model)
        result = await self.session.execute(query)
        return [
            self.schema.model_validate(model, from_attributes=True)
            for model in result.scalars().all()
        ]

    async def get_one_or_none(self, **filter_by):
        query = select(self.model).filter_by(**filter_by)
        result = await self.session.execute(query)
        model = result.scalars().one_or_none()
        if model is None:
            return None
        else:
            return self.schema.model_validate(model, from_attributes=True)

    # .returning works only with PostgreSQL and SQLite 3.35+
    async def add(self, model_instance: BaseModel):
        stmt = insert(self.model).values(**model_instance.model_dump()).returning(self.model.id)
        result = await self.session.execute(stmt)
        return result.scalars().one_or_none()

    async def delete(self, id_: int):
        stmt = delete(self.model).where(self.model.id == id_).returning(self.model.id)
        result = await self.session.execute(stmt)
        return result.scalars().one_or_none()

    async def update(self, id_: int, model_instance: BaseModel):
        values = model_instance.model_dump(exclude={"id"})
        stmt = (
            update(self.model)
            .where(self.model.id == id_)
            .values(**values)
            .returning(self.model.id)
        )
        result = await self.session.execute(stmt)
        return result.scalars().one_or_none()

    async def edit(self, id_: int, model_instance: BaseModel):
        values = model_instance.model_dump(exclude_unset=True, exclude={"id"})
        stmt = (
            update(self.model)
            .where(self.model.id == id_)
            .values(**values)
            .returning(self.model.id)
        )
        result = await self.session.execute(stmt)
        return result.scalars().one_or_none()

    async def get_filtered(self, *filter, **filter_by):
        query = (
            select(self.model)
            .filter(*filter)
            .filter_by(**filter_by)
        )
        result = await self.session.execute(query)
        return [self.schema.model_validate(model) for model in result.scalars().all()]
