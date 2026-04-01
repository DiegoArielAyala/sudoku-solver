from time import sleep

template = [[" "] * 9 for _ in range(9)]

def fill_template(row, column, number):
    template[row - 1][column -1] = number

def init_template():
    fill_template(1, 1, 3)
    fill_template(1, 5, 4)
    fill_template(1, 6, 9)
    fill_template(2, 4, 6)
    fill_template(2, 7, 5)
    fill_template(2, 9, 1)
    fill_template(3, 1, 7)
    fill_template(3, 2, 5)
    fill_template(3, 3, 2)
    fill_template(3, 6, 1)
    fill_template(4, 3, 1)
    fill_template(4, 7, 7)
    fill_template(5, 1, 5)
    fill_template(5, 4, 3)
    fill_template(5, 5, 9)
    fill_template(5, 6, 6)
    fill_template(6, 3, 8)
    fill_template(6, 4, 1)
    fill_template(6, 5, 5)
    fill_template(6, 8, 9)
    fill_template(6, 9, 6)
    fill_template(7, 3, 3)
    fill_template(7, 5, 1)
    fill_template(7, 8, 6)
    fill_template(8, 3, 4)
    fill_template(8, 7, 1)
    fill_template(9, 5, 2)
    fill_template(9, 6, 8)

def render_template():
    for row in enumerate(template):
        if row[0] % 3 == 0: print(" ")
        for column in enumerate(row[1]):
            if column[0] % 3 == 0: print("  ", end="")
            print(f"[{column[1]}]", end="")
        print("")

round = 1


def resolve_sudoku(round, template):
    number_filled_in_round = False
    print(f"Round: {round}")
    for row in enumerate(template):
        row_index = row[0]
        for column in enumerate(row[1]):
            column_index = column[0]

            if type(template[row_index][column_index]) == int:
                #print(f"Working with number {template[row_index][column_index]} in row {row_index} and column {column_index}")
                three_rows_check(row_index, column_index, number_filled_in_round)
                three_column_check(row_index, column_index, number_filled_in_round)
                continue

            posible_numbers = list(range(1, 10))
            posible_numbers = check_rows_posible_numbers(posible_numbers, row_index)
            # print(f"Row {row_index + 1} - column {column_index + 1}")
            number_filled_in_round = check_unique_posible_number(posible_numbers, row_index, column_index, number_filled_in_round)
            posible_numbers = check_columns_posible_numbers(posible_numbers, column_index)
            number_filled_in_round = check_unique_posible_number(posible_numbers, row_index, column_index, number_filled_in_round)
            posible_numbers = check_block_posible_numbers(posible_numbers, row_index, column_index)
            number_filled_in_round = check_unique_posible_number(posible_numbers, row_index, column_index, number_filled_in_round)
            #print(f"Posible numbers: {posible_numbers} for row {row_index} and column {column_index}")

            number_filled_in_round = unique_posible_position_in_column(column_index, number_filled_in_round)
            
        number_filled_in_round = unique_posible_position_in_row(row_index, number_filled_in_round)
        number_filled_in_round = unique_posible_position_in_block(number_filled_in_round)

    print(f"is_sudoku_completed: {is_sudoku_completed()}")
    print(f"number_filled_in_round: {number_filled_in_round}")
    if not is_sudoku_completed() and number_filled_in_round:
        round = round + 1
        resolve_sudoku(round, template)
    else:
        resolve_with_backtracking(round, template)

