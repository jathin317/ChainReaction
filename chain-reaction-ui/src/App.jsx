import { useState, useEffect } from 'react'
import './App.css'

const ROWS = 6;
const COLS = 9;

const createEmptyOrbs = () => Array(ROWS).fill().map(() => Array(COLS).fill(0));


const createEmptyOccupied = () => Array(ROWS).fill().map(() => Array(COLS).fill('n'));


function App()
{
  const [orbsGrid, setOrbsGrid] = useState(createEmptyOrbs());
  const [occupied, setOccupied] = useState(createEmptyOccupied());
  const [currentPlayer, setCurrentPlayer] = useState('p1');
  const [isAnimating, setIsAnimating] = useState(false);

  const [turnCount, setTurnCount] = useState(0);
  const [winner, setWinner] = useState(null);

  const [lastMove, setLastMove] = useState({r: null, c: null});

  useEffect(() => {
    if (turnCount > 1 && !isAnimating)
    {
      let p1Present = false;
      let p2Present = false;

      occupied.forEach(row => {
        row.forEach(cell => {
          if (cell === 'p1')
            p1Present = true;
          if (cell === 'p2')
            p2Present = true;
        });
      });

      if (!p1Present && p2Present)
        setWinner('p2');
      if (p1Present && !p2Present)
        setWinner('p1');
    }
  }, [turnCount, occupied, isAnimating])

  const playFrames = (frames) => {
    setIsAnimating(true);

    frames.forEach((frame, index) => {
      setTimeout(() => {
        setOrbsGrid(frame.orbs_grid);
        setOccupied(frame.occupied);

        if(index === frames.length - 1)
        {
          setIsAnimating(false);
          setCurrentPlayer(prev => prev === "p1" ? "p2" : "p1");
          setTurnCount(prev => prev + 1);
        }
      }, index * 150);
    });
  };

  useEffect(() => {
    if (currentPlayer === 'p2' && !isAnimating && !winner)
    {
      const fetchBotMove = async () => {
        const payload = {
          orbs_grid: orbsGrid,
          occupied: occupied,
          player: 'p2',
          row: -1,
          col: -1
        };

        try 
        {
          const response = await fetch("/api/bot_move", {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(payload)
          });

          const data = await response.json();

          setLastMove({ r: data.bot_row, c: data.bot_col });

          playFrames(data.frames);
        }
        catch(error)
        {
          console.error("Error fetching from bot,", error);
        }

      };
      setTimeout(fetchBotMove, 500);
    }
  }, [currentPlayer, isAnimating, orbsGrid, occupied, winner]);

  const handleCellClick = async (r, c) => {
    if (isAnimating || currentPlayer == 'p2' || winner != null)
    {
      return;
    }

    if (occupied[r][c] !== 'n' && occupied[r][c] !== currentPlayer)
    {
      return;
    }

    setLastMove({r, c});

    const payload = {
      orbs_grid: orbsGrid,
      occupied: occupied,
      player: currentPlayer,
      row: r,
      col: c
    };

    try
    {
      const response = await fetch("/api/human_move", {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(payload)
      });

      const data = await response.json();

      playFrames(data.frames);
    }
    catch(error)
    {
      console.error("Error communicating with backend: ", error);
    }
  };

  const resetGame = () => {
    setOrbsGrid(createEmptyOrbs());
    setOccupied(createEmptyOccupied());
    setCurrentPlayer('p1');
    setTurnCount(0);
    setWinner(null);
    setLastMove({r:null, c:null});
  }

  const renderOrbs = (count, owner) => {
    if (count === 0 || owner === 'n')
      return null;
    
    const colorClass = owner === 'p1' ? 'p1-orb' : 'p2-orb';

    if (count === 1)
    {
      return <div className={`orb ${colorClass} orb-1`}></div>;
    }
    if (count === 2)
    {
      return (
        <>
          <div className={`orb ${colorClass} orb-2-1`}></div>
          <div className={`orb ${colorClass} orb-2-2`}></div>
        </>
      );
    }
    if (count >= 3)
    {
      return (
        <>
          <div className={`orb ${colorClass} orb-3-1`}></div>
          <div className={`orb ${colorClass} orb-3-2`}></div>
          <div className={`orb ${colorClass} orb-3-3`}></div>
        </>
      );
    }
  };

  return (
    <div className='game-container'>
      <h1>Chain Reaction</h1>
      <h2>Current Turn: 
        <span style={{color: currentPlayer === 'p1' ? '#ff6b6b': '#6bff6b'}}>
          {currentPlayer === 'p1' ? 'Red' : 'Green'}
        </span>
      </h2>
      <div className='board-wrapper'>
        <div className='board'>
          {orbsGrid.map((row, rIndex) => (
            row.map((orbs, cIndex) => {
              const owner = occupied[rIndex][cIndex];

              const isLastMove = lastMove.r === rIndex && lastMove.c === cIndex;

              return (
                <div key={`${rIndex} - ${cIndex}`} className={`cell ${isLastMove ? 'highlight' : ''}`} onClick={() => handleCellClick(rIndex, cIndex)}>
                  {renderOrbs(orbs, owner)}
                </div>
              );
            })
          ))}
        </div>

        {winner && (
          <div className='game-over'>
            <h1 style={{color: winner === 'p1' ? '#ff6b6b' : '#6bff6b'}}>
              {winner === 'p1' ? 'Red' : 'Green'} Wins!
            </h1>
            <button className='reset-button' onClick={resetGame}>
              Play Again
            </button>
          </div>
        )}
      </div>
    </div>
  );
}

export default App;