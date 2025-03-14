const template = new Array(9).fill(null).map(() => new Array(9).fill(" "))

// Mostrar sudoku
function renderTemplate() {
    for(let i = 0; i < template.length; i++){
        console.log((i + 1) + " " + template[i].map((cell, index) => index % 3 === 2 ? "["+ cell + "]" + " " : "[" + cell +"]" ).join(" "));
        if (i % 3 === 2) console.log("");
    }
}

// Anotar un numero en el sudoku
function fillTemplate(row, column, number) {
    template[row - 1][column - 1] = number;
    // renderTemplate();
}

fillTemplate(1, 1, 2)
fillTemplate(7, 8, 4)
fillTemplate(6, 0, 1)
fillTemplate(5, 7, 9)

// Array con los posibles numeros para 1-1
const possibleNumbers11 = {
    "row": 1,
    "column": 1,
    "numeros": Array.from({ length: 9}, (_, i) => i + 1)
}
console.log(possibleNumbers11)

//Funcion que revise los numeros de la fila y los elimine del array
//@params objeto perteneciente a la casilla de la que se desea buscar
function rowNumbers(box) {
    const row = box.row - 1;
    for(i = 0; i<9 ; i++){
        const rowNumber = template[row][i]
        if(typeof rowNumber === "number") {
            const indexOfRowNumber = possibleNumbers11.numeros.indexOf(rowNumber)
            if( indexOfRowNumber !== -1){
                possibleNumbers11.numeros.splice(indexOfRowNumber, 1)
            }
        }
    }
    console.log("possibleNumbers11", possibleNumbers11);
    //console.log(row)
    //console.log(template[row])
}


rowNumbers(possibleNumbers11)
renderTemplate()