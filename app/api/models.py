from sqlmodel import SQLModel


class Contact(SQLModel, table=True):
    first_name: str
    last_name: str


class Invoice(SQLModel, table=True):
    invoice_number: str
