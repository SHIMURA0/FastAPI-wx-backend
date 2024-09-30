# app/crud/instruments.py

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from typing import List, Annotated
from fastapi import Depends
import logging
from sqlalchemy.exc import (
    SQLAlchemyError,
    IntegrityError
)
from pydantic import ValidationError
from app.models.WeChat.instrument_usage_records import InstrumentUsageRecord as InstrumentUsageRecordModel
from app.schemas.WeChat.instruments import InstrumentUsageRecord as InstrumentRecordSchema
from app.api.dependencies.Wechat.db import get_db_dependency

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class InstrumentRecordRepository:
    def __init__(
            self,
            db: AsyncSession
    ) -> None:
        self.db: AsyncSession = db

    async def create_record(
            self,
            instrument_record: InstrumentRecordSchema
    ) -> InstrumentUsageRecordModel:
        """
        Create a new instrument usage record in the database.

        This asynchronous method takes an InstrumentRecordSchema object,
        converts it to an InstrumentUsageRecordModel, and persists it in the database.

        Args:
            instrument_record (InstrumentRecordSchema): A Pydantic model instance
                containing the data for the new instrument usage record. This should
                include all necessary fields as defined in the InstrumentRecordSchema,
                but should not include an ID as it will be auto-generated.

        Returns:
            InstrumentUsageRecordModel: The newly created database model instance,
                including the auto-generated ID and any default values set by the database.

        Raises:
            SQLAlchemyError: If there's an error during the database operation.
            ValidationError: If the input data doesn't match the expected schema.

        Steps:
        1. Convert the Pydantic model to a dict and use it to instantiate an ORM model.
        2. Add the new record to the database session.
        3. Commit the transaction to persist the record.
        4. Refresh the record to ensure it reflects the current database state.

        Note:
            This method assumes that the database is configured to auto-generate
            the primary key (ID) for new records.
        """
        try:
            # Convert Pydantic model to ORM model
            new_id: int = await InstrumentUsageRecordModel.generate_id(self.db)
            details_json_string: str = await InstrumentUsageRecordModel.convert_details_to_json_string(
                instrument_record.details
            )
            db_record = InstrumentUsageRecordModel(
                id=new_id,
                instrument_code=instrument_record.instrument_code,
                instrument=instrument_record.instrument,
                instrument_status=instrument_record.instrument_status,
                operator_name=instrument_record.operator_name,
                details=details_json_string,
            )
            # Add the new record to the database session
            self.db.add(db_record)

            # Commit the transaction to persist the record
            await self.db.commit()

            # Refresh the record to ensure it reflects the current database state,
            # including any auto-generated fields like the ID
            await self.db.refresh(db_record)

            # Return the newly created record
            return db_record

        except IntegrityError as e:
            logger.error("Integrity error: %s", e)
            await self.db.rollback()  # 回滚事务
            raise e  # 重新抛出其他处理

        except ValidationError as ve:
            logger.error("Validation error: %s", ve)
            raise  # 重新抛出异常以便进一步处理

        except SQLAlchemyError as e:
            logger.error("Database error during record creation: %s", str(e))
            await self.db.rollback()  # 事务回滚以保持数据库状态的一致性
            raise  # 重新抛出异常以便进一步处理

        except Exception as e:
            logger.error("Unexpected error: %s", str(e))
            raise  # 重新抛出异常以便进一步处理

    async def read_record(
            self,
            skip: int = 0,
            limit: int = 100
    ) -> List[InstrumentUsageRecordModel]:
        """在 SQLAlchemy 2.0 及以上版本中，AsyncSession 不再直接支持 query() 方法"""
        result = await self.db.execute(
            select(InstrumentUsageRecordModel)
            .offset(skip)
            .limit(limit)
        )
        return list(result.scalars().all())

    # TODO: Implement update_record function
    #
    # This function should update a sequencing record in the database.
    # It should take a record_id and updated data as arguments, and return a boolean
    # indicating whether the update was successful.
    #
    # Planned implementation:
    # 1. Query the database for the record with the given ID
    # 2. If the record exists, update it with the new data
    # 3. Commit the transaction
    # 4. Return True if update was successful, False if the record was not found
    #
    # Example signature:
    # async def update_record(self, record_id: int, updated_data: dict) -> bool:
    #     pass

    # TODO: Implement delete_record function
    #
    # This function should delete a sequencing record from the database.
    # It should take a record_id as an argument and return a boolean
    # indicating whether the deletion was successful.
    #
    # Planned implementation:
    # 1. Query the database for the record with the given ID
    # 2. If the record exists, delete it and commit the transaction
    # 3. Return True if deletion was successful, False otherwise
    #
    # Example signature:
    # async def delete_record(self, record_id: int) -> bool:
    #     pass


# 可以创建一个便捷函数来获取 SequencingRecordRepository 实例
async def get_instrument_record_repository(
        db: Annotated[AsyncSession, Depends(get_db_dependency)]
) -> InstrumentRecordRepository:
    return InstrumentRecordRepository(db)
