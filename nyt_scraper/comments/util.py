from typing import List, Dict


def flatten_replies(comments: List[Dict]) -> List[Dict]:
    """Flattens all comments and replies into one list without copying or modifying the objects"""

    result = []
    for comment in comments:
        result.append(comment)
        result.extend(flatten_replies(comment['replies']))

    return result


def remove_reply_references(comments: List[Dict]) -> List[Dict]:
    """Removes the `replies` list from every comments"""

    result = []
    for comment in comments:
        copy = comment.copy()
        copy.pop('replies', None)
        result.append(copy)

    return result
