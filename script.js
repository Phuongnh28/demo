let qTable;
const board = Array(9).fill(null);
const player = "X";
const ai = "O";

// Load Q-table from JSON file
fetch('q_table.json')
    .then(response => response.json())
    .then(data => {
        qTable = data;
    })
    .catch(error => console.error('Error loading Q-table:', error));

const boardElement = document.getElementById('board');

// Event listener for human moves
boardElement.addEventListener('click', event => {
    const index = parseInt(event.target.id.split('-')[1]);
    if (board[index] || !qTable) return;

    playMove(index, player);
    if (checkGameOver()) return;
    aiMove();
});

function playMove(index, mark) {
    board[index] = mark;
    document.getElementById(`cell-${index}`).textContent = mark;
}

function aiMove() {
    const state = board.join("");
    const availableActions = board.map((cell, idx) => cell === null ? idx : null).filter(idx => idx !== null);
    const action = chooseAction(state, availableActions);
    playMove(action, ai);
    checkGameOver();
}

function chooseAction(state, availableActions) {
    if (Math.random() < 0.1 || !qTable[state]) return availableActions[Math.floor(Math.random() * availableActions.length)];
    const qValues = availableActions.map(a => qTable[state + a] || 0);
    return availableActions[qValues.indexOf(Math.max(...qValues))];
}

function checkGameOver() {
    const winningPatterns = [
        [0, 1, 2], [3, 4, 5], [6, 7, 8],
        [0, 3, 6], [1, 4, 7], [2, 5, 8],
        [0, 4, 8], [2, 4, 6]
    ];
    for (const pattern of winningPatterns) {
        const [a, b, c] = pattern;
        if (board[a] && board[a] === board[b] && board[a] === board[c]) {
            alert(`${board[a]} wins!`);
            resetBoard();
            return true;
        }
    }
    if (board.every(cell => cell !== null)) {
        alert("It's a tie!");
        resetBoard();
        return true;
    }
    return false;
}

function resetBoard() {
    board.fill(null);
    document.querySelectorAll('.cell').forEach(cell => cell.textContent = '');
}
