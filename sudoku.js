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

fillTemplate(1, 1, 4)
fillTemplate(1, 2, 2)
fillTemplate(1, 6, 3)
fillTemplate(1, 8, 8)
fillTemplate(1, 9, 1)
fillTemplate(2, 3, 1)
fillTemplate(2, 9, 3)
fillTemplate(3, 2, 7)
fillTemplate(3, 3, 8)
fillTemplate(3, 5, 1)
fillTemplate(3, 6, 5)
fillTemplate(3, 8, 6)
fillTemplate(3, 9, 9)
fillTemplate(4, 4, 6)
fillTemplate(4, 8, 3)
fillTemplate(4, 9, 5)
fillTemplate(5, 1, 2)
fillTemplate(5, 2, 5)
fillTemplate(5, 3, 7)
fillTemplate(5, 7, 9)
fillTemplate(5, 8, 4)
fillTemplate(5, 9, 6)
fillTemplate(6, 6, 9)
fillTemplate(6, 9, 8)
fillTemplate(7, 1, 1)
fillTemplate(7, 2, 9)
fillTemplate(7, 4, 2)
fillTemplate(7, 5, 8)
fillTemplate(7, 6, 4)
fillTemplate(8, 1, 7)
fillTemplate(8, 2, 4)
fillTemplate(8, 3, 5)
fillTemplate(8, 4, 3)
fillTemplate(8, 6, 6)
fillTemplate(8, 9, 2)
fillTemplate(9, 4, 1)
fillTemplate(9, 5, 5)
fillTemplate(9, 7, 6)
renderTemplate()





// Funcion que crea un objeto por cada casilla
function resolveSudoku() {
    let boxObject = {
        "row": null,
        "column": null,
        "blockRowInit": null,
        "blockRowFinish": null,
        "blockColumnInit": null,
        "blockColumnFinish": null,
        "numeros": Array.from({ length: 9}, (_, i) => i + 1)
    }
    let k = 0, l = 0;

    let interval = setInterval(() => {
        if (k >= 9) {
            clearInterval(interval);
            return;
        }

        boxObject = {
            row: k + 1,
            column: l + 1,
            blockRowInit: null,
            blockRowFinish: null,
            blockColumnInit: null,
            blockColumnFinish: null,
            numeros: Array.from({ length: 9 }, (_, n) => n + 1)
        };

        defineBlockInitAndFinish(boxObject);
        columnNumbers(boxObject);
        rowNumbers(boxObject);
        blockNumbers(boxObject);
        console.log(boxObject);
        renderTemplate();

        l++;
        if (l >= 9) {
            l = 0;
            k++;
        }

    }, 100);
    boxObject = {
        "row": null,
        "column": null,
        "blockRowInit": null,
        "blockRowFinish": null,
        "blockColumnInit": null,
        "blockColumnFinish": null,
        "numeros": Array.from({ length: 9}, (_, i) => i + 1)
    }
}
resolveSudoku();
sudokuIsCompleted();
/*
async function resolveSudoku() {
    for(let k = 0; k < 9; k++){
        for(let l = 0; l < 9; l++){
                boxObject.row = k + 1;
                boxObject.column = l + 1;
                console.log(boxObject);
                defineBlockInitAndFinish(boxObject);
                columnNumbers(boxObject);
                rowNumbers(boxObject);
                blockNumbers(boxObject);
                
                renderTemplate()
                boxObject = {
                    "row": null,
                    "column": null,
                    "blockRowInit": null,
                    "blockRowFinish": null,
                    "blockColumnInit": null,
                    "blockColumnFinish": null,
                    "numeros": Array.from({ length: 9}, (_, n) => n + 1)
                }
            } 
    }
}
resolveSudoku()
*/
// Funcion para revisar si se ha completado el sudoku:
function sudokuIsCompleted() {
    for(i = 0; i < 9; i++){
        for(j = 0; j < 9; j++){
            if(typeof template[i][j] !== "number"){
                resolveSudoku()
            } else {
                console.log("Sudoku terminado")
            }
        }
    }
}


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
    console.log("defineBlockInitAndFinish...");
    box.row >= 1 && box.row <= 3 ? (box.blockRowInit = 1, box.blockRowFinish = 3) : box.row >= 4 && box.row <= 6 ? (box.blockRowInit = 4, box.blockRowFinish = 6) : (box.blockRowInit = 7, box.blockRowFinish = 9);
    box.column >= 1 && box.column <= 3 ? (box.blockColumnInit = 1, box.blockColumnFinish = 3) : box.column >= 4 && box.column <= 6 ? (box.blockColumnInit = 4, box.blockColumnFinish = 6) : (box.blockColumnInit = 7, box.blockColumnFinish = 9);
    //console.log("box", box);
}
//defineBlockInitAndFinish(possibleNumbers11)


// Funcion que crea un array con los posibles numeros en del bloque

function defineBlocks(box) {
    console.log("defineBlocks...");
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
    console.log("rowNumbers...");
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
    console.log("columnNumbers...");
    const column = box.column - 1;
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
    console.log("blockNumbers...");
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
    console.log("detectOnlyOneNumber...");
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