from typing import Any, List, Optional


class Spreadsheet:

    def __init__(self, rows: int, cols: int, cell_width: int = 10) -> None:
        if rows <= 0 or cols <= 0:
            raise ValueError("rows y cols deben ser positivos")
        self.rows = rows
        self.cols = cols
        self.cell_width = cell_width
        self._data: List[List[Optional[Any]]] = self._build_matrix(rows, cols)

    #Build Matrix
    def _build_matrix(
        self, rows: int, cols: int
    ) -> List[List[Optional[Any]]]:
        data: List[Optional[List[Optional[Any]]]] = []
        i = 0
        while i < rows:
            row: List[Optional[Any]] = []
            j = 0
            while j < cols:
                row.append(None)
                j += 1
            data.append(row)
            i += 1
        return data

    #Validate Pos
    def _validate_pos(self, row: int, col: int) -> None:
        if row < 1 or row > self.rows or col < 1 or col > self.cols:
            raise IndexError("Posición fuera de rango")

    #Index
    def _to_index(self, row: int, col: int) -> (int, int):
        self._validate_pos(row, col)
        return row - 1, col - 1

    #blank
    @staticmethod
    def _is_blank_string(text: str) -> bool:
        n = len(text)
        if n == 0:
            return True
        i = 0
        while i < n:
            ch = text[i]
            if ch != " " and ch != "\t":
                return False
            i += 1
        return True

    #Whitout Value
    @staticmethod
    def _is_empty_value(value: Any) -> bool:
        if value is None:
            return True
        if isinstance(value, str):
            return Spreadsheet._is_blank_string(value)
        return False

    #Whit Value
    def has_value(self, row: int, col: int) -> bool:
        r, c = self._to_index(row, col)
        return not self._is_empty_value(self._data[r][c])

    #Insert Cell
    def insert_cell(self, row: int, col: int, value: Any) -> bool:
        r, c = self._to_index(row, col)
        if self.has_value(row, col):
            return False
        self._data[r][c] = value
        return True

    #Update Cell
    def update_cell(self, row: int, col: int, value: Any) -> bool:
        r, c = self._to_index(row, col)
        if not self.has_value(row, col):
            return False
        self._data[r][c] = value
        return True

    #Get Cell
    def set_cell(self, row: int, col: int, value: Any) -> None:
        r, c = self._to_index(row, col)
        self._data[r][c] = value

    #Get Row
    def get_row_elements(self, row: int) -> List[Optional[Any]]:
        self._validate_pos(row, 1)
        result: List[Optional[Any]] = []
        c = 0
        while c < self.cols:
            result.append(self._data[row - 1][c])
            c += 1
        return result

    #Get Col
    def get_col_elements(self, col: int) -> List[Optional[Any]]:
        self._validate_pos(1, col)
        result: List[Optional[Any]] = []
        r = 0
        while r < self.rows:
            result.append(self._data[r][col - 1])
            r += 1
        return result

    #Number
    @staticmethod
    def _to_number(value: Any) -> Optional[float]:
        try:
            return float(value)
        except Exception:
            return None

    #Sum Row
    def sum_row(self, row: int) -> float:
        elems = self.get_row_elements(row)
        total = 0.0
        i = 0
        n = len(elems)
        while i < n:
            num = self._to_number(elems[i])
            if num is not None:
                total += num
            i += 1
        return total

    #Sum Col
    def sum_col(self, col: int) -> float:
        elems = self.get_col_elements(col)
        total = 0.0
        i = 0
        n = len(elems)
        while i < n:
            num = self._to_number(elems[i])
            if num is not None:
                total += num
            i += 1
        return total

    #Adjust Cell
    def _pad(self, value: Any) -> str:
        if value is None:
            text = ""
        else:
            text = str(value)
        if len(text) > self.cell_width:
            text = text[: self.cell_width]
        needed = self.cell_width - len(text)
        spaces = ""
        k = 0
        while k < needed:
            spaces += " "
            k += 1
        return text + spaces

    #View Row x Col
    def render(self) -> str:
        # Header col
        line = self._pad("") 
        col_num = 1
        while col_num <= self.cols:
            line += self._pad(str(col_num))
            col_num += 1

        lines: List[str] = [line]

        # Header row
        row = 1
        while row <= self.rows:
            line = self._pad(str(row))
            col = 1
            while col <= self.cols:
                val = self._data[row - 1][col - 1]
                if val is None:
                    cell = ""
                else:
                    cell = str(val)
                line += self._pad(cell)
                col += 1
            lines.append(line)
            row += 1

        i = 0
        total = len(lines)
        result = ""
        while i < total:
            result += lines[i]
            if i != total - 1:
                result += "\n"
            i += 1
        return result

    def print_preview(self) -> None:
        print(self.render())