def unique_posible_position_in_row(row_index, number_filled_in_round):
    posible_numbers_in_row = list(range(1, 10))
    posible_positions = []
    #print(f"template row {row_index}: {template[row_index]}")
    for column in enumerate(template[row_index]):
        if type(column[1]) != int:
            posible_positions.append(column[0])
        if type(column[1]) == int:
            try:
                posible_numbers_in_row.remove(column[1])
            except:
                continue
    if posible_numbers_in_row == []:
        return number_filled_in_round
    #print(f"Posible numbers in row {row_index}: {posible_numbers_in_row}")
    #print(f"Posible positions in row {row_index}: {posible_positions}")
    for posible_number in posible_numbers_in_row:
        posible_positions_copy = posible_positions.copy()
        #print(f"Checking posible number {posible_number} in row {row_index}. Posible positions: {posible_positions_copy}")
        # Revisar cada columna de las posiciones posibles, si el numero esta en esa columna, eliminar esa posicion de las posiciones posibles
        # Revisar cada bloque de las posiciones posibles, si el numero esta en ese bloque, eliminar esa posicion de las posiciones posibles    
        for column in [1, 4, 7]:
            start_row_block, end_row_block, start_column_block, end_column_block = define_block(row_index, column)
            if number_in_block(posible_number, start_row_block, end_row_block, start_column_block, end_column_block):
                for column in range(start_column_block, end_column_block):
                    try:
                        posible_positions_copy.remove(column)
                    except:
                        continue
        for column in posible_positions_copy:
            if number_in_column(posible_number, column):
                try:
                    posible_positions_copy.remove(column)
                except:
                    continue
        #print(f"Posible positions left: {posible_positions_copy}")
        if len(posible_positions_copy) == 1 and review_number_before_fill(posible_number, row_index, posible_positions_copy[0]) and type(template[row_index][posible_positions_copy[0]]) != int:
            template[row_index][posible_positions_copy[0]] = posible_number
            number_filled_in_round = True
            render_template()
            print(f"Template in row {row_index} and column {posible_positions_copy[0]} = {posible_number} with unique posible position in row method")
    return number_filled_in_round

def unique_posible_position_in_column(column_index, number_filled_in_round):
    posible_numbers_in_column = list(range(1, 10))
    posible_positions = []
    #print(f"template column {column_index}: { [template[row][column_index] for row in range(9)] }")
    for row in range(9):
        if type(template[row][column_index]) != int:
            posible_positions.append(row)
        if type(template[row][column_index]) == int:
            try:
                posible_numbers_in_column.remove(template[row][column_index])
            except:
                continue
    if posible_numbers_in_column == []:
        return number_filled_in_round
    #print(f"Posible numbers in column {column_index}: {posible_numbers_in_column}")
    #print(f"Posible positions in column {column_index}: {posible_positions}")
    for posible_number in posible_numbers_in_column:
        posible_positions_copy = posible_positions.copy()
        #print(f"Checking posible number {posible_number} in column {column_index}. Posible positions: {posible_positions_copy}")
        # Revisar cada columna de las posiciones posibles, si el numero esta en esa columna, eliminar esa posicion de las posiciones posibles
        # Revisar cada bloque de las posiciones posibles, si el numero esta en ese bloque, eliminar esa posicion de las posiciones posibles    
        for row in [1, 4, 7]:
            start_row_block, end_row_block, start_column_block, end_column_block = define_block(row, column_index)
            if number_in_block(posible_number, start_row_block, end_row_block, start_column_block, end_column_block):
                for row in range(start_row_block, end_row_block):
                    try:
                        posible_positions_copy.remove(row)
                    except:
                        continue
        for row in posible_positions_copy:
            if posible_number in template[row]:
                try:
                    posible_positions_copy.remove(row)
                except:
                    continue
        #print(f"Posible positions left: {posible_positions_copy}")
        if len(posible_positions_copy) == 1 and review_number_before_fill(posible_number, posible_positions_copy[0], column_index) and type(template[posible_positions_copy[0]][column_index]) != int:
            template[posible_positions_copy[0]][column_index] = posible_number
            number_filled_in_round = True
            render_template()
            print(f"Template in column {column_index} and row {posible_positions_copy[0]} = {posible_number} with unique posible position in column method")
    return number_filled_in_round

