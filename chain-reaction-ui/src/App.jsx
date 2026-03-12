import { useState } from 'react'
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
        }
      }, index * 150);
    });
  };

  const handleCellClick = async (r, c) => {
    if (isAnimating)
    {
      return;
    }
    if (occupied[r][c] !== 'n' && occupied[r][c] !== currentPlayer)
    {
      return;
    }

    const payload = {
      orbs_grid: orbsGrid,
      occupied: occupied,
      player: currentPlayer,
      row: r,
      col: c
    };

    try
    {
      const response = await fetch("http://127.0.0.1:8000/human_move", {
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
      <div className='board'>
        {orbsGrid.map((row, rIndex) => (
          row.map((orbs, cIndex) => {
            const owner = occupied[rIndex][cIndex];

            return (
              <div key={`${rIndex} - ${cIndex}`} className='cell' onClick={() => handleCellClick(rIndex, cIndex)}>
                {renderOrbs(orbs, owner)}
              </div>
            );
          })
        ))}
      </div>
    </div>
  );
}

export default App;