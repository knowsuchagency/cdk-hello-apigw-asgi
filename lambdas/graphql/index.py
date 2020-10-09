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


def update_note(note):
    original = TABLE.get_item(Key={"id": note["id"]})

    params = dict(
        TableName=TABLE_NAME,
        ExpressionAttributeValues={},
        ExpressionAttributeNames={},
        UpdateExpression="",
        ReturnValues="UPDATED_NEW",
    )

    prefix = "set "

    for key, value in note.items():

        if key == "id":

            continue

        params["UpdateExpression"] += f"{prefix}#{key} = : {key}"

        params["ExpressionAttributeValues"][f":{key}"] = value

        params["ExpressionAttributeNames"][f"#{key}"] = key

        prefix = ", "

    print(f"{params=}")

    TABLE.update(
        Key={"id": note["id"]},
        AttributeUpdates={
            k: v for k, v in note.items() if original[k] != v or k == "id"
        },
    )

    return note


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
    elif field_name == "updateNote":
        return update_note(arguments["note"])
    else:
        return None