def unique_posible_position_in_block(number_filled_in_round):
    posible_numbers_in_block = list(range(1, 10))
    for row in [1, 4, 7]:
        for column in [1, 4, 7]:
            posible_positions = []
            copy_posible_numbers_in_block = posible_numbers_in_block.copy()
            start_row_block, end_row_block, start_column_block, end_column_block = define_block(row, column)
            if row >= start_row_block and row < end_row_block and column >= start_column_block and column < end_column_block:
                for row_in_block in range(start_row_block, end_row_block):
                    for column_in_block in range(start_column_block, end_column_block):
                        if type(template[row_in_block][column_in_block]) != int:
                            posible_positions.append([row_in_block, column_in_block])
                        if type(template[row_in_block][column_in_block]) == int:
                            try:
                                copy_posible_numbers_in_block.remove(template[row_in_block][column_in_block])
                            except:
                                continue
            #print(f"Posible numbers in block of row {row} and column {column}: {copy_posible_numbers_in_block} and posible positions {posible_positions}")
            
            for posible_number in copy_posible_numbers_in_block:
                copy_posible_positions = posible_positions.copy()
                #print(f"{copy_posible_positions} Inicial copy_posible_positions for number {posible_number}")
                #print(f" start row block { start_row_block} end row block { end_row_block}")
                for row_in_block in range(start_row_block, end_row_block):
                    #print(f"Searching {posible_number} in row {row_in_block} {template[row_in_block]}")
                    copy_copy_posible_positions = copy_posible_positions.copy()
                    if posible_number in template[row_in_block]:
                        #print(f"Copy copy posible positions {copy_copy_posible_positions} for number {posible_number} in row {row_in_block}")
                        for position in copy_posible_positions:
                            if position[0] == row_in_block:
                                try:
                                    copy_copy_posible_positions.remove(position)
                                    #print(f"Removed a posible position with row. Copy copy posible positions {copy_copy_posible_positions} for number {posible_number}")
                                except:
                                    continue
                #render_template()
                for column_in_block in range(start_column_block, end_column_block):
                    for posible_row in range(9):
                        #print(f"Searching {posible_number} in column {column_in_block} and row {posible_row} {template[posible_row][column_in_block]}")
                        if posible_number == template[posible_row][column_in_block]:
                            for position in copy_posible_positions:
                                if position[1] == column_in_block:
                                    #print(f"position {position} == column_in_block {column_in_block}")
                                    try:
                                        copy_copy_posible_positions.remove(position)
                                    except:
                                        continue
                                    #print(f"Removed a posible position {position} with column. Copy copy posible positions {copy_copy_posible_positions} for number {posible_number}")
                #print(f"{copy_copy_posible_positions} Final copy_posible_positions for number {posible_number} in row {row_in_block} and column {column_in_block}")
                if len(copy_copy_posible_positions) == 1 and review_number_before_fill(posible_number, copy_copy_posible_positions[0][0], copy_copy_posible_positions[0][1]) and template[copy_copy_posible_positions[0][0]][copy_copy_posible_positions[0][1]] != int:
                    template[copy_copy_posible_positions[0][0]][copy_copy_posible_positions[0][1]] = posible_number
                    number_filled_in_round = True
                    render_template()
                    #print(f"Unique posible position for {posible_number} in {copy_copy_posible_positions}")
                else:
                    # print(f"{copy_copy_posible_positions} Checking number {posible_number}  in row {row} column {column} in positions: ")
                    try:
                        if check_unique_row_in_block(copy_copy_posible_positions):
                            #print(f"Unique row in block for number {posible_number} in positions {copy_copy_posible_positions}")
                            pass
                        if check_unique_column_in_block(copy_copy_posible_positions):
                            #print(f"Unique column in block for number {posible_number} in positions {copy_copy_posible_positions}")
                            pass
                    except:
                        continue
                    
    return number_filled_in_round

def check_unique_row_in_block(copy_copy_posible_positions):
    row = copy_copy_posible_positions[0][0]
    for position in copy_copy_posible_positions:
        if position[0] == row:
            continue
        else:
            return False
    return True

def check_unique_column_in_block(copy_copy_posible_positions):
    column = copy_copy_posible_positions[0][1]
    for position in copy_copy_posible_positions:
        if position[1] == column:
            continue
        else:
            return False
    return True    

def check_rows_posible_numbers(posible_numbers, row_index):
    for box in template[row_index]:
        if type(box) == int:
            try:
                posible_numbers.remove(box)
                # print(f"Removed {box} from row")
                #sleep(1)
            except:
                continue
    return posible_numbers

def check_columns_posible_numbers(posible_numbers, column_index):
    for row in range(0, 9):
        box = template[row][column_index]
        if type(box) is int:
            try:
                posible_numbers.remove(box)
                # print(f"Removed {box} from column")
                #sleep(1)
            except:
                continue
    return posible_numbers

def check_block_posible_numbers(posible_numbers, row_index, column_index):
    start_row_block, end_row_block, start_column_block, end_column_block = define_block(row_index, column_index)
    # print(start_row_block, end_row_block, start_column_block, end_column_block)
    for row in range(start_row_block, end_row_block):
        for column in range(start_column_block, end_column_block):
            box = template[row][column]
            if type(box) == int:
                try:
                    posible_numbers.remove(box)
                    # print(f"Removed {box} from block")
                    #sleep(1)
                except:
                    continue
    return posible_numbers

