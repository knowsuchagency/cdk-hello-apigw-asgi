import os

import boto3


TABLE_NAME = os.environ["NOTES_TABLE"]
TABLE = boto3.resource("dynamodb").Table(TABLE_NAME)

dynamodb = boto3.client("dynamodb")


def get_note(id_):
    return TABLE.get_item(Key={"id": id_})


def create_note(note):
    TABLE.put_item(Item=note)
    return note


def list_notes():
    return TABLE.scan()["Items"]


def delete_note(id_):
    TABLE.delete_item(Key={"id": id_})
    return id_


def handler(event, context):

    print(f"{event=}")

    field_name = event["info"]["fieldName"]

    arguments = event["arguments"]

    if field_name == "getNotebyId":
        return get_note(arguments["noteId"])
    elif field_name == "createNote":
        return create_note(arguments["note"])
    elif field_name == "listNotes":
        return list_notes()
    elif field_name == "deleteNote":
        return delete_note(arguments["noteId"])

    else:
        return None
