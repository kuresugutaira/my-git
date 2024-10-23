from enum import Enum

class Type(Enum):
  UNDEFINED_OBJECT = 0
  COMMIT_OBJECT = 1
  TREE_OBJECT = 2
  BLOB_OBJECT = 3
  TAG_OBJECT = 4

def NewType(typeStr: str) -> Type:
  if typeStr == "commit":
    return Type.COMMIT_OBJECT
  elif typeStr == "tree":
    return Type.TREE_OBJECT
  elif typeStr == "blob":
    return Type.BLOB_OBJECT
  elif typeStr == "tag":
    return Type.TAG_OBJECT
  else:
    return Type.UNDEFINED_OBJECT