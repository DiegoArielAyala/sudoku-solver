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

fillTemplate(1, 2, 1)
fillTemplate(1, 3, 2)
fillTemplate(1, 4, 3)
fillTemplate(1, 5, 4)
fillTemplate(1, 6, 5)
fillTemplate(1, 7, 6)
fillTemplate(1, 8, 7)
fillTemplate(1, 9, 8)
fillTemplate(2, 4, 1)
fillTemplate(2, 6, 2)
fillTemplate(3, 7, 1)
fillTemplate(4, 7, 8)
fillTemplate(5, 7, 9)
fillTemplate(6, 7, 7)
fillTemplate(7, 7, 6)
fillTemplate(8, 7, 5)
renderTemplate()

const boxObject = {
    "row": null,
    "column": null,
    "blockRowInit": null,
    "blockRowFinish": null,
    "blockColumnInit": null,
    "blockColumnFinish": null,
    "numeros": Array.from({ length: 9}, (_, i) => i + 1)
}

// Funcion que crea un objeto por cada casilla
function createBoxObject() {
    for(i = 0; i < 9; i++){
        for(j = 0; j < 9; j++){
            boxObject.row = i + 1;
            boxObject.column = j + 1;
            defineBlockInitAndFinish(boxObject);
            console.log(boxObject);
            defineBlocks(boxObject);
            console.log(boxObject);
            rowNumbers(boxObject);
            columnNumbers(boxObject);
            blockNumbers(boxObject);
            renderTemplate()
        }
    }
}
createBoxObject()

// Array con los posibles numeros para 1-1
const possibleNumbers11 = {
    "row": 1,
    "column": 1,
    "blockRowInit": null,
    "blockRowFinish": null,
    "blockColumnInit": null,
    "blockColumnFinish": null,
    "numeros": Array.from({ length: 9}, (_, i) => i + 1)
}
//console.log(possibleNumbers11)

// Funcion que define el inicio y final del bloque dentro del objeto de cada casilla
function defineBlockInitAndFinish(box) {
    box.row >= 1 && box.row <= 3 ? (box.blockRowInit = 1, box.blockRowFinish = 3) : box.row >= 4 && box.row <= 6 ? (box.blockRowInit = 4, box.blockRowFinish = 6) : (box.blockRowInit = 7, box.blockRowFinish = 9);
    box.column >= 1 && box.column <= 3 ? (box.blockColumnInit = 1, box.blockColumnFinish = 3) : box.column >= 4 && box.column <= 6 ? (box.blockColumnInit = 4, box.blockColumnFinish = 6) : (box.blockColumnInit = 7, box.blockColumnFinish = 9);
    console.log("box", box);
}
//defineBlockInitAndFinish(possibleNumbers11)



// Funcion que crea un array con los posibles numeros en del bloque

function defineBlocks(box) {
    const blockNumbers = [];
    for(i = box.blockRowInit - 1; i < box.blockRowFinish; i++){
        for(j = box.blockColumnInit - 1; j < box.blockColumnFinish; j++){
            blockNumbers.push(template[i][j]);
        }
    }
    return blockNumbers;
}

//defineBlocks(possibleNumbers11)


//Funcion que revise los numeros de la fila y los elimine del array
//@params objeto perteneciente a la casilla de la que se desea buscar
function rowNumbers(box) {
    const row = box.row - 1;
    for(i = 0; i < 9 ; i++){
        const rowNumber = template[row][i];
        if(typeof rowNumber === "number") {
            const indexOfRowNumber = box.numeros.indexOf(rowNumber)
            if( indexOfRowNumber !== -1){
                box.numeros.splice(indexOfRowNumber, 1)
            }
        }
    }
    detectOnlyOneNumber(box)
}

//Funcion que revise los numeros de la columna y los elimine del array
function columnNumbers(box) {
    const column = box.column -1;
    for(i = 0; i < 9; i++){
        const columnNumber = template[i][column];
        if(typeof columnNumber === "number"){
            const indexOfColumnNumber = box.numeros.indexOf(columnNumber);
            if(indexOfColumnNumber !== -1){
                box.numeros.splice(indexOfColumnNumber, 1);
            }
        }
    }
    detectOnlyOneNumber(box)
}

//Funcion que revise los numeros del bloque y los elimine del array
function blockNumbers(box){
    const blockNumbers = defineBlocks(box);
    for(i = 0; i < 9; i++){
        if(typeof blockNumbers[i] === "number"){
            const indexOfBlockNumber = box.numeros.indexOf(blockNumbers[i]);
            if(indexOfBlockNumber !== -1){
                box.numeros.splice(indexOfBlockNumber, 1);
            }
        }
    }
    detectOnlyOneNumber(box)
}

// Funcion que detecta si en box.numeros queda solo 1 numero y lo agrega al template en la ubicacion del box

function detectOnlyOneNumber(box) {
    if (box.numeros.length === 1) {
        template[box.row - 1][box.column - 1] = box.numeros[0]
    }
}

//
//rowNumbers(possibleNumbers11)
//columnNumbers(possibleNumbers11)
//blockNumbers(possibleNumbers11)
//detectOnlyOneNumber(possibleNumbers11)
//renderTemplate()