def define_block(row_index, column_index):
    if row_index < 3:
        start_row_block = 0
        end_row_block = 3
    elif row_index < 6:
        start_row_block = 3
        end_row_block = 6
    else:
        start_row_block = 6
        end_row_block = 9
    
    if column_index < 3:
        start_column_block = 0
        end_column_block = 3
    elif column_index < 6:
        start_column_block = 3
        end_column_block = 6
    else:
        start_column_block = 6
        end_column_block = 9
    return start_row_block, end_row_block, start_column_block, end_column_block

def three_rows_check(row_index, column_index, number_filled_in_round):
    # Agarrar cada celda
    # Revisar si en una de las filas de su bloque esta ese numero
    # Revisar en la otra fila de ese bloque si esta ese numero
    # Si en solo una fila no esta el numero, revisar en los casilleros vacios, si en esas columnas esta el numero
    # Si solo hay un casillero vacio donde puede ir el numero, rellenarlo ahi
    number = template[row_index][column_index]
    
    start_row_block, end_row_block, start_column_block, end_column_block = define_block(row_index, column_index)

    counter, positions_of_number = count_number_in_row_block(start_row_block, end_row_block, number)
    
    # Si el counter es 2, buscar en que fila no esta el numero
    if counter == 2:
        #print(f"Working with number {template[row_index][column_index]} in row {row_index + 1} and column {column_index + 1} using three_rows_method")
        row = row_without_number(start_row_block, end_row_block, number)

        # Tomar esa fila, crear un rango del 0 al 8 con las columnas, eliminar cada numero si en esa casilla hay un numero o si en la columa existe el numero
        columns = get_posibles_columns(row, number, positions_of_number)
        fill_number_if_one_column_left(row, columns, number, number_filled_in_round)

        # Hay que buscar en que bloque esta el otro numero, no "number", sino el otro
        try:
            row_of_second_number = get_row_of_second_number(start_row_block, end_row_block, row_index, number)
            number_index = template[row].index(number)
            #print(f"number index {number_index}")
            _, _, start_column_block, end_column_block = define_block(row_of_second_number, number_index)
            
            for column in range(start_column_block, end_column_block):
                #print(f"Column {column}")
                try:
                    columns.remove(column)
                    #print(f"4 Removed column {column}. Columns left: {columns}")
                except:
                    continue
            fill_number_if_one_column_left(row, columns, number)
        except:
            return
        # print(f"Posible columns for number {number} in row {row + 1}: {columns}")

        fill_number_if_one_column_left(row, columns, number, number_filled_in_round)

def get_posibles_columns(row, number, positions_of_number):
    columns = list(range(0, 9))
    for column in range(0, 9):
        if type(template[row][column]) is int:
            try:
                columns.remove(column)
                #print(f"1 Removed column {column}. Columns left: {columns}")
            except:
                continue
        # Revisar columna
        if number_in_column(number, column):
            try:
                columns.remove(column)
                #print(f"2 Removed column {column}. Columns left: {columns}")
            except:
                continue
# Eliminar las columas del bloque donde esta number
    for position in positions_of_number:
        row_index = position[0]
        column_index = position[1]
        start_row_block, end_row_block, start_column_block, end_column_block = define_block(row_index, column_index)
        if number_in_block(number, start_row_block, end_row_block, start_column_block, end_column_block):
            for column in range(start_column_block, end_column_block):
                try:
                    columns.remove(column)
                    #print(f"3 Removed column {column}. rows left: {columns}")
                except:
                    continue
            #print(f"columns: {columns}")
    
    return columns

def count_number_in_row_block(start_row_block, end_row_block, number):
    counter = 0
    positions_of_number= []
    for row in range(start_row_block, end_row_block):
        if number in template[row]:
            column = template[row].index(number)
            counter += 1
            positions_of_number.append([row, column])
    #print(f"Number {number} is in row range {start_row_block} to {end_row_block - 1} {counter} times")
    #print(f"positions_of_number {number}: {positions_of_number}")
    return counter, positions_of_number

