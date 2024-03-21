from pydantic import BaseModel, Field
from typer import Typer, Option
import tempfile
import datetime

from faker import Faker

from typing import Literal

import pg8000.native

class Customer(BaseModel):

    name: str = Field(..., max_length=100)
    date_of_birth: datetime.date = Field(...)
    address: str = Field(...)
    phone_number: str = Field(...)

    @classmethod
    def fake(cls: "Customer", faker: Faker) -> "Customer":
       return cls(
           name=faker.name(),
           date_of_birth=faker.date_of_birth(),
           address=faker.address(),
           phone_number=faker.phone_number(),
       )

class CustomerRelaxedChange(BaseModel):

    name: str = Field(..., max_length=100)
    date_of_birth: datetime.date = Field(...)
    address: str = Field(...)
    phone_number: str = Field(...)
    signed_up_at: datetime.datetime = Field(...)

    @classmethod
    def fake(cls: "Customer", faker: Faker) -> "Customer":
       return cls(
           name=faker.name(),
           date_of_birth=faker.date_of_birth(),
           address=faker.address(),
           phone_number=faker.phone_number(),
           signed_up_at=faker.date_time(),
       )

class CustomerBreakingChange(BaseModel):

    name: str = Field(..., max_length=100)
    date_of_birth: int = Field(...)
    address: str = Field(...)
    phone_number: str = Field(...)
    signed_up_at: datetime.datetime = Field(...)

    @classmethod
    def fake(cls: "Customer", faker: Faker) -> "Customer":
       return cls(
           name=faker.name(),
           date_of_birth=faker.date_of_birth().timestamp(),
           address=faker.address(),
           phone_number=faker.phone_number(),
           signed_up_at=faker.date_time(),
       )

app = Typer()

@app.command()
def bootstrap(
    entity: str = Option(),
    number_of_entities: int = Option(default=100),
) -> None:
    connection = pg8000.native.Connection(
        user="postgres",
        host="127.0.0.1",
        password="postgres",
        database="main",
        port=5432,
    )
    connection.run("""
        CREATE TABLE IF NOT EXISTS customer (
            record_id UUID PRIMARY KEY,
            ingested_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            body JSONB
        )
    """)
    # with tempfile.NamedTemporaryFile() as tmp:  
    #     for _ in range(number_of_entities):
    #         entity = customer.fake(faker)
    #         cursor.execute(
    #             """
    #                 INSERT INTO 
    #             """
    #         )


if __name__ == "__main__":
    app()