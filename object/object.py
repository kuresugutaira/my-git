import hashlib
from typing import Optional
from object.object_type import Type, NewType
import io

class Object:
  def __init__(self, hash: hashlib._Hash, type: Type, size: int, data: bytes):
    self.hash = hash
    self.type = type
    self.size = size
    self.data = data

def _read_null_terminated_string(f: io.BufferedReader, sha1: hashlib._Hash) -> Optional[str]:
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

def read_object(file_path: str) -> Optional[Object]:
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
      return Object(hash, type, size, data)

  except FileNotFoundError:
    print("File not found.")
    return None
