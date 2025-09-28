from typing import Any, Dict, List, Tuple
import json, input

Filter = Tuple[str, str, Any]


def safe_get(item: Dict[str, Any], key: str, default: Any = None) -> Any:
    try:
        return item[key]
    except KeyError:
        return default
    

def to_bool_ascending(order: str) -> bool:
    if order is None:
        return True
    lowered = str(order).casefold()
    if lowered == "asc":
        return True
    if lowered == "desc":
        return False
    return True


def compare(left: Any, op: str, right: Any) -> bool:
    left_is_num = False
    right_is_num = False
    
    try:
        left_num = float(left)
        left_is_num = True
    except Exception:
        right_is_num = False

    try:
        right_num = float(right)
        right_is_num = True
    except Exception:
        right_is_num = False

    if left_is_num and right_is_num:
        a = left_num
        b = right_num
    else:
        a = str(left)
        b = str(right)

    if op == "=" or op == "==":
        return a == b
    if op == "!=":
        return a != b
    if op == ">":
        return a > b
    if op == "<":
        return a < b
    if op == ">=":
        return a >= b
    if op == "<=":
        return a <= b
    return False


def matches_filters(item: Dict[str, Any], filters: List[Filter]) -> bool:
    i = 0
    total = len(filters)
    while i < total:
        flt = filters[i]
        if len(flt) != 3:
            return False
        field = flt[0]
        op = flt[1]
        value = flt[2]
        left = safe_get(item, field, None)
        if not compare(left, op, value):
            return False
        i += 1
    return True
    

def insertion_sort_by_priority(
        items: List[Dict[str, Any]],
        ascending: bool,
) -> None:
    n = len(items)
    i = 1
    while i < n:
        current = items[i]
        p_curr = safe_get(current, "priority", 0)

        try:
            p_curr_num = float(p_curr)
            p_curr_is_num = True
        except Exception:
            p_curr_is_num = False

        j = i - 1
        while j >= 0:
            pj = safe_get(items[j], "priority", 0)
            try:
                pj_num = float(pj)
                pj_is_num = True
            except Exception:
                pj_is_num = False

            move = False
            if p_curr_is_num and pj_is_num:
                if ascending:
                    if pj_num > p_curr_num:
                        move = True
                else:
                    if pj_num < p_curr_num:
                        move = True
            else:
                s_curr = str(p_curr)
                s_j = str(pj)
                if ascending:
                    if s_j > s_curr:
                        move = True
                else:
                    if s_j < s_curr:
                        move = True

            if move:
                items[j + 1] = items[j]
                j -= 1
            else:
                break

        items[j + 1] = current
        i += 1

    
def process_items(
    items: List[Dict[str, Any]],
    filters: List[Filter],
    order: str = "ASC",
) -> List[Dict[str, Any]]:

    ascending = to_bool_ascending(order)

    filtered: List[Dict[str, Any]] = []
    rest: List[Dict[str, Any]] = []

    idx = 0
    total = len(items)
    while idx < total:
        it = items[idx]
        if matches_filters(it, filters):
            filtered.append(it)
        else:
            rest.append(it)
        idx += 1

    insertion_sort_by_priority(filtered, ascending)

    result: List[Dict[str, Any]] = []
    i = 0
    m = len(filtered)
    while i < m:
        result.append(filtered[i])
        i += 1

    j = 0
    r = len(rest)
    while j < r:
        result.append(rest[j])
        j += 1

    return result


def main() -> None:
    
    data = input.data

    filters: List[Filter] = [
        ("weight", "=", 3),
        ("width", ">", 2),
    ]
    #ASC o DESC
    order = "ASC"

    result = process_items(data, filters, order)
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()