def row_without_number(start_row_block, end_row_block, number):
    for row in range(start_row_block, end_row_block):
        if number not in template[row]:
            #print(f"Number {number} not in row {row}")
            return row

def fill_number_if_one_column_left(row, columns, number, number_filled_in_round):
    if len(columns) == 1 and review_number_before_fill(number, row, columns[0]) and type(template[row][columns[0]]) != int:
        template[row][columns[0]] = number
        number_filled_in_round = True
        render_template()
        print(f"Template in row {row} and column {columns[0]} = {number} with three rows check method")
    return number_filled_in_round

def get_row_of_second_number(start_row_block, end_row_block, row_index, number):
    rows = list(range(start_row_block, end_row_block))
    try:
        # Remover row del number
        rows.remove(row_index)
        # print(f"Removed row {row_index}")
    except:
        return
    
    for row in rows:
        if number in template[row]:
            return row

def number_in_column(number, column_index):
    for row in range(9):
        if template[row][column_index] == number:
            return True

def number_is_in_row(number, row_index):
    return number in template[row_index]
     

def three_column_check(row_index, column_index, number_filled_in_round):
    # Agarrar cada celda
    # Revisar si en una de las filas de su bloque esta ese numero
    # Revisar en la otra fila de ese bloque si esta ese numero
    # Si en solo una fila no esta el numero, revisar en los casilleros vacios, si en esas columnas esta el numero
    # Si solo hay un casillero vacio donde puede ir el numero, rellenarlo ahi
    number = template[row_index][column_index]

    start_row_block, end_row_block, start_column_block, end_column_block = define_block(row_index, column_index)

    counter, positions_of_number = count_number_in_column_block(start_column_block, end_column_block, number)

    # Si el counter es 2, buscar en que columna no esta el numero
    if counter == 2:
        #print(f"Working with number {template[row_index][column_index]} in row {row_index} and column {column_index} using three_column_method")
        column = column_without_number(start_column_block, end_column_block, number)
        # Tomar esa columna, crear un rango del 0 al 8 con las filas, eliminar cada numero si en esa casilla hay un numero o si en la columa existe el numero
        rows = get_posibles_rows(column, number, positions_of_number)
        fill_number_if_one_row_left(column, rows, number, number_filled_in_round)
        
        # Hay que buscar en que bloque esta el otro numero, no "number", sino el otro
        try:
            column_of_second_number, row_of_second_number = get_column_of_second_number(start_column_block, end_column_block, column_index, number)
            
            #print(f"number index {number_index}")
            start_row_block, end_row_block, _, _ = define_block(row_of_second_number, column_of_second_number)
            
            for row in range(start_row_block, end_row_block):
                #print(f"Column {column}")
                try:
                    rows.remove(row)
                    #print(f"4 Removed column {row}. Columns left: {rows}")
                except:
                    continue
            fill_number_if_one_row_left(column, rows, number, number_filled_in_round)
        except:
            return
        # print(f"Posible columns for number {number} in row {row + 1}: {columns}")

        fill_number_if_one_row_left(column, rows, number, number_filled_in_round)


def fill_number_if_one_row_left(column, rows, number, number_filled_in_round):
    if len(rows) == 1 and review_number_before_fill(number, rows[0], column) and type(template[rows[0]][column]) != int:
        template[rows[0]][column] = number
        number_filled_in_round = True
        render_template()
        #print(f"Template in row {rows[0]} and column {column} = {number} with three rows check method")
    return number_filled_in_round

def get_column_of_second_number(start_column_block, end_column_block, column_index, number):
    columns = list(range(start_column_block, end_column_block))
    try:
        # Remover row del number
        columns.remove(column_index)
        # print(f"Removed row {row_index}")
    except:
        return
    
    for column in columns:
        for row in range(0, 9):
            if number in template[row][column]:
                return column, row    

def count_number_in_column_block(start_column_block, end_column_block, number):
    counter = 0
    positions_of_number= []
    for column in range(start_column_block, end_column_block):
        for row in range(0, 9):
            if number == template[row][column]:
                counter += 1
                positions_of_number.append([row, column])
    #print(f"Number {number} is in column range {start_column_block} to {end_column_block - 1} {counter} times")
    #print(f"positions_of_number {number}: {positions_of_number}")
    return counter, positions_of_number


