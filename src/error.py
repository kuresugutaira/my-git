class InvalidObjectException(Exception):
  def __str__(self):
    return (
      f"invalid object"
    )
  
class NotCommitException(Exception):
  def __str__(self):
    return (
      f"not commit object"
    )
  
class InvalidCommitObject(Exception):
  def __str__(self):
    return (
      f"invalid commit object"
    )