import hashlib
from enum import Enum
import io
from __future__ import annotations
import hashlib
import re
from error import InvalidObjectException, NotCommitException, InvalidCommitObject
from datetime import datetime
from sha import SHA1

class Type(Enum):
  UNDEFINED_OBJECT = 0
  COMMIT_OBJECT = 1
  TREE_OBJECT = 2
  BLOB_OBJECT = 3
  TAG_OBJECT = 4

class Object:
  def __init__(self, hash: SHA1, type: Type, size: int, data: bytes):
    self.hash = hash
    self.type = type
    self.size = size
    self.data = data

class Sign:
  def __init__(self, name: str, email: str, timestamp: datetime):
    self.name = name
    self.email = email
    self.timestamp = timestamp
  
  def __str__(self) -> str:
    return f"{self.name}, {self.email}, {self.timestamp}"

class Commit:
  def __init__(self, hash: hashlib._Hash, size: int, tree: hashlib._Hash, parents: list[hashlib._Hash], author: Sign, commiter: Sign, message: str):
    self.hash = hash
    self.size = size
    self.tree = tree
    self.parents = parents
    self.author = author
    self.commiter = commiter
    self.message = message

  def __str__(self) -> str:
    str_joiner: list[str] = list()
    str_joiner.append(f"Commit   {self.hash.hexdigest()}")
    str_joiner.append(f"Tree     {self.tree.hexdigest()}")
    for p in self.parents:
      str_joiner.append(f"Parent   {p.hexdigest()}")
    str_joiner.append(f"Author   {self.author}")
    str_joiner.append(f"Commiter {self.commiter}")
    str_joiner.append(self.message)
    return "\n".join(str_joiner)

_EMAIL_REGEXP: str = r"([a-zA-Z0-9_.+-]+@([a-zA-Z0-9][a-zA-Z0-9-]*[a-zA-Z0-9]*\.)+[a-zA-Z]{2,})"
_TIMESTAMP_REGEXP: str = r"([1-9][0-9]* \+[0-9]{4})"

_HASH_VALID_REGEXP: str = r"[0-9a-f]{20}"
_SIGN_VALID_REGEXP: str = r"^[^<]* <" + _EMAIL_REGEXP + "> " + _TIMESTAMP_REGEXP + "$"

def _read_null_terminated_string(f: io.BufferedReader, sha1: hashlib._Hash) -> str:
  '''
  ヌル終端文字列を読み込んで返す関数。
  読み込んだbyteでsha1の更新も行う。
  '''
  try:
    result = bytearray()
    while True:
      byte: bytes = f.read(1)
      if not byte: # EOF検知
        break
      if byte == b"\x00": # ヌル文字検知
        break
      result.append(byte[0])
    sha1.update(result) # hashの更新も行う
    return result.decode('utf-8')
  except Exception:
    raise

def _read_header(f: io.BufferedReader, sha1: hashlib._Hash) -> tuple[Type, int]:
  '''
  ファイルのヘッダーを読んでObject TypeとSizeを返す関数。
  読み込んだbyteでsha1の更新も行う。
  '''
  try:
    header_list: list[str] = _read_null_terminated_string(f).split(" ")
    if len(header_list) != 2: # headerの数が正しくない場合
      return 0, 0
    objectType: Type = NewType(header_list[0])
    size: int = int(header_list[1])
    return objectType, size
  except Exception:
    raise

def read_object(file_path: str) -> Object:
  hash: hashlib._Hash = hashlib.sha1()
  try:
    with open(file_path, mode='rb') as f:
      # ヘッダーの読み込み
      try:
        type, size = _read_header(f, hash)
      except ValueError as e:
        print("Invalid file header")
        return None
      # ファイルの内容の読み込み
      data: bytes = f.read()
      hash.update(data)
      # HashインスタンスをSHA1インスタンスに変換
      sha1: SHA1 = SHA1(hash.digest())
      return Object(sha1, type, size, data)
  except Exception:
    raise

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

def read_hash(hash_str: str) -> SHA1:
  try:
    if _hash_valid.match(hash_str) is None:
      raise InvalidCommitObject
    

  except Exception:
    raise

def _test() -> None:
  # dummy hashの作成
  hash: hashlib._Hash = hashlib.sha1(b"hash")
  tree: hashlib._Hash = hashlib.sha1(b"tree")
  parents: list[hashlib._Hash] = [
    hashlib.sha1(b"parent1"),
    hashlib.sha1(b"parent2"),
    hashlib.sha1(b"parent3")
  ]
  # signオブジェクトとcommitオブジェクトの生成
  sign: Sign = Sign("author_name", "email@example.com", datetime.now())
  commit: Commit = Commit(hash, 100, tree, parents, sign, sign, "dummy commit")
  # __str__関数のテスト
  print(f"Sign:\n{str(sign)}\n")
  print(f"Commit:\n{str(commit)}")

_test()