def column_without_number(start_column_block, end_column_block, number):
    for column in range(start_column_block, end_column_block):
        # print(f"Column: {column}, number {number}, start_column_block {start_column_block}, end_column_block {end_column_block}")
        numbers_in_column = []
        for row in range(0, 9):
            if type(template[row][column]) == int:
                numbers_in_column.append(template[row][column])
        if number not in numbers_in_column:
            #print(f"Number {number} not in column {column}")
            return column


def get_posibles_rows(column, number, positions_of_number):
    rows = list(range(0, 9))
    for row in range(0, 9):
        if type(template[row][column]) is int:
            try:
                rows.remove(row)
                #print(f"1 Removed row {row}. rows left: {rows}")
            except:
                continue
        # Revisar fila
        if number_in_row(number, row):
            try:
                rows.remove(row)
                #print(f"2 Removed row {row}. rows left: {rows}")
            except:
                continue
# Eliminar las filas del bloque donde esta number
    

    """ Agregar que se eliminen las filas del bloque donde se repite number y hacer lo equivalente en get_posibles_columns """
    """ Esta mal hecha la funcion porque solo revisa el bloque que ya tiene el numero y necesito que revise los 3 bloques con los que estoy trabajando """
    for position in positions_of_number:
        row_index = position[0]
        column_index = position[1]
        start_row_block, end_row_block, start_column_block, end_column_block = define_block(row_index, column_index)
        if number_in_block(number, start_row_block, end_row_block, start_column_block, end_column_block):
            for row in range(start_row_block, end_row_block):
                try:
                    rows.remove(row)
                    #print(f"3 Removed row {row}. rows left: {rows}")
                except:
                    continue
            #print(f"Rows: {rows}")
    return rows


def number_in_row(number, row):
    if number in template[row]:
        return True

def number_in_block(number, start_row_block, end_row_block, start_column_block, end_column_block):
    for row in range(start_row_block, end_row_block):
        for column in range(start_column_block, end_column_block):
            if number == template[row][column]:
                #print(f"Number {number} is in block of rows {start_row_block} - {end_row_block} and columns {start_column_block} - {end_column_block}")
                return True

def check_unique_posible_number(posible_numbers, row_index, column_index, number_filled_in_round):
    #print(f"Check unique posible number for row {row_index} column {column_index}")
    if len(posible_numbers) == 1 and type(posible_numbers[0]) == int and review_number_before_fill(posible_numbers[0], row_index, column_index):
        template[row_index][column_index] = posible_numbers[0]
        render_template()
        print(f"Template in row {row_index + 1} and column {column_index + 1} = {posible_numbers[0]} with unique posible number method")
        number_filled_in_round = True
        return number_filled_in_round
    return number_filled_in_round

def resolve_with_backtracking(round, template):
    print(f"Backtracking:")
    copy_template = template.copy()
    for row in enumerate(copy_template):
        row_index = row[0]
        for column in enumerate(row[1]):
            column_index = column[0]
            if type(copy_template[row_index][column_index]) == int:
                continue

            posible_numbers = list(range(1, 10))
            posible_numbers = check_rows_posible_numbers(posible_numbers, row_index)
            posible_numbers = check_columns_posible_numbers(posible_numbers, column_index)
            posible_numbers = check_block_posible_numbers(posible_numbers, row_index, column_index)
            #print(f"Posible numbers: {posible_numbers} for row {row_index} and column {column_index}")
            if len(posible_numbers) == 2:
                copy_template[row_index][column_index] = posible_numbers[0]
                if resolve_sudoku(round, copy_template) == False:
                    print(f"Error in backtracking")
            else:
                continue


def review_number_before_fill(posible_number, row_index, column_index):
    start_row_block, end_row_block, start_column_block, end_column_block = define_block(row_index, column_index)
    if number_in_row(posible_number, row_index) or number_in_column(posible_number, column_index) or number_in_block(posible_number, start_row_block, end_row_block, start_column_block, end_column_block):
        print(f"review_number_before_fill False")
        return False
    print(f"review_number_before_fill True")
    return True

def is_sudoku_completed():
    for row in enumerate(template):
        for column in enumerate(row[1]):
            if type(template[row[0]][column[0]]) != int:
                return False
    print("Sudoku is completed")
    return True

init_template()
render_template()
resolve_sudoku(round, template)
