from typing import Optional

def count_ocurrences(
        paragraph: str,
        text: str,
        *,
        case_sensitive: bool = True,
        allow_overlapping: bool = False,
) -> int:
    if paragraph is None or text is None:
        return 0
    
    if not case_sensitive:
        paragraph_cmp = paragraph.casefold()
        text_cmp = text.casefold()
    else:
        paragraph_cmp = paragraph
        text_cmp = text

    n = len(paragraph_cmp)
    m = len(text_cmp)

    if m == 0 or n == 0 or m > n:
        return 0
    
    count = 0
    i = 0
    while i <= n - m:
        matched = True
        j = 0

        while j < m:
            if paragraph_cmp[i + j] != text_cmp[j]:
                matched = False
                break
            j += 1

        if matched:
            count += 1
            if allow_overlapping:
                i += 1
            else:
                i += m
        else:
            i += 1
        
    return count

def main() -> None:
    print("=== Contador de Ocurrecias ===")
    print("Ingrese el parrafo (finalice con Enter)")
    paragraph = input().strip()

    print("Ingrese el texto a buscar:")
    text = input().strip()

    case_sensitive = False
    allow_overlapping = False

    ocurrences = count_ocurrences(
        paragraph,
        text,
        case_sensitive = case_sensitive,
        allow_overlapping = allow_overlapping,
        )
    
    print(f"{ocurrences} ocurrecias encontradas")

if __name__ == "__main__":
    main()