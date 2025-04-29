from __future__ import annotations
import hashlib

class SHA1:
  def __init__(self, sha1: bytes):
    self.sha1 = sha1
  
  def __str__(self) -> str:
    return self.sha1.hex()
  
def _test():
  # 文字列から_Hashインスタンスを生成
  test_hash: hashlib._Hash = hashlib.sha1(b"test")
  print(f"test_hash: {test_hash.hexdigest()}")
  # _HashインスタンスからSHA1インスタンスに変換
  test_sha1: SHA1 = SHA1(test_hash.digest())
  print(f"test_sha1: {test_sha1}")

_test()