def _read_int(prompt: str) -> int:
    while True:
        try:
            value_str = input(prompt)
            # izquierda
            i = 0
            while i < len(value_str) and (value_str[i] == " " or value_str[i] == "\t"):
                i += 1
            j = len(value_str) - 1
            while j >= 0 and (value_str[j] == " " or value_str[j] == "\t"):
                j -= 1
            if j < i:
                raise ValueError("vacío")
            clean = ""
            k = i
            while k <= j:
                clean += value_str[k]
                k += 1
            return int(clean)
        except Exception:
            print("Entrada inválida. Intente de nuevo.")


def _read_cell(rows: int, cols: int) -> (int, int):
    while True:
        r = _read_int("Fila (1..{}): ".format(rows))
        c = _read_int("Columna (1..{}): ".format(cols))
        if 1 <= r <= rows and 1 <= c <= cols:
            return r, c
        print("Coordenadas fuera de rango. Intente de nuevo.")


def _read_value(prompt: str) -> Any:
    return input(prompt)


def main() -> None:
    print("=== Hoja de cálculo (menú interactivo) ===")
    filas = _read_int("Número de filas: ")
    columnas = _read_int("Número de columnas: ")
    sheet = Spreadsheet(rows=filas, cols=columnas, cell_width=12)

    while True:
        print("\nMenú:")
        print("1) Insertar celda")
        print("2) Actualizar celda")
        print("3) ¿Celda tiene información?")
        print("4) Ver (preview)")
        print("5) Sumar FILA")
        print("6) Sumar COLUMNA")
        print("0) Salir")

        opcion = _read_int("Opción: ")

        if opcion == 1:
            print("\n-- Insertar --")
            r, c = _read_cell(sheet.rows, sheet.cols)
            val = _read_value("Valor a insertar: ")
            ok = sheet.insert_cell(r, c, val)
            if ok:
                print("Insertado en ({}, {}).".format(r, c))
            else:
                print("No se pudo insertar: la celda ya tiene información.")

        elif opcion == 2:
            print("\n-- Actualizar --")
            r, c = _read_cell(sheet.rows, sheet.cols)
            val = _read_value("Nuevo valor: ")
            ok = sheet.update_cell(r, c, val)
            if ok:
                print("Actualizado ({}, {}).".format(r, c))
            else:
                print("No se pudo actualizar: la celda está vacía.")

        elif opcion == 3:
            print("\n-- Validar celda --")
            r, c = _read_cell(sheet.rows, sheet.cols)
            tiene = sheet.has_value(r, c)
            if tiene:
                print("La celda ({}, {}) TIENE información.".format(r, c))
            else:
                print("La celda ({}, {}) está VACÍA.".format(r, c))

        elif opcion == 4:
            print("\n-- Preview --")
            sheet.print_preview()

        elif opcion == 5:
            print("\n-- Sumar FILA --")
            r = _read_int("Fila (1..{}): ".format(sheet.rows))
            if r < 1 or r > sheet.rows:
                print("Fila fuera de rango.")
            else:
                elems = sheet.get_row_elements(r)
                print("Elementos fila {}:".format(r), end=" ")
                i = 0
                while i < len(elems):
                    print(elems[i], end=" ")
                    i += 1
                total = sheet.sum_row(r)
                print("\nSuma fila {} = {}".format(r, total))

        elif opcion == 6:
            print("\n-- Sumar COLUMNA --")
            c = _read_int("Columna (1..{}): ".format(sheet.cols))
            if c < 1 or c > sheet.cols:
                print("Columna fuera de rango.")
            else:
                elems = sheet.get_col_elements(c)
                print("Elementos columna {}:".format(c), end=" ")
                i = 0
                while i < len(elems):
                    print(elems[i], end=" ")
                    i += 1
                total = sheet.sum_col(c)
                print("\nSuma columna {} = {}".format(c, total))

        elif opcion == 0:
            print("¡Hasta luego!")
            break

        else:
            print("Opción no válida.")


if __name__ == "__main__":
    main()
