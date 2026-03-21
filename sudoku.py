from time import sleep

template = [[" "] * 9 for _ in range(9)]

def fill_template(row, column, number):
    template[row - 1][column -1] = number

fill_template(1, 1, 8)
fill_template(1, 3, 1)
fill_template(1, 9, 7)
fill_template(2, 2, 9)
fill_template(2, 3, 7)
fill_template(2, 4, 5)
fill_template(2, 5, 8)
fill_template(3, 5, 9)
fill_template(3, 6, 7)
fill_template(3, 7, 6)
fill_template(3, 9, 8)
fill_template(4, 5, 5)
fill_template(4, 9, 3)
fill_template(5, 1, 7)
fill_template(5, 2, 8)
fill_template(5, 4, 3)
fill_template(5, 6, 4)
fill_template(5, 9, 2)
fill_template(6, 3, 3)
fill_template(6, 4, 6)
fill_template(6, 5, 7)
fill_template(6, 7, 1)
fill_template(7, 1, 9)
fill_template(7, 2, 7)
fill_template(7, 3, 6)
fill_template(7, 4, 2)
fill_template(7, 5, 3)
fill_template(7, 6, 1)
fill_template(8, 2, 1)
fill_template(8, 7, 3)
fill_template(8, 8, 2)
fill_template(9, 2, 3)

def render_template():
    for row in enumerate(template):
        if row[0] % 3 == 0: print(" ")
        for column in enumerate(row[1]):
            if column[0] % 3 == 0: print("  ", end="")
            print(f"[{column[1]}]", end="")
        print("")


render_template()

# Funcion que revise en cada celda, si solo hay un valor posible

round = 1

def check_posible_numbers_for_each_box(round):
    number_filled_in_round = False
    print(f"Round: {round}")
    for row in enumerate(template):
        for column in enumerate(row[1]):
            row_index = row[0]
            column_index = column[0]

            if type(template[row[0]][column_index]) == int:
                three_rows_check(row_index, column_index)
                continue

            posible_numbers = list(range(1, 10))
            posible_numbers = check_rows_posible_numbers(posible_numbers, row_index)
            # print(f"Row {row_index + 1} - column {column_index + 1}")
            number_filled_in_round = check_unique_posible_number(posible_numbers, row_index, column_index, number_filled_in_round)
            posible_numbers = check_columns_posible_numbers(posible_numbers, column_index)
            number_filled_in_round = check_unique_posible_number(posible_numbers, row_index, column_index, number_filled_in_round)
            posible_numbers = check_block_posible_numbers(posible_numbers, row_index, column_index)
            number_filled_in_round = check_unique_posible_number(posible_numbers, row_index, column_index, number_filled_in_round)
            # print(f"Posible numbers: {posible_numbers} for row {row_index + 1} and column {column_index + 1}")

            

    print(f"is_sudoku_completed: {is_sudoku_completed()}")
    print(f"number_filled_in_round: {number_filled_in_round}")
    if not is_sudoku_completed() and number_filled_in_round:
        round = round + 1
        check_posible_numbers_for_each_box(round)
    else:
        return

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

def three_rows_check(row_index, column_index):
    # Agarrar cada celda
    # Revisar si en una de las filas de su bloque esta ese numero
    # Revisar en la otra fila de ese bloque si esta ese numero
    # Si en solo una fila no esta el numero, revisar en los casilleros vacios, si en esas columnas esta el numero
    # Si solo hay un casillero vacio donde puede ir el numero, rellenarlo ahi
    number = template[row_index][column_index]
    if type(template[row_index][column_index]) == int:
        start_row_block, end_row_block, start_column_block, end_column_block = define_block(row_index, column_index)

        counter = count_number_in_row_block(start_row_block, end_row_block, number)
        
    # Si el counter es 2, buscar en que fila no esta el numero
        if counter == 2:
            # print(f"Working with number {template[row_index][column_index]} in row {row_index + 1} and column {column_index + 1}")
            row = row_without_number(start_row_block, end_row_block, number)
 
    # Tomar esa fila, crear un rango del 0 al 8 con las columnas, eliminar cada numero si en esa casilla hay un numero o si en la columa existe el numero
            columns = get_posibles_columns(row, number, start_column_block, end_column_block)
            
# Hay que buscar en que bloque esta el otro numero, no "number", sino el otro
            try:
                row = row_of_second_number(start_row_block, end_row_block, row_index, number)
                number_index = template[row].index(number)
                #print(f"number index {number_index}")
                _, _, start_column_block, end_column_block = define_block(row, number_index)
                
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

            fill_number_if_one_column_left(row, columns, number)

def get_posibles_columns(row, number, start_column_block, end_column_block):
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
    for column in range(start_column_block, end_column_block):
        try:
            columns.remove(column)
            #print(f"3 Removed column {column}. Columns left: {columns}")
        except:
            continue
    return columns

def count_number_in_row_block(start_row_block, end_row_block, number):
    counter = 0
    for row in range(start_row_block, end_row_block):
            if number in template[row]:
                counter += 1
    # print(f"Number {number} is in row range {start_row + 1} to {end_row} {counter} times")
    return counter

def row_without_number(start_row_block, end_row_block, number):
    for row in range(start_row_block, end_row_block):
        if number not in template[row]:
            return row
    # print(f"Number {number} not in row {row + 1}")

def fill_number_if_one_column_left(row, columns, number):
    if len(columns) == 1 and review_number_before_fill():
        template[row][columns[0]] = number
        render_template()
        print(f"Template in row {row + 1} and column {columns[0] + 1} = {number} with three rows check method")

def row_of_second_number(start_row_block, end_row_block, row_index, number):
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
     

def three_column_check():
    pass

def check_unique_posible_number(posible_numbers, row_index, column_index, number_filled_in_round):
    if len(posible_numbers) == 1 and type(posible_numbers[0]) == int:
        if review_number_before_fill():
            template[row_index][column_index] = posible_numbers[0]
            render_template()
            print(f"Template in row {row_index + 1} and column {column_index + 1} = {posible_numbers[0]} with unique posible number method")
            number_filled_in_round = True
            return number_filled_in_round
    return number_filled_in_round

def review_number_before_fill():
    # Se le pasa el numero a colocar y se vuelve a revisar que ese numero no se repita en fila, columna o bloque
    # Retorna true o false
    return True

def is_sudoku_completed():
    for row in enumerate(template):
        for column in enumerate(row[1]):
            if type(template[row[0]][column[0]]) != int:
                return False
    print("Sudoku is completed")
    return True

check_posible_numbers_for_each_box(round)
